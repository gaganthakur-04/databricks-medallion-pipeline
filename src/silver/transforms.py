"""Spark transforms for Silver data-quality validation."""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import (
    col,
    concat,
    concat_ws,
    current_timestamp,
    lit,
    row_number,
    when,
)
from pyspark.sql.window import Window

from src.silver.config import SilverConfig
from src.silver.rules import (
    CUST_BIZ_001,
    CUST_COMP_001,
    CUST_UNIQ_001,
    ORD_BIZ_001,
    ORD_BIZ_002,
    ORD_COMP_001,
    ORD_COMP_002,
    ORD_REF_001,
    ORD_REF_002,
    ORD_UNIQ_001,
    PROD_BIZ_001,
    PROD_BIZ_002,
    PROD_BIZ_003,
    RULE_MESSAGES,
    VALID_CUSTOMER_SEGMENTS,
    VALID_ORDER_STATUSES,
)


def get_spark() -> SparkSession:
    return SparkSession.builder.getOrCreate()


def _rule_failure(rule_id: str, condition):
    return when(condition, concat(lit(f"{rule_id} — {RULE_MESSAGES[rule_id]}")))


def _finalize_quality(df: DataFrame, failure_columns: list) -> DataFrame:
    failure_text = concat_ws("; ", *failure_columns)
    return (
        df.withColumn(
            "quality_check_result",
            when(failure_text == "", lit("PASS")).otherwise(concat(lit("FAIL: "), failure_text)),
        )
        .withColumn("is_valid", col("quality_check_result") == lit("PASS"))
        .withColumn("_silver_processed_at", current_timestamp())
    )



def _duplicate_flag(df: DataFrame, key_col: str) -> DataFrame:
    window = Window.partitionBy(key_col).orderBy(key_col)
    return df.withColumn(f"__dup_{key_col}", row_number().over(window) > 1)


def transform_customers(bronze_df: DataFrame) -> DataFrame:
    source_cols = [
        "customer_id",
        "customer_name",
        "email",
        "country",
        "signup_date",
        "customer_segment",
        "lifetime_value",
    ]
    df = bronze_df.select(*source_cols)
    df = _duplicate_flag(df, "customer_id")

    failures = [
        _rule_failure(CUST_COMP_001, col("email").isNull()),
        _rule_failure(CUST_UNIQ_001, col("__dup_customer_id")),
        _rule_failure(
            CUST_BIZ_001,
            ~col("customer_segment").isin(list(VALID_CUSTOMER_SEGMENTS)),
        ),
    ]
    result = _finalize_quality(df, failures)
    return result.drop("__dup_customer_id")


def transform_products(bronze_df: DataFrame) -> DataFrame:
    source_cols = [
        "product_id",
        "product_name",
        "category",
        "price",
        "cost",
        "stock_quantity",
        "reorder_level",
    ]
    df = bronze_df.select(*source_cols)
    failures = [
        _rule_failure(PROD_BIZ_001, col("price") < 0),
        _rule_failure(PROD_BIZ_002, col("cost") < 0),
        _rule_failure(PROD_BIZ_003, col("stock_quantity") < 0),
    ]
    return _finalize_quality(df, failures)


def transform_orders(
    bronze_df: DataFrame,
    customers_df: DataFrame,
    products_df: DataFrame,
) -> DataFrame:
    source_cols = [
        "order_id",
        "customer_id",
        "order_date",
        "product_id",
        "quantity",
        "unit_price",
        "total_amount",
        "order_status",
        "payment_date",
    ]
    df = bronze_df.select(*source_cols)
    df = _duplicate_flag(df, "order_id")

    valid_customers = customers_df.select(col("customer_id").alias("valid_customer_id")).distinct()
    valid_products = products_df.select(col("product_id").alias("valid_product_id")).distinct()

    df = (
        df.join(valid_customers, df.customer_id == valid_customers.valid_customer_id, "left")
        .join(valid_products, df.product_id == valid_products.valid_product_id, "left")
    )

    amount_mismatch = col("total_amount").cast("double") != (
        col("quantity").cast("double") * col("unit_price").cast("double")
    )

    failures = [
        _rule_failure(ORD_COMP_001, col("customer_id").isNull()),
        _rule_failure(ORD_COMP_002, col("product_id").isNull()),
        _rule_failure(ORD_UNIQ_001, col("__dup_order_id")),
        _rule_failure(
            ORD_REF_001,
            col("customer_id").isNotNull() & col("valid_customer_id").isNull(),
        ),
        _rule_failure(
            ORD_REF_002,
            col("product_id").isNotNull() & col("valid_product_id").isNull(),
        ),
        _rule_failure(ORD_BIZ_001, ~col("order_status").isin(list(VALID_ORDER_STATUSES))),
        _rule_failure(ORD_BIZ_002, amount_mismatch),
    ]
    result = _finalize_quality(df, failures)
    return result.drop(
        "__dup_order_id",
        "valid_customer_id",
        "valid_product_id",
    )


def write_silver_table(df: DataFrame, table_name: str) -> None:
    (
        df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )


def validate_all_entities(spark: SparkSession, config: SilverConfig) -> dict[str, int]:
    bronze_products = spark.table(config.bronze_table("products"))
    bronze_customers = spark.table(config.bronze_table("customers"))
    bronze_orders = spark.table(config.bronze_table("orders"))

    silver_products = transform_products(bronze_products)
    write_silver_table(silver_products, config.silver_table("products"))
    product_count = silver_products.count()

    silver_customers = transform_customers(bronze_customers)
    write_silver_table(silver_customers, config.silver_table("customers"))
    customer_count = silver_customers.count()

    silver_orders = transform_orders(bronze_orders, bronze_customers, bronze_products)
    write_silver_table(silver_orders, config.silver_table("orders"))
    order_count = silver_orders.count()

    return {
        "products": product_count,
        "customers": customer_count,
        "orders": order_count,
    }

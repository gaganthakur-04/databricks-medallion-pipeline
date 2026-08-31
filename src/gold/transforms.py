"""Spark transforms for Gold business aggregations."""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import avg, col, count, lit, sum as spark_sum, when

from src.gold.config import GoldConfig


def get_spark() -> SparkSession:
    return SparkSession.builder.getOrCreate()


def _valid_completed_orders(orders: DataFrame) -> DataFrame:
    return orders.filter(col("is_valid") & (col("order_status") == lit("Completed")))


def build_sales_by_product(
    orders: DataFrame,
    products: DataFrame,
) -> DataFrame:
    valid_orders = _valid_completed_orders(orders)
    valid_products = products.filter(col("is_valid"))

    joined = valid_orders.join(
        valid_products.select("product_id", "product_name", "category"),
        on="product_id",
        how="inner",
    )

    return joined.groupBy("product_id", "product_name", "category").agg(
        count(lit(1)).alias("total_orders"),
        spark_sum("total_amount").cast("decimal(18,2)").alias("total_revenue"),
        avg("total_amount").cast("decimal(18,2)").alias("avg_order_value"),
    )


def build_revenue_by_customer(
    orders: DataFrame,
    customers: DataFrame,
) -> DataFrame:
    valid_orders = _valid_completed_orders(orders)
    valid_customers = customers.filter(col("is_valid"))

    joined = valid_orders.join(
        valid_customers.select("customer_id", "customer_name", "customer_segment"),
        on="customer_id",
        how="inner",
    )

    return joined.groupBy("customer_id", "customer_name", "customer_segment").agg(
        count(lit(1)).alias("total_orders"),
        spark_sum("total_amount").cast("decimal(18,2)").alias("total_revenue"),
        avg("total_amount").cast("decimal(18,2)").alias("avg_order_value"),
        spark_sum("total_amount").cast("decimal(18,2)").alias("lifetime_value_actual"),
    )


def build_customer_segmentation(
    orders: DataFrame,
    customers: DataFrame,
) -> DataFrame:
    valid_orders = _valid_completed_orders(orders)
    valid_customers = customers.filter(col("is_valid")).select("customer_id")

    order_stats = valid_orders.groupBy("customer_id").agg(
        count(lit(1)).alias("completed_order_count"),
        spark_sum("total_amount").cast("decimal(18,2)").alias("total_revenue"),
    )

    customer_activity = valid_customers.join(order_stats, on="customer_id", how="left").fillna(
        0, subset=["completed_order_count", "total_revenue"]
    )

    active_revenues = [
        float(row["total_revenue"])
        for row in customer_activity.filter(col("completed_order_count") > 0)
        .select("total_revenue")
        .collect()
    ]
    if active_revenues:
        active_revenues.sort()
        p75_index = int(0.75 * (len(active_revenues) - 1))
        high_value_threshold = active_revenues[p75_index]
    else:
        high_value_threshold = 0.0

    segmented = customer_activity.withColumn(
        "segment_type",
        when(col("completed_order_count") == 0, lit("Inactive"))
        .when(col("total_revenue") >= lit(high_value_threshold), lit("High-Value"))
        .when(col("completed_order_count") > 1, lit("Repeat"))
        .otherwise(lit("One-Time")),
    )

    return segmented.groupBy("segment_type").agg(
        count(lit(1)).alias("customer_count"),
        avg("total_revenue").cast("decimal(18,2)").alias("avg_revenue"),
        spark_sum("total_revenue").cast("decimal(18,2)").alias("total_revenue"),
    )


def write_gold_table(df: DataFrame, table_name: str) -> None:
    (
        df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )


def build_all_gold_tables(spark: SparkSession, config: GoldConfig) -> dict[str, int]:
    customers = spark.table(config.silver_table("customers"))
    orders = spark.table(config.silver_table("orders"))
    products = spark.table(config.silver_table("products"))

    sales_by_product = build_sales_by_product(orders, products)
    write_gold_table(sales_by_product, config.gold_table("sales_by_product"))

    revenue_by_customer = build_revenue_by_customer(orders, customers)
    write_gold_table(revenue_by_customer, config.gold_table("revenue_by_customer"))

    customer_segmentation = build_customer_segmentation(orders, customers)
    write_gold_table(customer_segmentation, config.gold_table("customer_segmentation"))

    return {
        "sales_by_product": sales_by_product.count(),
        "revenue_by_customer": revenue_by_customer.count(),
        "customer_segmentation": customer_segmentation.count(),
    }

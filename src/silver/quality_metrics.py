"""Quality metrics summary for Silver validation."""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col

from src.silver.config import SilverConfig
from src.silver.rules import (
    CUST_COMP_001,
    CUST_UNIQ_001,
    ORD_COMP_001,
    ORD_COMP_002,
    ORD_REF_001,
    ORD_REF_002,
    ORD_UNIQ_001,
)


def _rule_count(df: DataFrame, rule_id: str) -> int:
    return int(df.filter(col("quality_check_result").contains(rule_id)).count())


def summarize_entity(df: DataFrame, entity: str) -> list[dict[str, object]]:
    total = df.count()
    passed = df.filter(col("is_valid")).count()
    rows = [
        {
            "entity": entity,
            "check_name": "overall",
            "total_rows": total,
            "passed_rows": passed,
            "pct_passed": round(100.0 * passed / total, 2) if total else 0.0,
        }
    ]
    return rows


def summarize_rule_counts(spark: SparkSession, config: SilverConfig) -> list[dict[str, object]]:
    customers = spark.table(config.silver_table("customers"))
    orders = spark.table(config.silver_table("orders"))
    products = spark.table(config.silver_table("products"))

    metrics: list[dict[str, object]] = []
    metrics.extend(summarize_entity(customers, "customers"))
    metrics.extend(summarize_entity(orders, "orders"))
    metrics.extend(summarize_entity(products, "products"))

    rule_checks = [
        ("customers", customers, CUST_COMP_001),
        ("customers", customers, CUST_UNIQ_001),
        ("orders", orders, ORD_COMP_001),
        ("orders", orders, ORD_COMP_002),
        ("orders", orders, ORD_UNIQ_001),
        ("orders", orders, ORD_REF_001),
        ("orders", orders, ORD_REF_002),
    ]

    for entity, df, rule_id in rule_checks:
        flagged = _rule_count(df, rule_id)
        total = df.count()
        metrics.append(
            {
                "entity": entity,
                "check_name": rule_id,
                "total_rows": total,
                "flagged_rows": flagged,
                "pct_passed": round(100.0 * (total - flagged) / total, 2) if total else 0.0,
            }
        )

    return metrics


def print_quality_metrics(spark: SparkSession, config: SilverConfig) -> list[dict[str, object]]:
    metrics = summarize_rule_counts(spark, config)
    print("\nSilver quality metrics:")
    for row in metrics:
        if row["check_name"] == "overall":
            print(
                f"  {row['entity']}: {row['passed_rows']:,}/{row['total_rows']:,} valid "
                f"({row['pct_passed']}%)"
            )
        else:
            print(
                f"  {row['entity']} {row['check_name']}: {row['flagged_rows']:,} flagged "
                f"({row['pct_passed']}% passed)"
            )
    return metrics

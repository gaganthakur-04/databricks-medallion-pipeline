"""Shared Bronze ingestion utilities."""

from __future__ import annotations

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import current_timestamp, lit

from src.bronze.config import DATASETS, BronzeConfig


def get_spark() -> SparkSession:
    """Return active Spark session (Databricks notebook or local)."""
    return SparkSession.builder.getOrCreate()


def read_source_csv(spark: SparkSession, csv_path: str) -> DataFrame:
    """Read a CSV file with header and schema inference; no transformations."""
    return (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(csv_path)
    )


def add_audit_columns(df: DataFrame, batch_id: str, source_file: str) -> DataFrame:
    """Append Bronze audit metadata columns."""
    return (
        df.withColumn("_ingested_at", current_timestamp())
        .withColumn("_source_file", lit(source_file))
        .withColumn("_batch_id", lit(batch_id))
    )


def write_bronze_table(df: DataFrame, table_name: str) -> None:
    """Overwrite Delta table with ingested data (full reload per run)."""
    (
        df.write.format("delta")
        .mode("overwrite")
        .option("overwriteSchema", "true")
        .saveAsTable(table_name)
    )


def ingest_dataset(
    spark: SparkSession,
    config: BronzeConfig,
    entity: str,
    batch_id: str,
) -> int:
    """
    Ingest one CSV into its Bronze Delta table.

    Returns the number of rows written.
    """
    if entity not in DATASETS:
        raise ValueError(f"Unknown entity: {entity}")

    filename = DATASETS[entity]
    csv_path = config.csv_path(filename)
    table_name = config.table_name(entity)

    df = read_source_csv(spark, csv_path)
    df = add_audit_columns(df, batch_id=batch_id, source_file=filename)
    row_count = df.count()
    write_bronze_table(df, table_name)
    return row_count


def ingest_all_datasets(
    spark: SparkSession,
    config: BronzeConfig,
    batch_id: str,
) -> dict[str, int]:
    """Ingest customers, orders, and products; return row counts per entity."""
    results: dict[str, int] = {}
    for entity in DATASETS:
        results[entity] = ingest_dataset(spark, config, entity, batch_id)
    return results

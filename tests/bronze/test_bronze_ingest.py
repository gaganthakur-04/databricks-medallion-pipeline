"""Spark integration tests for Bronze ingestion (skipped without pyspark/delta)."""

import tempfile
from pathlib import Path

import pytest

pytest.importorskip("pyspark")
pytest.importorskip("delta")

from src.bronze.config import BronzeConfig
from src.bronze.ingest_utils import add_audit_columns, ingest_dataset, read_source_csv


def test_ingest_dataset_unknown_entity_raises():
    from src.bronze.ingest_utils import get_spark

    config = BronzeConfig(input_dir="data")
    with pytest.raises(ValueError, match="Unknown entity"):
        ingest_dataset(get_spark(), config, "invalid", "batch-1")


@pytest.fixture(scope="module")
def spark_session():
    from delta import configure_spark_with_delta_pip
    from pyspark.sql import SparkSession

    warehouse = tempfile.mkdtemp(prefix="bronze-test-warehouse-")
    builder = (
        SparkSession.builder.master("local[1]")
        .appName("bronze-ingest-tests")
        .config("spark.sql.warehouse.dir", warehouse)
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension")
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")
    )
    spark = configure_spark_with_delta_pip(builder).enableHiveSupport().getOrCreate()
    spark.sql("CREATE DATABASE IF NOT EXISTS bronze_test")
    yield spark
    spark.sql("DROP DATABASE IF EXISTS bronze_test CASCADE")
    spark.stop()


@pytest.fixture
def sample_csv_dir(tmp_path: Path) -> Path:
    customers = tmp_path / "customers.csv"
    customers.write_text(
        "customer_id,customer_name,email,country,signup_date,customer_segment,lifetime_value\n"
        "1,Alice,alice@example.com,US,2024-01-01,Premium,100.00\n"
        "2,Bob,,UK,2024-01-02,Standard,50.00\n",
        encoding="utf-8",
    )
    orders = tmp_path / "orders.csv"
    orders.write_text(
        "order_id,customer_id,order_date,product_id,quantity,unit_price,total_amount,order_status,payment_date\n"
        "100,1,2024-02-01,10,2,25.00,50.00,Completed,2024-02-02\n",
        encoding="utf-8",
    )
    products = tmp_path / "products.csv"
    products.write_text(
        "product_id,product_name,category,price,cost,stock_quantity,reorder_level\n"
        "10,Widget,Electronics,25.00,10.00,100,20\n",
        encoding="utf-8",
    )
    return tmp_path


def test_read_csv_and_audit_columns(spark_session, sample_csv_dir):
    csv_path = str(sample_csv_dir / "customers.csv")
    df = read_source_csv(spark_session, csv_path)
    assert set(df.columns) == {
        "customer_id",
        "customer_name",
        "email",
        "country",
        "signup_date",
        "customer_segment",
        "lifetime_value",
    }

    audited = add_audit_columns(df, batch_id="batch-abc", source_file="customers.csv")
    assert {"_ingested_at", "_source_file", "_batch_id"}.issubset(set(audited.columns))

    row = audited.collect()[0]
    assert row["_source_file"] == "customers.csv"
    assert row["_batch_id"] == "batch-abc"


def test_ingest_dataset_writes_delta_table(spark_session, sample_csv_dir):
    config = BronzeConfig(input_dir=str(sample_csv_dir), database="bronze_test")
    count = ingest_dataset(spark_session, config, "customers", "batch-test-1")
    assert count == 2

    result = spark_session.table("bronze_test.customers")
    assert result.count() == 2
    assert "_ingested_at" in result.columns
    assert result.filter("_batch_id = 'batch-test-1'").count() == 2

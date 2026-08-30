"""Tests for Bronze configuration."""

from pathlib import Path

import pytest

from src.bronze.config import BronzeConfig, build_arg_parser, default_input_dir, generate_batch_id


def test_default_input_dir_local_points_to_repo_data():
    path = default_input_dir()
    if not Path("/databricks").exists():
        assert path.endswith("/data") or path.endswith("\\data")
        assert Path(path).name == "data"


def test_bronze_config_csv_path_local():
    config = BronzeConfig(input_dir="/tmp/ecommerce/raw")
    assert config.csv_path("customers.csv") == "/tmp/ecommerce/raw/customers.csv"


def test_bronze_config_csv_path_dbfs():
    config = BronzeConfig(input_dir="dbfs:/FileStore/ecommerce/raw")
    assert config.csv_path("orders.csv") == "dbfs:/FileStore/ecommerce/raw/orders.csv"


def test_bronze_config_table_name():
    config = BronzeConfig(input_dir="data", database="bronze")
    assert config.table_name("customers") == "bronze.customers"


def test_generate_batch_id_unique():
    ids = {generate_batch_id() for _ in range(5)}
    assert len(ids) == 5
    for batch_id in ids:
        assert "_" in batch_id


def test_config_from_args_overrides():
    parser = build_arg_parser()
    args = parser.parse_args(
        ["--input-dir", "/custom/path", "--database", "bronze_test", "--batch-id", "test-batch"]
    )
    config = BronzeConfig(
        input_dir=args.input_dir,
        database=args.database,
        batch_id=args.batch_id,
    )
    assert config.input_dir == "/custom/path"
    assert config.database == "bronze_test"
    assert config.batch_id == "test-batch"

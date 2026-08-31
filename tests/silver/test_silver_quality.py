"""Tests for Silver data-quality validation (pandas engine)."""

from pathlib import Path

import pytest

from src.data_generation.generate_sample_data import write_csvs
from src.data_generation.validate_data import load_csvs
from src.silver.pandas_engine import (
    count_rule_occurrences,
    validate_customers_pandas,
    validate_orders_pandas,
    validate_products_pandas,
)
from src.silver.rules import (
    CUST_COMP_001,
    CUST_UNIQ_001,
    ORD_COMP_001,
    ORD_COMP_002,
    ORD_REF_001,
    ORD_REF_002,
    ORD_UNIQ_001,
)


@pytest.fixture(scope="module")
def generated_data(tmp_path_factory) -> Path:
    data_dir = tmp_path_factory.mktemp("silver_test_data")
    write_csvs(data_dir)
    return data_dir


def test_silver_retains_all_rows(generated_data: Path) -> None:
    customers, orders, products = load_csvs(generated_data)
    silver_customers = validate_customers_pandas(customers)
    silver_orders = validate_orders_pandas(orders, customers, products)
    silver_products = validate_products_pandas(products)

    assert len(silver_customers) == len(customers)
    assert len(silver_orders) == len(orders)
    assert len(silver_products) == len(products)


def test_intentional_dq_issue_counts(generated_data: Path) -> None:
    customers, orders, products = load_csvs(generated_data)
    silver_customers = validate_customers_pandas(customers)
    silver_orders = validate_orders_pandas(orders, customers, products)

    assert count_rule_occurrences(silver_customers, CUST_COMP_001) == 50
    assert count_rule_occurrences(silver_customers, CUST_UNIQ_001) == 10
    assert count_rule_occurrences(silver_orders, ORD_COMP_001) == 100
    assert count_rule_occurrences(silver_orders, ORD_COMP_002) == 200
    assert count_rule_occurrences(silver_orders, ORD_REF_001) == 50
    assert count_rule_occurrences(silver_orders, ORD_REF_002) == 30
    assert count_rule_occurrences(silver_orders, ORD_UNIQ_001) == 20


def test_valid_and_invalid_records_identified(generated_data: Path) -> None:
    customers, orders, products = load_csvs(generated_data)
    silver_customers = validate_customers_pandas(customers)

    assert silver_customers["is_valid"].sum() < len(silver_customers)
    assert (silver_customers["quality_check_result"] == "PASS").sum() == silver_customers["is_valid"].sum()
    assert silver_customers.loc[~silver_customers["is_valid"], "quality_check_result"].str.startswith("FAIL:").all()


def test_products_all_valid(generated_data: Path) -> None:
    _, _, products = load_csvs(generated_data)
    silver_products = validate_products_pandas(products)
    assert silver_products["is_valid"].all()

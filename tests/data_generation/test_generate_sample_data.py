"""Tests for sample data generation."""

from pathlib import Path

import pytest

from src.data_generation.generate_sample_data import write_csvs
from src.data_generation.validate_data import assert_issue_counts, load_csvs


@pytest.fixture
def generated_data(tmp_path: Path) -> Path:
    write_csvs(tmp_path)
    return tmp_path


def test_row_counts(generated_data: Path) -> None:
    customers, orders, products = load_csvs(generated_data)
    assert len(customers) == 10_000
    assert len(orders) == 100_000
    assert len(products) == 500


def test_intentional_dq_issues(generated_data: Path) -> None:
    assert_issue_counts(generated_data)


def test_customer_columns(generated_data: Path) -> None:
    customers, _, _ = load_csvs(generated_data)
    expected = {
        "customer_id",
        "customer_name",
        "email",
        "country",
        "signup_date",
        "customer_segment",
        "lifetime_value",
    }
    assert set(customers.columns) == expected


def test_order_columns(generated_data: Path) -> None:
    _, orders, _ = load_csvs(generated_data)
    expected = {
        "order_id",
        "customer_id",
        "order_date",
        "product_id",
        "quantity",
        "unit_price",
        "total_amount",
        "order_status",
        "payment_date",
    }
    assert set(orders.columns) == expected


def test_product_columns(generated_data: Path) -> None:
    _, _, products = load_csvs(generated_data)
    expected = {
        "product_id",
        "product_name",
        "category",
        "price",
        "cost",
        "stock_quantity",
        "reorder_level",
    }
    assert set(products.columns) == expected

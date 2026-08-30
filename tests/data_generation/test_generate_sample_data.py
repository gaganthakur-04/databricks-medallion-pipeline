"""Tests for sample data generation."""

import filecmp
from pathlib import Path

import pytest

from src.data_generation.generate_sample_data import (
    CUSTOMER_COUNT,
    DUP_CUSTOMER_ID_COUNT,
    DUP_ORDER_ID_COUNT,
    NULL_CUSTOMER_ID_COUNT,
    NULL_EMAIL_COUNT,
    NULL_PRODUCT_ID_COUNT,
    ORPHAN_CUSTOMER_ID_COUNT,
    ORPHAN_PRODUCT_ID_COUNT,
    ORDER_COUNT,
    PRODUCT_COUNT,
    RANDOM_SEED,
    UNIQUE_CUSTOMER_COUNT,
    write_csvs,
)
from src.data_generation.validate_data import (
    assert_issue_counts,
    count_duplicate_customer_ids,
    count_duplicate_order_ids,
    count_intentional_orphan_customer_ids,
    count_intentional_orphan_product_ids,
    count_null_customer_ids,
    count_null_emails,
    count_null_product_ids,
    count_orphan_customer_ids,
    count_orphan_product_ids,
    count_unintended_orphan_customer_ids,
    count_unintended_orphan_product_ids,
    load_csvs,
    summarize_counts,
)


@pytest.fixture
def generated_data(tmp_path: Path) -> Path:
    write_csvs(tmp_path)
    return tmp_path


def test_exactly_10000_customer_rows(generated_data: Path) -> None:
    customers, _, _ = load_csvs(generated_data)
    assert len(customers) == CUSTOMER_COUNT == 10_000


def test_exactly_100000_order_rows(generated_data: Path) -> None:
    _, orders, _ = load_csvs(generated_data)
    assert len(orders) == ORDER_COUNT == 100_000


def test_exactly_500_product_rows(generated_data: Path) -> None:
    _, _, products = load_csvs(generated_data)
    assert len(products) == PRODUCT_COUNT == 500


def test_exactly_50_null_customer_emails(generated_data: Path) -> None:
    customers, _, _ = load_csvs(generated_data)
    assert count_null_emails(customers) == NULL_EMAIL_COUNT == 50


def test_exactly_10_duplicate_customer_ids(generated_data: Path) -> None:
    customers, _, _ = load_csvs(generated_data)
    assert count_duplicate_customer_ids(customers) == DUP_CUSTOMER_ID_COUNT == 10


def test_exactly_100_null_order_customer_ids(generated_data: Path) -> None:
    _, orders, _ = load_csvs(generated_data)
    assert count_null_customer_ids(orders) == NULL_CUSTOMER_ID_COUNT == 100


def test_exactly_200_null_order_product_ids(generated_data: Path) -> None:
    _, orders, _ = load_csvs(generated_data)
    assert count_null_product_ids(orders) == NULL_PRODUCT_ID_COUNT == 200


def test_exactly_50_invalid_customer_foreign_keys(generated_data: Path) -> None:
    customers, orders, _ = load_csvs(generated_data)
    assert count_intentional_orphan_customer_ids(orders) == ORPHAN_CUSTOMER_ID_COUNT == 50
    assert count_orphan_customer_ids(orders, customers) == 50


def test_exactly_30_invalid_product_foreign_keys(generated_data: Path) -> None:
    _, orders, products = load_csvs(generated_data)
    assert count_intentional_orphan_product_ids(orders) == ORPHAN_PRODUCT_ID_COUNT == 30
    assert count_orphan_product_ids(orders, products) == 30


def test_exactly_20_duplicate_order_ids(generated_data: Path) -> None:
    _, orders, _ = load_csvs(generated_data)
    assert count_duplicate_order_ids(orders) == DUP_ORDER_ID_COUNT == 20


def test_no_unintended_customer_foreign_key_violations(generated_data: Path) -> None:
    customers, orders, _ = load_csvs(generated_data)
    assert count_unintended_orphan_customer_ids(orders, customers) == 0


def test_no_unintended_product_foreign_key_violations(generated_data: Path) -> None:
    _, orders, products = load_csvs(generated_data)
    assert count_unintended_orphan_product_ids(orders, products) == 0


def test_all_unique_customer_ids_present_in_customers_table(generated_data: Path) -> None:
    customers, _, _ = load_csvs(generated_data)
    assert customers["customer_id"].nunique() == UNIQUE_CUSTOMER_COUNT
    id_counts = customers["customer_id"].value_counts()
    for cid in range(1, DUP_CUSTOMER_ID_COUNT + 1):
        assert id_counts[cid] == 2
    for cid in range(DUP_CUSTOMER_ID_COUNT + 1, UNIQUE_CUSTOMER_COUNT + 1):
        assert id_counts[cid] == 1


def test_reproducibility_with_same_seed(tmp_path: Path) -> None:
    run_a = tmp_path / "a"
    run_b = tmp_path / "b"
    write_csvs(run_a, seed=RANDOM_SEED)
    write_csvs(run_b, seed=RANDOM_SEED)
    for filename in ("customers.csv", "orders.csv", "products.csv"):
        assert filecmp.cmp(run_a / filename, run_b / filename, shallow=False)


def test_different_seed_produces_different_output(tmp_path: Path) -> None:
    run_a = tmp_path / "seed42"
    run_b = tmp_path / "seed99"
    write_csvs(run_a, seed=42)
    write_csvs(run_b, seed=99)
    # At least one file should differ when seed changes
    same = all(
        filecmp.cmp(run_a / f, run_b / f, shallow=False)
        for f in ("customers.csv", "orders.csv", "products.csv")
    )
    assert not same


def test_intentional_dq_issues_combined(generated_data: Path) -> None:
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


def test_summarize_counts_matches_expectations(generated_data: Path) -> None:
    summary = summarize_counts(generated_data)
    assert summary["customer_rows"] == 10_000
    assert summary["order_rows"] == 100_000
    assert summary["product_rows"] == 500
    assert summary["unintended_orphan_customer_ids"] == 0
    assert summary["unintended_orphan_product_ids"] == 0

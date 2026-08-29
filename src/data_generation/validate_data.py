"""Validation helpers for generated CSV data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data_generation.generate_sample_data import (
    CUSTOMER_COUNT,
    DUP_CUSTOMER_ID_COUNT,
    DUP_ORDER_ID_COUNT,
    NULL_CUSTOMER_ID_COUNT,
    NULL_EMAIL_COUNT,
    NULL_PRODUCT_ID_COUNT,
    ORPHAN_CUSTOMER_IDS,
    ORPHAN_PRODUCT_IDS,
    ORDER_COUNT,
    PRODUCT_COUNT,
)


def load_csvs(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers = pd.read_csv(data_dir / "customers.csv")
    orders = pd.read_csv(data_dir / "orders.csv")
    products = pd.read_csv(data_dir / "products.csv")
    return customers, orders, products


def count_null_emails(customers: pd.DataFrame) -> int:
    return int(customers["email"].isna().sum())


def count_duplicate_customer_ids(customers: pd.DataFrame) -> int:
    """Rows beyond the first occurrence per customer_id."""
    return int(customers["customer_id"].duplicated(keep="first").sum())


def count_null_customer_ids(orders: pd.DataFrame) -> int:
    return int(orders["customer_id"].isna().sum())


def count_null_product_ids(orders: pd.DataFrame) -> int:
    return int(orders["product_id"].isna().sum())


def count_orphan_customer_ids(orders: pd.DataFrame, customers: pd.DataFrame) -> int:
    valid_ids = set(customers["customer_id"].dropna().unique())
    mask = orders["customer_id"].notna() & ~orders["customer_id"].isin(valid_ids)
    return int(mask.sum())


def count_orphan_product_ids(orders: pd.DataFrame, products: pd.DataFrame) -> int:
    valid_ids = set(products["product_id"].unique())
    mask = orders["product_id"].notna() & ~orders["product_id"].isin(valid_ids)
    return int(mask.sum())


def count_duplicate_order_ids(orders: pd.DataFrame) -> int:
    return int(orders["order_id"].duplicated(keep="first").sum())


def assert_issue_counts(data_dir: Path) -> None:
    customers, orders, products = load_csvs(data_dir)

    assert len(customers) == CUSTOMER_COUNT
    assert len(orders) == ORDER_COUNT
    assert len(products) == PRODUCT_COUNT

    assert count_null_emails(customers) == NULL_EMAIL_COUNT
    assert count_duplicate_customer_ids(customers) == DUP_CUSTOMER_ID_COUNT
    assert count_null_customer_ids(orders) == NULL_CUSTOMER_ID_COUNT
    assert count_null_product_ids(orders) == NULL_PRODUCT_ID_COUNT
    assert count_orphan_customer_ids(orders, customers) == len(ORPHAN_CUSTOMER_IDS)
    assert count_orphan_product_ids(orders, products) == len(ORPHAN_PRODUCT_IDS)
    assert count_duplicate_order_ids(orders) == DUP_ORDER_ID_COUNT

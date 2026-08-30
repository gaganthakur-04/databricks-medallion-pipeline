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
    UNIQUE_CUSTOMER_COUNT,
)


def load_csvs(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    customers = pd.read_csv(data_dir / "customers.csv")
    orders = pd.read_csv(data_dir / "orders.csv")
    products = pd.read_csv(data_dir / "products.csv")
    return customers, orders, products


def valid_customer_ids(customers: pd.DataFrame) -> set:
    return set(customers["customer_id"].dropna().unique())


def valid_product_ids(products: pd.DataFrame) -> set:
    return set(products["product_id"].unique())


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
    valid_ids = valid_customer_ids(customers)
    mask = orders["customer_id"].notna() & ~orders["customer_id"].isin(valid_ids)
    return int(mask.sum())


def count_intentional_orphan_customer_ids(orders: pd.DataFrame) -> int:
    return int(orders["customer_id"].isin(ORPHAN_CUSTOMER_IDS).sum())


def count_unintended_orphan_customer_ids(orders: pd.DataFrame, customers: pd.DataFrame) -> int:
    valid_ids = valid_customer_ids(customers)
    orphan_mask = orders["customer_id"].notna() & ~orders["customer_id"].isin(valid_ids)
    intentional_mask = orders["customer_id"].isin(ORPHAN_CUSTOMER_IDS)
    return int((orphan_mask & ~intentional_mask).sum())


def count_orphan_product_ids(orders: pd.DataFrame, products: pd.DataFrame) -> int:
    valid_ids = valid_product_ids(products)
    mask = orders["product_id"].notna() & ~orders["product_id"].isin(valid_ids)
    return int(mask.sum())


def count_intentional_orphan_product_ids(orders: pd.DataFrame) -> int:
    return int(orders["product_id"].isin(ORPHAN_PRODUCT_IDS).sum())


def count_unintended_orphan_product_ids(orders: pd.DataFrame, products: pd.DataFrame) -> int:
    valid_ids = valid_product_ids(products)
    orphan_mask = orders["product_id"].notna() & ~orders["product_id"].isin(valid_ids)
    intentional_mask = orders["product_id"].isin(ORPHAN_PRODUCT_IDS)
    return int((orphan_mask & ~intentional_mask).sum())


def count_duplicate_order_ids(orders: pd.DataFrame) -> int:
    return int(orders["order_id"].duplicated(keep="first").sum())


def count_valid_customer_fk_violations(orders: pd.DataFrame, customers: pd.DataFrame) -> int:
    """Non-null customer_id values outside customers, excluding intentional orphan IDs."""
    return count_unintended_orphan_customer_ids(orders, customers)


def count_valid_product_fk_violations(orders: pd.DataFrame, products: pd.DataFrame) -> int:
    """Non-null product_id values outside products, excluding intentional orphan IDs."""
    return count_unintended_orphan_product_ids(orders, products)


def assert_issue_counts(data_dir: Path) -> None:
    customers, orders, products = load_csvs(data_dir)

    assert len(customers) == CUSTOMER_COUNT
    assert len(orders) == ORDER_COUNT
    assert len(products) == PRODUCT_COUNT

    assert count_null_emails(customers) == NULL_EMAIL_COUNT
    assert count_duplicate_customer_ids(customers) == DUP_CUSTOMER_ID_COUNT
    assert count_null_customer_ids(orders) == NULL_CUSTOMER_ID_COUNT
    assert count_null_product_ids(orders) == NULL_PRODUCT_ID_COUNT
    assert count_intentional_orphan_customer_ids(orders) == len(ORPHAN_CUSTOMER_IDS)
    assert count_orphan_customer_ids(orders, customers) == len(ORPHAN_CUSTOMER_IDS)
    assert count_intentional_orphan_product_ids(orders) == len(ORPHAN_PRODUCT_IDS)
    assert count_orphan_product_ids(orders, products) == len(ORPHAN_PRODUCT_IDS)
    assert count_duplicate_order_ids(orders) == DUP_ORDER_ID_COUNT
    assert count_unintended_orphan_customer_ids(orders, customers) == 0
    assert count_unintended_orphan_product_ids(orders, products) == 0

    # IDs 1..10 appear twice (duplicate rows); IDs 11..UNIQUE_CUSTOMER_COUNT appear once
    id_counts = customers["customer_id"].value_counts()
    for cid in range(1, DUP_CUSTOMER_ID_COUNT + 1):
        assert id_counts.get(cid, 0) == 2, f"customer_id {cid} should appear exactly twice"
    for cid in range(DUP_CUSTOMER_ID_COUNT + 1, UNIQUE_CUSTOMER_COUNT + 1):
        assert id_counts.get(cid, 0) == 1, f"customer_id {cid} should appear exactly once"


def summarize_counts(data_dir: Path) -> dict[str, int]:
    """Return observed DQ and row counts for reporting."""
    customers, orders, products = load_csvs(data_dir)
    return {
        "customer_rows": len(customers),
        "order_rows": len(orders),
        "product_rows": len(products),
        "null_emails": count_null_emails(customers),
        "duplicate_customer_ids": count_duplicate_customer_ids(customers),
        "null_order_customer_ids": count_null_customer_ids(orders),
        "null_order_product_ids": count_null_product_ids(orders),
        "orphan_customer_ids": count_orphan_customer_ids(orders, customers),
        "intentional_orphan_customer_ids": count_intentional_orphan_customer_ids(orders),
        "unintended_orphan_customer_ids": count_unintended_orphan_customer_ids(orders, customers),
        "orphan_product_ids": count_orphan_product_ids(orders, products),
        "intentional_orphan_product_ids": count_intentional_orphan_product_ids(orders),
        "unintended_orphan_product_ids": count_unintended_orphan_product_ids(orders, products),
        "duplicate_order_ids": count_duplicate_order_ids(orders),
        "unique_customer_ids_in_customers": customers["customer_id"].nunique(),
    }

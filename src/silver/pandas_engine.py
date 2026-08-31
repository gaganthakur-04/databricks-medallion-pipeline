"""Pandas-based Silver quality evaluation for local testing."""

from __future__ import annotations

import pandas as pd

from src.silver.rules import (
    CUST_BIZ_001,
    CUST_COMP_001,
    CUST_UNIQ_001,
    ORD_BIZ_001,
    ORD_BIZ_002,
    ORD_COMP_001,
    ORD_COMP_002,
    ORD_REF_001,
    ORD_REF_002,
    ORD_UNIQ_001,
    PROD_BIZ_001,
    PROD_BIZ_002,
    PROD_BIZ_003,
    VALID_CUSTOMER_SEGMENTS,
    VALID_ORDER_STATUSES,
    build_quality_result,
    format_failure,
)


def _duplicate_mask(series: pd.Series) -> pd.Series:
    return series.duplicated(keep="first")


def validate_customers_pandas(customers: pd.DataFrame) -> pd.DataFrame:
    df = customers.copy()
    duplicate_ids = _duplicate_mask(df["customer_id"])
    failures: list[list[str]] = []

    for _, row in df.iterrows():
        row_failures: list[str] = []
        if pd.isna(row["email"]):
            row_failures.append(format_failure(CUST_COMP_001))
        if duplicate_ids.loc[row.name]:
            row_failures.append(format_failure(CUST_UNIQ_001))
        if row["customer_segment"] not in VALID_CUSTOMER_SEGMENTS:
            row_failures.append(format_failure(CUST_BIZ_001))
        failures.append(row_failures)

    results = [build_quality_result(f) for f in failures]
    df["quality_check_result"] = [r[0] for r in results]
    df["is_valid"] = [r[1] for r in results]
    return df


def validate_products_pandas(products: pd.DataFrame) -> pd.DataFrame:
    df = products.copy()
    failures: list[list[str]] = []

    for _, row in df.iterrows():
        row_failures: list[str] = []
        if row["price"] < 0:
            row_failures.append(format_failure(PROD_BIZ_001))
        if row["cost"] < 0:
            row_failures.append(format_failure(PROD_BIZ_002))
        if row["stock_quantity"] < 0:
            row_failures.append(format_failure(PROD_BIZ_003))
        failures.append(row_failures)

    results = [build_quality_result(f) for f in failures]
    df["quality_check_result"] = [r[0] for r in results]
    df["is_valid"] = [r[1] for r in results]
    return df


def validate_orders_pandas(
    orders: pd.DataFrame,
    customers: pd.DataFrame,
    products: pd.DataFrame,
) -> pd.DataFrame:
    df = orders.copy()
    valid_customer_ids = set(customers["customer_id"].dropna().unique())
    valid_product_ids = set(products["product_id"].dropna().unique())
    duplicate_ids = _duplicate_mask(df["order_id"])

    failures: list[list[str]] = []
    for _, row in df.iterrows():
        row_failures: list[str] = []
        if pd.isna(row["customer_id"]):
            row_failures.append(format_failure(ORD_COMP_001))
        if pd.isna(row["product_id"]):
            row_failures.append(format_failure(ORD_COMP_002))
        if duplicate_ids.loc[row.name]:
            row_failures.append(format_failure(ORD_UNIQ_001))
        if pd.notna(row["customer_id"]) and row["customer_id"] not in valid_customer_ids:
            row_failures.append(format_failure(ORD_REF_001))
        if pd.notna(row["product_id"]) and row["product_id"] not in valid_product_ids:
            row_failures.append(format_failure(ORD_REF_002))
        if row["order_status"] not in VALID_ORDER_STATUSES:
            row_failures.append(format_failure(ORD_BIZ_001))
        expected_total = round(float(row["quantity"]) * float(row["unit_price"]), 2)
        actual_total = round(float(row["total_amount"]), 2)
        if expected_total != actual_total:
            row_failures.append(format_failure(ORD_BIZ_002))
        failures.append(row_failures)

    results = [build_quality_result(f) for f in failures]
    df["quality_check_result"] = [r[0] for r in results]
    df["is_valid"] = [r[1] for r in results]
    return df


def count_rule_occurrences(df: pd.DataFrame, rule_id: str) -> int:
    return int(df["quality_check_result"].str.contains(rule_id, regex=False).sum())

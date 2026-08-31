"""Silver data-quality rule identifiers and messages."""

from __future__ import annotations

# Completeness
CUST_COMP_001 = "CUST_COMP_001"
ORD_COMP_001 = "ORD_COMP_001"
ORD_COMP_002 = "ORD_COMP_002"

# Uniqueness
CUST_UNIQ_001 = "CUST_UNIQ_001"
ORD_UNIQ_001 = "ORD_UNIQ_001"

# Referential integrity
ORD_REF_001 = "ORD_REF_001"
ORD_REF_002 = "ORD_REF_002"

# Business / type validation
CUST_BIZ_001 = "CUST_BIZ_001"
ORD_BIZ_001 = "ORD_BIZ_001"
ORD_BIZ_002 = "ORD_BIZ_002"
PROD_BIZ_001 = "PROD_BIZ_001"
PROD_BIZ_002 = "PROD_BIZ_002"
PROD_BIZ_003 = "PROD_BIZ_003"

VALID_CUSTOMER_SEGMENTS = ("Premium", "Standard", "Basic")
VALID_ORDER_STATUSES = ("Pending", "Completed", "Cancelled")

RULE_MESSAGES: dict[str, str] = {
    CUST_COMP_001: "email is NULL",
    CUST_UNIQ_001: "duplicate customer_id",
    CUST_BIZ_001: "invalid customer_segment",
    ORD_COMP_001: "customer_id is NULL",
    ORD_COMP_002: "product_id is NULL",
    ORD_UNIQ_001: "duplicate order_id",
    ORD_REF_001: "customer_id not found in customers",
    ORD_REF_002: "product_id not found in products",
    ORD_BIZ_001: "invalid order_status",
    ORD_BIZ_002: "total_amount does not equal quantity * unit_price",
    PROD_BIZ_001: "price is negative",
    PROD_BIZ_002: "cost is negative",
    PROD_BIZ_003: "stock_quantity is negative",
}


def format_failure(rule_id: str) -> str:
    return f"{rule_id} — {RULE_MESSAGES[rule_id]}"


def build_quality_result(failures: list[str]) -> tuple[str, bool]:
    if not failures:
        return "PASS", True
    return "FAIL: " + "; ".join(failures), False

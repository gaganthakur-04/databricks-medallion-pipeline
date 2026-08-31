"""Silver layer: referential integrity (customer_id, product_id FK checks)."""

from src.silver.rules import ORD_REF_001, ORD_REF_002

__all__ = ["ORD_REF_001", "ORD_REF_002"]

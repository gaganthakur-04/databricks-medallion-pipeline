"""
Generate e-commerce sample CSV files with intentional data quality issues.

Assessment specs:
  customers.csv  — 10,000 rows
  orders.csv     — 100,000 rows
  products.csv   — 500 rows
"""

from __future__ import annotations

import argparse
import random
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

import pandas as pd
from faker import Faker

# ---------------------------------------------------------------------------
# Row counts
# ---------------------------------------------------------------------------
CUSTOMER_COUNT = 10_000
ORDER_COUNT = 100_000
PRODUCT_COUNT = 500

# ---------------------------------------------------------------------------
# Intentional DQ issue counts (assessment-required)
# ---------------------------------------------------------------------------
NULL_EMAIL_COUNT = 50
DUP_CUSTOMER_ID_COUNT = 10
NULL_CUSTOMER_ID_COUNT = 100
NULL_PRODUCT_ID_COUNT = 200
ORPHAN_CUSTOMER_ID_COUNT = 50
ORPHAN_PRODUCT_ID_COUNT = 30
DUP_ORDER_ID_COUNT = 20

# Unique customer IDs in the parent table (1..UNIQUE_CUSTOMER_COUNT); plus DUP duplicate rows.
UNIQUE_CUSTOMER_COUNT = CUSTOMER_COUNT - DUP_CUSTOMER_ID_COUNT  # 9,990

# IDs that do not exist in parent tables (for referential integrity issues)
ORPHAN_CUSTOMER_IDS = list(range(90_001, 90_001 + ORPHAN_CUSTOMER_ID_COUNT))
ORPHAN_PRODUCT_IDS = list(range(901, 901 + ORPHAN_PRODUCT_ID_COUNT))

SEGMENTS = ["Premium", "Standard", "Basic"]
ORDER_STATUSES = ["Pending", "Completed", "Cancelled"]
CATEGORIES = ["Electronics", "Clothing", "Home", "Sports", "Books", "Beauty", "Toys"]
COUNTRIES = ["US", "UK", "CA", "AU", "DE", "FR", "IN", "JP", "BR", "MX"]

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parents[2] / "data"
RANDOM_SEED = 42

# Order rows receiving each injected issue (disjoint random samples, seed-driven).
ORDER_DQ_SAMPLE_SIZES = [
    NULL_CUSTOMER_ID_COUNT,
    NULL_PRODUCT_ID_COUNT,
    ORPHAN_CUSTOMER_ID_COUNT,
    ORPHAN_PRODUCT_ID_COUNT,
    DUP_ORDER_ID_COUNT,
]


def _money(value: float) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def _customer_row(fake: Faker, customer_id: int, start: date, span: int) -> dict:
    signup = start + timedelta(days=random.randint(0, span))
    return {
        "customer_id": customer_id,
        "customer_name": fake.name(),
        "email": fake.email(),
        "country": random.choice(COUNTRIES),
        "signup_date": signup.isoformat(),
        "customer_segment": random.choice(SEGMENTS),
        "lifetime_value": _money(random.uniform(100, 50_000)),
    }


def _sample_disjoint_indices(total: int, sizes: list[int]) -> list[list[int]]:
    """Return disjoint row-index groups of the given sizes (shuffled, seed-driven)."""
    if sum(sizes) > total:
        raise ValueError("Sample sizes exceed total row count")
    indices = list(range(total))
    random.shuffle(indices)
    groups: list[list[int]] = []
    offset = 0
    for size in sizes:
        groups.append(indices[offset : offset + size])
        offset += size
    return groups


def generate_products(fake: Faker) -> pd.DataFrame:
    rows = []
    for product_id in range(1, PRODUCT_COUNT + 1):
        cost = _money(random.uniform(5, 200))
        markup = random.uniform(1.2, 2.5)
        price = _money(float(cost) * markup)
        rows.append(
            {
                "product_id": product_id,
                "product_name": fake.catch_phrase(),
                "category": random.choice(CATEGORIES),
                "price": price,
                "cost": cost,
                "stock_quantity": random.randint(0, 500),
                "reorder_level": random.randint(10, 50),
            }
        )
    return pd.DataFrame(rows)


def generate_customers(fake: Faker) -> pd.DataFrame:
    start = date(2020, 1, 1)
    end = date(2024, 12, 31)
    span = (end - start).days

    rows = []
    # 9,990 rows with unique customer_id 1..9,990
    for customer_id in range(1, UNIQUE_CUSTOMER_COUNT + 1):
        rows.append(_customer_row(fake, customer_id, start, span))

    # 10 additional rows duplicating customer_id 1..10 (uniqueness violations)
    for duplicate_id in range(1, DUP_CUSTOMER_ID_COUNT + 1):
        rows.append(_customer_row(fake, duplicate_id, start, span))

    df = pd.DataFrame(rows)

    # Completeness: 50 NULL emails on randomly sampled rows (seed-driven)
    null_email_idx = random.sample(range(CUSTOMER_COUNT), NULL_EMAIL_COUNT)
    df.loc[null_email_idx, "email"] = None

    return df


def generate_orders(fake: Faker, products: pd.DataFrame, customers: pd.DataFrame) -> pd.DataFrame:
    product_ids = products["product_id"].tolist()
    product_price = dict(zip(products["product_id"], products["price"]))
    valid_customer_ids = set(customers["customer_id"].unique())
    start = date(2023, 1, 1)
    end = date(2024, 12, 31)
    span = (end - start).days

    rows = []
    for order_id in range(1, ORDER_COUNT + 1):
        # Only reference customer IDs that exist in the customers dataset (1..9,990)
        customer_id = random.randint(1, UNIQUE_CUSTOMER_COUNT)
        product_id = random.choice(product_ids)
        quantity = random.randint(1, 5)
        unit_price = product_price[product_id]
        total_amount = _money(float(unit_price) * quantity)
        status = random.choices(ORDER_STATUSES, weights=[10, 80, 10], k=1)[0]
        order_date = start + timedelta(days=random.randint(0, span))
        payment_date = order_date if status == "Completed" else None

        rows.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date.isoformat(),
                "product_id": product_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_amount": total_amount,
                "order_status": status,
                "payment_date": payment_date.isoformat() if payment_date else None,
            }
        )

    df = pd.DataFrame(rows)

    (
        idx_null_customer,
        idx_null_product,
        idx_orphan_customer,
        idx_orphan_product,
        idx_dup_order,
    ) = _sample_disjoint_indices(ORDER_COUNT, ORDER_DQ_SAMPLE_SIZES)

    for row_idx in idx_null_customer:
        df.at[row_idx, "customer_id"] = None

    for row_idx in idx_null_product:
        df.at[row_idx, "product_id"] = None

    for i, row_idx in enumerate(idx_orphan_customer):
        df.at[row_idx, "customer_id"] = ORPHAN_CUSTOMER_IDS[i]

    for i, row_idx in enumerate(idx_orphan_product):
        df.at[row_idx, "product_id"] = ORPHAN_PRODUCT_IDS[i]

    for i, row_idx in enumerate(idx_dup_order):
        df.at[row_idx, "order_id"] = (i % DUP_ORDER_ID_COUNT) + 1

    # Sanity: valid rows must only use customer IDs present in customers
    assert valid_customer_ids == set(range(1, UNIQUE_CUSTOMER_COUNT + 1))

    return df


def write_csvs(output_dir: Path, seed: int = RANDOM_SEED) -> dict[str, Path]:
    fake = Faker()
    Faker.seed(seed)
    random.seed(seed)

    output_dir.mkdir(parents=True, exist_ok=True)

    products = generate_products(fake)
    customers = generate_customers(fake)
    orders = generate_orders(fake, products, customers)

    paths = {
        "customers": output_dir / "customers.csv",
        "orders": output_dir / "orders.csv",
        "products": output_dir / "products.csv",
    }

    customers.to_csv(paths["customers"], index=False)
    orders.to_csv(paths["orders"], index=False)
    products.to_csv(paths["products"], index=False)

    return paths


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate assessment sample CSV files.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=RANDOM_SEED,
        help=f"Random seed (default: {RANDOM_SEED})",
    )
    args = parser.parse_args()

    paths = write_csvs(args.output_dir, seed=args.seed)
    for name, path in paths.items():
        row_count = sum(1 for _ in open(path)) - 1  # exclude header
        print(f"Wrote {path} ({row_count:,} rows)")


if __name__ == "__main__":
    main()

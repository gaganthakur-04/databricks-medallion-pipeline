# Data Generation Notes

## Purpose

Generate realistic e-commerce CSV files for the Databricks Medallion assessment with **intentional data quality issues** for Silver layer validation.

## Script

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/data_generation/generate_sample_data.py
```

Output: `data/customers.csv`, `data/orders.csv`, `data/products.csv`

Optional: `--seed <int>` to change the random seed (default `42`).

## Reproducibility

| Mechanism | Value | Purpose |
|-----------|-------|---------|
| `RANDOM_SEED` | `42` (default) | Seeds Python `random` module |
| `Faker.seed(seed)` | called in `write_csvs()` | Seeds Faker text generation |
| Generation order | products → customers → orders | Fixed call sequence |

Re-running with the **same seed** produces byte-identical CSV files. Changing the seed changes row content and which rows receive injected issues, but **counts remain exact**.

## Row Counts

| File | Rows | How |
|------|------|-----|
| `customers.csv` | **10,000** | 9,990 unique rows + 10 duplicate-key rows |
| `orders.csv` | **100,000** | One row per `order_id` 1..100,000 |
| `products.csv` | **500** | One row per `product_id` 1..500 |

## Customer Generation Strategy

### Unique customers (9,990 rows)

`customer_id` **1..9,990** — each appears **exactly once**.

### Duplicate customers (10 rows)

10 additional rows appended with `customer_id` **1..10**, creating exactly **10 uniqueness violations** (`duplicated(keep="first") == 10`).

### Why this prevents unintended orphan orders

The previous approach **overwrote** 10 existing rows to duplicate IDs 1..10, which **removed** 10 legitimate `customer_id` values from the parent table. Orders referencing those IDs became unintended referential-integrity failures.

The corrected approach **appends** 10 duplicate rows instead of overwriting, so:

- All IDs **1..9,990** remain in `customers.csv`
- IDs **1..10** each appear twice (once in unique set, once in duplicate set)
- Valid orders sample `customer_id` from **1..9,990** only
- Only the **50 intentionally injected** orphan rows use IDs **90,001..90,050**

### NULL emails (50 rows)

50 rows selected via `random.sample(range(10000), 50)` (seed-driven, not fixed positions).

## Order Generation Strategy

### Valid orders (99,600 rows after DQ injection)

- `customer_id`: random integer **1..9,990** (always exists in customers)
- `product_id`: random from **1..500**
- `total_amount = quantity × unit_price`
- `payment_date` set only when `order_status = Completed`

### Injected issues (400 rows, disjoint random samples)

Order DQ issues are applied to **disjoint randomly sampled row indices** (via `_sample_disjoint_indices`), not fixed positions 0..399. The seed determines which rows are affected, so issues are traceable and reproducible without hard-coding row numbers.

| Issue | Count | Value applied |
|-------|-------|---------------|
| NULL `customer_id` | 100 | `None` |
| NULL `product_id` | 200 | `None` |
| Orphan `customer_id` | 50 | 90,001..90,050 |
| Orphan `product_id` | 30 | 901..930 |
| Duplicate `order_id` | 20 | Reassigned to `order_id` 1..20 |

Sample groups are **disjoint** — a row receives at most one injected issue type.

## Intentional Quality Issue Summary

| Entity | Issue | Count |
|--------|-------|-------|
| customers | NULL `email` | 50 |
| customers | Duplicate `customer_id` | 10 |
| orders | NULL `customer_id` | 100 |
| orders | NULL `product_id` | 200 |
| orders | Orphan `customer_id` | 50 |
| orders | Orphan `product_id` | 30 |
| orders | Duplicate `order_id` | 20 |
| products | (none) | — |

**Unintended FK violations:** 0 (verified by tests).

## Testing

```bash
pytest tests/data_generation/ -v
```

Validation helpers: `src/data_generation/validate_data.py`

## Assumptions

1. Duplicate `customer_id` means 10 rows fail uniqueness, not 10 extra rows beyond 10,000.
2. Orphan ID ranges 90,001..90,050 and 901..930 are outside valid parent keys.
3. Valid orders reference `customer_id` 1..9,990 only.
4. Faker is acceptable for realistic text fields.

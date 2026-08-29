# Data Generation

Scripts to generate source CSV files with required row counts, schemas, and intentional data quality issues.

## Planned Contents

- `generate_data.py` — main generator
- Configuration for row counts and DQ issue injection
- Validation script to verify output against assessment specs

## Output

Generated files written to `data/sample/`:

- `customers.csv` (10,000 rows)
- `orders.csv` (100,000 rows)
- `products.csv` (500 rows)

## Status

Not started. See `cursor-workflow/task-breakdown.md` Phase 2.

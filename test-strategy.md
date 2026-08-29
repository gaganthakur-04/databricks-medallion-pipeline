# Test Strategy

## Objectives

Verify pipeline correctness, data quality detection, and aggregation accuracy against assessment acceptance criteria.

## Test Tiers

| Tier | Scope | Location | When |
|------|-------|----------|------|
| Data generation | Row counts, schemas, intentional DQ issue counts | `tests/data_generation/` | After CSV generation |
| Silver DQ | Each quality check flags correct rows | `tests/silver/` | Silver implementation |
| Gold | Aggregation math on known fixtures | `tests/gold/` | Gold implementation |
| Integration | CSV → Bronze → Silver → Gold end-to-end | `tests/integration/` | After all layers |

## Data Quality Validation Targets

After Silver processing, flag counts must match intentional seeded issues:

| Check | Expected count |
|-------|----------------|
| NULL email (customers) | 50 |
| Duplicate customer_id | 10 rows involved |
| NULL customer_id (orders) | 100 |
| NULL product_id (orders) | 200 |
| Orphan customer_id | 50 |
| Orphan product_id | 30 |
| Duplicate order_id | 20 rows involved |

## Running Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Databricks Validation

Manual checklist in Databricks after deployment:

- [ ] Bronze row counts match CSVs
- [ ] Silver retains all Bronze rows
- [ ] Quality metrics report shows % passed per check
- [ ] Gold tables populated
- [ ] Dashboard displays 3 visualizations

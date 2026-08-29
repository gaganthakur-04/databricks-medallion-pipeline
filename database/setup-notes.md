# Database Setup Notes

## Prerequisites

- Databricks workspace (Community Edition or other)
- SQL warehouse or cluster with Unity Catalog enabled **(Assumption)**

## Execution

1. Open `database/schema.sql` in a Databricks SQL editor or notebook
2. Run the full script to create catalog, schemas, and empty Delta tables
3. Verify:

```sql
SHOW SCHEMAS IN ecommerce_dev;
SHOW TABLES IN ecommerce_dev.bronze;
SHOW TABLES IN ecommerce_dev.silver;
SHOW TABLES IN ecommerce_dev.gold;
```

## Catalog Naming

Default catalog: `ecommerce_dev`. Update `docs/candidate-info.md` if using a different name, then find-replace in pipeline code.

## CSV Landing Zone

**(Assumption)** Upload generated CSVs from `data/` to DBFS or a volume:

```
/dbfs/FileStore/ecommerce/raw/customers.csv
/dbfs/FileStore/ecommerce/raw/orders.csv
/dbfs/FileStore/ecommerce/raw/products.csv
```

Bronze ingestion scripts will reference these paths (configured in Phase 3).

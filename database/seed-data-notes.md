# Seed Data Notes

## Generation

```bash
pip install -r requirements.txt
python src/data_generation/generate_sample_data.py
```

Output files (gitignored due to size):

| File | Rows | Location |
|------|------|----------|
| customers.csv | 10,000 | `data/customers.csv` |
| orders.csv | 100,000 | `data/orders.csv` |
| products.csv | 500 | `data/products.csv` |

## Intentional Quality Issues

See `src/data_generation/DATA_GENERATION_NOTES.md` for full details (~700 problematic rows).

## Upload to Databricks

Upload CSVs to DBFS or a Unity Catalog volume before Bronze ingestion:

```
/dbfs/FileStore/ecommerce/raw/customers.csv
/dbfs/FileStore/ecommerce/raw/orders.csv
/dbfs/FileStore/ecommerce/raw/products.csv
```

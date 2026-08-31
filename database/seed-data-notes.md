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

**Free Edition (validated 2026-08-31):** public DBFS `/FileStore` is disabled. Upload to UC volume:

```bash
databricks fs cp data/customers.csv dbfs:/Volumes/workspace/default/ecommerce_raw/customers.csv --profile ce --overwrite
# repeat for orders.csv and products.csv
```

Deploy/run with `--var="csv_input_dir=/Volumes/workspace/default/ecommerce_raw"`.

**DBFS-enabled workspaces:**

```
/dbfs/FileStore/ecommerce/raw/customers.csv
/dbfs/FileStore/ecommerce/raw/orders.csv
/dbfs/FileStore/ecommerce/raw/products.csv
```

# Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Structure

```
tests/
├── bronze/            # Config, datasets, ingest (Spark test skipped locally)
├── bundle/            # Bundle config and setup_schema SQL parsing
├── data_generation/   # Row counts, DQ issue counts, schemas
├── silver/            # Rule logic and flag counts
└── gold/              # Aggregation correctness
```

**Latest result:** 40 passed, 1 skipped (Spark bronze integration — requires local PySpark).

See [test-strategy.md](../test-strategy.md).

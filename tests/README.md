# Tests

```bash
pip install -r requirements.txt
pytest tests/ -v
```

## Structure

```
tests/
├── data_generation/   # Row counts, DQ issue counts, schemas
├── silver/            # (planned) Rule logic and flag counts
├── gold/              # (planned) Aggregation correctness
└── integration/       # (planned) End-to-end pipeline
```

See [test-strategy.md](../test-strategy.md).

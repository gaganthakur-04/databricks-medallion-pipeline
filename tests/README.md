# Tests

Automated tests for data generation, pipeline layers, and data quality validation.

## Planned Structure

```
tests/
├── data_generation/   # Row counts, issue counts, schema
├── bronze/            # Ingestion verification
├── silver/            # Rule logic and flag counts
├── gold/              # Aggregation correctness
└── integration/       # End-to-end pipeline
```

## Status

Not started. See `cursor-workflow/task-breakdown.md` Phase 7.

# Databricks Medallion Pipeline — E-Commerce Sales

Production-quality Databricks Medallion Architecture pipeline for an e-commerce sales use case, built as part of an AI-first data engineering assessment.

## Purpose

Ingest source CSV files through Bronze → Silver → Gold layers and expose business metrics via a Databricks SQL Dashboard. The project demonstrates the full AI-assisted engineering lifecycle.

## Architecture

```
Source CSVs (customers, orders, products)
        │
        ▼
   Bronze Layer          Raw ingestion (src/bronze/)
        │
        ▼
   Silver Layer          DQ validation (src/silver/)
        │
        ▼
   Gold Layer            Aggregations (src/gold/)
        │
        ▼
   Databricks SQL        Dashboard (src/dashboard/)
   Dashboard
```

## Current Status

| Phase | Status |
|-------|--------|
| Requirements analysis | Complete |
| Repository structure | Complete |
| Data generation | Complete (`src/data_generation/`) |
| Bronze layer | Complete (`src/bronze/`) |
| Silver layer | Complete (`src/silver/`) |
| Gold layer | Complete (`src/gold/`) |
| End-to-end pipeline | Complete (`src/pipeline/run_all.py`) |
| Databricks Asset Bundle | Complete (`databricks.yml`, `BUNDLE.md`) |
| Dashboard SQL queries | Complete (`src/dashboard/dashboard_queries.sql`) |
| Automated tests | Complete — 40 passed, 1 skipped |
| Databricks deploy / E2E / Dashboard UI | **Pending** — workspace authentication unavailable |

## Repository Structure

```
databricks-medallion-pipeline/
├── README.md
├── candidate-info.md
├── tool-workflow.md                    # Part A: AI Workflow Foundation
├── requirements-analysis.md
├── design-notes.md
├── data-model.md
├── data-quality-strategy.md
├── debugging-notes.md
├── reflection.md
├── final-ai-usage-summary.md
├── test-strategy.md                    # Assessment artifact
├── code-review-notes.md                # Assessment artifact
│
├── src/
│   ├── data_generation/
│   ├── bronze/
│   ├── silver/
│   ├── gold/
│   └── dashboard/
│
├── data/                               # Generated CSVs (gitignored)
├── database/                           # schema.sql, setup notes
├── tests/                              # pytest suites
├── ai-prompts/                         # Prompt history by activity
└── cursor-workflow/                    # Cursor-specific context (required)
```

## Getting Started

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Generate sample CSVs
python src/data_generation/generate_sample_data.py

# 3. Run tests
pytest tests/ -v

# 4. Databricks setup and pipeline (when workspace access is available)
#    See database/schema_community_edition.sql and BUNDLE.md
```

## Databricks Deployment

Bundle configuration is in `databricks.yml`. Local tests pass; actual Databricks deployment, end-to-end job execution, and SQL Dashboard UI creation remain **pending** because workspace authentication is currently unavailable. See `BUNDLE.md` and `src/dashboard/DASHBOARD_GUIDE.md`.

## Documentation Index

| Document | Purpose |
|----------|---------|
| [requirements-analysis.md](requirements-analysis.md) | Assessment requirements |
| [design-notes.md](design-notes.md) | Architecture decisions |
| [data-model.md](data-model.md) | Schemas across layers |
| [data-quality-strategy.md](data-quality-strategy.md) | DQ rules and flagging |
| [tool-workflow.md](tool-workflow.md) | AI workflow (Part A) |
| [candidate-info.md](candidate-info.md) | Candidate and environment |
| [cursor-workflow/project-context.md](cursor-workflow/project-context.md) | Cursor project context |
| [cursor-workflow/spec.md](cursor-workflow/spec.md) | Technical specification |
| [cursor-workflow/task-breakdown.md](cursor-workflow/task-breakdown.md) | Implementation phases |

## Assessment Artifacts

- **AI prompts:** `ai-prompts/` (one file per activity)
- **Cursor workflow:** `cursor-workflow/`
- **Reflection:** `reflection.md`, `final-ai-usage-summary.md`

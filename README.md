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
| Repository structure | Aligned to assessment template |
| Data generation | Script ready (`src/data_generation/`) |
| Bronze layer | Placeholder modules |
| Silver layer | Placeholder modules |
| Gold layer | Placeholder SQL/modules |
| Dashboard | Placeholder queries |
| Tests | Data generation tests |

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

# 4. Run database setup in Databricks
#    See database/schema.sql
```

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

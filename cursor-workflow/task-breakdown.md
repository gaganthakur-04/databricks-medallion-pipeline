# Task Breakdown

Logical implementation sequence for the Databricks Medallion pipeline. Archive significant AI prompts in `ai-prompts/<activity>.md`.

---

## Phase 0: Foundation ✅

- [x] Initialize git repository
- [x] Create folder structure (aligned to assessment template)
- [x] Write initial documentation
- [x] Establish Cursor workflow files
- [ ] Confirm open assumptions in `design-notes.md`

---

## Phase 1: Environment & Setup ✅

- [x] `database/schema.sql` — catalog, schemas, Delta tables
- [x] `.gitignore`, `requirements.txt`, `pytest.ini`
- [ ] Fill `candidate-info.md` with workspace details

**Prompt history:** `ai-prompts/documentation.md`

---

## Phase 2: Data Generation ✅

- [x] `src/data_generation/generate_sample_data.py`
- [x] Tests in `tests/data_generation/`
- [x] Output to `data/*.csv`

**Prompt history:** `ai-prompts/data-generation.md`

---

## Phase 3: Bronze Layer

| # | Task | Output |
|---|------|--------|
| 3.1 | Implement ingest modules | `src/bronze/01_*.py`, `ingest_all.py` |
| 3.2 | Add audit columns | `_ingested_at`, `_source_file`, `_batch_id` |
| 3.3 | Write to `bronze.*` Delta tables | Three tables |
| 3.4 | Verify row counts | Match CSVs |

**Prompt history:** `ai-prompts/bronze-layer.md`

---

## Phase 4: Silver Layer

| # | Task | Output |
|---|------|--------|
| 4.1 | Implement four quality checks | `src/silver/01_*.py` … `05_*.py` |
| 4.2 | Create silver tables | `create_silver_tables.py` |
| 4.3 | Quality metrics report | % passed per check |
| 4.4 | Tests | `tests/silver/` |

**Prompt history:** `ai-prompts/silver-layer.md`

---

## Phase 5: Gold Layer

| # | Task | Output |
|---|------|--------|
| 5.1 | Sales by Product | `src/gold/01_sales_by_product.sql` |
| 5.2 | Revenue by Customer | `src/gold/02_revenue_by_customer.sql` |
| 5.3 | Customer Segmentation | `src/gold/04_customer_segmentation.sql` |
| 5.4 | Orchestration | `create_gold_tables.py` |

**Prompt history:** `ai-prompts/gold-layer.md`

---

## Phase 6: Dashboard

| # | Task | Output |
|---|------|--------|
| 6.1 | Dashboard queries | `src/dashboard/dashboard_queries.sql` |
| 6.2 | Databricks SQL Dashboard | 3+ visualizations |
| 6.3 | Guide | `DASHBOARD_GUIDE.md` |

**Prompt history:** `ai-prompts/dashboard.md`

---

## Phase 7–8: Testing, Documentation & Submission

See `test-strategy.md`. Log issues in `debugging-notes.md`. Complete `reflection.md`, `final-ai-usage-summary.md`, `tool-workflow.md`.

## Recommended Next Task

**Phase 3: Bronze Layer** — implement `src/bronze/` ingestion modules.

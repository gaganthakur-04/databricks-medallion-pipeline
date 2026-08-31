# Task Breakdown

Logical implementation sequence for the Databricks Medallion pipeline. Archive significant AI prompts in `ai-prompts/<activity>.md`.

---

## Phase 0: Foundation ✅

- [x] Initialize git repository
- [x] Create folder structure (aligned to assessment template)
- [x] Write initial documentation
- [x] Establish Cursor workflow files
- [x] Confirm open assumptions in `design-notes.md`

---

## Phase 1: Environment & Setup ✅

- [x] `database/schema.sql` — catalog, schemas, Delta tables
- [x] `database/schema_community_edition.sql` — Hive metastore for Free Edition
- [x] `.gitignore`, `requirements.txt`, `pytest.ini`
- [x] Fill `candidate-info.md` with workspace details

**Prompt history:** `ai-prompts/documentation.md`

---

## Phase 2: Data Generation ✅

- [x] `src/data_generation/generate_sample_data.py`
- [x] Tests in `tests/data_generation/`
- [x] Output to `data/*.csv`

**Prompt history:** `ai-prompts/data-generation.md`

---

## Phase 3: Bronze Layer ✅

| # | Task | Output | Status |
|---|------|--------|--------|
| 3.1 | Implement ingest modules | `src/bronze/01_*.py`, `ingest_all.py` | Done |
| 3.2 | Add audit columns | `_ingested_at`, `_source_file`, `_batch_id` | Done |
| 3.3 | Write to `bronze.*` Delta tables | Three tables | Done — validated 10K/100K/500 |
| 3.4 | Verify row counts | Match CSVs | Done on Databricks |

**Prompt history:** `ai-prompts/bronze.md`

---

## Phase 4: Silver Layer ✅

| # | Task | Output | Status |
|---|------|--------|--------|
| 4.1 | Implement quality checks | `src/silver/` rules + `validate_all.py` | Done |
| 4.2 | Create silver tables | `silver.*` Delta tables | Done |
| 4.3 | Quality metrics report | % passed per check | Done — job logs + SQL |
| 4.4 | Tests | `tests/silver/` | Done |

**Prompt history:** `ai-prompts/silver-layer.md`

---

## Phase 5: Gold Layer ✅

| # | Task | Output | Status |
|---|------|--------|--------|
| 5.1 | Sales by Product | `gold.sales_by_product` | Done — 500 rows |
| 5.2 | Revenue by Customer | `gold.revenue_by_customer` | Done — 9,931 rows |
| 5.3 | Customer Segmentation | `gold.customer_segmentation` | Done — 4 segments |
| 5.4 | Orchestration | `src/gold/build_all.py` | Done |

**Prompt history:** `ai-prompts/gold-layer.md`

---

## Phase 6: Dashboard

| # | Task | Output | Status |
|---|------|--------|--------|
| 6.1 | Dashboard queries | `src/dashboard/dashboard_queries.sql` | Done — SQL validated |
| 6.2 | Databricks SQL Dashboard | 3+ visualizations | Not done — manual UI step |
| 6.3 | Guide | `DASHBOARD_GUIDE.md` | Done |

**Prompt history:** `ai-prompts/dashboard.md`

---

## Phase 7–8: Testing, Documentation & Submission ✅

- [x] Local pytest suite (40 passed, 1 skipped)
- [x] Databricks E2E validation (bundle deploy + job run)
- [x] Update `candidate-info.md`, `BUNDLE.md`, status docs
- [x] Log deploy issues in `debugging-notes.md`
- [ ] Complete `reflection.md` (candidate self-review)
- [ ] Finalize `final-ai-usage-summary.md` effectiveness ratings

## Recommended Next Task

**Create Databricks SQL Dashboard UI** — build three visualizations from validated queries in `src/dashboard/dashboard_queries.sql`.

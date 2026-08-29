# Task Breakdown

Logical implementation sequence for the Databricks Medallion pipeline. Each phase should update relevant documentation and archive significant AI prompts under `ai-prompt-history/<activity>/`.

---

## Phase 0: Foundation ✅ (current)

- [x] Initialize git repository
- [x] Create folder structure
- [x] Write initial documentation
- [x] Establish Cursor workflow files
- [ ] Confirm open assumptions with assessor or document decisions in `docs/design-notes.md`

**Exit criteria:** Repository structure and docs in place; no pipeline code yet.

---

## Phase 1: Environment & Setup

| # | Task | Output |
|---|------|--------|
| 1.1 | Define catalog/schema naming in `docs/candidate-info.md` | Named environment |
| 1.2 | Write `setup/` DDL scripts (catalog, schemas, volumes/paths) | Runnable setup |
| 1.3 | Add `.gitignore` (CSV data, `.env`, Databricks creds) | Clean repo hygiene |
| 1.4 | **(Assumption)** Configure local dev dependencies (`requirements.txt` or `pyproject.toml`) | Reproducible env |

**Exit criteria:** Setup scripts run successfully in Databricks workspace.

---

## Phase 2: Data Generation

| # | Task | Output |
|---|------|--------|
| 2.1 | Implement `data-generation/generate_data.py` | Generator script |
| 2.2 | Generate valid base data for all three entities | Valid rows |
| 2.3 | Inject intentional DQ issues with exact counts | Seeded bad data |
| 2.4 | Validate output: row counts, schemas, issue counts | Generator tests |
| 2.5 | Write CSVs to `data/sample/` | Source files |

**Exit criteria:** CSVs match assessment specs; tests confirm issue counts.

**Prompt history:** `ai-prompt-history/data-generation/`

---

## Phase 3: Bronze Layer

| # | Task | Output |
|---|------|--------|
| 3.1 | Implement Bronze ingest for customers, orders, products | `bronze/` modules |
| 3.2 | Add audit columns (`_ingested_at`, `_source_file`, `_batch_id`) | Traceable loads |
| 3.3 | Write to Delta tables in `bronze` schema | Three Bronze tables |
| 3.4 | Verify row counts match source CSVs | Bronze validation |

**Exit criteria:** Bronze tables = source row counts (including bad rows).

**Prompt history:** `ai-prompt-history/bronze/`

---

## Phase 4: Silver Layer

| # | Task | Output |
|---|------|--------|
| 4.1 | Define rule functions per quality area | `silver/rules/` or equivalent |
| 4.2 | Implement Silver transforms with flag columns | `silver/` modules |
| 4.3 | Process in order: products → customers → orders | Correct FK checks |
| 4.4 | Verify intentional issue detection counts | Silver validation |
| 4.5 | Confirm no records deleted vs Bronze | Row count parity |
| 4.6 | Write Silver unit and integration tests | `tests/silver/` |

**Exit criteria:** All DQ issues flagged; all Bronze rows present in Silver.

**Prompt history:** `ai-prompt-history/silver/`

---

## Phase 5: Gold Layer

| # | Task | Output |
|---|------|--------|
| 5.1 | Implement `gold.sales_by_product` | Gold table |
| 5.2 | Implement `gold.revenue_by_customer` | Gold table |
| 5.3 | Implement `gold.customer_segmentation` | Gold table |
| 5.4 | Write Gold tests with known fixtures | `tests/gold/` |
| 5.5 | Document business rules in `docs/design-notes.md` | Decision log |

**Exit criteria:** Three Gold tables populated from valid Silver data.

**Prompt history:** `ai-prompt-history/gold/`

---

## Phase 6: Dashboard

| # | Task | Output |
|---|------|--------|
| 6.1 | Write SQL for top 10 products by revenue | `dashboard/top_products_by_revenue.sql` |
| 6.2 | Write SQL for customer revenue distribution | `dashboard/customer_revenue_distribution.sql` |
| 6.3 | Write SQL for customer segmentation | `dashboard/customer_segmentation.sql` |
| 6.4 | Create Databricks SQL Dashboard | Live dashboard |
| 6.5 | Screenshot or link in `docs/candidate-info.md` | Submission evidence |

**Exit criteria:** Dashboard live with all three required visualizations.

**Prompt history:** `ai-prompt-history/dashboard/`

---

## Phase 7: Testing & Validation

| # | Task | Output |
|---|------|--------|
| 7.1 | End-to-end integration test | `tests/integration/` |
| 7.2 | DQ count regression tests | Flag count assertions |
| 7.3 | Manual validation checklist | Documented in README or candidate-info |
| 7.4 | Fix failures; log in `docs/debugging-notes.md` | Clean test run |

**Exit criteria:** All tests pass; DQ counts verified.

**Prompt history:** `ai-prompt-history/testing/`, `ai-prompt-history/debugging/`

---

## Phase 8: Documentation & Submission

| # | Task | Output |
|---|------|--------|
| 8.1 | Finalize `docs/design-notes.md` | Complete decision log |
| 8.2 | Complete `docs/reflection.md` | Reflection |
| 8.3 | Complete `docs/final-ai-usage-summary.md` | AI usage summary |
| 8.4 | Archive all significant prompts | `ai-prompt-history/` |
| 8.5 | Update README status table | Current state |
| 8.6 | Fill `docs/candidate-info.md` | Submission ready |

**Exit criteria:** All assessment artifacts complete.

**Prompt history:** `ai-prompt-history/documentation/`

---

## Dependency Graph

```
Phase 0 (Foundation)
    │
    ▼
Phase 1 (Setup)
    │
    ▼
Phase 2 (Data Generation)
    │
    ▼
Phase 3 (Bronze)
    │
    ▼
Phase 4 (Silver) ──► Phase 7 (Testing)
    │
    ▼
Phase 5 (Gold)
    │
    ▼
Phase 6 (Dashboard)
    │
    ▼
Phase 8 (Documentation & Submission)
```

## Recommended Next Task

**Phase 1: Environment & Setup** — Write `setup/` DDL scripts, add `.gitignore`, and confirm catalog/schema naming assumptions in `docs/design-notes.md`.

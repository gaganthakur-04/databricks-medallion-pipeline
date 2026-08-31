# AI Prompts — Silver Layer

## Prompt 1: Silver and Gold implementation (2026-08-31)

**PROMPT SENT:**

> Data generation is complete and merged. Bronze has been implemented and reviewed. Do not revisit those phases unless you encounter an actual blocker.
>
> Implement the remaining core Medallion layers: Silver and Gold.
>
> Use existing assessment requirements, `requirements-analysis.md`, `design-notes.md`, `data-model.md`, `data-quality-strategy.md`, and `cursor-workflow` documentation as source of truth.
>
> Silver: read Bronze tables, retain all rows, implement DQ validations with rule IDs, add quality/status columns, preserve invalid records, referential integrity checks, no silent removal.
>
> Gold: read from Silver, valid records for business metrics, required aggregations, dashboard-ready tables, simple assessment-focused implementation.
>
> Create end-to-end entry point Bronze → Silver → Gold. Add tests. Update documentation. Record in ai-prompts. Do not commit or push.

**AI RESPONSE SUMMARY:**

Implemented Silver and Gold with shared PySpark transforms:

**Silver (`src/silver/`):**
- `rules.py` — 13 rule IDs (COMP/UNIQ/REF/BIZ)
- `transforms.py` — Spark DQ transforms; processing order products → customers → orders
- `pandas_engine.py` — pandas mirror for local tests
- `validate_all.py` — orchestrator with quality metrics report
- Output columns: `quality_check_result`, `is_valid`, `_silver_processed_at`

**Gold (`src/gold/`):**
- `transforms.py` — sales_by_product, revenue_by_customer, customer_segmentation
- `build_all.py` — orchestrator
- Updated SQL reference files for dashboard queries
- Valid Silver + Completed orders for revenue; behavioral segmentation with priority

**Pipeline (`src/pipeline/run_all.py`):** Bronze → Silver → Gold with `--skip-bronze` option.

**Tests:** 7 new tests in `tests/silver/` and `tests/gold/` — all passing (intentional DQ counts verified).

**Schema:** added `is_valid` to `schema_community_edition.sql` silver tables.

**Assumptions:**
- Referential integrity uses distinct parent keys from Bronze customers/products
- Duplicate PK rows flagged via `row_number() > 1` (10 customer, 20 order rows)
- High-Value segment = revenue ≥ 75th percentile among customers with completed orders
- Gold revenue excludes Pending/Cancelled orders

**YOUR EVALUATION:** _Pending_

---

## Prompt 2: Separate branch for Silver/Gold (2026-08-31)

**PROMPT SENT:**

> We needed these changes in a separate branch because this is not part of phase1 setup and data generation. Could you please do the needful if possible.

**AI RESPONSE SUMMARY:**

Created branch `cursor/phase2-silver-gold` from phase1 tip. Committed all 33 Silver/Gold/pipeline files as `15678a7`. Left `cursor/phase1-setup-and-data-generation` unchanged (data generation + Bronze only).

**YOUR EVALUATION:** _Pending_

---

## Prompt 3: Silver/Gold Git checkpoint (2026-08-31)

**PROMPT SENT:**

> The Silver and Gold implementation is complete for the current stage and the tests are passing. Prepare for Git checkpoint: inspect diff, stage Silver/Gold work only, commit with message about Silver quality validation and Gold analytics, push to `cursor/phase2-silver-gold`.

**AI RESPONSE SUMMARY:**

Verified 17 files, 20 tests passing. Committed `855a566` then later full implementation as `15678a7` on `cursor/phase2-silver-gold`. Pushed to remote.

**YOUR EVALUATION:** _Pending_

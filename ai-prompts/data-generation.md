# AI Prompts — Data Generation

## Prompt 1: Project scaffolding (2026-08-29)

**PROMPT SENT:**
Establish project documentation and folder structure for Databricks Medallion pipeline assessment.

**AI RESPONSE SUMMARY:**
Created initial docs, cursor-workflow files, and folder structure.

**YOUR EVALUATION:**
✓ Accepted — foundation for all subsequent work.

---

## Prompt 2: Data generation review (2026-08-30)

**PROMPT SENT:**
Before Bronze implementation, review `src/data_generation/generate_sample_data.py` against assessment requirements. Verify row counts (10K/100K/500), all intentional DQ issue counts, duplicate record handling while preserving row counts, schema/enums/dates/values, reproducibility, maintainability, and `DATA_GENERATION_NOTES.md`. Do not implement Bronze/Silver/Gold/Dashboard. Do not modify generator unless actual issues found. Do not commit.

**AI RESPONSE SUMMARY:**
Ran generator and pytest in venv. Row counts, schemas, enums, dates, monetary values, and reproducibility (seed 42) pass. DQ counts mostly pass except orphan `customer_id`: 153 actual vs 50 required due to duplicate customer_id injection removing 10 IDs from customers table (~103 unintended order orphans). Tests fail on `test_intentional_dq_issues`. Updated `DATA_GENERATION_NOTES.md` with reproducibility detail and known issue. Generator not modified pending approval.

**YOUR EVALUATION:**
✓ **Accepted** — fix applied; all tests pass; no unintended orphan FK violations.

---

## Prompt 3: Fix duplicate customer_id strategy (2026-08-30)

**PROMPT SENT:**
Apply recommended fix: 9,990 unique customers + 10 duplicate rows; orders sample customer_id 1..9990; disjoint random sampling for order DQ issues; expanded tests; update DATA_GENERATION_NOTES. Do not commit.

**AI RESPONSE SUMMARY:**
Refactored generator, validate_data, and tests. All 19 tests pass. Generated fresh CSVs to data/.

**YOUR EVALUATION:**
✓ Accepted.

---

## Prompt 4: Sample data generator implementation

**PROMPT SENT:**
_To be captured when generator fix is implemented._

**AI RESPONSE SUMMARY:**
_Pending._

**YOUR EVALUATION:** Superseded by Prompt 3 — generator fix completed and all tests pass.

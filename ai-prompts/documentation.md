# AI Prompts — Documentation

## Prompt 1: Project scaffolding (2026-08-29)

**PROMPT SENT:**
Establish project documentation and folder structure for a Databricks Medallion Architecture e-commerce pipeline assessment.

**AI RESPONSE SUMMARY:**
Created directory structure, initial documentation, and Cursor workflow files.

**YOUR EVALUATION:**
✓ **Accepted** — provided foundation for implementation phases.

---

## Prompt 2: Repository structure alignment

**PROMPT SENT:**
Refine repository structure to match Required Repository Structure in assessment document.

**AI RESPONSE SUMMARY:**
Moved docs to root, created `src/` layer placeholders, migrated to `ai-prompts/`.

**YOUR EVALUATION:**
✓ **Accepted** — aligns with submission template.

---

## Prompt 3: Prompt history tracking (2026-08-31)

**PROMPT SENT:**

> I hope you are adding all my prompts to you in the apt folder.

**AI RESPONSE SUMMARY:**

Confirmed the convention: user prompts are recorded under `ai-prompts/` by phase (`bronze.md`, `data-generation.md`, `silver-layer.md`, etc.). Noted that only the initial Bronze implementation prompt had been logged; backfilled missing prompts from this session into `ai-prompts/bronze.md` (execution checklist, commit/push) and this entry in `ai-prompts/documentation.md`.

**YOUR EVALUATION:** _Pending_

---

## Prompt 4: Ongoing prompt logging (2026-08-31)

**PROMPT SENT:**

> Yes please add all the prompts whatever I send you in the respective folders.

**AI RESPONSE SUMMARY:**

Confirmed standing practice: every substantive user prompt will be recorded under `ai-prompts/` in the file matching the work phase (`bronze.md`, `silver-layer.md`, `gold-layer.md`, `dashboard.md`, `data-generation.md`, `documentation.md`, `debugging.md`). Backfilled missing Bronze-session prompts and committed the updates.

**YOUR EVALUATION:** _Pending_

---

## Prompt 5: Databricks Asset Bundle and end-to-end validation (2026-08-31)

**PROMPT SENT:**

> Silver and Gold implementation is complete and committed/pushed. Proceed with Databricks Asset Bundle and end-to-end validation (Bronze → Silver → Gold). Inspect repository first; propose Bundle design before implementing. Constraints: do not rewrite Bronze/Silver/Gold logic; no secrets; no commit/push; validate locally and on Databricks if CLI auth available.

**AI RESPONSE SUMMARY:**

Phase 1 assessment: no existing `databricks.yml`; pipeline entry point `src/pipeline/run_all.py`; config via CLI args and env vars; Hive databases `bronze`/`silver`/`gold`; CE schema in `database/schema_community_edition.sql`; no valid Databricks CLI profile locally (`dev` profile invalid).

Implemented minimum Bundle: `databricks.yml`, `resources/medallion_pipeline.job.yml`, `scripts/run_pipeline.py`, `scripts/setup_schema.py`, `pyproject.toml`, `BUNDLE.md`, `tests/bundle/`. Job tasks: setup_schema → run_pipeline with wheel artifact. Local tests and wheel build validated; `databricks bundle validate/deploy/run` blocked on missing workspace authentication.

**YOUR EVALUATION:** _Pending_

---

## Prompt 6: Bundle deploy and E2E validation (2026-08-31)

**PROMPT SENT:**

> Get existing Databricks Bundle to deployable/executable state; perform real E2E validation (Bronze → Silver → Gold); prepare final Git checkpoint. Do not redesign Bronze/Silver/Gold. Fix only concrete blockers. Do not commit/push yet.

**AI RESPONSE SUMMARY:**

Readiness check passed on bundle files. Auth blocked: only profile `dev` exists (enterprise workspace, IP ACL blocked — not CE). Applied minimal CE single-node cluster fix in job YAML. Local tests: 20 passed. Databricks deploy/run/E2E not executed — user must authenticate to CE workspace first.

**YOUR EVALUATION:** _Pending_

---

## Prompt 7: Finalize repository and Git checkpoint (2026-08-31)

**PROMPT SENT:**

> Databricks CE CLI authentication is blocked; actual deployment and E2E cannot be validated. Treat as external/environment limitation. Finalize repository in production-quality state and create final Git checkpoint. Run tests, update docs, commit with message `Implement Databricks Bundle and finalize medallion pipeline`, push to branch. Do not fabricate Databricks E2E results.

**AI RESPONSE SUMMARY:**

Final review: all changes limited to Bundle, packaging, tests, docs, `.gitignore`, and prompt history. No Bronze/Silver/Gold business-logic changes. Tests: 20 passed. Wheel build succeeded. Bundle static validation passed locally; Databricks deploy/E2E documented as pending due to CLI auth blocker. Committed and pushed to `cursor/phase2-silver-gold`.

**YOUR EVALUATION:** _Pending_

---

## Prompt 8: Final assessment-completeness pass (2026-08-31)

**PROMPT SENT:**

> We are doing the final assessment-completeness pass. Do NOT revisit Bronze, Silver, Gold, pipeline, or Bundle implementation. Create a separate branch. Complete dashboard SQL (Top 10 products bar, customer revenue histogram, customer segmentation pie) from Gold tables. Complete `candidate-info.md` and update README status. Run pytest. Commit `Complete dashboard artifacts and assessment documentation`. Document Databricks E2E/dashboard UI as pending. Do not falsely mark dashboard as deployed.

**AI RESPONSE SUMMARY:**

Branch `cursor/assessment-completion`. Dashboard SQL and guide completed. `candidate-info.md` and README status table updated. Full pytest: 40 passed, 1 skipped. Databricks deployment/dashboard UI documented as pending due to workspace auth.

**YOUR EVALUATION:** _Pending_

---

## Prompt 9: Commit only, no push (2026-08-31)

**PROMPT SENT:**

> Don't push the changes, just commit them. I'll review the candidate information myself. Also add all the prompts that I have shared with you in the respective folder.

**AI RESPONSE SUMMARY:**

Backfilled missing prompt history (Silver/Gold branch, Git checkpoint, assessment pass). Committed assessment-completion changes locally without push. User to review `candidate-info.md` before any push.

**YOUR EVALUATION:** _Pending_

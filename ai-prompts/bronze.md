# AI Prompts — Bronze Layer

## Prompt 1

**PROMPT SENT:**

> The data-generation phase is complete, committed, pushed and merged. I have reviewed and approved that work, so don't revalidate or redesign the data-generation phase unless a later implementation exposes a specific issue.
>
> I have also created the free Databricks Community Edition workspace, which will be the execution and validation environment for this assessment.
>
> Let's now move forward to the Bronze layer.
>
> Before writing the Bronze implementation, inspect the existing `database/` setup files, `cursor-workflow/spec.md`, `design-notes.md`, `data-model.md` and the original assessment document.
>
> I want the Bronze implementation to be practical for Databricks Community Edition and not depend on enterprise-only features.
>
> The Bronze layer should take the generated CSV files from `data/` and ingest them as Bronze tables while keeping the source data as close to the original CSV structure as possible.
>
> For each source dataset (customers, orders, products) create a corresponding Bronze table.
>
> The Bronze layer should include audit metadata: `_ingested_at`, `_source_file`, `_batch_id`.
>
> Keep source columns intact; no Silver-style DQ validation or business transformations in Bronze.
>
> Structure under `src/bronze/` with `ingest_all.py` entry point.
> Configurable input/output paths (Databricks + local dev).
> Prefer straightforward PySpark and Delta; no Unity Catalog, Asset Bundles, or external orchestration.
>
> Review `database/schema.sql` for CE compatibility (minimum changes).
> Create Bronze README, tests, and record this interaction here.
> Do not implement Silver, Gold, or Dashboard. Do not commit or push.

**AI RESPONSE SUMMARY:**

Implemented a shared Bronze ingestion module for Databricks Community Edition:

- **`database/schema_community_edition.sql`** — Hive metastore `CREATE DATABASE` variant (bronze/silver/gold) replacing Unity Catalog for CE
- **`database/schema.sql`** — added banner pointing CE users to the new script
- **`database/setup-notes.md`** — CE-first setup and CSV upload instructions
- **`src/bronze/config.py`** — configurable paths, CLI args, batch id generation
- **`src/bronze/ingest_utils.py`** — CSV read, audit columns, Delta overwrite write
- **`src/bronze/01_*.py`, `02_*.py`, `03_*.py`** — per-dataset entry points
- **`src/bronze/ingest_all.py`** — single batch id across all three ingests
- **`src/bronze/README.md`** — runbook for CE and local dev
- **`tests/bronze/`** — config unit tests + optional Spark/Delta integration tests

**Approach:**

1. Read existing spec, data model, and database setup before coding
2. Keep Bronze logic minimal: Spark CSV read with `inferSchema`, add three audit columns, `overwrite` Delta tables
3. Use Hive database `bronze` on CE (not `ecommerce_dev.bronze` Unity Catalog path)
4. Auto-detect environment: `/databricks` → `dbfs:/FileStore/ecommerce/raw`, else repo `data/`
5. One shared `batch_id` per `ingest_all` run for traceability

**Important design decisions:**

| Decision | Rationale |
|----------|-----------|
| Separate `schema_community_edition.sql` | CE has no Unity Catalog; avoids breaking enterprise `schema.sql` |
| `overwrite` mode per run | Matches spec idempotency assumption; simple for assessment |
| `inferSchema=true` | Preserves CSV structure without manual schema enforcement at Bronze |
| `_source_file` = filename only | Stable, readable audit field (not full DBFS path) |
| Shared `ingest_utils.py` | DRY; single-dataset scripts remain thin entry points |
| No Autoloader / streaming | Batch CSV ingest is sufficient for assessment scope |

**Assumptions:**

- CSVs uploaded to `dbfs:/FileStore/ecommerce/raw/` on Databricks CE
- Hive database name `bronze` (configurable via `--database` / `BRONZE_DATABASE`)
- Databricks runtime includes PySpark + Delta (no extra pip install on cluster)
- Local Spark tests optional (`pytest.importorskip` if pyspark/delta not installed)
- Silver/Gold table DDL included in CE schema script for pipeline consistency but not populated yet

**YOUR EVALUATION:** _Pending_

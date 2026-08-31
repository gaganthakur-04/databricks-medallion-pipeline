# Debugging Notes

Issues encountered during implementation and Databricks deployment.

## Template

### [DATE] — Short title

**Symptom:** What was observed  
**Root cause:** Why it happened  
**Resolution:** What fixed it  
**Prevention:** How to avoid recurrence  
**AI assistance:** How AI tools helped (if applicable)

---

## Issues

### 2026-08-31 — Terraform GPG key expired (Databricks CLI)

**Symptom:** `databricks bundle validate` failed with `openpgp: keyexpired`  
**Root cause:** Homebrew CLI v0.238.0 has expired HashiCorp GPG key for Terraform checksum verification  
**Resolution:** Use patched `~/bin/databricks` v0.238.1  
**Prevention:** Keep CLI updated; use `~/bin/databricks` for bundle commands on this machine  

---

### 2026-08-31 — Public DBFS `/FileStore` disabled on Free Edition

**Symptom:** `databricks fs ls dbfs:/FileStore/ecommerce/raw/` → Access denied  
**Root cause:** Databricks Free Edition disables public DBFS root  
**Resolution:** Created UC volume `workspace.default.ecommerce_raw`, uploaded CSVs, deployed with `--var="csv_input_dir=/Volumes/workspace/default/ecommerce_raw"`  
**Prevention:** Document UC volume path in `BUNDLE.md` and `candidate-info.md`  

---

### 2026-08-31 — Serverless job `Client-1` not supported

**Symptom:** Job failed: `Workspace doesn't support Client-1 channel for REPL`  
**Root cause:** Free Edition serverless requires `client: "2"` in job environment spec  
**Resolution:** Updated `resources/medallion_pipeline.job.yml` environment spec  
**Prevention:** Use serverless config from validated `BUNDLE.md`  

---

### 2026-08-31 — `__file__` undefined in serverless spark_python_task

**Symptom:** `setup_schema` failed with `NameError: name '__file__' is not defined`  
**Root cause:** Serverless executes script via `exec()` without `__file__`  
**Resolution:** Added `--bundle-root ${workspace.file_path}` parameter to `setup_schema.py`  
**Prevention:** Avoid `__file__` in Databricks job entry scripts; use bundle path variable  

---

### 2026-08-31 — SQL parse error on semicolon in comment

**Symptom:** `PARSE_SYNTAX_ERROR` near `populated` when applying schema DDL  
**Root cause:** `schema_community_edition.sql` line comment contains `;` which broke naive SQL splitter  
**Resolution:** Added `_strip_sql_comments()` before splitting statements in `setup_schema.py`  
**Prevention:** Strip line comments before `;` split; added unit test  

---

### 2026-08-31 — Wheel path interpolation error

**Symptom:** `file doesn't exist resources//Users/.../databricks-medallion-pipeline`  
**Root cause:** `${artifacts.medallion_whl.path}` resolves to project root, not wheel file  
**Resolution:** Changed job libraries to `../dist/*.whl`  
**Prevention:** Follow Databricks bundle wheel examples; use relative dist glob  

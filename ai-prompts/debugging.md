# AI Prompts — Debugging

_Prompt history for issue investigation and fixes._

## Prompt 1: Databricks CLI and bundle deploy errors (2026-08-31)

**PROMPT SENT:**

> Terminal showing errors during `databricks bundle validate/deploy` on Community Edition / Free Edition workspace.

**AI RESPONSE SUMMARY:**

Diagnosed and resolved a chain of deployment blockers:

| Error | Root cause | Fix |
|-------|------------|-----|
| `openpgp: keyexpired` (Terraform) | Databricks CLI v0.238.0 bug | Use patched `~/bin/databricks` v0.238.1 |
| `pip: command not found` | Wheel build without venv | `source .venv/bin/activate`; `python3 -m pip` in `databricks.yml` |
| `file doesn't exist resources//Users/...` | Wrong `${artifacts.medallion_whl.path}` reference | Use `../dist/*.whl` in job libraries |
| `Only serverless compute is supported` | Free Edition rejects job clusters | Serverless `environment_key` + dependencies |
| `Client-1` not supported | Wrong serverless client channel | `client: "2"` |
| `__file__ is not defined` | Serverless `spark_python_task` exec context | `--bundle-root ${workspace.file_path}` in setup_schema |
| SQL parse error near `populated` | Semicolon inside SQL comment split statements | `_strip_sql_comments()` before splitting |
| Public DBFS `/FileStore` disabled | Free Edition restriction | UC volume + `csv_input_dir` override |

Final result: `bundle run medallion_pipeline` SUCCESS on profile `ce`.

**YOUR EVALUATION:** Systematic debugging — each deploy blocker diagnosed and fixed without scope creep.

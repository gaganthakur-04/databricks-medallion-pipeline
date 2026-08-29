# AI Workflow Foundation (Part A)

> Document how AI tools are used across the data engineering lifecycle for this assessment.

## Primary AI Tool

**Cursor** — primary IDE and AI assistant for requirement analysis, design, code generation, testing, and documentation.

## Project Context Setup

Persistent context is maintained in:

| File | Purpose |
|------|---------|
| `cursor-workflow/project-context.md` | Layer responsibilities, schemas, DQ rules, conventions |
| `cursor-workflow/spec.md` | Technical specification and acceptance criteria |
| `cursor-workflow/task-breakdown.md` | Phased implementation sequence |
| `cursor-workflow/cursor-rules-or-instructions.md` | Rules governing AI assistance |

Before each implementation session, context files are referenced so the AI assistant works from the same design baseline.

## AI Usage by Lifecycle Phase

| Phase | How AI is used | Validation approach |
|-------|----------------|---------------------|
| Requirements analysis | Parse assessment doc; draft `requirements-analysis.md`; flag ambiguities | Cross-check against official `DE_C1_Coding_Evaluation.docx` |
| Design | Draft data model, DQ strategy, Gold schemas | Review against acceptance criteria before coding |
| Data generation | Generate `generate_sample_data.py`; inject DQ issues | Automated tests verify row/issue counts |
| Bronze/Silver/Gold | PySpark modules per layer spec | Unit + integration tests |
| Dashboard | SQL queries for 3 visualizations | Manual verification in Databricks SQL |
| Testing | pytest suites per layer | CI/local test runs |
| Debugging | Root-cause analysis with AI; log in `debugging-notes.md` | Re-run failing tests after fix |
| Documentation | Draft and refine markdown artifacts | Human review for accuracy and ownership |

## What I Avoid Sharing with AI

- Real customer PII or production credentials
- Client/work (Tabcorp) repository contents or secrets
- Databricks tokens, API keys, or `.env` values
- Proprietary data beyond the synthetic assessment datasets

## Validation of AI-Generated Code

1. **Read before accepting** — understand logic, especially DQ rules and aggregations
2. **Run tests** — every module has pytest coverage for core behaviour
3. **Verify counts** — intentional DQ issue counts must match assessment exactly
4. **Reject mismatches** — e.g. wrong Gold segmentation dimension, silent row deletion in Silver
5. **Iterate** — refine prompts when output doesn't match spec; document in `ai-prompt-history/`

## Reuse in Production

This workflow transfers to production pipelines:

1. Maintain a `project-context.md` / spec per pipeline
2. Use phased task breakdowns with clear exit criteria
3. Archive significant prompts for team knowledge sharing
4. Require tests before merging AI-generated code
5. Separate work and personal Git/AI contexts on shared machines

## Lessons Learned

_To be updated as the project progresses._

### What worked

- Establishing documentation and folder structure before implementation code
- Cross-referencing official assessment document against initial requirements

### What didn't work

_To be filled during implementation._

### What I would do differently

_To be filled during reflection._

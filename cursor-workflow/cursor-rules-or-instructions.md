# Cursor Rules & Instructions

Practical rules for AI assistants (primarily Cursor) working on this Databricks Medallion assessment project.

---

## 1. Project Identity

This is an **AI-first data engineering assessment**. Every significant AI interaction should be archivable. The pipeline must be **production-quality** while the repo must also demonstrate the **AI-assisted engineering lifecycle**.

## 2. Before Writing Code

1. Read `cursor-workflow/project-context.md` and `cursor-workflow/spec.md`
2. Check `cursor-workflow/task-breakdown.md` for the current phase
3. Consult `docs/data-model.md` and `docs/data-quality-strategy.md` for schemas and rules
4. Do not invent requirements — mark assumptions explicitly
5. Do not skip ahead to later phases unless the user requests it

## 3. Implementation Rules

### Medallion Layers

| Layer | Do | Don't |
|-------|----|-------|
| Bronze | Ingest raw; add audit columns | Validate, deduplicate, or drop rows |
| Silver | Flag all DQ issues; retain every row | Silently delete or filter invalid records |
| Gold | Business aggregates from valid Silver | Re-implement DQ logic |
| Dashboard | Query Gold tables | Embed business logic duplicating Gold |

### Data Quality

- Use rule IDs from `docs/data-quality-strategy.md` (e.g., `ORD_REF_001`)
- Flag NULL FKs under **Completeness**, not referential integrity
- A record may have multiple flags
- Intentional issue counts are acceptance criteria — verify with tests

### Source Data

- Exact row counts: customers 10,000 | orders 100,000 | products 500
- Exact DQ issue counts as specified in requirements
- Enum values must match exactly (case-sensitive unless decided otherwise)

## 4. Code Style

- Follow existing patterns in the repo — read surrounding code before adding
- Prefer minimal, reviewable diffs
- Match naming conventions in `project-context.md`
- No hardcoded credentials, tokens, or workspace URLs with secrets
- Do not add dependencies without justification

## 5. File Organization

| What | Where |
|------|-------|
| Generator scripts | `data-generation/` |
| Bronze code | `bronze/` |
| Silver code + rules | `silver/` |
| Gold transforms | `gold/` |
| Dashboard SQL | `dashboard/` |
| Tests | `tests/` mirroring layer structure |
| Setup DDL | `setup/` |
| Generated CSVs | `data/sample/` |
| Assessment docs | `docs/` |
| Cursor context | `cursor-workflow/` |

## 6. Documentation Obligations

Update docs when making design decisions:

| Event | Update |
|-------|--------|
| Architecture choice | `docs/design-notes.md` |
| Schema change | `docs/data-model.md` |
| New DQ rule | `docs/data-quality-strategy.md` |
| Bug found and fixed | `docs/debugging-notes.md` |
| Phase completed | `README.md` status table |

## 7. AI Prompt History

After significant AI-assisted work in a phase:

1. Save the prompt (and optionally the key response) to `ai-prompt-history/<activity>/`
2. Use filename format: `YYYY-MM-DD-short-description.md`
3. Activities: `requirements`, `data-generation`, `bronze`, `silver`, `gold`, `dashboard`, `testing`, `debugging`, `documentation`

## 8. Testing Requirements

- Add tests when behavior or logic changes
- Silver: test each rule in isolation and verify flag counts
- Gold: test aggregations with known fixtures
- Integration: end-to-end CSV → Gold with DQ count assertions
- State clearly if tests were not run and why

## 9. Git & Commits

- Only commit when the user asks
- Never force-push to main
- Never commit secrets or large generated data without `.gitignore`
- Use clear commit messages focused on "why"

## 10. Interaction Style

- Inspect the repo before making changes
- Propose structure/decisions before large changes when asked
- Explain what changed, why, and which files were modified
- Flag ambiguities rather than guessing silently
- Run commands and tests yourself — do not just suggest them

## 11. Common Pitfalls to Avoid

1. **Dropping bad rows in Silver** — the most critical assessment requirement
2. **Wrong DQ issue counts** — generator must seed exactly the specified counts
3. **Inventing Gold schemas** without documenting assumptions
4. **Skipping prompt history** — undermines the AI-first assessment goal
5. **Mixing layers** — keep Bronze/Silver/Gold responsibilities separate
6. **Dashboard querying Silver/Bronze** — use Gold tables

## 12. When Stuck

1. Re-read `docs/requirements-analysis.md` for stated vs assumed requirements
2. Check open questions in `cursor-workflow/spec.md` §9
3. Log the issue in `docs/debugging-notes.md`
4. Ask the user to resolve ambiguities that affect correctness

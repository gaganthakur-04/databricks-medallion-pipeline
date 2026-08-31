# AI Prompts — Gold Layer

See **`silver-layer.md` Prompt 1** — Silver and Gold were implemented in the same session (2026-08-31).

## Gold-specific decisions

- Revenue metrics use valid Silver rows with `order_status = 'Completed'`
- `lifetime_value_actual` = sum of completed order amounts per customer
- Behavioral segments: Inactive → High-Value → Repeat → One-Time (priority order)
- Reference SQL in `src/gold/01_*.sql`, `02_*.sql`, `04_*.sql` for dashboard phase

**YOUR EVALUATION:** Gold logic matches spec and was validated on Databricks.

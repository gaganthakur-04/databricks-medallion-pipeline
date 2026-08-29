# Candidate Information

> Fill in before submission.

| Field | Value |
|-------|-------|
| **Name** | _[Your name]_ |
| **Email** | _[Your email]_ |
| **Assessment date** | _[Date]_ |
| **Databricks workspace** | _[Workspace URL or identifier]_ |
| **Repository URL** | _[Git remote URL]_ |

## Environment Details

| Item | Value |
|------|-------|
| Databricks runtime | _[e.g., 15.4 LTS]_ |
| Cluster / SQL warehouse | _[Details]_ |
| Catalog / schema naming | _[e.g., `ecommerce_dev`]_ |

## Submission Checklist

- [ ] All three source CSVs generated with required row counts and DQ issues
- [ ] Bronze layer ingests all source files
- [ ] Silver layer flags all intentional DQ issues without silently deleting records
- [ ] Gold layer produces Sales by Product, Revenue by Customer, Customer Segmentation
- [ ] Databricks SQL Dashboard deployed with required visualizations
- [ ] Tests pass
- [ ] Documentation complete (design, DQ strategy, reflection, AI usage summary)
- [ ] AI prompt history captured under `ai-prompt-history/`

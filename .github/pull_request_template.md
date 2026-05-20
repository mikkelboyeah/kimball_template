## Summary
- Briefly describe the change and why it’s needed.
- Note the data sources (EODHD via dlt REST API) and where the analytics land (DuckDB + dbt models).

## Validation
- [ ] `uv run dbt run --project-dir transform --profiles-dir profiles`
# Coding Standards

To maintain consistency in this analytics project, follow these rules:

## Python (dlt & Generators)
- Use `uv` for all package management.
- Prefer type hints in all `src/` functions.
- Follow PEP8.

## SQL & dbt
- **Lowercase**: Use lowercase for all SQL keywords and identifiers.
- **CTEs**: Use Common Table Expressions (CTEs) at the start of models for readability.
- **Naming**: 
  - Staging: `stg_<source>__<object>`
  - Intermediate: `int_<concept>__<action>`
  - Marts: `fct_<fact>` or `dim_<dimension>`

## Documentation
- Every new dbt model must have a description in a `.yml` file.
- New scripts in `src/` must be documented in the root `README.md` or `.agent/README.md`.

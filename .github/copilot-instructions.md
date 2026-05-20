# GitHub Copilot Instructions

This repository is a **domain-adaptable analytics stack** built on DuckDB, dlt, dbt, and Power BI.
The current reference implementation covers the **insurance domain**; the architecture is designed
to be replicated for any industry domain.

## Start Here (for new domain implementation)

If you have a `docs/*_target_markdown.md` file for a new domain, follow these steps in order:

1. **Find the domain markdown** — look in `docs/` for a `*_target_markdown.md` file.
2. **Read the domain markdown guide** → `.agent/skills/architecture/03-reading-the-target-markdown.md`
   Extract all star schemas, tables, grains, measures, and column types.
3. **Understand the starting state** → `.agent/skills/architecture/01-as-is-template-architecture.md`
4. **Build layer by layer** → `.agent/skills/architecture/02-to-be-target-architecture.md`
5. **Verify end-to-end** — run `task delete-all-and-full-load`.

## Core Stack

| Layer | Tool | Location |
|---|---|---|
| Mock data generation | Python + pandas + pyarrow | `src/data_generators/` |
| Ingestion | dlt (Data Load Tool) | `src/pipeline/` |
| Storage | DuckDB | `data/db.duckdb` |
| Transformation | dbt Core | `transform/` |
| Export | Python + duckdb | `src/export_reporting/` |
| BI Layer | Power BI PBIP (TMDL) | `powerbi/` (generated) |
| Orchestration | Taskfile | `Taskfile.yml` |

## Key Conventions

- All Python managed via `uv`. Use `uv run <command>` — never bare `python`.
- Run tasks via `task <taskname>` — see `Taskfile.yml` for all available tasks.
- Data flows: `data/raw/` → DuckDB `raw` schema → dbt staging → dbt mart → dbt reporting → `data/exports/` → `powerbi/`
- Each **star schema** lives in its own subfolder under `src/data_generators/`, `data/raw/`, `transform/models/staging/`, `transform/models/mart/`, `transform/models/reporting/`.
- SQL identifiers: lowercase, `snake_case`.
- dbt naming: `stg_<prefix>__<table>`, `dim_<name>`, `fct_<name>`.
- `date_id` columns in `dim_date` are **strings** `'YYYY-MM-DD'` — fact date FK columns must match.

## Relevant Skills & Instructions

| File | Purpose |
|---|---|
| `.agent/skills/architecture/SKILL.md` | Master skill for domain adaptation |
| `.agent/skills/architecture/01-as-is-template-architecture.md` | What the clean starting state provides |
| `.agent/skills/architecture/02-to-be-target-architecture.md` | What must be built for any domain |
| `.agent/skills/architecture/03-reading-the-target-markdown.md` | How to interpret the Kimball domain markdown |
| `.agent/instructions/coding_standards.md` | Python and SQL coding standards |
| `.agent/instructions/powerbi_generation.md` | Power BI PBIP/TMDL generation rules |
| `.agent/skills/dbt-transformation-patterns/SKILL.md` | dbt patterns reference |

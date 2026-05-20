# Agent Entry Point

Welcome to this **domain-adaptable analytics stack** — a modern, multi-layer data engineering
project built on DuckDB, dlt, dbt, and Power BI. The current reference implementation covers the
**insurance domain**; the architecture is designed to be replicated for any industry domain.

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

## How to Work Here

1. **Always use Task**: Run `task --list` to see all tasks. Key tasks: `task bootstrap`, `task ingest`, `task transform`, `task full-load`.
2. **Schema Conventions**: Development schemas are prefixed with `z_<user>_`.
3. **Data Generation**: Mock data can be refreshed using `task generate-data`.
4. **Never use bare `python`**: Always use `uv run python` or `uv run <tool>`.

## Building a New Domain Implementation

If you have a `docs/*_target_markdown.md` file for a new domain, start here:

```
.agent/skills/architecture/SKILL.md
```

This skill walks you through reading the domain markdown, understanding the template state,
and implementing every layer of the stack.

## .agent Folder Map

| Path | Purpose |
|---|---|
| `skills/architecture/` | **Master skill** for domain adaptation (start here) |
| `skills/dbt-transformation-patterns/` | dbt model patterns reference |
| `skills/powerbi/` | Power BI semantic model and report skills |
| `skills/fabric/` | Microsoft Fabric skills |
| `instructions/coding_standards.md` | Python and SQL coding standards |
| `instructions/powerbi_generation.md` | PBIP/TMDL generation rules |
| `instructions/kimball_insurance_tables.md` | Insurance domain table reference |

## Multi-Star Architecture

Each **star schema** lives in its own named subfolder across all layers:

| Layer | Path pattern |
|---|---|
| Data generator | `src/data_generators/<star_name>/` |
| Raw Parquet | `data/raw/<star_name>/` |
| dbt staging | `transform/models/staging/<star_name>/` |
| dbt mart | `transform/models/mart/<star_name>/` |
| dbt reporting | `transform/models/reporting/<star_name>/` |
| Parquet exports | `data/exports/<star_name>/` |
| Power BI project | `powerbi/<star_name>/` |

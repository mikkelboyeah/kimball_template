# 01 — AS-IS Template Architecture

This document describes the **clean template state** of the repository — what is already built and
working before any domain-specific code is added. When you receive this repo for a new domain, all
the infrastructure described here is present and ready to use.

---

## Top-Level Directory Structure

```
.agent/          Agent skills and instructions
.github/         GitHub Copilot instructions + CI workflow
data/
  raw/           Landing zone for generated Parquet files (empty at start)
  exports/       Output Parquet files from dbt reporting models (empty at start)
docs/            Domain markdown files (e.g., *_target_markdown.md)
powerbi/         Generated Power BI PBIP projects (empty at start)
profiles/        dbt connection profiles (duckdb, points to data/db.duckdb)
src/
  data_generators/    << YOU FILL THIS IN — empty at start
  export_reporting/   Already built — exports DuckDB reporting views to Parquet
  generate_powerbi/   Already built — generates PBIP from Parquet exports
  pipeline/           Already built — dlt ingestion from Parquet → DuckDB
transform/
  dbt_project.yml     Pre-configured — you add new reporting schema entries
  models/
    src_raw.yml       Source definitions — you add new table entries
    staging/          << YOU FILL THIS IN — empty at start
    mart/             << YOU FILL THIS IN — empty at start
    reporting/        << YOU FILL THIS IN — empty at start
Taskfile.yml          Orchestration — you add new generate-data commands
pyproject.toml        Python dependencies (pandas, pyarrow, dlt, dbt-duckdb, duckdb)
```

---

## Pre-Built Components (Do Not Modify)

### 1. dlt Ingestion Pipeline — `src/pipeline/pipeline.py`

Recursively scans `data/raw/` for `.parquet` files and loads each one into DuckDB's `raw` schema.
The table name is the **filename stem** (e.g., `claim_accumulating_snapshot.parquet` → table
`raw.claim_accumulating_snapshot`).

Run via: `task ingest` or `task ingest -- <subfolder>` for a single star schema.

**Key behaviour:**
- Uses `write_disposition="replace"` — full reload every run.
- Supports an optional subfolder argument to target a single star schema.
- Requires `data/db.duckdb` to exist (`task bootstrap` creates it).

### 2. Export Reporting — `src/export_reporting/export_reporting.py`

Scans `transform/models/reporting/` for subfolders. For each subfolder `<star_name>`, it:
1. Connects to the DuckDB schema `reporting_<star_name>`.
2. Exports every table/view in that schema to `data/exports/<star_name>/<table_name>.parquet`.

This script is fully automatic — adding a new reporting subfolder and a matching `dbt_project.yml`
entry is all that's needed to make it work for a new star schema.

Run via: `task export-reporting`

### 3. Power BI Generation — `src/generate_powerbi/generate_powerbi.py`

Reads `data/exports/` and generates a complete Power BI Project (PBIP) folder structure in
`powerbi/<star_name>/`. The generated project includes:
- A `.pbip` project file
- A `<star_name>.SemanticModel/` folder with TMDL files for all tables and relationships
- A `<star_name>.Report/` folder with an empty report definition

Tables are auto-discovered from the Parquet files. Relationships are inferred by matching column
names ending in `_id` between fact and dimension tables.

Run via: `task generate-powerbi` (or with `ROOT="C:/path"` for absolute path binding)

See `.agent/instructions/powerbi_generation.md` for TMDL syntax rules.

### 4. dbt Project Skeleton — `transform/`

The dbt project (`name: generic_project`) is pre-configured with four model layers:

| Layer | Schema | Materialisation | Path |
|---|---|---|---|
| staging | `staging` | view | `models/staging/` |
| intermediate | `intermediate` | ephemeral | `models/intermediate/` |
| mart | `mart` | table | `models/mart/` |
| reporting | `reporting_<star_name>` | view | `models/reporting/<star_name>/` |

The reporting layer is the only one that produces the separate per-star schemas consumed by
`export_reporting.py`. Each star schema subfolder under `models/reporting/` must also appear in
`dbt_project.yml` with its own `+schema: reporting_<star_name>` entry.

### 5. Taskfile Orchestration — `Taskfile.yml`

Pre-built tasks:

| Task | What it does |
|---|---|
| `task bootstrap` | Install Python deps, create empty `data/db.duckdb` |
| `task ingest` | Load all Parquet from `data/raw/` into DuckDB |
| `task transform` | Run dbt in dev mode (with prod deferral if available) |
| `task transform-prod` | Run dbt in prod mode, save manifest for deferral |
| `task export-reporting` | Export reporting models to `data/exports/` |
| `task generate-powerbi` | Generate PBIP projects in `powerbi/` |
| `task full-load` | Run all steps in sequence |
| `task delete-all-and-full-load` | Clean everything and run full-load |

**Missing at start:** The `generate-data` task body is empty (or absent). You must add one
`uv run python` line per generator script you create.

### 6. dbt Profiles — `profiles/profiles.yml`

Points to `data/db.duckdb`. Two targets: `dev` (default) and `prod`. No changes needed.

### 7. Source Definitions — `transform/models/src_raw.yml`

At start this file contains only the skeleton header (version: 2, sources section with an empty
tables list). For a new domain, you must add one `- name: <table>` entry under `sources.raw.tables`
for every Parquet file your generators will produce.

---

## What Is NOT Present at Start

The following are **domain-specific** and must be created by you:

1. `src/data_generators/<star_name>/generate_facts.py` — for every star schema
2. `src/data_generators/<star_name>/generate_dims.py` — for every star schema
3. `transform/models/staging/<star_name>/stg_<prefix>__<table>.sql` — one per raw table
4. `transform/models/mart/<star_name>/fct_<name>.sql` and `dim_<name>.sql`
5. `transform/models/reporting/<star_name>/` — reporting views + `schema.yml`
6. Entries in `transform/models/src_raw.yml`
7. Entries in `transform/dbt_project.yml` (reporting schema per star schema)
8. `generate-data` commands in `Taskfile.yml`

For detailed instructions on building each of these, see
[02-to-be-target-architecture.md](02-to-be-target-architecture.md).

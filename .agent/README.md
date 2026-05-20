# Agent Entry Point

Welcome to the **Insurance Mockups** project. This repository is a modern analytics stack designed for maximum agent effectiveness.

## Core Stack
- **Database**: DuckDB (`data/db.duckdb`)
- **Ingestion**: dlt (Data Load Tool) in `src/`
- **Transformation**: dbt (Core logic in `transform/`)
- **Environment**: `uv` for Python, `Taskfile.yml` for orchestration.

## How to work here
1. **Always use Task**: Before running raw commands, check `Taskfile.yml`. Preferred commands: `task bootstrap`, `task ingest`, `task transform`.
2. **Schema Conventions**: Development schemas are prefixed with `z_<user>_`.
3. **Data Generation**: Mock data can be refreshed using `task generate-data`.

## .agent Folder Map
- `/workflows`: Operational guides for complex tasks.
- `/instructions`: Technical constraints and coding standards.
- `/context`: Domain knowledge about insurance data models.

## Multi-Star Architecture
The project is structured to support multiple independent star schemas (e.g., `claim_accumulated_snapshot`).

### Directory Structure
- **Data Generators**: `src/data_generators/<star_name>/`
- **Raw Data**: `data/raw/<star_name>/`
- **Staging Models**: `transform/models/staging/<star_name>/`
- **Mart Models**: `transform/models/mart/<star_name>/`

### Adding a New Star Schema
1. Create a new subfolder under `src/data_generators/` for the new star.
2. Update generator scripts to output to a matching subfolder in `data/raw/`.
3. Create matching subfolders under `transform/models/staging/` and `transform/models/mart/`.
4. Add the new tables to `transform/models/src_raw.yml`.
5. Run `task ingest -- [new_subfolder]` for targeted ingestion, or `task ingest` for all.

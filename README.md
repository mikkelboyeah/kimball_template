# Template Analytics

A minimal, modern analytics template powered by **dlt**, **dbt**, **DuckDB**, and **uv**.

This repository is designed to be cloned and used as a starting point for any new analytics project. It provides:
- A generic ingestion pipeline template using `dlt`.
- A generic `dbt` project structure (seeds, staging, intermediate, mart) with pre-configured schemas.
- A streamlined developer experience using `uv` for dependency management and `go-task` for running commands locally.
- A GitHub Actions CI/CD workflow testing ingestion and transformation.

## Domain Knowledge

The `docs/` folder contains domain reference material used by agents and developers to understand the target data model for this project.

### Adapting to a New Domain

If you are using this template for a domain other than the included insurance example, you can generate your own domain summary using the **Kimball Chapter Summary Creator**:

1. **Open `docs/kimball_summary_setup_guide.md`** — it contains a step-by-step guide for generating a domain summary with your AI tool of choice.
2. **Upload the Kimball book** (or the relevant chapter) **and `docs/skill-kimball-summary-setup.md`** to your AI tool — NotebookLM, Claude, ChatGPT/Codex, or any assistant that supports document uploads.
3. **Run the prompt** from the guide to produce a structured markdown document covering fact tables, lineage, grain definitions, and business questions.
4. **Save the output** as a `.md` file in `docs/` and update your agent instructions to reference it.

> **Example output:** [`docs/insurance_target_markdown_example.md`](docs/insurance_target_markdown_example.md) shows what a completed domain summary looks like, generated for the insurance domain from Kimball's Chapter 14.

## Quickstart

### 1. Prerequisites
Ensure you have `uv` installed ([astral.sh/uv](https://astral.sh/uv)). This project uses `uv` for lightning-fast python dependency management.

### 2. Bootstrap the project
Run the bootstrap command to install dependencies and create an initial empty database:
```bash
task bootstrap
```
*Note: If you don't have `task` installed globally, you can run `uv tool install go-task-bin`.*

### 3. Full Load
To run the entire pipeline (ingestion via `dlt` + transformation via `dbt`) in one command:
```bash
task full-load
```

### 4. Verify & Explore
Run the architecture tests to ensure everything is set up correctly, then explore the data:
```bash
task test
task duckdb-ui
```

## Task Reference

The project uses `go-task` to manage workflows. Below is a description of the available tasks in `Taskfile.yml`:

| Task | Description |
| :--- | :--- |
| `task bootstrap` | Installs Python dependencies using `uv sync` and initializes an empty DuckDB database at `data/db.duckdb`. |
| `task ingest` | Runs the `dlt` pipeline to extract data from sources and load it into the `raw` schema. |
| `task transform` | (Dev) Runs `dbt build`. Uses the `z_<user>_` schema prefix. Defer to prod state if a manifest exists. |
| `task transform-prod` | (Prod) Runs `dbt build` with the `prod` target. Generates a manifest for dev deferral. |
| `task full-load` | Sequences `ingest` followed by `transform` (dev). |
| `task test` | Runs `pytest` to validate database architecture, naming conventions, and data integrity. |
| `task duckdb-ui` | Launches a web-based UI (via `db-ui`) to interactively query the DuckDB database. |
| `task drop-db` | Deletes the local `data/db.duckdb` file. |
| `task ingest:ui` | (Preview) Launches the dlt progressive web app to explore your loaded data. |

## Configuration (dlt)

The ingestion pipeline uses **dlt** (data load tool). By default, it is configured to be "zero-config" for local development, but it can be customized easily:

### 1. Database Path
The pipeline respects the `DB_PATH` environment variable. In `Taskfile.yml`, this is pre-configured to `data/db.duckdb`. If you need to point to a different file, you can override it:
```bash
DB_PATH=/path/to/my/db.duckdb task ingest
```

### 2. Pipeline State
State is stored locally in `.dlt/pipelines` within the project root. This ensures your project remains isolated from other `dlt` pipelines on your system.

### 3. Credentials & Settings
If you add more complex sources (e.g., API keys, database passwords), `dlt` looks for them in:
- **Environment Variables**: e.g., `SOURCES__REST_API__API_KEY`
- **Local Files**: `.dlt/secrets.toml` (for sensitive data) and `.dlt/config.toml` (for non-sensitive settings).
- **Global Files**: `~/.dlt/secrets.toml` (not recommended for this template to maintain isolation).

Refer to the [dlt docs](https://dlthub.com/docs/general-usage/credentials) for a full guide on configuration.
1. **Pipelines**: Modify `src/pipeline/pipeline.py` to point to your actual data sources.
2. **Models**: Replace models in `transform/models/` and seeds in `transform/seeds/`.
3. **Naming**: Update `pyproject.toml` with your project name.
4. **CI/CD**: The `.github/workflows` are pre-configured to run these tasks on every push.

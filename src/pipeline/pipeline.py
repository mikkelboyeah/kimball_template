"""dlt pipeline template for loading data into DuckDB."""

from __future__ import annotations
import argparse
import sys
import time
from pathlib import Path
import dlt
import os
import pandas as pd
from dlt.pipeline.exceptions import PipelineStepFailed

DEFAULT_DB_PATH = Path("data/db.duckdb")
_RETRY_ATTEMPTS = 3
_RETRY_DELAY_SECONDS = 2


def _run_with_retry(pipeline: dlt.Pipeline, *args, **kwargs) -> None:
    """Run pipeline.run() with retry logic to handle Windows file-locking races (WinError 5)."""
    for attempt in range(1, _RETRY_ATTEMPTS + 1):
        try:
            pipeline.run(*args, **kwargs)
            return
        except PipelineStepFailed as exc:
            if attempt < _RETRY_ATTEMPTS and isinstance(exc.__cause__, PermissionError):
                print(
                    f"  PermissionError on attempt {attempt}/{_RETRY_ATTEMPTS}, "
                    f"retrying in {_RETRY_DELAY_SECONDS}s..."
                )
                time.sleep(_RETRY_DELAY_SECONDS)
            else:
                raise


def load_data(subfolder: str | None = None) -> None:
    """Initialize the DuckDB database and load parquet files from data/raw into the raw schema.
    
    Args:
        subfolder: Optional subfolder within data/raw to limit ingestion to.
    """
    # Support DB_PATH env var, falling back to default
    db_path = Path(os.environ.get("DB_PATH", DEFAULT_DB_PATH))
    
    if not db_path.exists():
        print(f"Error: Database not found at {db_path}. Please run 'task bootstrap' first.", file=sys.stderr)
        sys.exit(1)
        
    pipeline = dlt.pipeline(
        pipeline_name="template_pipeline",
        pipelines_dir=".dlt/pipelines",  # Isolate state to project directory
        destination=dlt.destinations.duckdb(credentials={"database": str(db_path)}),
        dataset_name="raw",
    )
    
    # Path to raw data
    raw_data_base_dir = Path("data/raw")
    if not raw_data_base_dir.exists():
        print(f"Warning: Raw data directory {raw_data_base_dir} not found. No data to ingest.")
        return

    search_dir = raw_data_base_dir
    if subfolder:
        search_dir = raw_data_base_dir / subfolder
        if not search_dir.exists():
            print(f"Error: Subfolder {search_dir} not found.", file=sys.stderr)
            sys.exit(1)

    # Ingest parquet files
    if subfolder:
        parquet_files = list(search_dir.glob("*.parquet"))
    else:
        parquet_files = list(raw_data_base_dir.rglob("*.parquet"))

    if not parquet_files:
        print(f"No parquet files found in {search_dir}.")
        return

    print(f"Found {len(parquet_files)} parquet files. Starting ingestion...")

    # Build one dlt resource per file and run them all in a single pipeline.run() call.
    # This reduces the number of normalize/rename cycles from N to 1, which greatly
    # reduces the chance of hitting Windows file-locking races (WinError 5).
    def _make_resource(table_name: str, df: pd.DataFrame):
        """Factory that captures table_name and df in a closure to avoid dlt introspection issues."""
        @dlt.resource(name=table_name, write_disposition="replace")
        def _resource():
            yield df
        return _resource

    resources = []
    for file_path in parquet_files:
        table_name = file_path.stem
        print(f"Loading {file_path.name} from {file_path.parent} into table '{table_name}'...")
        df = pd.read_parquet(file_path)
        resources.append(_make_resource(table_name, df))

    @dlt.source
    def all_tables_source():
        return resources

    _run_with_retry(pipeline, all_tables_source())

    print("Ingestion complete.")

def main():
    parser = argparse.ArgumentParser(description="Ingest parquet files from data/raw into DuckDB.")
    parser.add_argument(
        "subfolder", 
        nargs="?", 
        help="Optional subfolder within data/raw to ingest (e.g., 'claim_accumulated_snapshot'). If omitted, all subfolders are searched recursively."
    )
    
    args = parser.parse_args()
    load_data(subfolder=args.subfolder)

if __name__ == "__main__":
    main()

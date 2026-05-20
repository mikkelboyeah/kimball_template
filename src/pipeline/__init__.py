"""Lightweight CLI entrypoint for triggering the ingestion pipeline."""

from __future__ import annotations

from .pipeline import load_data


def main() -> None:
    """Load sample data into DuckDB via dlt's REST API helper."""
    print("Starting ingestion pipeline...")
    load_data()
    print("Ingestion complete. Data loaded into DuckDB at data/db.duckdb")

import duckdb
import os
import pytest
from pathlib import Path

DB_PATH = Path("data/db.duckdb")

@pytest.fixture(scope="module")
def con():
    """Provides a DuckDB connection for testing."""
    if not DB_PATH.exists():
        pytest.fail(f"Database file not found at {DB_PATH}. Run 'task full-load' first.")
    
    connection = duckdb.connect(str(DB_PATH), read_only=True)
    yield connection
    connection.close()

def get_schemas(con) -> set[str]:
    """Helper to fetch all custom schemas in the database."""
    result = con.execute("SELECT schema_name FROM information_schema.schemata WHERE catalog_name = 'db' AND schema_name NOT IN ('information_schema', 'pg_catalog', 'main')").fetchall()
    return {row[0] for row in result}

def get_tables_in_schema(con, schema_name: str) -> set[str]:
    """Helper to fetch all tables/views in a specific schema."""
    query = f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}'"
    result = con.execute(query).fetchall()
    return {row[0] for row in result}

def test_raw_schema_exists(con):
    """Verifies that the dlt ingestion schema 'raw' exists and contains metadata."""
    schemas = get_schemas(con)
    assert 'raw' in schemas, "'raw' schema is missing. Did the ingest run successfully?"
    
    # Check for dlt metadata tables
    tables = get_tables_in_schema(con, 'raw')
    assert '_dlt_loads' in tables, "dlt metadata table '_dlt_loads' is missing in 'raw' schema."
    assert '_dlt_pipeline_state' in tables, "dlt metadata table '_dlt_pipeline_state' is missing in 'raw' schema."

def test_staging_table_naming_convention(con):
    """Verifies that all tables in staging schemas start with 'stg_'."""
    schemas = get_schemas(con)
    staging_schemas = [s for s in schemas if 'staging' in s]
    
    if not staging_schemas:
        pytest.skip("No staging schemas found to validate naming conventions.")
        
    for schema in staging_schemas:
        tables = get_tables_in_schema(con, schema)
        for table in tables:
            assert table.startswith('stg_'), f"Table '{table}' in schema '{schema}' violates naming convention (must start with 'stg_')."

def test_intermediate_models_are_ephemeral(con):
    """Verifies that intermediate models do not exist as tables or views (should be ephemeral)."""
    schemas = get_schemas(con)
    # Check if any schema contains 'intermediate' (it shouldn't if they are all ephemeral)
    intermediate_schemas = [s for s in schemas if 'intermediate' in s]
    
    assert not intermediate_schemas, f"Found unexpected intermediate schemas: {intermediate_schemas}. Intermediate models should be ephemeral."
    
    # Also check all schemas for any tables starting with 'int_'
    for schema in schemas:
        tables = get_tables_in_schema(con, schema)
        int_tables = [t for t in tables if t.startswith('int_')]
        assert not int_tables, f"Found unexpected intermediate tables/views in schema '{schema}': {int_tables}. They should be ephemeral."

def test_dbt_dev_schemas_exist(con):
    """Verifies that the dbt development schemas (prefixed with z_USER_) exist."""
    schemas = get_schemas(con)
    
    # In dev, schemas are prefixed with z_<username>_
    dev_schemas = [s for s in schemas if s.startswith('z_')]
    
    if not dev_schemas:
        pytest.skip("No dev schemas found. Run 'task transform' first.")
        
    suffixes = [s.split('_', 2)[-1] for s in dev_schemas]
    
    assert 'staging' in suffixes, "Dev staging schema is missing."
    assert 'seeds' in suffixes, "Dev seeds schema is missing."

def test_dbt_prod_schemas_exist(con):
    """Verifies that the dbt production schemas (unprefixed) exist."""
    schemas = get_schemas(con)
    
    if 'staging' not in schemas and 'seeds' not in schemas:
        pytest.skip("No prod schemas found. Run 'task transform-prod' first.")
        
    assert 'staging' in schemas, "Prod staging schema is missing."
    assert 'seeds' in schemas, "Prod seeds schema is missing."

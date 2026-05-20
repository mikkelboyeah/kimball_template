import os
import re

def pretty_column_name(col):
    """
    Renames columns according to rules:
    - underscores replaced with spaces
    - Camel case with space (Title Case)
    - id -> ID
    - nok -> NOK
    """
    # Replace underscores with spaces
    name = col.replace('_', ' ')
    
    # Split into words and process
    words = name.split()
    processed_words = []
    for word in words:
        upper_word = word.upper()
        if upper_word == 'ID':
            processed_words.append('ID')
        elif upper_word == 'NOK':
            processed_words.append('NOK')
        else:
            # Capitalize word
            processed_words.append(word.capitalize())
    
    return ' '.join(processed_words)

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def export_table_to_parquet(conn, schema, table, output_path):
    """
    Exports a table from DuckDB to Parquet with renamed columns.
    """
    # Get columns
    cols_query = f"SELECT column_name FROM information_schema.columns WHERE table_schema = '{schema}' AND table_name = '{table}' ORDER BY ordinal_position"
    cols = [r[0] for r in conn.execute(cols_query).fetchall()]
    
    # Build the SELECT statement with aliases
    select_parts = []
    for col in cols:
        pretty_name = pretty_column_name(col)
        select_parts.append(f'"{col}" AS "{pretty_name}"')
    
    select_stmt = ", ".join(select_parts)
    export_query = f"COPY (SELECT {select_stmt} FROM {schema}.{table}) TO '{output_path}' (FORMAT PARQUET)"
    
    conn.execute(export_query)

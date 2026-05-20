import os
import shutil
import duckdb
from utils import ensure_dir, export_table_to_parquet

# Configuration
REPORTING_MODELS_DIR = "transform/models/reporting"
EXPORTS_DIR = "data/exports"
DB_PATH = os.getenv("DB_PATH", "data/db.duckdb")

def main():
    print(f"Starting export from {DB_PATH} to {EXPORTS_DIR}...")
    
    if not os.path.exists(DB_PATH):
        print(f"Error: Database file {DB_PATH} not found.")
        return

    conn = duckdb.connect(DB_PATH)
    
    # 1. Get all subfolders in reporting models
    if not os.path.exists(REPORTING_MODELS_DIR):
        print(f"Error: Reporting models directory {REPORTING_MODELS_DIR} not found.")
        return
        
    reporting_subfolders = [f for f in os.listdir(REPORTING_MODELS_DIR) 
                            if os.path.isdir(os.path.join(REPORTING_MODELS_DIR, f))]
    
    # Ensure export base dir exists
    ensure_dir(EXPORTS_DIR)
    
    # Sync folders: remove folders in EXPORTS_DIR that are not in reporting_subfolders
    existing_export_folders = [f for f in os.listdir(EXPORTS_DIR) 
                                if os.path.isdir(os.path.join(EXPORTS_DIR, f))]
    for folder in existing_export_folders:
        if folder not in reporting_subfolders:
            print(f"Removing obsolete export folder: {folder}")
            shutil.rmtree(os.path.join(EXPORTS_DIR, folder))

    # 2. Process each star schema folder
    for folder in reporting_subfolders:
        print(f"Processing star schema: {folder}")
        
        schema_name = f"reporting_{folder}"
        output_folder = os.path.join(EXPORTS_DIR, folder)
        ensure_dir(output_folder)
        
        # Check if schema exists in DuckDB
        schema_exists = conn.execute(f"SELECT count(*) FROM information_schema.schemata WHERE schema_name = '{schema_name}'").fetchone()[0]
        if not schema_exists:
            # Maybe it's just 'reporting' if not configured otherwise? 
            # But dbt_project.yml says specifically reporting_<folder>
            print(f"Warning: Schema {schema_name} not found in database. Skipping.")
            continue
            
        # Get all tables and views in this schema
        tables = conn.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}'").fetchall()
        tables = [t[0] for t in tables]
        
        export_files = []
        for table in tables:
            filename = f"{table}.parquet"
            output_path = os.path.join(output_folder, filename)
            
            print(f"  Exporting {schema_name}.{table} -> {filename}")
            export_table_to_parquet(conn, schema_name, table, output_path)
            export_files.append(filename)
            
        # Create manifest.txt
        manifest_path = os.path.join(output_folder, "manifest.txt")
        with open(manifest_path, "w") as f:
            for file in sorted(export_files):
                f.write(f"{file}\n")
        print(f"  Created manifest for {folder}")

    conn.close()
    print("Export completed successfully.")

if __name__ == "__main__":
    main()

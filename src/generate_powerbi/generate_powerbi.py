import os
import shutil
import json
import duckdb
import argparse
from src.export_reporting.utils import pretty_column_name
from src.generate_powerbi.docs_parser import load_descriptions, normalize_column_name

# Configuration
EXPORTS_DIR = "data/exports"
POWERBI_DIR = "powerbi"
DOCS_PATH = "transform/models/docs.md"

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)

def generate_pbip(schema_name, pbip_path):
    pbip_content = {
      "version": "1.0",
      "artifacts": [
        {
          "report": {
            "path": f"{schema_name}.Report"
          }
        }
      ],
      "settings": {
        "enableAutoRecovery": True
      }
    }
    with open(pbip_path, "w") as f:
        json.dump(pbip_content, f, indent=2)

def generate_report_folder(schema_name, report_dir):
    ensure_dir(report_dir)
    
    # definition.pbir
    pbir_content = {
      "version": "4.0",
      "datasetReference": {
        "byPath": {
          "path": f"../{schema_name}.SemanticModel"
        }
      }
    }
    with open(os.path.join(report_dir, "definition.pbir"), "w") as f:
        json.dump(pbir_content, f, indent=2)
        
    # definition folder structure
    definition_dir = os.path.join(report_dir, "definition")
    ensure_dir(definition_dir)
    
    report_json = {
      "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/report/3.1.0/schema.json",
      "themeCollection": {
        "baseTheme": {
          "name": "CY26SU02",
          "reportVersionAtImport": {
            "visual": "2.6.0",
            "report": "3.1.0",
            "page": "2.3.0"
          },
          "type": "SharedResources"
        }
      },
      "objects": {
        "section": [
          {
            "properties": {
              "verticalAlignment": {
                "expr": {
                  "Literal": {
                    "Value": "'Top'"
                  }
                }
              }
            }
          }
        ]
      },
      "resourcePackages": [
        {
          "name": "SharedResources",
          "type": "SharedResources",
          "items": [
            {
              "name": "CY26SU02",
              "path": "BaseThemes/CY26SU02.json",
              "type": "BaseTheme"
            }
          ]
        }
      ],
      "settings": {
        "useStylableVisualContainerHeader": True,
        "exportDataMode": "AllowSummarized",
        "defaultDrillFilterOtherVisuals": True,
        "allowChangeFilterTypes": True,
        "useEnhancedTooltips": True,
        "useDefaultAggregateDisplayName": True
      }
    }
    with open(os.path.join(definition_dir, "report.json"), "w") as f:
        json.dump(report_json, f, indent=2)
        
    # version.json
    version_json = {
      "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
      "version": "2.0.0"
    }
    with open(os.path.join(definition_dir, "version.json"), "w") as f:
        json.dump(version_json, f, indent=2)
        
    pages_dir = os.path.join(definition_dir, "pages")
    ensure_dir(pages_dir)
    
    page_id = "62f12bd1026a35b3ca83"
    pages_json = {
      "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.0.0/schema.json",
      "pageOrder": [
        page_id
      ],
      "activePageName": page_id
    }
    with open(os.path.join(pages_dir, "pages.json"), "w") as f:
        json.dump(pages_json, f, indent=2)
        
    page_dir = os.path.join(pages_dir, page_id)
    ensure_dir(page_dir)
    
    page_json = {
      "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.0.0/schema.json",
      "name": page_id,
      "displayName": "Page 1",
      "displayOption": "FitToPage",
      "height": 720,
      "width": 1280
    }
    with open(os.path.join(page_dir, "page.json"), "w") as f:
        json.dump(page_json, f, indent=2)

def _duckdb_to_powerbi_type(duckdb_type):
    """Maps duckdb types to power bi data types for TMDL/M."""
    duckdb_type = duckdb_type.upper()
    if duckdb_type in ['BIGINT', 'INTEGER', 'SMALLINT', 'TINYINT']:
        return "int64"
    elif duckdb_type in ['DOUBLE', 'FLOAT', 'DECIMAL', 'NUMERIC']:
        return "double"
    elif duckdb_type in ['BOOLEAN']:
        return "boolean"
    elif duckdb_type in ['DATE', 'TIMESTAMP', 'TIME']:
        return "dateTime"
    else:
        return "string"

def generate_semantic_model(schema_name, semantic_model_dir, repo_root_abs):
    ensure_dir(semantic_model_dir)

    # Load descriptions from docs.md
    descriptions = load_descriptions(DOCS_PATH)

    # 1. definition.pbism
    pbism_content = {
      "version": "4.2",
      "settings": {}
    }
    with open(os.path.join(semantic_model_dir, "definition.pbism"), "w") as f:
        json.dump(pbism_content, f, indent=2)

    definition_dir = os.path.join(semantic_model_dir, "definition")
    ensure_dir(definition_dir)

    # 2. model.tmdl
    model_tmdl = f"""model Model
\tculture: en-US
\tdefaultPowerBIDataSourceVersion: powerBI_V3
\tsourceQueryCulture: en-US
\tdataAccessOptions
\t\tlegacyRedirects
\t\treturnErrorValuesAsNull

/// Repository root path for local parquet files
expression RepoRoot = "{repo_root_abs}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]

annotation __PBI_TimeIntelligenceEnabled = 1

annotation PBI_ProTooling = ["DevMode"]

ref cultureInfo en-US
"""
    with open(os.path.join(definition_dir, "model.tmdl"), "w", encoding='utf-8') as f:
        f.write(model_tmdl)

    # 3. database.tmdl
    database_tmdl = "database\n\tcompatibilityLevel: 1600\n"
    with open(os.path.join(definition_dir, "database.tmdl"), "w", encoding='utf-8') as f:
        f.write(database_tmdl)

    tables_dir = os.path.join(definition_dir, "tables")
    ensure_dir(tables_dir)

    conn = duckdb.connect()
    
    exports_schema_dir = os.path.join(EXPORTS_DIR, schema_name)
    parquet_files = [f for f in os.listdir(exports_schema_dir) if f.endswith('.parquet')]
    
    dimensions = []
    facts = []
    
    fact_schemas = {}
    dim_schemas = {}

    for parquet_file in parquet_files:
        table_name = parquet_file.replace('.parquet', '')
        if table_name.startswith('dim_'):
            dimensions.append(table_name)
        elif table_name.startswith('fact_'):
            facts.append(table_name)
            
        pretty_table_name = pretty_column_name(table_name)
            
        # Path relative to repo root, using forward slashes for M-code compatibility
        rel_parquet_path = f"{exports_schema_dir}/{parquet_file}".replace('\\', '/')
        
        # Get schema from duckdb
        cols_query = f"DESCRIBE SELECT * FROM parquet_scan('{exports_schema_dir}/{parquet_file}')"
        schema_info = conn.execute(cols_query).fetchall()
        
        # Build TMDL Table
        tmdl_lines = []
        
        # Add table description if available
        table_desc = descriptions.get(f"table_{table_name}")
        if table_desc:
            tmdl_lines.append(f"/// {table_desc}")
            
        tmdl_lines.append(f"table '{pretty_table_name}'")
        tmdl_lines.append("")

        for col in schema_info:
            col_name = col[0]
            col_type = col[1]
            pbi_type = _duckdb_to_powerbi_type(col_type)
            
            # Add column description if available
            # We need to map the "Pretty Column Name" back to snake_case for lookup
            # Actually, col_name is from the parquet file, which is already Pretty Column Name
            normalized_col = normalize_column_name(col_name)
            col_desc = descriptions.get(f"column_{normalized_col}")
            if col_desc:
                tmdl_lines.append(f"\t/// {col_desc}")
                
            tmdl_lines.append(f"\tcolumn '{col_name}'")
            tmdl_lines.append(f"\t\tdataType: {pbi_type}")
            tmdl_lines.append(f"\t\tsourceColumn: {col_name}")
            tmdl_lines.append("")

        # Partition with M Code using RepoRoot parameter
        m_code = f"""\t\t\tlet
\t\t\t\tSource = Parquet.Document(File.Contents(RepoRoot & "/{rel_parquet_path}"))
\t\t\tin
\t\t\t\tSource"""
        
        tmdl_lines.append(f"\tpartition '{pretty_table_name}' = m")
        tmdl_lines.append("\t\tmode: import")
        tmdl_lines.append("\t\tsource = ")
        tmdl_lines.append(m_code)
        
        tmdl_content = "\n".join(tmdl_lines)
        with open(os.path.join(tables_dir, f"{pretty_table_name}.tmdl"), "w", encoding='utf-8') as f:
            f.write(tmdl_content)
        
        # Save schema for relationship matching
        if table_name.startswith('fact_'):
            fact_schemas[pretty_table_name] = [c[0] for c in schema_info]
        elif table_name.startswith('dim_'):
            dim_schemas[pretty_table_name] = [c[0] for c in schema_info]

    conn.close()
    
    # Generate relationships
    # We will append them to the model.tmdl file or create separate relationship definitions
    # It is standard to declare relationships at the bottom of model.tmdl or in separate files.
    # TMDL supports defining relationships directly within `model.tmdl`.
    
    with open(os.path.join(definition_dir, "model.tmdl"), "a", encoding='utf-8') as f:
        for fact_table, fact_cols in fact_schemas.items():
            for dim_table, dim_cols in dim_schemas.items():
                # Find matching columns by exact string match
                common_cols = set(fact_cols).intersection(set(dim_cols))
                for col in common_cols:
                    # Skip common columns that aren't IDs if you want, but ID suffix implies keys
                    if col.upper().endswith("ID"):
                        import uuid
                        rel_id = str(uuid.uuid4())
                        f.write(f"\nrelationship {rel_id}\n")
                        f.write(f"\tfromColumn: '{fact_table}'.'{col}'\n")
                        f.write(f"\ttoColumn: '{dim_table}'.'{col}'\n")

def main():
    parser = argparse.ArgumentParser(description="Generate Power BI PBIP folders.")
    parser.add_argument("--root", help="Optional Repository root path for local parquet files.")
    args = parser.parse_args()

    # Detect or use provided RepoRoot and normalize
    if args.root:
        repo_root_abs = os.path.abspath(args.root).replace('\\', '/')
    else:
        repo_root_abs = os.path.abspath(os.getcwd()).replace('\\', '/')

    print(f"Starting Power BI generation from {EXPORTS_DIR} to {POWERBI_DIR}...")
    print(f"Using RepoRoot: {repo_root_abs}")
    
    if not os.path.exists(EXPORTS_DIR):
        print(f"Error: Exports directory {EXPORTS_DIR} not found.")
        return
        
    schemas = [f for f in os.listdir(EXPORTS_DIR) if os.path.isdir(os.path.join(EXPORTS_DIR, f))]
    
    ensure_dir(POWERBI_DIR)
    
    for schema_name in schemas:
        print(f"Processing PBIP for schema: {schema_name}")
        schema_dir = os.path.join(POWERBI_DIR, schema_name)
        ensure_dir(schema_dir)
        
        # 1. Generate .pbip
        pbip_path = os.path.join(schema_dir, f"{schema_name}.pbip")
        generate_pbip(schema_name, pbip_path)
        
        # 2. Generate .Report directory
        report_dir = os.path.join(schema_dir, f"{schema_name}.Report")
        generate_report_folder(schema_name, report_dir)
        
        # 3. Generate .SemanticModel directory
        semantic_model_dir = os.path.join(schema_dir, f"{schema_name}.SemanticModel")
        generate_semantic_model(schema_name, semantic_model_dir, repo_root_abs)
        print(f"  Created report definition and semantic model for {schema_name}")

if __name__ == "__main__":
    main()

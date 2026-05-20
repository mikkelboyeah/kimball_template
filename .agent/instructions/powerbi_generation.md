# Power BI Project (PBIP) Generation Guidelines

These guidelines are based on lessons learned while programmatically generating Power BI Projects (PBIP) using Python, Parquet, and TMDL.

## 1. Required Files for PBIP/PBIR
Power BI Desktop is strict about the presence of certain metadata files. Without these, it will throw "Cannot find file" errors.
- **Report Definition**: Always include `Report.Report/definition/version.json`.
    ```json
    {
      "$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json",
      "version": "2.0.0"
    }
    ```
- **Semantic Model Definition**: Always include `SemanticModel.SemanticModel/definition/database.tmdl`.
    ```tmdl
    database
        compatibilityLevel: 1600
    ```

## 2. TMDL Parameter Syntax
When defining parameters (expressions with metadata) in TMDL files:
- **Rule**: The `meta` block MUST be on the same line as the expression value.
- **Incorrect**:
    ```tmdl
    expression ParamName = "Value"
        meta [IsParameterQuery=true, ...]
    ```
- **Correct**:
    ```tmdl
    expression ParamName = "Value" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]
    ```

## 3. Handling Absolute Paths (RepoRoot)
Power BI's `File.Contents` function (used for loading Parquet or CSV files) does NOT support relative paths.
- **Solution**: Define a `RepoRoot` parameter in the Semantic Model.
- **Implementation**:
    1. Define the parameter: `expression RepoRoot = "C:/Path/To/Repo" meta [...]`
    2. Use it in Table Partitions: `Source = Parquet.Document(File.Contents(RepoRoot & "/data/exports/..."))`
- **Benefit**: This makes the project shareable; a new user only needs to update the single `RepoRoot` parameter once to fix all data sources.

## 4. Relationship Inference
When generating a Star Schema semantic model from flat files:
- Differentiate tables by prefix (e.g., `fact_` and `dim_`).
- Auto-detect relationships by finding matching column names between Facts and Dimensions.
- Prioritize columns ending in `ID` (e.g., `Policyholder ID`) as relationship keys.
- Relationships should be declared at the bottom of `model.tmdl`:
    ```tmdl
    relationship <uuid>
        fromColumn: 'fact_table'.'Key ID'
        toColumn: 'dim_table'.'Key ID'
    ```

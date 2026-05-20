# Data Generators

This directory contains Python scripts for generating mock insurance claim data, including a fact table and its associated dimension tables.

## Purpose

The scripts simulate a **Claim Accumulating Snapshot** fact table and its corresponding star schema dimensions. This is used to populate the `transform/seeds` directory with data for dbt transformation and analysis.

## Files

- **`generate_facts.py`**: Generates the primary fact table (`claim_accumulating_snapshot.csv`). 
  - Simulates 5,000 unique claims.
  - Implements realistic date progressions (Accident Date → Open Date → Estimate Date → Payment Dates → Close Date).
  - Generates financial values (reserves, payments, salvage/subrogation) in NOK.
  - Calculates various "lags" between lifecycle events.
- **`generate_dims.py`**: Generates 9 dimension tables based on the keys and attributes found in the fact table.
  - Ensures referential integrity by pulling unique IDs from the fact data.
  - Generates realistic attributes for policyholders, employees, coverage types, etc.
- **`test_generation.py`**: A `pytest` suite to verify that the generated data matches the expected schema and directory structure.

## How to Run

### 1. Prerequisites
Ensure you have the required Python dependencies installed (e.g., in a virtual environment):
```bash
pip install pandas numpy pytest
```

### 2. Generate the Data
The scripts are designed to be run from the `data_generators` folder or the project root. They output CSV files directly to the `transform/seeds` directory.

Run the fact generator first, followed by the dimension generator:

```bash
# 1. Generate the core facts
python generate_facts.py

# 2. Generate dimensions linked to those facts
python generate_dims.py
```

### 3. Verify the Output
After generation, you can run the tests to ensure the files were created correctly:

```bash
pytest test_generation.py
```

## Technical Details

- **Output Location**: Files are saved to `../transform/seeds/`.
- **Randomness**: Both generators use a fixed seed (`42`) to ensure reproducibility.
- **Naming Convention**: All columns are strictly `snake_case` according to the project's data standards.
- **Key Strategy**: Primary and foreign keys consistently use the `_id` suffix.

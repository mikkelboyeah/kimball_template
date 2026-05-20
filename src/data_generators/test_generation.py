import os
import pandas as pd
import pytest

# Determine the seed directory relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SEED_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', 'transform', 'seeds'))

EXPECTED_FILES = [
    'claim_accumulating_snapshot.csv',
    'dim_claim.csv',
    'dim_claimant.csv',
    'dim_claim_profile.csv',
    'dim_claim_status.csv',
    'dim_coverage.csv',
    'dim_covered_item.csv',
    'dim_date.csv',
    'dim_employee.csv',
    'dim_policyholder.csv'
]

def test_all_files_exist():
    """Verify that all target CSV files have been properly generated."""
    for f in EXPECTED_FILES:
        file_path = os.path.join(SEED_DIR, f)
        assert os.path.exists(file_path), f"Missing file: {f}. Did you run the generators?"

def test_columns_are_snake_case():
    """Verify that all columns in the CSV are fully lowercased snake_case without spaces."""
    for f in EXPECTED_FILES:
        file_path = os.path.join(SEED_DIR, f)
        if not os.path.exists(file_path):
            continue
        
        df = pd.read_csv(file_path, nrows=1)
        for col in df.columns:
            assert ' ' not in col, f"File {f} has column '{col}' with spaces."
            assert col == col.lower(), f"File {f} has column '{col}' with uppercase letters."
            assert col == col.strip(), f"File {f} has column '{col}' with leading/trailing whitespaces."

def test_columns_use_id_suffix():
    """Verify that no primary or foreign key uses '_key', but correctly uses '_id'."""
    for f in EXPECTED_FILES:
        file_path = os.path.join(SEED_DIR, f)
        if not os.path.exists(file_path):
            continue
        
        df = pd.read_csv(file_path, nrows=1)
        for col in df.columns:
            assert not col.endswith('_key'), f"File {f} has column '{col}' ending in '_key'. It should be '_id'."

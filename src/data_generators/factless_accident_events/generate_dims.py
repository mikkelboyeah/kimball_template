import pandas as pd
import numpy as np
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, '..', '..', '..', 'data', 'raw', 'factless_accident_events'))
os.makedirs(OUT_DIR, exist_ok=True)

def generate_dim_loss_party():
    data = [
        {'loss_party_id': 1, 'party_name': 'ABC Mold Assessors', 'party_type': 'Consultant', 'contact_info': 'contact@abcmold.com'},
        {'loss_party_id': 2, 'party_name': 'XYZ Remediation', 'party_type': 'Contractor', 'contact_info': 'info@xyzremediation.com'},
        {'loss_party_id': 3, 'party_name': 'Pest Killers Inc.', 'party_type': 'Contractor', 'contact_info': 'support@pestkillers.com'},
        {'loss_party_id': 4, 'party_name': 'Legal Eagles LLP', 'party_type': 'Legal', 'contact_info': 'justice@legaleagles.com'},
        {'loss_party_id': 5, 'party_name': 'Pure Water Experts', 'party_type': 'Consultant', 'contact_info': 'water@pureexperts.com'}
    ]
    df = pd.DataFrame(data)
    df.to_parquet(os.path.join(OUT_DIR, 'dim_loss_party.parquet'), index=False)
    print("Generated dim_loss_party")

def generate_dim_loss_party_role():
    data = [
        {'loss_party_role_id': 1, 'role_description': 'Initial Inspector'},
        {'loss_party_role_id': 2, 'role_description': 'Primary Remediator'},
        {'loss_party_role_id': 3, 'role_description': 'Legal Representative'},
        {'loss_party_role_id': 4, 'role_description': 'Independent Assessor'},
        {'loss_party_role_id': 5, 'role_description': 'Witness'}
    ]
    df = pd.DataFrame(data)
    df.to_parquet(os.path.join(OUT_DIR, 'dim_loss_party_role.parquet'), index=False)
    print("Generated dim_loss_party_role")

def main():
    generate_dim_loss_party()
    generate_dim_loss_party_role()

if __name__ == "__main__":
    main()

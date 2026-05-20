select
    policy_transaction_audit_id,
    etl_job_name,
    data_quality_flag,
    source_system
from {{ ref('stg_pol_tr__dim_policy_transaction_audit') }}

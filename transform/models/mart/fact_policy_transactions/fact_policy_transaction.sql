select
    policy_transaction_date_id,
    policy_effective_date_id,
    policyholder_id,
    employee_id,
    coverage_id,
    covered_item_id,
    policy_transaction_type_id,
    policy_transaction_audit_id,
    policy_number,
    policy_transaction_number,
    policy_transaction_amount_nok
from {{ ref('stg_pol_tr__fact_policy_transaction') }}

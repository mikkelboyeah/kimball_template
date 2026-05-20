select
    policy_transaction_type_id,
    transaction_category,
    transaction_reason_description
from {{ ref('stg_pol_tr__dim_policy_transaction_type') }}

select
    policy_status_id,
    status_name,
    status_description
from {{ ref('stg_prem_ps__dim_policy_status') }}

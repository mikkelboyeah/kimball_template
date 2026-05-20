with source as (
    select * from {{ source('raw', 'fact_policy_transaction') }}
),

renamed as (
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
    from source
)

select * from renamed

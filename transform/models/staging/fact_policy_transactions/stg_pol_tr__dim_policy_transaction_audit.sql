with source as (
    select * from {{ source('raw', 'dim_policy_transaction_audit') }}
),

renamed as (
    select
        policy_transaction_audit_id,
        etl_job_name,
        data_quality_flag,
        source_system
    from source
)

select * from renamed

with source as (
    select * from {{ source('raw', 'dim_loss_party') }}
),

renamed as (
    select
        loss_party_id,
        party_name,
        party_type,
        contact_info
    from source
)

select * from renamed

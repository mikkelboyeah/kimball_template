with source as (
    select * from {{ source('raw', 'dim_loss_party_role') }}
),

renamed as (
    select
        loss_party_role_id,
        role_description
    from source
)

select * from renamed

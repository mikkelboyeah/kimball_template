select * from {{ source('raw', 'claim_accumulating_snapshot') }}

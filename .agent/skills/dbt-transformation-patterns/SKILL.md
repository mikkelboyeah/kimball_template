# dbt Transformation Patterns

Production-ready patterns for dbt (data build tool) including model organization, testing strategies, documentation, and incremental processing.

## When to Use This Skill

**Project setup & structure**
- Setting up dbt project structure
- Organizing models into staging, intermediate, and marts layers

**Development**
- Building data transformation pipelines with dbt
- Creating incremental models for large datasets

**Quality & documentation**
- Implementing data quality tests
- Documenting data models and lineage

## Core Concepts

### 1. Model Layers (Medallion Architecture)
- **sources/**: Raw data definitions
- **staging/**: 1:1 with source, light cleaning
- **intermediate/**: Business logic, joins, aggregations
- **marts/**: Final analytics tables

### 2. Naming Conventions
Apply in layer order (staging → intermediate → marts):
- `stg_`: Staging models (e.g., `stg_stripe__payments`)
- `int_`: Intermediate models (e.g., `int_payments_pivoted`)
- `dim_`: Dimension tables (e.g., `dim_customers`)
- `fct_`: Fact tables (e.g., `fct_orders`)

## Quick Start (dbt_project.yml)
```yaml
name: "analytics"
version: "1.0.0"
profile: "analytics"

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]

vars:
  start_date: "2020-01-01"

models:
  analytics:
    staging:
      +materialized: view
      +schema: staging
    intermediate:
      +materialized: ephemeral
    marts:
      +materialized: table
      +schema: analytics
```

## Project Structure
```text
models/
├── staging/
│   ├── stripe/
│   │   ├── _stripe__sources.yml
│   │   ├── _stripe__models.yml
│   │   ├── stg_stripe__customers.sql
│   │   └── stg_stripe__payments.sql
├── intermediate/
│   └── finance/
│       └── int_payments_pivoted.sql
└── marts/
    ├── core/
    │   ├── _core__models.yml
    │   ├── dim_customers.sql
    │   └── fct_orders.sql
```

## Patterns

### Pattern 1: Source Definitions
```yaml
version: 2
sources:
  - name: stripe
    database: raw
    schema: stripe
    tables:
      - name: customers
        tests:
          - unique
          - not_null
      - name: payments
        tests:
          - unique
          - not_null
          - relationships:
              arguments:
                to: source('stripe', 'customers')
                field: id
```

### Pattern 2: Staging Models
```sql
-- models/staging/stripe/stg_stripe__customers.sql
with source as (
    select * from {{ source('stripe', 'customers') }}
),
renamed as (
    select
        id as customer_id,
        lower(email) as email,
        name as customer_name,
        created as created_at,
        _fivetran_synced as _loaded_at
    from source
)
select * from renamed
```

### Pattern 3: Intermediate Models
```sql
-- models/intermediate/finance/int_payments_pivoted_to_customer.sql
with payments as (
    select * from {{ ref('stg_stripe__payments') }}
),
customers as (
    select * from {{ ref('stg_stripe__customers') }}
),
payment_summary as (
    select
        customer_id,
        count(*) as total_payments,
        sum(case when payment_status = 'succeeded' then amount else 0 end) as total_amount_paid
    from payments
    group by customer_id
)
select
    customers.customer_id,
    customers.email,
    coalesce(payment_summary.total_payments, 0) as total_payments,
    coalesce(payment_summary.total_amount_paid, 0) as lifetime_value
from customers
left join payment_summary using (customer_id)
```

### Pattern 4: Mart Models (Dimensions and Facts)
```sql
-- models/marts/core/dim_customers.sql
{{ config(materialized='table', unique_key='customer_id') }}
with customers as (
    select * from {{ ref('int_payments_pivoted_to_customer') }}
),
final as (
    select
        {{ dbt_utils.generate_surrogate_key(['customer_id']) }} as customer_key,
        customer_id,
        email,
        total_payments,
        lifetime_value,
        current_timestamp as _loaded_at
    from customers
)
select * from final
```

### Pattern 5: Testing and Documentation
```yaml
version: 2
models:
  - name: dim_customers
    columns:
      - name: customer_key
        tests:
          - unique
          - not_null
      - name: email
        tests:
          - not_null
```

### Pattern 6: Macros and DRY Code
```sql
-- macros/cents_to_dollars.sql
{% macro cents_to_dollars(column_name, precision=2) %}
    round({{ column_name }} / 100.0, {{ precision }})
{% endmacro %}
```

### Pattern 7: Incremental Strategies
- **Delete+Insert**: Default for most warehouses.
- **Merge**: Best for late-arriving data.
- **Insert Overwrite**: Partition-based.

## dbt Commands
- `dbt run`: Run all models
- `dbt test`: Run all tests
- `dbt build`: Run + test in DAG order
- `dbt docs generate`: Generate docs
- `dbt compile`: Compile SQL without running

## Best Practices

### For Data Quality
- Test aggressively — not null, unique, and relationship tests on every model
- Document column descriptions in `.yml` files alongside models

### For Large Datasets
- Use incremental models for tables exceeding 1M rows
- Prefer merge or insert-overwrite strategies for late-arriving data

### For Team Collaboration
- Always use the staging layer — clean data once, reuse everywhere; skipping it creates tech debt
- Extract repeated logic into macros to keep models DRY
- Never hardcode dates — use `{{ var('start_date') }}` instead

### For Safe Development
- Run and test against a dev target; never run destructive changes directly in prod

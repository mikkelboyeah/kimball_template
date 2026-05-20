# dbt Documentation Blocks

## Table Descriptions

{% docs table_dim_claim %}
Dimension table for claim.
{% enddocs %}

{% docs table_dim_claim_profile %}
Dimension table for claim profile.
{% enddocs %}

{% docs table_dim_claim_status %}
Dimension table for claim status.
{% enddocs %}

{% docs table_dim_claimant %}
Dimension table for claimant.
{% enddocs %}

{% docs table_dim_coverage %}
Dimension table for coverage.
{% enddocs %}

{% docs table_dim_covered_item %}
Dimension table for covered item.
{% enddocs %}

{% docs table_dim_date %}
Dimension table for date.
{% enddocs %}

{% docs table_dim_employee %}
Dimension table for employee.
{% enddocs %}

{% docs table_dim_loss_party %}
Dimension table for loss party.
{% enddocs %}

{% docs table_dim_loss_party_role %}
Dimension table for loss party role.
{% enddocs %}

{% docs table_dim_policy_status %}
Dimension table for policy status.
{% enddocs %}

{% docs table_dim_policy_transaction_audit %}
Dimension table for policy transaction audit.
{% enddocs %}

{% docs table_dim_policy_transaction_type %}
Dimension table for policy transaction type.
{% enddocs %}

{% docs table_dim_policyholder %}
Dimension table for policyholder.
{% enddocs %}

{% docs table_fact_accident_events %}
A factless fact table that records the many-to-many correlations between the people (loss parties) and vehicles/properties (loss items) involved in an accident. It captures the collision of keys at a point in time and space, enabling complex queries about accident involvements without including standard numeric measurements.
{% enddocs %}

{% docs table_fact_claim_accumulating_snapshot %}
An accumulating snapshot fact table that provides an updated status and final disposition of each claim. One row is created when the claim is opened, and the row is destructively updated throughout the life of the claim as it reaches standard intermediate milestones.
{% enddocs %}

{% docs table_fact_claim_periodic_snapshot %}
A periodic snapshot fact table recording the status and metrics of active claims at a regular snapshot interval, such as monthly. This is particularly useful for long-term claims (like bodily injury or long-term disability) where tracking the claim's financial impact across standardized monthly reporting periods is required.
{% enddocs %}

{% docs table_fact_insurance_consolidated_snapshot %}
A **consolidated fact table** that combines premium revenue and claim loss financial metrics from separate business processes (policy and claims) at a common, least-common-denominator granularity. This table allows business users to easily analyze profit metrics and drill across processes without needing their BI tools to stitch together separate result sets.
{% enddocs %}

{% docs table_fact_policy_transaction %}
A **transaction grain fact table** where one row represents each individual policy transaction (e.g., create, alter, cancel, rate, or underwrite). This table enables the business to analyze detailed transactional behavior in extreme detail, capturing the events that formulate or modify a policy over time.
{% enddocs %}

{% docs table_fact_premium_periodic_snapshot %}
A **periodic snapshot fact table** designed to quickly determine the status and financial value of in-force policies at a point in time. Because customers pay in advance for insurance, the complex rules of earned revenue recognition make analyzing transactions directly too difficult; this table solves that by taking a snapshot at the end of each month at the grain of one row per coverage and covered item.
{% enddocs %}

## Column Descriptions


 {% docs column_accident_involvement_count %}
A dummy fact, always valued at 1, to facilitate counting and aggregation of accident involvements.
{% enddocs %}

{% docs column_agent_id %}
Foreign key to the Agent dimension.
{% enddocs %}

{% docs column_amount_claimed %}
Numeric, additive fact representing the total amount claimed during the snapshot period.
{% enddocs %}

{% docs column_amount_paid %}
Numeric, additive fact representing the total amount paid out on the claim during the snapshot period.
{% enddocs %}

{% docs column_appraised_value_range %}
Column containing appraised value range information.
{% enddocs %}

{% docs column_catastrophe_indicator %}
Column containing catastrophe indicator information.
{% enddocs %}

{% docs column_change_in_reserve %}
Numeric, additive fact representing adjustments made to the claim's reserve estimate during the snapshot period.
{% enddocs %}

{% docs column_city %}
The city portion of the address.
{% enddocs %}

{% docs column_claim_1st_payment_date_id %}
Role-playing date foreign key representing when the first claim payment was made.
{% enddocs %}

{% docs column_claim_accident_date_id %}
Role-playing date foreign key representing when the loss/accident occurred.
{% enddocs %}

{% docs column_claim_accident_to_open_lag %}
Metric representing the time duration/lag between the loss date and the open date.
{% enddocs %}

{% docs column_claim_close_date_id %}
Role-playing date foreign key representing when the claim was officially closed.
{% enddocs %}

{% docs column_claim_estimate_date_id %}
Role-playing date foreign key representing when the claim estimate was established.
{% enddocs %}

{% docs column_claim_id %}
Foreign key to the Claim dimension.
{% enddocs %}

{% docs column_claim_loss_date_id %}
Foreign key to the Date dimension representing when the loss event occurred.
{% enddocs %}

{% docs column_claim_most_recent_payment_date_id %}
Role-playing date foreign key representing the date of the most recent claim payment.
{% enddocs %}

{% docs column_claim_number %}
Degenerate dimension for the claim number.
{% enddocs %}

{% docs column_claim_number_dd %}
Degenerate dimension capturing the operational transaction control number for the claim.
{% enddocs %}

{% docs column_claim_open_date_id %}
Role-playing date foreign key representing when the claim was opened.
{% enddocs %}

{% docs column_claim_open_to_1st_payment_lag %}
Metric representing the time duration/lag between the open date and the first payment date.
{% enddocs %}

{% docs column_claim_open_to_closed_lag %}
Metric representing the overall time duration/lag from when the claim was opened to when it was closed.
{% enddocs %}

{% docs column_claim_open_to_estimate_lag %}
Metric representing the time duration/lag between the open date and the estimate date.
{% enddocs %}

{% docs column_claim_open_to_subrogation_lag %}
Metric representing the time duration/lag between the open date and subrogation date.
{% enddocs %}

{% docs column_claim_paid_dollar_amount %}
Numeric fact representing the total amount paid out for claims against this policy/coverage during the snapshot period.
{% enddocs %}

{% docs column_claim_paid_to_date_nok_amount %}
Cumulative numeric fact of all payments made on the claim to date.
{% enddocs %}

{% docs column_claim_profile_id %}
Foreign key to the Claim Profile junk dimension.
{% enddocs %}

{% docs column_claim_report_method %}
Column containing claim report method information.
{% enddocs %}

{% docs column_claim_status_id %}
Foreign key to the Claim Status dimension indicating the state of any claims against this policy at month-end.
{% enddocs %}

{% docs column_claim_subrogation_date_id %}
Role-playing date foreign key representing when subrogation proceedings began.
{% enddocs %}

{% docs column_claim_supervisor_id %}
Foreign key to the Employee dimension for the supervisor managing the claim during this period.
{% enddocs %}

{% docs column_claim_total_claimed_dollar_amount %}
Numeric fact representing the total dollar amount claimed against this policy during the period.
{% enddocs %}

{% docs column_claimant_id %}
Foreign key to the Claimant dimension.
{% enddocs %}

{% docs column_claimant_natural_id %}
Unique identifier (surrogate key) for the claimant.
{% enddocs %}

{% docs column_contact_info %}
Column containing contact info information.
{% enddocs %}

{% docs column_coverage_code %}
Column containing coverage code information.
{% enddocs %}

{% docs column_coverage_id %}
Foreign key to the conformed Coverage dimension.
{% enddocs %}

{% docs column_coverage_limit %}
Column containing coverage limit information.
{% enddocs %}

{% docs column_coverage_type %}
Column containing coverage type information.
{% enddocs %}

{% docs column_covered_item_id %}
Foreign key to the conformed Covered Item dimension.
{% enddocs %}

{% docs column_current_reserve_balance %}
Semi-additive fact representing the total reserve balance remaining on the claim at the close of the snapshot period.
{% enddocs %}

{% docs column_current_reserve_to_date_nok_amount %}
Numeric fact representing the current reserve dollar amount associated with the claim to date.
{% enddocs %}

{% docs column_customer_segment %}
Column containing customer segment information.
{% enddocs %}

{% docs column_data_quality_flag %}
Column containing data quality flag information.
{% enddocs %}

{% docs column_date_id %}
Unique identifier (surrogate key) for the date.
{% enddocs %}

{% docs column_day_of_week %}
Column containing day of week information.
{% enddocs %}

{% docs column_deductible_amount %}
Column containing deductible amount information.
{% enddocs %}

{% docs column_earned_premium_revenue_amount %}
Numeric, additive fact representing the premium revenue earned month by month as the insurance company provides coverage.
{% enddocs %}

{% docs column_earned_premium_revenue_dollar_amount %}
Numeric fact representing the portion of the premium revenue earned by the insurance company during this period as the service is provided.
{% enddocs %}

{% docs column_employee_id %}
Foreign key to the Employee dimension representing the specific employee (e.g., underwriter) who executed the transaction.
{% enddocs %}

{% docs column_employee_natural_id %}
Unique identifier (surrogate key) for the employee.
{% enddocs %}

{% docs column_estimate_nok_amount %}
Numeric fact representing the estimated dollar amount of the claim.
{% enddocs %}

{% docs column_etl_job_name %}
Column containing etl job name information.
{% enddocs %}

{% docs column_fault_indicator %}
Column containing fault indicator information.
{% enddocs %}

{% docs column_first_name %}
The individual's first name.
{% enddocs %}

{% docs column_full_date %}
The full date in YYYY-MM-DD format.
{% enddocs %}

{% docs column_is_holiday %}
Column containing is holiday information.
{% enddocs %}

{% docs column_is_weekend %}
Column containing is weekend information.
{% enddocs %}

{% docs column_item_description %}
Descriptive text for the item.
{% enddocs %}

{% docs column_item_type %}
Column containing item type information.
{% enddocs %}

{% docs column_job_title %}
Column containing job title information.
{% enddocs %}

{% docs column_last_name %}
The individual's last name.
{% enddocs %}

{% docs column_line_of_business %}
Column containing line of business information.
{% enddocs %}

{% docs column_loss_description %}
Descriptive text for the loss.
{% enddocs %}

{% docs column_loss_party_id %}
Foreign key to the Loss Party dimension capturing the specific individuals involved in the accident.
{% enddocs %}

{% docs column_loss_party_role_id %}
Foreign key to the Loss Party Role dimension identifying the capacity of the individual (e.g., passenger, witness, or legal representation).
{% enddocs %}

{% docs column_month %}
The calendar month (1-12).
{% enddocs %}

{% docs column_month_end_snapshot_date_id %}
Foreign key to the conformed Month-end Date dimension.
{% enddocs %}

{% docs column_month_name %}
The full name of the month.
{% enddocs %}

{% docs column_number_of_claim_transactions %}
Additive fact counting the total number of transactions that have occurred on this claim workflow.
{% enddocs %}

{% docs column_original_reserve_nok_amount %}
Numeric fact representing the preliminary estimate of the insurance company's liability when the claim is opened.
{% enddocs %}

{% docs column_party_name %}
Column containing party name information.
{% enddocs %}

{% docs column_party_type %}
Column containing party type information.
{% enddocs %}

{% docs column_police_report_filed %}
Column containing police report filed information.
{% enddocs %}

{% docs column_policy_effective_date_id %}
Role-playing date foreign key representing when the transaction legally takes effect.
{% enddocs %}

{% docs column_policy_number %}
Degenerate dimension for the policy number.
{% enddocs %}

{% docs column_policy_number_dd %}
Degenerate dimension capturing the operational transaction control number for the policy.
{% enddocs %}

{% docs column_policy_status_id %}
Foreign key to a Status dimension quickly identifying the current state of a coverage or policy (e.g., new, canceled).
{% enddocs %}

{% docs column_policy_transaction_amount_nok %}
Numeric fact capturing the dollar amount associated with the specific policy transaction.
{% enddocs %}

{% docs column_policy_transaction_audit_id %}
Foreign key to an Audit dimension that tracks ETL metadata, data lineage, and data quality indicators at the time this fact row was loaded.
{% enddocs %}

{% docs column_policy_transaction_date_id %}
Role-playing date foreign key representing when the transaction was entered into the operational system.
{% enddocs %}

{% docs column_policy_transaction_number %}
Degenerate dimension for the operational control number associated with this specific transaction.
{% enddocs %}

{% docs column_policy_transaction_type_id %}
Foreign key to a low-cardinality dimension describing the specific transaction type (e.g., rate coverage, cancel policy) and the reason for it.
{% enddocs %}

{% docs column_policyholder_id %}
Foreign key to the conformed Policyholder dimension.
{% enddocs %}

{% docs column_policyholder_natural_id %}
Unique identifier (surrogate key) for the policyholder.
{% enddocs %}

{% docs column_quarter %}
The calendar quarter (Q1-Q4).
{% enddocs %}

{% docs column_region %}
Column containing region information.
{% enddocs %}

{% docs column_relationship_to_policyholder %}
Column containing relationship to policyholder information.
{% enddocs %}

{% docs column_role_description %}
Descriptive text for the role.
{% enddocs %}

{% docs column_salvage_collected_to_date_nok_amount %}
Cumulative numeric fact of salvage payments received by the insurance company to date.
{% enddocs %}

{% docs column_source_system %}
Column containing source system information.
{% enddocs %}

{% docs column_state %}
The state or province portion of the address.
{% enddocs %}

{% docs column_status_description %}
Descriptive text for the status.
{% enddocs %}

{% docs column_status_name %}
Column containing status name information.
{% enddocs %}

{% docs column_sub_status_description %}
Descriptive text for the sub status.
{% enddocs %}

{% docs column_subro_payment_collected_to_date_nok_amount %}
Cumulative numeric fact of subrogation payments collected to date.
{% enddocs %}

{% docs column_transaction_category %}
Column containing transaction category information.
{% enddocs %}

{% docs column_transaction_reason_description %}
Descriptive text for the transaction reason.
{% enddocs %}

{% docs column_written_premium_revenue_amount %}
Numeric, additive fact representing the premium revenue written (sold) in this period.
{% enddocs %}

{% docs column_written_premium_revenue_dollar_amount %}
Numeric fact representing the total premium revenue written (sold) for this period.
{% enddocs %}

{% docs column_year %}
The calendar year.
{% enddocs %}

{% docs column_zip_code %}
The postal code.
{% enddocs %}


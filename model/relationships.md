# Relationships

| From | To | Cardinality | Active |
|------|----|-------------|--------|
| fact_budget[JobId] | dim_job[JobId] | Many:1 | Yes |
| fact_actuals[JobId] | dim_job[JobId] | Many:1 | Yes |
| fact_ar_aging[JobId] | dim_job[JobId] | Many:1 | Yes |
| fact_change_orders[JobId] | dim_job[JobId] | Many:1 | Yes |
| fact_wip[JobId] | dim_job[JobId] | Many:1 | Yes |
| fact_labour[JobId] | dim_job[JobId] | Many:1 | Yes |

### Recommended date handling

Create `dim_date` (calendar) and relate:

- fact_budget[Period] → dim_date[Date] (month-start dates in sample)
- fact_actuals[Period] → dim_date[Date]
- fact_labour[WorkDate] → dim_date[Date] (inactive or separate role-playing tables if needed)

Keep WIP as a **snapshot** fact filtered to latest AsOfDate.

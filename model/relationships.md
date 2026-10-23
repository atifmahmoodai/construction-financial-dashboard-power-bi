# Relationships

| From | To | Card | Filter | Active |
|------|----|------|--------|--------|
| fact_actuals[JobKey] | dim_job[JobKey] | *∶1 | Single | Y |
| fact_actuals[CostCodeKey] | dim_cost_code[CostCodeKey] | *∶1 | Single | Y |
| fact_actuals[TxnDateKey] | dim_date[DateKey] | *∶1 | Single | Y |
| fact_budget[JobKey] | dim_job[JobKey] | *∶1 | Single | Y |
| fact_budget[CostCodeKey] | dim_cost_code[CostCodeKey] | *∶1 | Single | Y |
| fact_labour[JobKey] | dim_job[JobKey] | *∶1 | Single | Y |
| fact_labour[WorkDateKey] | dim_date[DateKey] | *∶1 | Single | Y |
| fact_change_orders[JobKey] | dim_job[JobKey] | *∶1 | Single | Y |
| fact_wip[JobKey] | dim_job[JobKey] | *∶1 | Single | Y |
| fact_wip[PeriodDateKey] | dim_date[DateKey] | *∶1 | Single | Y |
| fact_ar_aging[JobKey] | dim_job[JobKey] | *∶1 | Single | Y |
| dim_job[EntityKey] | dim_entity[EntityKey] | *∶1 | Single | Y |

Avoid bidirectional job↔actuals. Filter budget version in measures, not with bi-di.

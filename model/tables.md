# Model tables — construction financials

## dim_job (grain: one construction job)

JobId, JobName, ClientName, JobType, Status, ContractValue, StartDate, EstEndDate, PercentComplete, PM.

## fact_budget (grain: Job × Period month × Category)

BudgetAmount for Labour, Materials, Subcontractors, Equipment, Overhead.

## fact_actuals (grain: Job × Period month × Category)

ActualAmount with Source = QBO-style export.

## fact_ar_aging (grain: one invoice)

Amount, AmountPaid, DaysOutstanding, AgingBucket (Current / 31-60 / 61-90 / 90+).

## fact_change_orders (grain: one CO)

ApprovedAmount (can be negative), Status, ApprovedDate.

## fact_wip (grain: one job as-of snapshot)

ContractValue, PercentComplete, CostToDate, BilledToDate, EarnedRevenue, OverUnderBilling, BacklogRemaining.

## fact_labour (grain: one timesheet line)

Craft, Hours, HourlyRate, EmployeeId, WorkDate.

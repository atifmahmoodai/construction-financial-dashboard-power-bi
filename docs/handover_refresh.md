# Owner-friendly handover & refresh

## Monthly refresh (Import)

1. Export actuals from accounting (QBO / Xero / etc.) to CSV matching `fact_actuals` columns.  
2. Update budget workbook → save CSV to `fact_budget` shape.  
3. Drop files into the OneDrive / SharePoint folder connected to the dataset (or refresh local Desktop then publish).  
4. In Power BI Service: open the workspace → dataset → **Refresh now**.  
5. Open the app and check: Budget vs Actual tile, WIP backlog, AR 90+.

## What owners should glance at after refresh

| Check | Healthy signal |
|-------|----------------|
| Budget vs Actual Var % | Within agreed tolerance (e.g. ±10%) |
| Over/Under billing | Not persistently large under-billing |
| AR 90+ | Stable or declining |
| Labour cost per job | No unexplained spikes |

## Page map

- **Company** — portfolio P&L / cash proxies  
- **Construction** — job drill-through  
- **Labour** — craft mix and cost  

## Contacts

Finance owner · PM lead · BI maintainer (portfolio demo — replace with real names)

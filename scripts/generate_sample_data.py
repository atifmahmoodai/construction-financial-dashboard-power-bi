#!/usr/bin/env python3
"""Regenerate construction financial sample CSVs (deterministic)."""
import csv, random
from datetime import datetime, timedelta
from pathlib import Path
random.seed(42)
OUT = Path(__file__).resolve().parents[1] / "data" / "sample"

def write_csv(path, rows, fields):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    print(path.name, len(rows))

jobs = []
for i in range(1, 31):
    start_j = datetime(2024, 1, 1) + timedelta(days=random.randint(0, 400))
    contract = round(random.uniform(120000, 4500000), 2)
    jobs.append({
        "JobId": f"JOB{i:03d}", "JobName": f"Project {chr(64+((i-1)%26)+1)}-{i}",
        "ClientName": f"Client {random.choice(['Alpha','Beta','Gamma','Delta','Omega'])} {i}",
        "JobType": random.choice(["Residential", "Commercial", "Infrastructure", "Renovation"]),
        "Status": random.choice(["Active", "Active", "Active", "Complete", "On Hold"]),
        "ContractValue": contract, "StartDate": start_j.strftime("%Y-%m-%d"),
        "EstEndDate": (start_j + timedelta(days=random.randint(90, 540))).strftime("%Y-%m-%d"),
        "PercentComplete": round(random.uniform(0.05, 1.0), 2),
        "PM": random.choice(["S. Khan", "A. Patel", "J. Rivera", "M. Chen", "L. Okonkwo"]),
    })
write_csv(OUT/"dim_job.csv", jobs,
    ["JobId","JobName","ClientName","JobType","Status","ContractValue","StartDate","EstEndDate","PercentComplete","PM"])

categories = ["Labour", "Materials", "Subcontractors", "Equipment", "Overhead"]
budget_rows, actual_rows = [], []
for job in jobs:
    for m in range(1, 13):
        for cat in categories:
            bud = round(job["ContractValue"] * random.uniform(0.008, 0.035), 2)
            ym = f"2025-{m:02d}-01"
            budget_rows.append({"JobId": job["JobId"], "Period": ym, "Category": cat, "BudgetAmount": bud})
            actual_rows.append({"JobId": job["JobId"], "Period": ym, "Category": cat,
                "ActualAmount": round(bud * random.uniform(0.75, 1.25), 2), "Source": "QBO-style export"})
write_csv(OUT/"fact_budget.csv", budget_rows, ["JobId","Period","Category","BudgetAmount"])
write_csv(OUT/"fact_actuals.csv", actual_rows, ["JobId","Period","Category","ActualAmount","Source"])

ar = []
for i in range(1, 81):
    job = random.choice(jobs)
    inv_dt = datetime(2025, 1, 1) + timedelta(days=random.randint(0, 280))
    amount = round(random.uniform(5000, 180000), 2)
    days_out = random.choice([15, 25, 40, 55, 75, 95, 120])
    bucket = ("Current" if days_out <= 30 else "31-60" if days_out <= 60
              else "61-90" if days_out <= 90 else "90+")
    ar.append({"InvoiceId": f"INV{i:04d}", "JobId": job["JobId"],
        "InvoiceDate": inv_dt.strftime("%Y-%m-%d"),
        "DueDate": (inv_dt + timedelta(days=30)).strftime("%Y-%m-%d"),
        "Amount": amount, "AmountPaid": round(amount * random.choice([0, 0, 0.5, 1.0, 1.0]), 2),
        "DaysOutstanding": days_out, "AgingBucket": bucket})
write_csv(OUT/"fact_ar_aging.csv", ar,
    ["InvoiceId","JobId","InvoiceDate","DueDate","Amount","AmountPaid","DaysOutstanding","AgingBucket"])

cos = [{"ChangeOrderId": f"CO{i:03d}", "JobId": random.choice(jobs)["JobId"],
    "Description": f"Scope change {i}", "ApprovedAmount": round(random.uniform(-15000, 120000), 2),
    "Status": random.choice(["Approved", "Approved", "Pending", "Rejected"]),
    "ApprovedDate": (datetime(2025,1,1)+timedelta(days=random.randint(0,280))).strftime("%Y-%m-%d")}
    for i in range(1, 61)]
write_csv(OUT/"fact_change_orders.csv", cos,
    ["ChangeOrderId","JobId","Description","ApprovedAmount","Status","ApprovedDate"])

wip = []
for job in jobs:
    billed = round(job["ContractValue"] * job["PercentComplete"] * random.uniform(0.85, 1.05), 2)
    cost_to_date = round(job["ContractValue"] * job["PercentComplete"] * random.uniform(0.7, 0.95), 2)
    wip.append({"JobId": job["JobId"], "AsOfDate": "2025-10-01", "ContractValue": job["ContractValue"],
        "PercentComplete": job["PercentComplete"], "CostToDate": cost_to_date, "BilledToDate": billed,
        "EarnedRevenue": round(job["ContractValue"] * job["PercentComplete"], 2),
        "OverUnderBilling": round(billed - job["ContractValue"] * job["PercentComplete"], 2),
        "BacklogRemaining": round(job["ContractValue"] * (1 - job["PercentComplete"]), 2)})
write_csv(OUT/"fact_wip.csv", wip,
    ["JobId","AsOfDate","ContractValue","PercentComplete","CostToDate","BilledToDate","EarnedRevenue","OverUnderBilling","BacklogRemaining"])

labour = [{"LabourId": f"LAB{i:04d}", "JobId": random.choice(jobs)["JobId"],
    "WorkDate": (datetime(2025,1,1)+timedelta(days=random.randint(0,280))).strftime("%Y-%m-%d"),
    "Craft": random.choice(["Carpenter","Electrician","Labourer","Foreman","Plumber"]),
    "Hours": round(random.uniform(4,12),1), "HourlyRate": round(random.uniform(28,85),2),
    "EmployeeId": f"EMP{random.randint(1,40):03d}"} for i in range(1, 501)]
write_csv(OUT/"fact_labour.csv", labour,
    ["LabourId","JobId","WorkDate","Craft","Hours","HourlyRate","EmployeeId"])
print("Done.")

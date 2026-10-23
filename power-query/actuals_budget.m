// Merge budget + actuals for a unified variance table (optional pattern)
let
    Budget = Csv.Document(File.Contents("data/sample/fact_budget.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    BudgetH = Table.PromoteHeaders(Budget, [PromoteAllScalars=true]),
    BudgetT = Table.TransformColumnTypes(BudgetH, {
        {"JobId", type text}, {"Period", type date}, {"Category", type text}, {"BudgetAmount", type number}
    }),
    Actual = Csv.Document(File.Contents("data/sample/fact_actuals.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    ActualH = Table.PromoteHeaders(Actual, [PromoteAllScalars=true]),
    ActualT = Table.TransformColumnTypes(ActualH, {
        {"JobId", type text}, {"Period", type date}, {"Category", type text},
        {"ActualAmount", type number}, {"Source", type text}
    }),
    Merged = Table.NestedJoin(BudgetT, {"JobId","Period","Category"}, ActualT, {"JobId","Period","Category"}, "Act", JoinKind.LeftOuter),
    Expanded = Table.ExpandTableColumn(Merged, "Act", {"ActualAmount", "Source"}, {"ActualAmount", "Source"}),
    WithVar = Table.AddColumn(Expanded, "Variance", each [ActualAmount] - [BudgetAmount], type number)
in
    WithVar

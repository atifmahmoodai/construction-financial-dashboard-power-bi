// Labour fact typing + cost column
let
    Source = Csv.Document(File.Contents("data/sample/fact_labour.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promoted, {
        {"LabourId", type text}, {"JobId", type text}, {"WorkDate", type date},
        {"Craft", type text}, {"Hours", type number}, {"HourlyRate", type number},
        {"EmployeeId", type text}
    }),
    AddCost = Table.AddColumn(Typed, "LineCost", each [Hours] * [HourlyRate], type number)
in
    AddCost

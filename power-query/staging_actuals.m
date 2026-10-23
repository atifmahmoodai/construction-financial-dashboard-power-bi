let
    Source = Csv.Document(File.Contents(pSourcePath & "/fact_actuals.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Promote = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promote,{{"ActualKey",Int64.Type},{"JobKey",Int64.Type},{"CostCodeKey",Int64.Type},{"TxnDateKey",Int64.Type},{"ActualAmount",type number},{"IsCommitted",Int64.Type}}),
    RowHash = Table.AddColumn(Typed,"RowHash",each Text.Combine({Text.From([ActualKey]),Text.From([ActualAmount])}),type text)
in RowHash // Load OFF

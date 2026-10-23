let
    Source = Csv.Document(File.Contents(pSourcePath & "/dim_job.csv"),[Delimiter=",",Encoding=65001,QuoteStyle=QuoteStyle.Csv]),
    Promote = Table.PromoteHeaders(Source,[PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(Promote,{{"JobKey",Int64.Type},{"EntityKey",Int64.Type},{"ContractValue",type number}})
in Typed

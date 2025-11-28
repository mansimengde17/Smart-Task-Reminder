let
    // Update this relative path to point at your local repo copy if needed
    FilePath = "./data/Interruptions.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",", Columns=5, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"InterruptionID", type text},
            {"SessionID", type text},
            {"Category", type text},
            {"StartDT", type datetime},
            {"DurationMin", Int64.Type}
        }
    ),
    NonNegative = Table.TransformColumns(Typed, {{"DurationMin", each Number.Max(_, 0), Int64.Type}})
    // Note: SessionID integrity is enforced in the model by relating to Sessions
in
    NonNegative

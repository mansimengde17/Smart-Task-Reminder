let
    // Update the path if your repo lives elsewhere
    FilePath = "./data/Sessions.csv",
    Source = Csv.Document(File.Contents(FilePath),[Delimiter=",", Columns=10, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    Typed = Table.TransformColumnTypes(
        PromotedHeaders,
        {
            {"SessionID", type text},
            {"UserID", type text},
            {"Date", type date},
            {"StartTime", type time},
            {"EndTime", type time},
            {"DurationMin", Int64.Type},
            {"CompletedCount", Int64.Type},
            {"AbandonedCount", Int64.Type},
            {"TabSwitchCount", Int64.Type},
            {"TaskType", type text}
        }
    ),
    FillDuration = Table.AddColumn(
        Typed,
        "DurationComputed",
        each if [DurationMin] = null or [DurationMin] = 0 then Duration.Minutes([EndTime] - [StartTime]) else [DurationMin],
        Int64.Type
    ),
    DroppedDuration = Table.RemoveColumns(FillDuration, {"DurationMin"}),
    DurationFinal = Table.RenameColumns(DroppedDuration, {{"DurationComputed", "DurationMin"}}),
    StandardTask = Table.TransformColumns(DurationFinal, {{"TaskType", each Text.Proper(Text.Trim(_)), type text}})
in
    StandardTask

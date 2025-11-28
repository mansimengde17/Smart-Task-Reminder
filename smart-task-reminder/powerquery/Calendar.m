let
    // UC3.1: VEVENT blocks become Busy windows that line up with Sessions by Date/Time
    FilePath = "./data/Calendar.ics",
    RawText = Text.FromBinary(File.Contents(FilePath), TextEncoding.Utf8),
    EventBlocks = List.Skip(Text.Split(RawText, "BEGIN:VEVENT"), 1),
    ToTable = Table.FromList(EventBlocks, Splitter.SplitByNothing(), {"EventText"}),
    Trimmed = Table.TransformColumns(ToTable, {{"EventText", each Text.BeforeDelimiter(_, "END:VEVENT", 1), type text}}),
    Extracted = Table.AddColumn(
        Trimmed,
        "Parsed",
        each [
            DTSTART = Text.Trim(Text.BetweenDelimiters([EventText], "DTSTART:", "#(lf)")),
            DTEND = Text.Trim(Text.BetweenDelimiters([EventText], "DTEND:", "#(lf)")),
            SUMMARY = Text.Trim(Text.BetweenDelimiters([EventText], "SUMMARY:", "#(lf)")),
            DESCRIPTION = Text.Trim(Text.BetweenDelimiters([EventText], "DESCRIPTION:", "#(lf)"))
        ]
    ),
    Expanded = Table.ExpandRecordColumn(Extracted, "Parsed", {"DTSTART", "DTEND", "SUMMARY", "DESCRIPTION"}),
    Typed = Table.TransformColumnTypes(
        Expanded,
        {
            {"DTSTART", type datetimezone},
            {"DTEND", type datetimezone},
            {"SUMMARY", type text},
            {"DESCRIPTION", type text}
        }
    ),
    ToUtc = Table.TransformColumns(Typed, {{"DTSTART", DateTimeZone.ToUtc}, {"DTEND", DateTimeZone.ToUtc}}),
    AsLocal = Table.TransformColumns(ToUtc, {{"DTSTART", DateTimeZone.RemoveZone, type datetime}, {"DTEND", DateTimeZone.RemoveZone, type datetime}}),
    WithDuration = Table.AddColumn(AsLocal, "DurationMin", each Duration.TotalMinutes([DTEND] - [DTSTART]), type number),
    WithStatus = Table.AddColumn(WithDuration, "Status", each if [DurationMin] > 0 then "Busy" else "Free", type text)
in
    WithStatus

[StagingDefinition = [Kind = "FastCopy"]]
section Section1;
shared #"departments csv" = let
  Source = Lakehouse.Contents([HierarchicalNavigation = null, EnableVorder = true, OutputMetadataRefresh = true]),
  #"Navigation 1" = Source{[workspaceId = "c8a28174-0838-4802-87c4-fd773d95207b"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "e65a43b2-b89c-4d57-b796-b9f2946506f7"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "Files", ItemKind = "Folder"]}[Data],
  #"Navigation 4" = #"Navigation 3"{[Name = "dp700_data"]}[Content],
  #"Navigation 5" = #"Navigation 4"{[Name = "departments.csv"]}[Content],
  #"Imported CSV" = Csv.Document(#"Navigation 5", [Delimiter = ",", Columns = 4, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"department_id", Int64.Type}, {"department_name", type text}, {"manager", type text}, {"location", type text}})
in
  #"Changed column type";
shared #"employees csv" = let
  Source = Lakehouse.Contents([HierarchicalNavigation = null, EnableVorder = true, OutputMetadataRefresh = true]),
  #"Navigation 1" = Source{[workspaceId = "c8a28174-0838-4802-87c4-fd773d95207b"]}[Data],
  #"Navigation 2" = #"Navigation 1"{[lakehouseId = "e65a43b2-b89c-4d57-b796-b9f2946506f7"]}[Data],
  #"Navigation 3" = #"Navigation 2"{[Id = "Files", ItemKind = "Folder"]}[Data],
  #"Navigation 4" = #"Navigation 3"{[Name = "dp700_data"]}[Content],
  #"Navigation 5" = #"Navigation 4"{[Name = "employees.csv"]}[Content],
  #"Imported CSV" = Csv.Document(#"Navigation 5", [Delimiter = ",", Columns = 5, QuoteStyle = QuoteStyle.None]),
  #"Promoted headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars = true]),
  #"Changed column type" = Table.TransformColumnTypes(#"Promoted headers", {{"employee_id", Int64.Type}, {"name", type text}, {"department_id", Int64.Type}, {"hire_date", type date}, {"salary", Int64.Type}})
in
  #"Changed column type";
[DataDestinations = {[Definition = [Kind = "Reference", QueryName = "Merge_DataDestination", IsNewTarget = true], Settings = [Kind = "Automatic", TypeSettings = [Kind = "Table"]]]}]
shared Merge = let
  Source = Table.NestedJoin(#"employees csv", {"department_id"}, #"departments csv", {"department_id"}, "departments csv", JoinKind.LeftOuter),
  #"Expanded departments csv" = Table.ExpandTableColumn(Source, "departments csv", {"department_name", "manager", "location"}, {"department_name", "manager", "location"}),
  #"Split column by delimiter" = Table.SplitColumn(#"Expanded departments csv", "name", Splitter.SplitTextByDelimiter(" "), {"first_name", "last_name"}),
  #"Choose columns" = Table.SelectColumns(#"Split column by delimiter", {"employee_id", "first_name", "last_name", "department_name", "location"})
in
  #"Choose columns";
shared Merge_DataDestination = let
  Pattern = Lakehouse.Contents([CreateNavigationProperties = false, EnableFolding = false, HierarchicalNavigation = true, EnableVorder = true, OutputMetadataRefresh = true]),
  Navigation_1 = Pattern{[workspaceId = "c8a28174-0838-4802-87c4-fd773d95207b"]}[Data],
  Navigation_2 = Navigation_1{[lakehouseId = "e65a43b2-b89c-4d57-b796-b9f2946506f7"]}[Data],
  Navigation_3 = Navigation_2{[Id = "dp700_data", ItemKind = "Schema"]}[Data],
  TableNavigation = Navigation_3{[Id = "dp700_data_person", ItemKind = "Table"]}?[Data]?
in
  TableNavigation;

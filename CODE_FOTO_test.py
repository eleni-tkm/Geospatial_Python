import arcpy

# Set workspace
arcpy.env.workspace = r'blah\blah\blah.shp'

# Set feature class name
feature_class = 'theNameOfFeatureClassInGDB'


# Task 2: Keep a list called 'initial_fields' with the names of the fields of the feature class 'subFOTOSHMEIA_SP_working'
initial_fields = [field.name for field in arcpy.ListFields(feature_class)]

# Task 3: Perform Spatial join
join_features = r'blah\blah\blah2.shp'
output_feature_class = 'theNameOfFeatureClassInGDB_ToSaveResults'


arcpy.SpatialJoin_analysis(feature_class, join_features, output_feature_class)

# Task 4: Open field calculator and copy values
arcpy.CalculateField_management(output_feature_class, 'CODE_FOTO', '!kwdikos!', 'PYTHON')

fields_to_delete = [field.name for field in arcpy.ListFields(output_feature_class) if field.name not in initial_fields]


arcpy.DeleteField_management(output_feature_class, fields_to_delete)
print("Script executed successfully.")


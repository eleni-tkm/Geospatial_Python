import arcpy

# Set workspace
arcpy.env.workspace = r'blah\blah\BLAH.gdb'

# Task 1: Take the feature class 'nameOfFeatureClass' by setting the feature_class name
feature_class = 'nameOfFeatureClass'


# Task 2: Keep a list called 'initial_fields' with the names of the fields of the feature class 'nameOfFeatureClass'
initial_fields = [field.name for field in arcpy.ListFields(feature_class)]

# Task 3: Perform Spatial join
join_features = r'blah\blah\BLAH.shp'
output_feature_class = 'nameOfFeatureClass_Joined'


arcpy.SpatialJoin_analysis(feature_class, join_features, output_feature_class) #bydefault one-to-one and intersects

# Task 4: Open field calculator and copy values
arcpy.CalculateField_management(output_feature_class, 'CODE_FOTO', '!kwdikos!', 'PYTHON')

fields_to_delete = [field.name for field in arcpy.ListFields(output_feature_class) if field.name not in initial_fields]

#clean your workspace
arcpy.DeleteField_management(output_feature_class, fields_to_delete)
#print("Script executed successfully.")


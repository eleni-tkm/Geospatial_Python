import arcpy

# Set workspace
arcpy.env.workspace = r'\\SERVER\kartECO SHARED\Temporary\eleni_data\k196\3h_Tmhmatiki\01_SAP_subFot_SP.gdb'

# Set feature class name
feature_class = 'subFOTOSHMEIA_SP_working'

# Task 1: Take the feature class 'subFOTOSHMEIA_SP_working'
# Task 2: Keep a list called 'initial_fields' with the names of the fields of the feature class 'subFOTOSHMEIA_SP_working'
initial_fields = [field.name for field in arcpy.ListFields(feature_class)]

# Task 3: Perform Spatial join
join_features = r'\\SERVER\kartECO SHARED\Projects\Dimosio\K196 - Apografi Daswn\Working_files\Data_Help_Photos\Data\YPOERGO_8\01_DATA\02_PERIGRAMMA_FOTOSHMEIOU\YPXSX00_FOT_ypoergo_8.shp'
output_feature_class = 'subFOTOSHMEIA_SP_working_Joined2'


arcpy.SpatialJoin_analysis(feature_class, join_features, output_feature_class)

# Task 4: Open field calculator and copy values
arcpy.CalculateField_management(output_feature_class, 'CODE_FOTO', '!kwdikos!', 'PYTHON')

fields_to_delete = [field.name for field in arcpy.ListFields(output_feature_class) if field.name not in initial_fields]


arcpy.DeleteField_management(output_feature_class, fields_to_delete)
print("Script executed successfully.")


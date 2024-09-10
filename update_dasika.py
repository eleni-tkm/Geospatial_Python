import arcpy

# Set the workspace
workspace = r'blah\Data\blah\aVEGETATIONmap.gdb'
arcpy.env.workspace = workspace

# Task 1
expression = """ "VEG_TYPE" IN (6, 7, 8, 9, 10) """
arcpy.Select_analysis("SP02_Veg_Map_final", "mh_dasika", expression)

# Task 2
expression = """ "VEG_TYPE" IN (1, 2, 3, 4, 5) """
arcpy.Select_analysis("SP02_Veg_Map_final", "dasika", expression)

# Task 3
arcpy.CalculateField_management("dasika", "EFLEKTOTITA", 0, "PYTHON")

# Task 4
arcpy.Buffer_analysis("dasika", "dasika_buffer100", "100 Meters")

# Task 5
#arcpy.Merge_management(["mh_dasika", "dasika_buffer100"], "dasika_buffer_mh_dasika")

# Task 6
arcpy.Intersect_analysis(["dasika_buffer100", "mh_dasika"], "overlapping_areas")

# Make EFLEKTOTITA=1 in mh_dasika of VEG_MAP
# Make a copy of SP02_Veg_Map_Diss
input_feature_class = "SP02_Veg_Map_final"
output_feature_class_copy = "SP02_Veg_Map_final_copy"
arcpy.Copy_management(input_feature_class, output_feature_class_copy)

# Save the copy as a new feature class
temp_layer = "temp_layer"
arcpy.MakeFeatureLayer_management(output_feature_class_copy, temp_layer)

expression = """ "VEG_TYPE" IN (6, 7, 8, 9, 10) """

# Use a cursor to select features
with arcpy.da.UpdateCursor(temp_layer, ["EFLEKTOTITA"], where_clause=expression) as cursor:
    for row in cursor:
        row[0] = 1
        cursor.updateRow(row)

# Save the temporary layer as a new feature class
output_feature_class = "SP02_Veg_Map_final_copy_updated"
arcpy.FeatureClassToFeatureClass_conversion(temp_layer, workspace, output_feature_class)


# Task 8
#Update Veg_Map_Diss_copy_updated" with update features:overlapping areas and name it 'Veg_Map_Diss_copy_updated_overlapping_areas'
#dissolve the'Veg_Map_Diss_copy_updated_overlapping_areas' and name it'Veg_Map_Diss_copy_updated_overlapping_areas_DISS'

#str( !VEG_TYPE! )+'_'+'VEG_TYPE'



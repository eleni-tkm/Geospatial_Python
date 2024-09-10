import arcpy
import os


# Define input shapefiles
shapefileAa = arcpy.GetParameterAsText(0)
shapefileBb = arcpy.GetParameterAsText(1)

output_folder = arcpy.GetParameterAsText(2)
result_name = arcpy.GetParameterAsText(3) + 'PosEdaf.shp'

shapefileA = os.path.join(output_folder, 'shapefileA.shp')
shapefileB = os.path.join(output_folder, 'shapefileB.shp')

arcpy.management.CopyFeatures(shapefileAa, shapefileA)
arcpy.management.CopyFeatures(shapefileBb, shapefileB)



# Allow time for the system to release any locks
time.sleep(2)

# Clear workspace cache to release locks
arcpy.ClearWorkspaceCache_management()

            
#CAT_EDAF
arcpy.AddField_management(shapefileA, 'POS_EDAFb', 'LONG')
arcpy.CalculateField_management(shapefileA, 'POS_EDAFb', '!POS_EDAF!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'POS_EDAF')




# Define output names
shpA_bound = os.path.join(output_folder, "shpA_bound.shp")
shpB_bound = os.path.join(output_folder, "shpB_bound.shp")
shp_A_B_intersJoin = os.path.join(output_folder, "shp_A_B_intersJoin.shp")


# Create feature layers for shapefiles
arcpy.MakeFeatureLayer_management(shapefileA, "shapefileA_lyr")
arcpy.MakeFeatureLayer_management(shapefileB, "shapefileB_lyr")

# Step 1: SELECT BY LOCATION polygons from shapefileA that share a line with polygons from shapefileB
arcpy.SelectLayerByLocation_management("shapefileA_lyr", "BOUNDARY_TOUCHES", "shapefileB_lyr")
arcpy.CopyFeatures_management("shapefileA_lyr", shpA_bound)

# Step 2: SELECT BY LOCATION polygons from shapefileB that intersect the polygons of shpA_bound.shp
arcpy.MakeFeatureLayer_management(shpA_bound, "shpA_bound_lyr")
arcpy.SelectLayerByLocation_management("shapefileB_lyr", "INTERSECT", "shpA_bound_lyr")
arcpy.CopyFeatures_management("shapefileB_lyr", shpB_bound)



missmatched_posedaf = os.path.join(output_folder, result_name)


arcpy.SpatialJoin_analysis(shpB_bound, shpA_bound, shp_A_B_intersJoin, join_operation="JOIN_ONE_TO_MANY", match_option="SHARE_A_LINE_SEGMENT_WITH")

# Define the query to select features where JOIN_FID = -1
query = '"JOIN_FID" = -1'

# Start an edit session to enable row deletion
with arcpy.da.UpdateCursor(shp_A_B_intersJoin, ["JOIN_FID"], where_clause=query) as cursor:
    for row in cursor:
        cursor.deleteRow()  # Delete the row if the condition is met


arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_posedaf, "POS_EDAF <> POS_EDAFb" )
arcpy.AddField_management(missmatched_posedaf, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_posedaf, 'WHY', '"POS_EDAF NOT EQUAL"' , "PYTHON_9.3")



deleteFiles=[shp_A_B_intersJoin, shapefileA,shapefileB, shpA_bound, shpB_bound]

for shp in deleteFiles:
    arcpy.Delete_management(shp)


fields = arcpy.ListFields(os.path.join(output_folder, result_name))
fields_list=[]

for field in fields:
    fields_list.append(field.name)
    
for a in fields_list:
    if a not in ['WHY', 'FID', 'Shape']:
        arcpy.management.DeleteField(os.path.join(output_folder, result_name), a)
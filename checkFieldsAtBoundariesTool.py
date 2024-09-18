import arcpy
import os


# let the user define the inputs
shapefileAa = arcpy.GetParameterAsText(0)
shapefileBb = arcpy.GetParameterAsText(1)

output_folder = arcpy.GetParameterAsText(2)
result_name = arcpy.GetParameterAsText(3) + '.shp'

shapefileA = os.path.join(output_folder, 'shapefileA.shp')
shapefileB = os.path.join(output_folder, 'shapefileB.shp')

arcpy.management.CopyFeatures(shapefileAa, shapefileA)
arcpy.management.CopyFeatures(shapefileBb, shapefileB)



# Allow time for the system to release any locks
time.sleep(2)

# Clear workspace cache to release locks
arcpy.ClearWorkspaceCache_management()
#Rename fields just to be sure that you won't have any problems in the spatial join
#this is becasue in my case the shapefiles that I want to compare have the same names for the fields
#it is a painfull process though at least for the version of arcmap that I am using...
#renaming......          
#CAT_EDAF
arcpy.AddField_management(shapefileA, 'CAT_EDAFb', 'TEXT', field_length=2)
arcpy.CalculateField_management(shapefileA, 'CAT_EDAFb', '!CAT_EDAF!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'CAT_EDAF')

#CAT_ID
arcpy.AddField_management(shapefileA, 'CAT_IDb', 'TEXT', field_length=8)
arcpy.CalculateField_management(shapefileA, 'CAT_IDb', '!CAT_ID!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'CAT_ID')

# Reorder ORIZ_DOMI
arcpy.AddField_management(shapefileA, 'ORIZ_DOMIb', 'TEXT', field_length=8)
arcpy.CalculateField_management(shapefileA, 'ORIZ_DOMIb', '!ORIZ_DOMI!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'ORIZ_DOMI')


#EIDOS1
arcpy.AddField_management(shapefileA, 'EIDOS1b', 'TEXT', field_length=6)
arcpy.CalculateField_management(shapefileA, 'EIDOS1b', '!EIDOS1!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'EIDOS1')

#POSOSTO1
arcpy.AddField_management(shapefileA, 'POSOSTO1b', 'DOUBLE')
arcpy.CalculateField_management(shapefileA, 'POSOSTO1b', '!POSOSTO1!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'POSOSTO1')

#EIDOS2
arcpy.AddField_management(shapefileA, 'EIDOS2b', 'TEXT', field_length=6)
arcpy.CalculateField_management(shapefileA, 'EIDOS2b', '!EIDOS2!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'EIDOS2')

#POSOSTO2
arcpy.AddField_management(shapefileA, 'POSOSTO2b', 'DOUBLE')
arcpy.CalculateField_management(shapefileA, 'POSOSTO2b', '!POSOSTO2!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'POSOSTO2')


#EIDOS3
arcpy.AddField_management(shapefileA, 'EIDOS3b', 'TEXT', field_length=6)
arcpy.CalculateField_management(shapefileA, 'EIDOS3b', '!EIDOS3!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'EIDOS3')

#POSOSTO3
arcpy.AddField_management(shapefileA, 'POSOSTO3b', 'DOUBLE')
arcpy.CalculateField_management(shapefileA, 'POSOSTO3b', '!POSOSTO3!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'POSOSTO3')


#CAT_O2
arcpy.AddField_management(shapefileA, 'CAT_O2b', 'TEXT', field_length=4)
arcpy.CalculateField_management(shapefileA, 'CAT_O2b', '!CAT_O2!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'CAT_O2')

#TYPOSDAS
arcpy.AddField_management(shapefileA, 'TYPOSDASb', 'TEXT', field_length=8)
arcpy.CalculateField_management(shapefileA, 'TYPOSDASb', '!TYPOSDAS!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'TYPOSDAS')


#OTHEREIDOS
arcpy.AddField_management(shapefileA, 'OTHEREIDSb', 'TEXT', field_length=250)
arcpy.CalculateField_management(shapefileA, 'OTHEREIDSb', '!OTHEREIDOS!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'OTHEREIDOS')


#MESOYPSOS
arcpy.DeleteField_management(shapefileA, 'MESOYPSOS')
arcpy.DeleteField_management(shapefileB, 'MESOYPSOS')


#TDASOSEIS
arcpy.AddField_management(shapefileA, 'TDASOSEISb', 'TEXT', field_length=20)
arcpy.CalculateField_management(shapefileA, 'TDASOSEISb', '!TDASOSEIS!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'TDASOSEIS')


#MESOYPSOS_
arcpy.AddField_management(shapefileA, 'MESOYPSOSb', 'DOUBLE')
arcpy.CalculateField_management(shapefileA, 'MESOYPSOSb', '!MESOYPSOS_!', 'PYTHON')
arcpy.DeleteField_management(shapefileA, 'MESOYPSOS_')


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



missmatched_CATEDAF = os.path.join(output_folder,"missmatched_CATEDAF.shp")
missmatched_CATID = os.path.join(output_folder,"missmatched_CATID.shp")
missmatched_ORIZ_DOMI = os.path.join(output_folder, "missmatched_ORIZ_DOMI.shp")
missmatched_EIDOS1 = os.path.join(output_folder, "missmatched_EIDOS1.shp")
missmatched_POSOSTO1 = os.path.join(output_folder, "missmatched_POSOSTO1.shp")
missmatched_EIDOS2 = os.path.join(output_folder, "missmatched_EIDOS2.shp")
missmatched_POSOSTO2= os.path.join(output_folder, "missmatched_POSOSTO2.shp")
missmatched_EIDOS3=os.path.join(output_folder,"missmatched_EIDOS3.shp")
missmatched_POSOSTO3=os.path.join(output_folder,"missmatched_POSOSTO3.shp")
missmatched_CATO2=os.path.join(output_folder,"missmatched_CATO2.shp")
missmatched_TYPOSDAS=os.path.join(output_folder,"missmatched_TYPDAS.shp")
missmatched_OTHEREIDOS=os.path.join(output_folder,"missmatched_OTHEREIDOS.shp")
missmatched_TDASOSEIS=os.path.join(output_folder,"missmatched_TDASOSEIS.shp")
missmatched_MESOYPSOS=os.path.join(output_folder,"missmatched_MESOYPSOS.shp")

arcpy.SpatialJoin_analysis(shpB_bound, shpA_bound, shp_A_B_intersJoin, join_operation="JOIN_ONE_TO_MANY", match_option="SHARE_A_LINE_SEGMENT_WITH")

# Define the query to select features where JOIN_FID = -1 - this means that there is no matching polygon for the target polygon that actually shares a line segmant with the inputs. That is why i want to ignore -by deleting-
#these values
query = '"JOIN_FID" = -1'

# this is how you start an edit session to enable row deletion
with arcpy.da.UpdateCursor(shp_A_B_intersJoin, ["JOIN_FID"], where_clause=query) as cursor:
    for row in cursor:
        cursor.deleteRow()  # Delete the row if the condition is met


arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_CATEDAF, "CAT_EDAF <> CAT_EDAFb" )
arcpy.AddField_management(missmatched_CATEDAF, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_CATEDAF, 'WHY', '"CAT_EDAF NOT EQUAL"' , "PYTHON_9.3")

              
arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_CATID, "CAT_ID <> CAT_IDb" )
arcpy.AddField_management(missmatched_CATID, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_CATID, 'WHY', '"CAT_ID NOT EQUAL"', "PYTHON_9.3")


arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_ORIZ_DOMI, "ORIZ_DOMI <> ORIZ_DOMIb" )
arcpy.AddField_management(missmatched_ORIZ_DOMI, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_ORIZ_DOMI, 'WHY', '"ORIZ_DOMI NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_EIDOS1, "EIDOS1 <> EIDOS1b" )
arcpy.AddField_management(missmatched_EIDOS1, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_EIDOS1, 'WHY', '"EIDOS1 IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_POSOSTO1, "POSOSTO1 <> POSOSTO1b" )
arcpy.AddField_management(missmatched_POSOSTO1, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_POSOSTO1, 'WHY', '"POS1 IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_EIDOS2, "EIDOS2 <> EIDOS2b" )
arcpy.AddField_management(missmatched_EIDOS2, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_EIDOS2, 'WHY', '"EIDOS2 IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_POSOSTO2, "POSOSTO2 <> POSOSTO2b" )
arcpy.AddField_management(missmatched_POSOSTO2, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_POSOSTO2, 'WHY', '"POS2 IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_EIDOS3, "EIDOS3 <> EIDOS3b" )
arcpy.AddField_management(missmatched_EIDOS3, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_EIDOS3, 'WHY', '"EIDOS3 IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_POSOSTO3, "POSOSTO3 <> POSOSTO3b" )
arcpy.AddField_management(missmatched_POSOSTO3, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_POSOSTO3, 'WHY', '"POS3 IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_CATO2, "CAT_O2 <> CAT_O2b" )
arcpy.AddField_management(missmatched_CATO2, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_CATO2, 'WHY', '"CATO2 IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_TYPOSDAS, "TYPOSDAS <> TYPOSDASb" )
arcpy.AddField_management(missmatched_TYPOSDAS, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_TYPOSDAS, 'WHY', '"TYPOSDAS IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_OTHEREIDOS, "OTHEREIDOS <> OTHEREIDSb" )
arcpy.AddField_management(missmatched_OTHEREIDOS, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_OTHEREIDOS, 'WHY', '"OTHEREIDOS IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_TDASOSEIS, "TDASOSEIS <> TDASOSEISb" )
arcpy.AddField_management(missmatched_TDASOSEIS, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_TDASOSEIS, 'WHY', '"TDASOSEIS IS NOT EQUAL"', "PYTHON_9.3")

arcpy.Select_analysis(shp_A_B_intersJoin, missmatched_MESOYPSOS, "MESOYPSOS_ <> MESOYPSOSb" )
arcpy.AddField_management(missmatched_MESOYPSOS, 'WHY', 'TEXT', field_length=200)
arcpy.management.CalculateField(missmatched_MESOYPSOS, 'WHY', '"MESOYPSOS_ IS NOT EQUAL"', "PYTHON_9.3")


mergedFiles=[missmatched_CATEDAF, missmatched_CATID, missmatched_ORIZ_DOMI, missmatched_EIDOS1, missmatched_POSOSTO1, missmatched_EIDOS2, missmatched_POSOSTO2, 
missmatched_EIDOS3, missmatched_POSOSTO3,missmatched_CATO2, missmatched_TYPOSDAS, missmatched_OTHEREIDOS, missmatched_TDASOSEIS,missmatched_MESOYPSOS]

arcpy.Merge_management(mergedFiles, os.path.join(output_folder, result_name))


deleteFiles=[shp_A_B_intersJoin, shapefileA,shapefileB, shpA_bound, shpB_bound, missmatched_CATEDAF, missmatched_CATID, missmatched_ORIZ_DOMI, missmatched_EIDOS1, missmatched_POSOSTO1, 
missmatched_EIDOS2, missmatched_POSOSTO2, missmatched_EIDOS3, missmatched_POSOSTO3,missmatched_CATO2, missmatched_TYPOSDAS, missmatched_OTHEREIDOS, missmatched_TDASOSEIS,missmatched_MESOYPSOS]

for shp in deleteFiles:
    arcpy.Delete_management(shp)


fields = arcpy.ListFields(os.path.join(output_folder, result_name))
fields_list=[]

for field in fields:
    fields_list.append(field.name)
    
for a in fields_list:
    if a not in ['WHY', 'FID', 'Shape']:
        arcpy.management.DeleteField(os.path.join(output_folder, result_name), a)

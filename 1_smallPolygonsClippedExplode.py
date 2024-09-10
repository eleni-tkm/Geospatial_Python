import arcpy
import os

# Set workspace
arcpy.env.workspace = r"\\SERVER\kartECO SHARED\Projects\Dimosio\K196 - Apografi Daswn\Working_files\Fwtoermhneia_Working\6_General\03Tmhmatikh_Paradosi\10_Telikes_vaseis\Malevisiou\Malevisiou_edaf.gdb"
cws = arcpy.env.workspace
# Input shapefile and feature class
dasikos_shp = r"\\192.168.1.5\kartECO SHARED\Projects\Dimosio\K196 - Apografi Daswn\Working_files\Plans_Annexes\3h_Tmhmatikh\5_Dasikos\DASIKOS_Krhth_Dissolve_tel.shp"
vegMap_feature_class = r"\\SERVER\kartECO SHARED\Projects\Dimosio\K196 - Apografi Daswn\Working_files\Fwtoermhneia_Working\6_General\03Tmhmatikh_Paradosi\10_Telikes_vaseis\Malevisiou\Old\maleviziou_edaf.shp"

# Output feature layers
dasikos_clipped = "dasikos_clipped"
dasikos_exploded = "dasikos_exploded"
dasikos_smallPolygons = "dasikos_smallPolygons"
vegMap_smallPolygons = "vegMap_smallPolygons"
vegMap_smallPolygons_notDas = "vegMap_smallPolygons_notDas"


fc_Delete=[dasikos_clipped, dasikos_smallPolygons, vegMap_smallPolygons]
# 1. Clip dasikos.shp to the boundaries of vegMapFeatureClass and save it as dasikos_clipped layer
arcpy.Clip_analysis(dasikos_shp, vegMap_feature_class, dasikos_clipped)

# 2. Explode multipart features in dasikos_clipped layer
arcpy.MultipartToSinglepart_management(dasikos_clipped, dasikos_exploded)

# 3. Choose the polygons from dasikos_clipped that are less than 15.000 square meters (Shape area)
arcpy.Select_analysis(dasikos_exploded, dasikos_smallPolygons, '"Shape_Area" < 15000')

# 4. Choose the polygons from vegMapFeatureClass feature class that are less than 15.000 square meters (Shape area)
arcpy.Select_analysis(vegMap_feature_class, vegMap_smallPolygons, '"AREA" < 15000')

# 5. From vegMap_smallPolygons layer find the polygons that are completely identical to dasikos_smallPolygons layer and then SWITCH selection
arcpy.SelectLayerByLocation_management(vegMap_smallPolygons, "ARE_IDENTICAL_TO", dasikos_smallPolygons)
arcpy.SelectLayerByAttribute_management(vegMap_smallPolygons, "SWITCH_SELECTION")

# 6. Save the output of the switched selection in vegMap_smallPolygons_notDas layer
arcpy.CopyFeatures_management(vegMap_smallPolygons, vegMap_smallPolygons_notDas)

print("Output feature class 'vegMap_smallPolygons_notDasExplode' is created in the geodatabase.")

for fc in fc_Delete:
  fc_path = os.path.join(cws, fc)
  if arcpy.Exists(fc_path):
    arcpy.Delete_management(fc_path)
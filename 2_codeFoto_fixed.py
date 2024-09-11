import arcpy

# Set the workspace
arcpy.env.workspace = r"blah\blah\BLAH.gdb"

# Define the input feature class and shapefile
input_fc = "yourInputFeatureClass"
shapefile = r"blah\blah\BLAH.shp"

# Task 1: Explode the feature class
exploded_fc = "Exploded_" + input_fc
arcpy.MultipartToSinglepart_management(input_fc, exploded_fc)

# Task 2: Intersect polygons
intersect_fc = "Intersected_Features"
arcpy.Intersect_analysis([exploded_fc, shapefile], intersect_fc)

# Task 3: Update values
with arcpy.da.UpdateCursor(intersect_fc, ["CODE_FOTO", "code_foto"]) as cursor:
    for row in cursor:
        row[0] = row[1]  # Assign value from 'code_foto' field to 'CODE_FOTO' field
        cursor.updateRow(row)

# Cleanup
arcpy.Delete_management(exploded_fc)


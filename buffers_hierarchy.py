import arcpy

# Set the workspace
arcpy.env.workspace = r"\\192.168.1.5\kartECO SHARED\Projects\Dimosio\K207 - TAIPED\02_Antipirika_sxedia_SP02\Working_files\Data_help_photos\Data\4. Paragomena Stoixeia\xartis_apeiloumenwn_aksiwn\SP02_Veg_Map_new.gdb"

# Input shapefile
merged_buffers = "APEILOUMENES_AKSIES_new"

# Output shapefiles
intersections_output = "merged_Buffers_intersections"
erase_intersections_output = "erase_intersections"
max_aitio_output = "intersections_only_max_aitio"
output_test = "output_test"

# Task 1: Find Intersections
arcpy.analysis.Intersect(merged_buffers, intersections_output)

# Task 2: Erase Intersections
arcpy.analysis.Erase(merged_buffers, intersections_output, erase_intersections_output)

# Task 3: Select Polygons with Maximum 'aitio' Value in Intersections
# Create a dictionary to store the maximum 'aitio' value for each geometry
aitio_max_dict = {}
fields = ['SHAPE@', 'aitio']
with arcpy.da.SearchCursor(intersections_output, fields) as cursor:
    for row in cursor:
        geometry, aitio = row
        # Serialize the geometry to a string for comparison
        geom_str = str(geometry.JSON)
        if geom_str not in aitio_max_dict or aitio > aitio_max_dict[geom_str][1]:
            aitio_max_dict[geom_str] = (geometry, aitio)

# Create a new feature class for selected polygons
arcpy.management.CreateFeatureclass(arcpy.env.workspace, max_aitio_output, "POLYGON", spatial_reference=intersections_output)

# Add fields to the new feature class
arcpy.management.AddField(max_aitio_output, 'aitio', 'DOUBLE')

# Insert selected polygons with maximum 'aitio' value
with arcpy.da.InsertCursor(max_aitio_output, fields) as cursor:
    for geometry, aitio in aitio_max_dict.values():
        cursor.insertRow((geometry, aitio))

# Task 5: Merge 'max_aitio_output' with 'erase_intersections_output'
arcpy.management.Merge([max_aitio_output, erase_intersections_output], output_test)

# Task 6: Dissolve 'output_test' based on 'aitio'
arcpy.management.Dissolve(output_test, "dissolved_AKSIES_new", "aitio", multi_part="SINGLE_PART")

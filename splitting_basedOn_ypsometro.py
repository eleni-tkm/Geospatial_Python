import arcpy

# Set your workspace and input/output feature classes
arcpy.env.workspace = r'where\is\your\database'
input_polygons = r"blah\blah\a_shapefile.shp"
contours = r"blah\blah\contours200.shp"
output_feature_class = 'output_split_polygons.shp'

# Create a list to store split features
split_features = []

# Use a SearchCursor to iterate through the contour
with arcpy.da.SearchCursor(contours, ['SHAPE@', 'ELEV']) as line_cursor:
    for line_row in line_cursor:
        line = line_row[0]
        elevation = line_row[1]

        # Check if the line has the desired elevation
        if elevation in [600, 1200]:
            # Use a SearchCursor to iterate through the polygons
            with arcpy.da.SearchCursor(input_polygons, ['SHAPE@', 'SHAPE@AREA']) as polygon_cursor:
                for polygon_row in polygon_cursor:
                    polygon = polygon_row[0]
                    area = polygon_row[1]

                    # Calculate the area of the polygon
                    if area > 50000:
                        # Check if the line intersects the polygon
                        if line.crosses(polygon):
                            # Split the polygon with the line
                            split_geometry = polygon.cut(line)

                            # Add the split parts to the list
                            for part in split_geometry:
                                split_features.append(part)

# Create the output feature class
arcpy.CreateFeatureclass_management(arcpy.env.workspace, output_feature_class, "POLYGON")

# Use an InsertCursor to add the split features to the output feature class
with arcpy.da.InsertCursor(output_feature_class, ['SHAPE@']) as insert_cursor:
    for geometry in split_features:
        insert_cursor.insertRow([geometry])

# Perform Identity analysis
identity_output = 'split_initial_identity.shp'
arcpy.Identity_analysis(input_polygons, output_feature_class, identity_output)

# Delete the output_split_polygons.shp
arcpy.Delete_management(output_feature_class)

# Iterate through split_initial_identity.shp and explode features
with arcpy.da.UpdateCursor(identity_output, ['SHAPE@']) as cursor:
    for row in cursor:
        cursor.updateRow([row[0]])

# Make a list of field names for input_polygons
field_names_initial = [field.name for field in arcpy.ListFields(input_polygons)]

# Remove fields from split_initial_identity.shp that are not in field_names_initial
#fields_to_keep = [field for field in arcpy.ListFields(identity_output) if field.name in field_names_initial]
#arcpy.DeleteField_management(identity_output, [field.name for field in arcpy.ListFields(identity_output) if field.name not in field_names_initial])


# Explode all features of the final output
final_output = 'Notio_phlio_contours.shp'
arcpy.MultipartToSinglepart_management(identity_output, final_output)
#fields_to_keep2 = [field for field in arcpy.ListFields(final_output) if field.name in field_names_initial]
arcpy.DeleteField_management(final_output, [field.name for field in arcpy.ListFields(final_output) if field.name not in field_names_initial])



arcpy.Delete_management(identity_output)
print("Splitting operation completed.")

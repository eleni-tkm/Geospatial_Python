import geopandas as gpd
#HOW TO COMPARE THE FIELDS FOR TWO DIFFERENT SHAPEFILES USING GEOPANDAS (JUST ONE WAY... THYERE ARE TOO MANY THOUGHHHH :))
# Define the file paths
file_path1 = r"blah\blah\firstShapefile.shp"
file_path2 = r"blah\blah\secondShapefile.shp"

# Read the shapefiles with geopandas
gdf1 = gpd.read_file(file_path1)
gdf2 = gpd.read_file(file_path2)

# Pre-create a unique identifier (id) field in gdf2
gdf2['unique_id'] = range(len(gdf2))

# Perform a spatial join based on intersection (ypou can create a spatial join with the use of a tone of other geospatial relationships though, i need intersections here one to one which is the default behavior od a spatial join)
intersections = gpd.sjoin(gdf1, gdf2, how='inner', predicate='intersects')

# here I define some conditions based on field values
condition1 = (intersections['KATHGORIA'] == 'Δ') & (intersections['VEG_TYPE'].isin([1, 2, 3, 4])) #IN (1, 2, 3, 4) for sql
condition2 = (intersections['KATHGORIA'] == 'X') & (intersections['VEG_TYPE'] == 5)
condition3 = (intersections['KATHGORIA'] == 'Α') & (intersections['VEG_TYPE'].isin([6, 7, 8, 9, 10]))
condition4 = (intersections['KATHGORIA'].isin(['A', ''])) & (intersections['VEG_TYPE'] == 11)

# Identify unmatched polygons from gdf2 based on the conditions from the intersection
unmatched_conditions = ~(condition1 | condition2 | condition3 | condition4)
unmatched_polygons_gdf2 = gdf2[gdf2['unique_id'].isin(intersections[unmatched_conditions]['unique_id'])]

# output file name
output_unmatched_path_gdf2 = r"blah\blah\output_unmatched.shp"

# Save the unmatched polygons from gdf2 to a new shapefile
unmatched_polygons_gdf2.to_file(output_unmatched_path_gdf2)

# Check the resulting DataFrames
#print("Intersecting Polygons:")
#print(intersections)
#print("\nUnmatched Polygons from gdf2:")
#print(unmatched_polygons_gdf2)

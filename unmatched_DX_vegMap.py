import geopandas as gpd

# Define the file paths
file_path1 = r"Z:\Temporary\eleni_data\TAIPED\data\SP_02_DX.shp"
file_path2 = r"Z:\Projects\Dimosio\K207 - TAIPED\02_Antipirika_sxedia_SP02\Working_files\Data_Help_Photos\Data\4. Paragomena Stoixeia\temp_files\polygonsUnmatched.shp"

# Read the shapefiles
gdf1 = gpd.read_file(file_path1)
gdf2 = gpd.read_file(file_path2)

# Pre-create a unique identifier field in gdf2
gdf2['unique_id'] = range(len(gdf2))

# Perform a spatial join
intersections = gpd.sjoin(gdf1, gdf2, how='inner', predicate='intersects')

# Define the conditions
condition1 = (intersections['KATHGORIA'] == 'Δ') & (intersections['VEG_TYPE'].isin([1, 2, 3, 4]))
condition2 = (intersections['KATHGORIA'] == 'X') & (intersections['VEG_TYPE'] == 5)
condition3 = (intersections['KATHGORIA'] == 'Α') & (intersections['VEG_TYPE'].isin([6, 7, 8, 9, 10]))
condition4 = (intersections['KATHGORIA'].isin(['A', ''])) & (intersections['VEG_TYPE'] == 11)

# Identify unmatched polygons from gdf2 based on the conditions from the intersection
unmatched_conditions = ~(condition1 | condition2 | condition3 | condition4)
unmatched_polygons_gdf2 = gdf2[gdf2['unique_id'].isin(intersections[unmatched_conditions]['unique_id'])]

# Define the output file path for unmatched polygons from gdf2
output_unmatched_path_gdf2 = r"Z:\Projects\Dimosio\K207 - TAIPED\02_Antipirika_sxedia_SP02\Working_files\Data_Help_Photos\Data\output_unmatched_gdf2.shp"

# Save the unmatched polygons from gdf2 to a new shapefile
unmatched_polygons_gdf2.to_file(output_unmatched_path_gdf2)

# Check the resulting DataFrames
print("Intersecting Polygons:")
print(intersections)
print("\nUnmatched Polygons from gdf2:")
print(unmatched_polygons_gdf2)

import geopandas as gpd
from shapely.geometry import MultiPolygon
from fiona import drivers
import fiona

# Load the first shapefile
shp1_path = r'E:\taiped\rasterClass_polygon_only.shp' #this is stable
gdf1 = gpd.read_file(shp1_path)

# Load the second shapefile
shp2_path = r'Z:\Projects\Dimosio\K207 - TAIPED\02_Antipirika_sxedia_SP02\Working_files\Data_Help_Photos\Data\4. Paragomena Stoixeia\temp_files\SP02_DIKTYO_DEDHE_Buffer.shp'
gdf2 = gpd.read_file(shp2_path)

# Create a spatial index for faster spatial queries
gdf1_sindex = gdf1.sindex

# Function to get the majority 'gridcode' value for a given geometry
def get_majority_gridcode(geometry):
    possible_matches_index = list(gdf1_sindex.intersection(geometry.bounds))
    possible_matches = gdf1.iloc[possible_matches_index]
    precise_matches = possible_matches[possible_matches.intersects(geometry)]
    
    if len(precise_matches) == 0:
        return None
    
    # Calculate the area of intersection with each 'gridcode'
    intersection_areas = precise_matches.intersection(geometry).area
    
    # Get the 'gridcode' with the maximum area of intersection
    majority_gridcode = intersection_areas.idxmax()
    return gdf1.at[majority_gridcode, 'gridcode']

# Apply the function to the 'geometry' column of the second shapefile
gdf2['YPSOMETRO2'] = gdf2['geometry'].apply(get_majority_gridcode)

# Save the updated shapefile
output_path = r'\\192.168.1.5\kartECO SHARED\Temporary\eleni_data\TAIPED\data\finals\Buffered_DEDDHE_Ypso.shp'
gdf2.to_file(output_path)

import geopandas as gpd
import pandas as pd

# Load the two feature classes as GeoDataFrames
gdf1 = gpd.read_file(r"\\SERVER\kartECO SHARED\Projects\Dimosio\K196 - Apografi Daswn\Working_files\Fwtoermhneia_Working\6_General\03Tmhmatikh_Paradosi\10_Telikes_vaseis\Malevisiou\Malevisiou_veg.gdb" , layer='Malevisiou_veg') #vlastisis H edafokalypsis

gdf2 = gpd.read_file(r"\\SERVER\kartECO SHARED\Projects\Dimosio\K196 - Apografi Daswn\Working_files\Fwtoermhneia_Working\6_General\03Tmhmatikh_Paradosi\10_Telikes_vaseis\Malevisiou\Old\fotoshm_merged.shp") #fotosimeia

#gdf2_path = r"\\192.168.1.5\kartECO SHARED\Temporary\eleni_data\k196\01_SAP_subFot_SP_1.gdb"

# Add a unique identifier field to gdf2
gdf2['FID_gdf2'] = range(len(gdf2))

# Perform a spatial join based on intersection
joined_gdf = gpd.sjoin(gdf1, gdf2, how="inner", predicate="intersects")

# Initialize a set to store the FID values of matched polygons from gdf2
matched_ids = set()

# Iterate through the resulting joined GeoDataFrame and compare 'EIDOS1' values
for idx, row in joined_gdf.iterrows():
    #if (row['POS_EDAF_left'] == row['POS_EDAF_right']):
    if (row['CAT_ID_left'] == row['CAT_ID_right']) and (row['CAT_O2_left'] == row['CAT_O2_right']):
        matched_ids.add(row['FID_gdf2'])

# Get the FID values of unmatched polygons from gdf2
unmatched_ids = set(gdf2['FID_gdf2']) - matched_ids

# Filter the unmatched polygons based on spatial intersection with polygons from gdf1
spatially_matched_ids = set()
for idx, row in gdf2.iterrows():
    if row['FID_gdf2'] in unmatched_ids and any(row['geometry'].intersects(geom) for geom in gdf1['geometry']):
        spatially_matched_ids.add(row['FID_gdf2'])

# Create a new GeoDataFrame containing the unmatched polygons
unmatched_gdf = gdf2[gdf2['FID_gdf2'].isin(spatially_matched_ids)]

# Specify the output shapefile path
output_shapefile = r'\\SERVER\kartECO SHARED\Projects\Dimosio\K196 - Apografi Daswn\Working_files\Fwtoermhneia_Working\6_General\03Tmhmatikh_Paradosi\10_Telikes_vaseis\Malevisiou\unmatched\unmatched_veg.shp'

# Save the unmatched GeoDataFrame to a shapefile
unmatched_gdf.to_file(output_shapefile)

print(f"Exported unmatched polygons to {output_shapefile}")

#0.29999999999999999
#def replace_value(value):
    #if value ==' ':
        #return ''
    #else:
        #return value

import geopandas as gpd
import pandas as pd

# Load the two feature classes as GeoDataFrames
gdf1 = gpd.read_file(r"C:\Users\user\Documents\ArcGIS\Default.gdb" , layer='Export_Output_9') #vlastisis H edafokalypsis

gdf2 = gpd.read_file(r"C:\Users\user\Documents\ArcGIS\Default.gdb", layer="FOTOSHMEIA_DK_Clip") #fotosimeia


#gdf2_path = r"\\192.168.1.5\kartECO SHARED\Temporary\eleni_data\k196\01_SAP_subFot_SP_1.gdb"

# Add a unique identifier field to gdf2
gdf2['FID_gdf2'] = range(len(gdf2))

# Perform a spatial join based on intersection
joined_gdf = gpd.sjoin(gdf1, gdf2, how="inner", predicate="intersects")
#print(joined_gdf)
joined_gdf.loc[:,'EIDOS1_right']=(joined_gdf.loc[:,'EIDOS1_right']).str.strip()
joined_gdf.loc[:,'EIDOS1_left']=(joined_gdf.loc[:,'EIDOS1_left']).str.strip()

joined_gdf.loc[:,'EIDOS2_right']=(joined_gdf.loc[:,'EIDOS2_right']).str.strip()
joined_gdf.loc[:,'EIDOS2_left']=(joined_gdf.loc[:,'EIDOS2_left']).str.strip()

joined_gdf.loc[:,'EIDOS3_right']=(joined_gdf.loc[:,'EIDOS3_right']).str.strip()
joined_gdf.loc[:,'EIDOS3_left']=(joined_gdf.loc[:,'EIDOS3_left']).str.strip()

joined_gdf.loc[:,'CAT_O2_right']=(joined_gdf.loc[:,'CAT_O2_right']).str.strip()
joined_gdf.loc[:,'CAT_O2_left']=(joined_gdf.loc[:,'CAT_O2_left']).str.strip()

# Initialize a set to store the FID values of matched polygons from gdf2
matched_ids = set()
dasika_list=['01010100','01020100','01030100','01030200']
# Iterate through the resulting joined GeoDataFrame and compare 'EIDOS1' values
for idx, row in joined_gdf.iterrows():
    #if (row['POS_EDAF_left'] == row['POS_EDAF_right']):
    if (row['CAT_ID_left'] == row['CAT_ID_right']) and (row['CAT_ID_left'] in dasika_list) and (row['EIDOS1_left'] == row['EIDOS1_right']) and (row['EIDOS2_left'] == row['EIDOS2_right']) and (row['EIDOS3_left'] == row['EIDOS3_right'])and (row['CAT_O2_left'] == row['CAT_O2_right']):
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
output_shapefile = r'\\SERVER\kartECO SHARED\Temporary\eleni_data\AgNikolaos\unmatched\unmatched_veg44.shp'

# Save the unmatched GeoDataFrame to a shapefile
unmatched_gdf.to_file(output_shapefile)

print(f"Exported unmatched polygons to {output_shapefile}")

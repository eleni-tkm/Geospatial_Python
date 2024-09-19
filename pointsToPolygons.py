import pandas as pd
from shapely.geometry import Polygon
import geopandas as gpd

#small Description:
#How to read points (x,y) data from excel spreadsheets
#Create a polygon from each set of x,y pairs
#save outputs to shapefiles
#for my case there is an empty row between the end and the start of each set of X,Y values that build a polygon

# Function to create a polygon from a list of coordinates
def create_polygon(coords):
    return Polygon(coords)

# Function to create the extra field value based on sheet name
def get_extra_field(sheet_name):
    if sheet_name == 'STEIRA':
        return '2020_STEIRA'
    elif sheet_name == 'LATOMIKOS':
        return '2020_LATOMIKOS'
    else:
        return None

# Read both sheets 'STEIRA' and 'LATOMIKOS' from the '2020.xlsx' file into pandas DataFrames
xls_file = pd.ExcelFile(r"blah\blah\2020\2020.xlsx")
df_steira = pd.read_excel(xls_file, sheet_name='STEIRA')
df_latomikos = pd.read_excel(xls_file, sheet_name='LATOMIKOS')

# Function to process the DataFrame and create polygons
def process_sheet(df, sheet_name):
    # List to store polygons and their corresponding sheet names
    polygons = []
    sheet_names = []

    # Variables to store coordinates temporarily
    x_coords = []
    y_coords = []

    for index, row in df.iterrows():
        # If X or Y is NaN, we reached the end of the current polygon
        if pd.isnull(row['X']) or pd.isnull(row['Y']):
            # Create the polygon and add it to the list
            if x_coords and y_coords:  # Check if there are valid coordinates
                polygon = create_polygon(list(zip(x_coords, y_coords)))
                polygons.append(polygon)
                sheet_names.append(get_extra_field(sheet_name))
                x_coords = []
                y_coords = []
        else:
            x_coords.append(row['X'])
            y_coords.append(row['Y'])

    # Add the last polygon if there are any remaining coordinates
    if x_coords and y_coords:
        polygon = create_polygon(list(zip(x_coords, y_coords)))
        polygons.append(polygon)
        sheet_names.append(get_extra_field(sheet_name))

    return polygons, sheet_names

# Process both sheets to create polygons and sheet names
polygons_steira, sheet_names_steira = process_sheet(df_steira, 'STEIRA')
polygons_latomikos, sheet_names_latomikos = process_sheet(df_latomikos, 'LATOMIKOS')

# Create separate GeoDataFrames for 'STEIRA' and 'LATOMIKOS' which are my sheet names in the excel file
gdf_steira = gpd.GeoDataFrame({'geometry': polygons_steira, 'sheet_name': sheet_names_steira})
gdf_latomikos = gpd.GeoDataFrame({'geometry': polygons_latomikos, 'sheet_name': sheet_names_latomikos})

# Concatenate the GeoDataFrames for both sheets
gdf_combined = pd.concat([gdf_steira, gdf_latomikos])

# Save the combined GeoDataFrame to a shapefile
gdf_combined.to_file('both2020.shp', driver='ESRI Shapefile')

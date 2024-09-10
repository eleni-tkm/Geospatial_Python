import geopandas as gpd
from shapely.geometry import Polygon

def create_polygon(gdf):
    # Filter out points with X=0 and Y=0
    gdf = gdf.loc[(gdf['X'] != 0) & (gdf['Y'] != 0)]

    # Create a list of (x, y) tuples from the points
    points = [(x, y) for x, y in zip(gdf['X'], gdf['Y'])]

    # Create a polygon from the points
    polygon = Polygon(points)

    return polygon

if __name__ == "__main__":
   
    gdf = gpd.read_file(r"Z:\Temporary\eleni_data\PointstoPoly\simple_case\albt.shp")

    # Create the polygon from the ordered points
    polygon = create_polygon(gdf)

    # Create a new GeoDataFrame for the resulting polygon
    polygon_gdf = gpd.GeoDataFrame(geometry=[polygon], crs=gdf.crs)

    # Export the GeoDataFrame to a new Shapefile
  
    polygon_gdf.to_file('ext.shp', driver='ESRI Shapefile')

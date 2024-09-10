import geopandas as gpd
from shapely.geometry import Polygon

def create_polygon(gdf):
    # Filter out points with X=0 and Y=0
    gdf = gdf.loc[(gdf['X'] != 0) & (gdf['Y'] != 0)]

   
    points = [(x, y) for x, y in zip(gdf['X'], gdf['Y'])]

    # points to polygon
    polygon = Polygon(points)

    return polygon

if __name__ == "__main__":
   
    gdf = gpd.read_file(r'blah\blah\myShapefile.shp")

    # Create the polygon from the ordered points
    polygon = create_polygon(gdf)

    # Create a new GeoDataFrame for the resulting polygon
    polygon_gdf = gpd.GeoDataFrame(geometry=[polygon], crs=gdf.crs)

    # Export the GeoDataFrame to a new Shapefile
  
    polygon_gdf.to_file('ext.shp', driver='ESRI Shapefile')

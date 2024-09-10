import geopandas as gpd
from shapely.geometry import LineString, MultiPoint, Polygon, MultiLineString
from shapely.ops import unary_union, polygonize

def group_points_by_polygon(gdf, geometry_column):
    polygons = {}
    for index, row in gdf.iterrows():
        polygon_id = row['ORIG_FID']
        x, y = row[geometry_column].x, row[geometry_column].y
        if polygon_id not in polygons:
            polygons[polygon_id] = []
        polygons[polygon_id].append((x, y))
    # Convert the lists of points to a list of lists of points
    return [coords for coords in polygons.values()]

def create_lines(coordinates_list):
    lines = [LineString(coords) for coords in coordinates_list]
    return lines

def create_polygon(points):
    # Create a MultiPoint from the list of points
    multi_point = MultiPoint(points)
    # Find the convex hull of the MultiPoint to form the outer boundary
    convex_hull = multi_point.convex_hull
    return convex_hull

if __name__ == "__main__":
    gdf = gpd.read_file('Z:\Temporary\eleni_data\PointstoPoly\pointsToPoly.gdb', layer='Habitats_PolygonToLine_Gener1')

    # Find the correct geometry column name
    geometry_column = gdf.geometry.name

    # Group points by polygon
    coordinates_list = group_points_by_polygon(gdf, geometry_column)

    # Convert each group of points to lines
    lines = create_lines(coordinates_list)

    # Convert the list of lines to a MultiLineString
    multiline = MultiLineString(lines)

    # Convert MultiLineString to polygons using polygonize function
    polygons = list(polygonize(multiline))

    # Create a new GeoDataFrame for the resulting polygons
    polygons_gdf = gpd.GeoDataFrame(geometry=polygons)
    polygons_gdf.crs = "EPSG:4326"

    # Export the GeoDataFrame to a new Shapefile
       polygons_gdf.to_file('output_file_path.shp', driver='ESRI Shapefile')

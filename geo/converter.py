import geopandas as gpd

geodf = gpd.read_file('./00ent.shp')
geodf = geodf.to_crs(epsg='4326')
geodf.to_file('./mexico.geojson', driver='GeoJSON')
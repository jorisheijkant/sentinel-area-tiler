import math

from shapely.geometry import box
from shapely.geometry.base import BaseGeometry

KM_PER_DEGREE_LAT = 111.32

def tile_region(region: BaseGeometry, tile_size_in_meters: int, tile_overlap_in_meters: int) -> list[tuple[tuple[float, float, float, float], int, int]]:
    lon_min, lat_min, lon_max, lat_max = region.bounds
    center_lat = (lat_min + lat_max) / 2
    lat_rad = math.radians(center_lat)

    tile_size_km = tile_size_in_meters / 1000
    overlap_km = tile_overlap_in_meters / 1000

    deg_per_tile_lat = tile_size_km / KM_PER_DEGREE_LAT
    deg_per_tile_lon = tile_size_km / (KM_PER_DEGREE_LAT * math.cos(lat_rad))

    step_lat = (tile_size_km - overlap_km) / KM_PER_DEGREE_LAT
    step_lon = (tile_size_km - overlap_km) / (KM_PER_DEGREE_LAT * math.cos(lat_rad))

    tiles = []
    row, lat = 0, lat_min
    while lat < lat_max:
        col, lon = 0, lon_min
        while lon < lon_max:
            tile_bbox = (lon, lat, lon + deg_per_tile_lon, lat + deg_per_tile_lat)
            if region.intersects(box(*tile_bbox)):
                tiles.append((tile_bbox, row, col))
            lon += step_lon
            col += 1
        lat += step_lat
        row += 1

    return tiles

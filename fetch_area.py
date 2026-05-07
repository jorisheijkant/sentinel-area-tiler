import json
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from shapely.geometry import box, mapping
from tqdm import tqdm

from functions import get_sentinel_token, get_sentinel_visual, tile_region, convert_tiff_to_jpg

load_dotenv()
CLIENT_ID = os.environ["SENTINEL_CLIENT_ID"]
CLIENT_SECRET = os.environ["SENTINEL_CLIENT_SECRET"]

area_name = "middle_suriname"
area_bounding_box = [-57.2772, 3.2474, -54.55, 4.6612]  # [west, south, east, north] in EPSG:4326
tile_size_in_meters = 5000
tile_overlap_in_meters = 200
start_date = "2025-01-01"
end_date = "2026-06-01"
max_cloud_coverage = 10 # In percent

region = box(*area_bounding_box)
tiles = tile_region(region, tile_size_in_meters, tile_overlap_in_meters)

output_dir = Path(f"data/{area_name}")
geotiffs_dir = output_dir / "tiles" / "geotiffs"
jpgs_dir = output_dir / "tiles" / "jpgs"
geotiffs_dir.mkdir(parents=True, exist_ok=True)
jpgs_dir.mkdir(parents=True, exist_ok=True)

tile_grid = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": mapping(box(*bbox)),
            "properties": {"row": row, "col": col, "tile_id": f"tile_{row}_{col}"},
        }
        for bbox, row, col in tiles
    ],
}
with open(output_dir / "tile_grid.geojson", "w") as f:
    json.dump(tile_grid, f, indent=2)

oauth = get_sentinel_token(CLIENT_ID, CLIENT_SECRET)

for bbox, row, col in tqdm(tiles, desc="Fetching tiles", unit="tile"):
    tile_id = f"tile_{row}_{col}"
    tiff_path = str(geotiffs_dir / f"{tile_id}_visual.tiff")
    jpg_path = str(jpgs_dir / f"{tile_id}_visual.jpg")
    if get_sentinel_visual(oauth, bbox, start_date, end_date, max_cloud_coverage, tiff_path):
        convert_tiff_to_jpg(tiff_path, jpg_path)
    time.sleep(5)

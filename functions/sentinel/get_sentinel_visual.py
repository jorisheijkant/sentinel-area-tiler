import os
import math


def get_sentinel_visual(oauth, bbox, min_date, max_date, max_cloud_coverage, output_path):
    if os.path.exists(output_path):
        print(f"    Skipping visual (exists)")
        return True

    lon_min, lat_min, lon_max, lat_max = bbox

    center_lat = (lat_min + lat_max) / 2
    lat_rad = math.radians(center_lat)

    delta_lon = lon_max - lon_min
    delta_lat = lat_max - lat_min

    corrected_bbox_w = delta_lon * math.cos(lat_rad)
    aspect_ratio = delta_lat / corrected_bbox_w if corrected_bbox_w > 0 else 1

    output_width = 2500
    output_height = max(1, int(output_width * aspect_ratio))

    evalscript = """
    //VERSION=3
    function setup() {
      return {
        input: ["B02", "B03", "B04"],
        output: { bands: 3 },
      }
    }

    function evaluatePixel(sample) {
      return [
        Math.cbrt(0.6 * sample.B04),
        Math.cbrt(0.6 * sample.B03),
        Math.cbrt(0.6 * sample.B02)
      ]
    }
    """

    request = {
        "input": {
            "bounds": {
                "properties": {"crs": "http://www.opengis.net/def/crs/OGC/1.3/CRS84"},
                "bbox": list(bbox),
            },
            "data": [
                {
                    "type": "sentinel-2-l2a",
                    "dataFilter": {
                        "timeRange": {
                            "from": f"{min_date}T00:00:00Z",
                            "to": f"{max_date}T00:00:00Z",
                        },
                        "maxCloudCoverage": max_cloud_coverage
                    },
                    "mosaickingOrder": "leastCC",
                }
            ],
        },
        "output": {
            "width": output_width,
            "height": output_height,
        },
        "evalscript": evalscript,
    }

    url = "https://sh.dataspace.copernicus.eu/api/v1/process"
    response = oauth.post(url, json=request, headers={"Accept": "image/tiff"})

    if response.status_code != 200:
        print(f"    Visual fetch failed: {response.status_code}")
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"    Visual saved: {len(response.content)} bytes")
    return True

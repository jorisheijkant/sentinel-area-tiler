import os
import math


def get_sentinel_sar(oauth, bbox, min_date, max_date, output_path):
    if os.path.exists(output_path):
        print(f"    Skipping SAR (exists)")
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
        input: ["VV", "VH"],
        output: {
          bands: 3,
          sampleType: "FLOAT32"
        }
      }
    }

    function evaluatePixel(sample) {
      var vv_db = 10 * Math.log(sample.VV) / Math.LN10;
      var vh_db = 10 * Math.log(sample.VH) / Math.LN10;

      var vv_norm = (vv_db + 25) / 25;
      var vh_norm = (vh_db + 25) / 25;

      return [
        Math.max(0, Math.min(1, vv_norm)),
        Math.max(0, Math.min(1, vh_norm)),
        Math.max(0, Math.min(1, vv_norm - vh_norm))
      ];
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
                    "type": "sentinel-1-grd",
                    "dataFilter": {
                        "timeRange": {
                            "from": f"{min_date}T00:00:00Z",
                            "to": f"{max_date}T00:00:00Z",
                        },
                        "acquisitionMode": "IW",
                        "polarization": "DV",
                        "resolution": "HIGH",
                    },
                    "processing": {
                        "orthorectify": True,
                        "backCoeff": "GAMMA0_TERRAIN"
                    }
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
        print(f"    SAR fetch failed: {response.status_code}")
        return False

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(response.content)

    print(f"    SAR saved: {len(response.content)} bytes")
    return True

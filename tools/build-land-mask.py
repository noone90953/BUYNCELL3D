"""Build the globe's packed land lookup from public-domain Natural Earth data.

Python 3 standard library only. Normal use reads the checked-in source archives:
    python tools/build-land-mask.py
Use --download to retrieve those official archives again. The website never runs
this script and never fetches geography or reads an image through a canvas.
"""

import argparse
import base64
import hashlib
import json
import math
from pathlib import Path
import struct
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "assets" / "data"
SOURCE = DATA / "source"
WIDTH, HEIGHT = 1440, 720
GOLDEN_ANGLE = math.pi * (3 - math.sqrt(5))
SOURCES = {
    "land": "https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_land.zip",
    "lakes": "https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_lakes.zip",
}


def load_polygons(path):
    """Read ESRI Polygon records, retaining all rings, including inner holes."""
    with zipfile.ZipFile(path) as archive:
        shp = archive.read(path.stem + ".shp")
        version = archive.read(path.stem + ".VERSION.txt").decode().strip()
    if struct.unpack_from(">i", shp, 0)[0] != 9994:
        raise ValueError("Not an ESRI shapefile")
    polygons, offset = [], 100
    while offset < len(shp):
        size = struct.unpack_from(">i", shp, offset + 4)[0] * 2
        offset += 8
        record = memoryview(shp)[offset:offset + size]
        offset += size
        shape_type = struct.unpack_from("<i", record, 0)[0]
        if shape_type == 0:
            continue
        if shape_type != 5:
            raise ValueError("Expected Polygon shape records")
        parts, points = struct.unpack_from("<2i", record, 36)
        starts = list(struct.unpack_from("<" + "i" * parts, record, 44)) + [points]
        coords = list(struct.iter_unpack("<2d", record[44 + parts * 4:]))
        if len(coords) != points:
            raise ValueError("Incorrect shape point count")
        polygons.append([coords[starts[i]:starts[i + 1]] for i in range(parts)])
    return polygons, version


def rasterize(polygons, width, height):
    """Even/odd scanlines at cell centers; rings of a feature share parity.

    Union features after their holes have been processed, avoiding a lake or an
    overlapping feature cancelling another feature. Natural Earth splits land at
    the antimeridian; keep its -180/+180 edges as given (especially Antarctica).
    """
    mask = bytearray(width * height)
    for rings in polygons:
        edges = [(a, b) for ring in rings for a, b in zip(ring, ring[1:]) if a[1] != b[1]]
        if not edges:
            continue
        min_lat = min(min(a[1], b[1]) for a, b in edges)
        max_lat = max(max(a[1], b[1]) for a, b in edges)
        row_start = max(0, math.ceil((90 - max_lat) * height / 180 - .5))
        row_stop = min(height, math.floor((90 - min_lat) * height / 180 - .5) + 1)
        for y in range(row_start, row_stop):
            lat = 90 - (y + .5) * 180 / height
            crossings = sorted(a[0] + (lat - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
                               for a, b in edges if (a[1] > lat) != (b[1] > lat))
            if len(crossings) % 2:
                raise ValueError("Unpaired polygon intersection")
            for left, right in zip(crossings[::2], crossings[1::2]):
                x0 = max(0, math.ceil((left + 180) * width / 360 - .5))
                x1 = min(width, math.ceil((right + 180) * width / 360 - .5))
                if x1 > x0:
                    start = y * width + x0
                    mask[start:start + x1 - x0] = b"\x01" * (x1 - x0)
    return mask


def is_land(mask, lat, lon):
    x = math.floor(((lon + 180) % 360) / 360 * WIDTH)
    y = min(HEIGHT - 1, max(0, math.floor((90 - lat) / 180 * HEIGHT)))
    return bool(mask[y * WIDTH + x])


def fibonacci_count(mask, count):
    total = 0
    for i in range(count):
        lat = math.degrees(math.asin(1 - 2 * (i + .5) / count))
        lon = math.degrees((i * GOLDEN_ANGLE) % (2 * math.pi)) - 180
        total += is_land(mask, lat, lon)
    return total


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--download", action="store_true", help="download official source archives")
    args = parser.parse_args()
    SOURCE.mkdir(parents=True, exist_ok=True)
    polygons, metadata = {}, {}
    for kind, url in SOURCES.items():
        path = SOURCE / f"ne_110m_{kind}.zip"
        if args.download:
            with urllib.request.urlopen(url) as response:
                path.write_bytes(response.read())
        if not path.exists():
            raise SystemExit(f"Missing {path}; run with --download")
        polygons[kind], version = load_polygons(path)
        metadata[kind] = {"source": url, "version": version,
                          "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    mask = rasterize(polygons["land"], WIDTH, HEIGHT)
    lakes = rasterize(polygons["lakes"], WIDTH, HEIGHT)
    for i, lake in enumerate(lakes):
        if lake:
            mask[i] = 0
    probes = {
        "Dubai": (25.20, 55.27, True),
        "Africa interior": (10, 20, True),
        "Cairo": (30.04, 31.24, True),
        "Johannesburg": (-26.20, 28.05, True),
        "Central Atlantic": (0, -30, False),
        "Pacific west of dateline": (0, 179.9, False),
        "Pacific east of dateline": (0, -179.9, False),
        "Antarctica west of dateline": (-85, 179.9, True),
        "Antarctica east of dateline": (-85, -179.9, True),
        "Lake Victoria": (-1, 33, False),
        "Lake Superior": (47.7, -87.5, False),
        "Caspian Sea": (42, 51, False),
    }
    results = {name: is_land(mask, lat, lon) == expected for name, (lat, lon, expected) in probes.items()}
    if not all(results.values()):
        raise AssertionError({name: ok for name, ok in results.items() if not ok})
    packed = bytearray((WIDTH * HEIGHT + 7) // 8)
    for i, land in enumerate(mask):
        packed[i >> 3] |= land << (i & 7)
    sample_count = 14000
    land_count = fibonacci_count(mask, sample_count)
    payload = {
        "width": WIDTH, "height": HEIGHT,
        "bits": base64.b64encode(packed).decode("ascii"),
        "source": SOURCES["land"], "version": metadata["land"]["version"],
        "license": "Public domain",
        "licenseUrl": "https://www.naturalearthdata.com/about/terms-of-use/",
        "projection": "equirectangular", "bitOrder": "little-endian",
        "bounds": [-180, -90, 180, 90], "sampleAt": "cell-center",
        "fibonacciSamples": sample_count, "fibonacciLandCount": land_count,
        "fibonacciLongitude": "degrees((i * PI * (3-sqrt(5))) % (2*PI)) - 180",
        "sources": metadata,
    }
    target = DATA / "land-mask.js"
    target.write_text("/* Made with Natural Earth. Public domain. See NATURAL-EARTH.md.\n"
                      " * Generated by tools/build-land-mask.py; no runtime network or image access. */\n"
                      "window.NATURAL_EARTH_LAND = Object.freeze(" + json.dumps(payload, separators=(",", ":")) + ");\n", encoding="utf-8")
    print(json.dumps({"output": str(target), "bytes": target.stat().st_size,
                      "width": WIDTH, "height": HEIGHT, "samples": sample_count,
                      "landPoints": land_count, "probes": results, "sources": metadata}, indent=2))


if __name__ == "__main__":
    main()

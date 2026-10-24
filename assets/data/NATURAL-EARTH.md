# Globe land data

Made with Natural Earth. The globe uses **Natural Earth 1:110 million Land**,
with the matching 110m lakes removed so lakes and inland seas remain water.
This is an illustrative land outline, not a political map.

## Source and permission

- [110m Land description](https://www.naturalearthdata.com/downloads/110m-physical-vectors/110m-land/)
- [Official 110m physical data catalog](https://www.naturalearthdata.com/downloads/110m-physical-vectors/)
- [Land archive](https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_land.zip)
- [Lakes archive](https://naturalearth.s3.amazonaws.com/110m_physical/ne_110m_lakes.zip)
- [Natural Earth terms of use](https://www.naturalearthdata.com/about/terms-of-use/)

Natural Earth makes its vector and raster data public domain, permitting
modification and commercial use without a permission or attribution requirement.
The physical-data catalog identifies Amazon Web Services as its download host.
The archives here came directly from that official distribution on **2026-10-23**.

The land archive's own `ne_110m_land.VERSION.txt` says **4.1.0**; the description
page still labels its download 4.0.0. The archive version is recorded in the
generated JavaScript. Lakes are **5.0.0**.

| Source archive | SHA-256 |
| --- | --- |
| `source/ne_110m_land.zip` | `1926c621afd6ac67c3f36639bb1236134a48d82226dc675d3e3df53d02d2a3de` |
| `source/ne_110m_lakes.zip` | `f2eed3c738a93010770acb0ba44273ea6a83b053641588bc902d9d6fd1cdafcb` |

## Runtime interface

`land-mask.js` is a normal local script, loaded before the inline scene script:

```html
<script src="assets/data/land-mask.js"></script>
```

It defines `window.NATURAL_EARTH_LAND` with `width`, `height`, `bits` (base64),
`source`, `version`, and provenance fields. The mask is **1440 x 720** cells.
It is a packed geographic lookup table, never a texture or rendered image.
Reading it requires neither `fetch()` nor a canvas and works with a `file:` page.

Coordinates are equirectangular, west to east and north to south, with each bit
representing the cell center. Rows begin at longitude -180 and latitude +90.
Longitude wraps; latitude clamps at the poles. One means land, zero means water.
Bits are row-major and little-endian within each byte:

```js
const mask = window.NATURAL_EARTH_LAND;
const bytes = Uint8Array.from(atob(mask.bits), c => c.charCodeAt(0));
function isLand(lat, lon) {
  const x = Math.floor((((lon + 180) % 360 + 360) % 360) / 360 * mask.width);
  const y = Math.max(0, Math.min(mask.height - 1,
    Math.floor((90 - lat) / 180 * mask.height)));
  const bit = y * mask.width + x;
  return Boolean((bytes[bit >> 3] >> (bit & 7)) & 1);
}
```

For the scene's uniform Fibonacci lattice, use **14,000 candidates**:

```js
const n = 14000, goldenAngle = Math.PI * (3 - Math.sqrt(5));
for (let i = 0; i < n; i++) {
  const lat = Math.asin(1 - 2 * (i + .5) / n) * 180 / Math.PI;
  const lon = ((i * goldenAngle) % (2 * Math.PI)) * 180 / Math.PI - 180;
  if (isLand(lat, lon)) { /* add a Haze dot to the single InstancedMesh */ }
}
```

This produces **4,024 land dots**. The positions are independent of animation
time and of load order. The mask does not supply or alter route coordinates.

## Reproduce and check

From the project directory, using any Python 3 installation:

```text
python tools/build-land-mask.py
```

No Python packages or network access are needed. The script reads the two
checked-in official archives, uses even/odd polygon scanlines to preserve inner
rings, unions separate features, subtracts lakes, then writes `land-mask.js`.
Natural Earth's antimeridian edges remain intact, including Antarctica's pole.
`--download` explicitly replaces the source archives from their official URLs;
review version and hash changes before accepting new geography.

The script asserts twelve geographic samples: Dubai, Cairo, Johannesburg and an
African interior point are land; the central Atlantic and both sides of the
equatorial Pacific dateline are ocean; both dateline sides in Antarctica are
land; Victoria, Superior and the Caspian Sea are water. It also reports the
Fibonacci count. JavaScript decoding was checked separately against the same
4,024-point result.

The 110m source and quarter-degree lookup deliberately simplify coasts and omit
small islands. Route markers use their supplied latitude/longitude even when a
small coastal feature is below the outline's resolution.

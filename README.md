# BUY & CELL — From Dubai. To your world.

A buildless, offline-capable website. All application CSS and JavaScript are in **index.html**. Three.js r160 and Archivo are stored locally, with their licenses. No framework, package install, CDN, imported model, texture, or post-processing dependency.

For saved versions and double-click switching shortcuts, see [VERSION_HISTORY.md](VERSION_HISTORY.md).

## Open

Open `index.html` directly in a browser, or run the optional local preview:

```powershell
node tools/preview.cjs
```

Visit `http://127.0.0.1:4173`. Deploy by copying `index.html`, `vendor/`, and `assets/` to any static host; no build is needed. The `tools/` and `qa/` folders are development helpers and need not be deployed.

## Journey contract

`window.setProgress(p)` is defined in the head before Three.js loads. Calls made early retain the latest clamped progress. Every call restores the base transforms and calculates the whole scene analytically; it does not integrate animation state. Only water shimmer uses time. Reduced-motion preferences disable shimmer, parallax and scroll easing.

| Progress | Moment |
| --- | --- |
| 0 | Warehouse, cartons, forklift and scanner |
| .2 | Pallet loaded; doors close from .184 through .216 |
| .4 | Truck on the curved road, following departure at .24 |
| .6 | Near top-down ship shot over the Gulf |
| .8 | Plane crossing the sea |
| 1 | World: complete Dubai routes on the dotted globe, all markers lit, planes hidden |

Every original timing is scaled by 0.8 using one legacy progress clock. The pallet becomes a child of `Container` at .216. Scrubbing backward reparents it to `World` and reconstructs its world pose without a discontinuity. All named scene objects in the brief are unique `THREE.Group`s. Carton groups carry their corresponding `instanceId`, while the rendered cartons use shared instanced batches plus labels. Truck and forklift wheels, container ribs, road markings, cartons, globe dots and ship stacks are instanced.

Six `MeshStandardMaterial` assets are shared throughout: `Mat_Chalk`, `Mat_Asphalt`, `Mat_Gulf`, `Mat_Signal`, `Mat_Haze`, and `Mat_Graphite`. Roughness is 1 and metalness is 0. The shared shaders handle soft contact shadows, the scanner, a tapered wake fade and subtle procedural surface grain without extra materials or texture maps. Signal is authored as exact `#FF5B1F` in sRGB; output is sRGB with no tone mapping. There are two lights, a 2048px desktop / 1024px phone shadow map, and a device-pixel-ratio cap of 2. The scene contains 60,692 triangles and 5,131 repeated instances.

The perspective camera starts low beside the pallet, then rises and pulls back for loading. Off-axis framing reserves the copy zones. The truck and all its children follow the road centreline and tangent. Its rear doors open 180 degrees and close outward through the .184–.216 interval. The warehouse bay shares the loading axis. The ground extends beyond the camera rather than ending as a display slab.

## World finale

From .8 to .88 the aircraft continues out of frame, the camera climbs, the Sea fades and the globe rises against the same Gulf background. From .88 to 1, nine lifted great-circle arcs stagger from Dubai to Cairo, Dakar, Accra, Lagos, Kinshasa, Nairobi, Mombasa, Dar es Salaam and Johannesburg. These are illustrative destination placeholders. Each route reuses the original Plane group's geometry and materials, faces its tangent, draws a trailing Signal arc and lights its destination on arrival with one expanding/fading ring. Archivo labels are projected from the marker positions, kept inside the subject area, spaced to avoid collisions and hidden on the far side. At 1 all routes are complete and every plane/pulse is hidden.

The globe is an Asphalt sphere. A single Haze `InstancedMesh` holds 4,024 hexagonal dots selected from a 14,000-point Fibonacci lattice using Natural Earth's public-domain 110m land outline. `assets/data/land-mask.js` is a plain classic script containing packed geographic bits. It uses no fetch, canvas image sampling, imported models or texture maps and can load from disk. Source archives, licensing and reproducible offline generation are described in [assets/data/NATURAL-EARTH.md](assets/data/NATURAL-EARTH.md).

All transforms, route draw ranges, Sea opacity, globe rotation, label visibility and arrival pulses depend only on `setProgress(p)` and viewport size. The World copy is the sixth nearest-key block (active from .9), with the quote CTA moved from Air to World. The header quote link navigates to this finale. The existing enquiry dialog still prepares a shareable draft; no delivery backend was added.

The page has a 500svh track, a sticky full-height stage, and a fixed full-viewport canvas. Copy switches to the nearest key moment. Desktop copy occupies the left 45%; phone copy sits below the upper subject area. Mobile chapter navigation sits above an 85px bottom safe area. The local SVG poster appears if the library or WebGL fails or a WebGL context is lost.

## Cutouts

The cutout layer is currently **hidden pending 3D approval**. After approval, remove `hidden` from the `.cutouts` element to restore it. See `assets/cutouts/README.md`. Five original transparent WebP phone illustrations stand in for product photography. Replace those files with final cutouts. They are HTML layers clipped to the subject area, with progress-based parallax, fading and blur. They never become scene textures.

## Debug and validation

- `?debug`: progress slider, FPS and “Use scroll”. The slider sets exact progress; scrolling resumes the smoothed scroll controller.
- `?debug&p=1`: open directly at the World finale for visual review.
- `?debug&test`: runs invariants and reversibility checks against the real scene. Results are in the `#scene-test-results` element and `window.sceneTestReport`.
- `?debug&review&p=0`: exact screenshot pose, debug controls hidden and water time frozen; `body[data-review-ready]` is set after fonts and the rendered frame are ready.
- `?debug&poster`: exercise the WebGL failure path and poster.
- `qa/viewport.html?p=1`: a 390 × 844 preview iframe. Optional `w` and `h` parameters change its real viewport.
- `window.journeyScene` exposes the world, named objects, material registry, rendering statistics and deterministic snapshot for inspection.

The FPS readout reflects browser scheduling, which can be throttled in background or embedded previews. A physical mid-range phone performance test is still recommended before launch.

The 22 October review is in `qa/review-2026-10-22/index.html`: eight ordered five-frame capture sets, a final five-frame phone set, comparisons against `SCENE_SPEC.md`, and 40 passing scene checks. `before.html` is the pre-change source backup, not an independently runnable page.

The World review is in `qa/world-finale/`: six desktop/phone key frames, transition/route captures, contact sheets and 78 scene checks. The pre-globe checkpoint is `v2-before-world-finale`; the completed globe version is `v3-world-finale`.

## Enquiries

No sales address or WhatsApp number was supplied. The working enquiry dialog validates the visitor’s details, then creates a downloadable/copyable text brief. It does not claim to send anything. Wire a verified contact address into this flow before using it for inbound leads. No personal data is stored or transmitted by the current implementation.

## Assets and attribution

- Three.js r160: `vendor/three.min.js`, MIT license in `vendor/THREE-LICENSE.txt`.
- Archivo variable font: `assets/fonts/Archivo.ttf`, SIL Open Font License in `assets/fonts/OFL.txt`.
- Procedural models, poster, phone placeholders and page design are original to this project.
- The editorial pacing and layered composition take inspiration from [Kage](https://mengto.github.io/kage/); no reference-site assets or code are used.

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
| .25 | Pallet loaded; doors close from .23 through .27 |
| .5 | Truck on the curved road, following departure at .30 |
| .75 | Near top-down ship shot over the Gulf |
| 1 | Plane crossing the sea and a calm final frame |

The pallet becomes a child of `Container` at .27. Scrubbing backward reparents it to `World` and reconstructs its world pose without a discontinuity. All named scene objects in the brief are unique `THREE.Group`s. Carton groups carry their corresponding `instanceId`, while the rendered cartons use two shared instanced batches plus labels. Truck and forklift wheels, container ribs, road markings, cartons and ship stacks are instanced.

Six `MeshStandardMaterial` assets are shared throughout: `Mat_Chalk`, `Mat_Asphalt`, `Mat_Gulf`, `Mat_Signal`, `Mat_Haze`, and `Mat_Graphite`. Roughness is 1 and metalness is 0. The shared shaders handle soft contact shadows, the scanner, a tapered wake fade and subtle procedural surface grain without extra materials or texture maps. Signal is authored as exact `#FF5B1F` in sRGB; output is sRGB with no tone mapping. There are two lights, a 2048px desktop / 1024px phone shadow map, and a device-pixel-ratio cap of 2. The scene contains 14,716 triangles and 855 repeated instances.

The perspective camera starts low beside the pallet, then rises and pulls back for loading. Off-axis framing reserves the copy zones. The truck and all its children follow the road centreline and tangent. Its rear doors open 180 degrees and close outward through the .23–.27 interval. The warehouse bay shares the loading axis. The ground extends beyond the camera rather than ending as a display slab.

The page has a 500svh track, a sticky full-height stage, and a fixed full-viewport canvas. Copy switches to the nearest key moment. Desktop copy occupies the left 45%; phone copy sits below the upper subject area. Mobile chapter navigation sits above an 85px bottom safe area. The local SVG poster appears if the library or WebGL fails or a WebGL context is lost.

## Cutouts

The cutout layer is currently **hidden pending 3D approval**. After approval, remove `hidden` from the `.cutouts` element to restore it. See `assets/cutouts/README.md`. Five original transparent WebP phone illustrations stand in for product photography. Replace those files with final cutouts. They are HTML layers clipped to the subject area, with progress-based parallax, fading and blur. They never become scene textures.

## Debug and validation

- `?debug`: progress slider, FPS and “Use scroll”. The slider sets exact progress; scrolling resumes the smoothed scroll controller.
- `?debug&p=.75`: open directly at a key moment for visual review.
- `?debug&test`: runs invariants and reversibility checks against the real scene. Results are in the `#scene-test-results` element and `window.sceneTestReport`.
- `?debug&review&p=0`: exact screenshot pose, debug controls hidden and water time frozen; `body[data-review-ready]` is set after fonts and the rendered frame are ready.
- `?debug&poster`: exercise the WebGL failure path and poster.
- `qa/viewport.html?p=.75`: a 390 × 844 preview iframe. Optional `w` and `h` parameters change its real viewport.
- `window.journeyScene` exposes the world, named objects, material registry, rendering statistics and deterministic snapshot for inspection.

The FPS readout reflects browser scheduling, which can be throttled in background or embedded previews. A physical mid-range phone performance test is still recommended before launch.

The 22 October review is in `qa/review-2026-10-22/index.html`: eight ordered five-frame capture sets, a final five-frame phone set, comparisons against `SCENE_SPEC.md`, and 40 passing scene checks. `before.html` is the pre-change source backup, not an independently runnable page.

## Enquiries

No sales address or WhatsApp number was supplied. The working enquiry dialog validates the visitor’s details, then creates a downloadable/copyable text brief. It does not claim to send anything. Wire a verified contact address into this flow before using it for inbound leads. No personal data is stored or transmitted by the current implementation.

## Assets and attribution

- Three.js r160: `vendor/three.min.js`, MIT license in `vendor/THREE-LICENSE.txt`.
- Archivo variable font: `assets/fonts/Archivo.ttf`, SIL Open Font License in `assets/fonts/OFL.txt`.
- Procedural models, poster, phone placeholders and page design are original to this project.
- The editorial pacing and layered composition take inspiration from [Kage](https://mengto.github.io/kage/); no reference-site assets or code are used.

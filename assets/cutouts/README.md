# Cutout layers

Replace `warehouse.webp`, `loading.webp`, `road.webp`, `sea.webp`, and `air.webp` with transparent cutouts. The current original phone illustrations are placeholders, not product photography. Keep the names to swap them without changing code. PNGs also work: change the corresponding `img src` in `index.html`.

Recommended canvas: 640 × 800 or 960 × 1200, with transparency and a tightly framed subject. These are HTML image layers, never Three.js textures. Each fades and blurs out as the journey advances. The containing element clips them to the right 55% on desktop and the upper subject area on phones.

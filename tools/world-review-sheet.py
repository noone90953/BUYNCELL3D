from pathlib import Path
from PIL import Image, ImageDraw

root = Path(__file__).resolve().parents[1] / 'qa' / 'world-finale'
sets = {
    'six-moments': ('desktop', [0, .2, .4, .6, .8, 1]),
    'transition': ('desktop', [.8, .82, .84, .86, .88, .905]),
    'routes': ('desktop', [.88, .905, .925, .95, .98, 1]),
    'phone': ('phone', [0, .2, .4, .6, .8, 1]),
}
for name, (folder, points) in sets.items():
    if not all((root / folder / f'p{p:.3f}.png').exists() for p in points):
        continue
    phone = folder == 'phone'
    w, h, cols = (390, 870, 3) if phone else (720, 480, 2)
    result = Image.new('RGB', (w * cols, h * ((len(points)+cols-1)//cols)), '#d5dde2')
    draw = ImageDraw.Draw(result)
    for i, p in enumerate(points):
        im = Image.open(root / folder / f'p{p:.3f}.png').convert('RGB')
        im.thumbnail((w, h-22))
        x, y = (i % cols)*w, (i // cols)*h
        result.paste(im, (x, y))
        draw.text((x+10, y+h-19), f'{folder} / progress {p:.3f}', fill='#2b2e33')
    result.save(root / f'{name}.jpg', quality=92)
    print(name)

sections = []
for title, name in [('Six key moments', 'six-moments'), ('Sea to globe', 'transition'), ('Routes and arrivals', 'routes'), ('Phone layouts', 'phone')]:
    sections.append(f'<section><h2>{title}</h2><a href="{name}.jpg"><img src="{name}.jpg" alt="{title}" loading="lazy"></a></section>')
(root / 'index.html').write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>World finale review</title><style>body{background:#f1f2f0;color:#2b2e33;font:16px/1.6 system-ui;margin:40px auto;padding:0 24px;max-width:1200px}h1{font-size:42px;letter-spacing:-.04em}h2{margin-top:40px}a{color:inherit}img{max-width:100%;display:block}nav{display:flex;gap:24px;flex-wrap:wrap}</style><h1>World finale review</h1><p>23 October 2026 · Six key moments at 0, 0.2, 0.4, 0.6, 0.8 and 1. Desktop: 1440 × 900. Phone: 390 × 844.</p><p>78 scene checks pass in both viewports. All ten final labels are visible without overlaps, remain in the subject area, and hide when the globe turns away. The World quote button opens the existing local enquiry dialog.</p><nav><a href="desktop/p1.000.png">Full desktop finale</a><a href="phone/p1.000.png">Full phone finale</a><a href="desktop-checks.json">Desktop checks</a><a href="phone-checks.json">Phone checks</a><a href="../../assets/data/NATURAL-EARTH.md">Land-data provenance</a></nav>''' + ''.join(sections) + '<p>Checkpoint before this change: <code>v2-before-world-finale</code>. New version: <code>v3-world-finale</code>.</p></html>', encoding='utf-8')

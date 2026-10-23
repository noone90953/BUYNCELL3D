from pathlib import Path
from PIL import Image, ImageDraw
import sys

root = Path(__file__).resolve().parents[1] / 'qa' / 'review-2026-10-22'
step = sys.argv[1]
frames = sorted((root / step).glob('p*.png'))
sheet = Image.new('RGB', (1440, 1260), '#e8eae8')
draw = ImageDraw.Draw(sheet)
draw.text((20, 15), step, fill='#2b2e33')
for i, file in enumerate(frames):
    im = Image.open(file).convert('RGB')
    im.thumbnail((710, 390))
    x, y = (i % 2) * 720, 45 + (i // 2) * 405
    sheet.paste(im, (x, y))
    draw.text((x + 12, y + 374), file.stem, fill='#2b2e33')
sheet.save(root / step / 'contact-sheet.jpg', quality=92)
print(root / step / 'contact-sheet.jpg')

"""Create original transparent stand-ins; replace the five WebPs with brand cutouts."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

root = Path(__file__).resolve().parents[1] / 'assets' / 'cutouts'
root.mkdir(exist_ok=True, parents=True)
scale = 3
def make_phone(back=False):
    im = Image.new('RGBA', (180*scale, 340*scale))
    d = ImageDraw.Draw(im)
    def rr(box, radius, fill, outline=None, width=1):
        d.rounded_rectangle(tuple(int(v*scale) for v in box), radius=radius*scale, fill=fill, outline=outline, width=width*scale)
    rr((8,5,172,332),24,'#4A5058')
    rr((11,8,169,329),22,'#D5DDE2' if back else '#2B2E33')
    if back:
        rr((21,20,87,91),15,'#b9c3ca')
        for x,y in [(29,28),(57,55)]:
            d.ellipse((x*scale,y*scale,(x+23)*scale,(y+23)*scale), fill='#2B2E33')
            d.ellipse(((x+6)*scale,(y+6)*scale,(x+17)*scale,(y+17)*scale), fill='#4A5058')
        d.ellipse((65*scale,29*scale,75*scale,39*scale),fill='#F1F2F0')
        rr((76,173,104,210),6,'#bbc5cd')
    else:
        rr((17,15,163,321),17,'#e6ebec')
        d.ellipse((-35*scale,120*scale,170*scale,360*scale),fill='#D5DDE2')
        d.ellipse((58*scale,68*scale,230*scale,280*scale),fill='#c0cdd5')
        rr((62,21,118,33),6,'#2B2E33')
        rr((69,309,111,313),2,'#4A5058')
    return im

for index,name in enumerate(['warehouse','loading','road','sea','air']):
    canvas = Image.new('RGBA',(320*scale,400*scale))
    back=make_phone(True).resize((145*scale,274*scale)).rotate(14,resample=Image.Resampling.BICUBIC,expand=True)
    front=make_phone().resize((148*scale,280*scale)).rotate(-10,resample=Image.Resampling.BICUBIC,expand=True)
    canvas.alpha_composite(back,(8*scale,30*scale))
    canvas.alpha_composite(front,(120*scale,80*scale))
    canvas.resize((320,400),Image.Resampling.LANCZOS).save(root/(name+'.webp'),quality=90)
print('Created five transparent WebP placeholders.')

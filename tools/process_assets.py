"""Derive optimised web assets from the untouched capture (read-only source)."""
import json, os
from PIL import Image

SRC = '/home/claude/work/noraengineers-mirror/site_mirror/wp-content/uploads/2018'
ROOT = '/home/claude/nora-redesign'
OUT = f'{ROOT}/site/assets/img'

jobs = {  # name: (source file, target widths; [0] = keep native width)
    'res-bedroom-1': ('09/1-1.jpg', [800, 1600]), 'res-bedroom-2': ('09/2-1.jpg', [800, 1600]),
    'res-bedroom-3': ('09/3-1.jpg', [800, 1600]), 'res-dressing': ('09/4-1.jpg', [800, 1600]),
    'res-bath-1': ('09/5-1.jpg', [800, 1600]), 'res-bath-2': ('09/6-1.jpg', [800, 1600]),
    'res-bath-3': ('09/7-1.jpg', [800, 1600]), 'res-bath-4': ('09/8-1.jpg', [800, 1600]),
    'com-cafe-1': ('11/PHOTO-2018-11-04-12-23-27.jpg', [0]), 'com-cafe-2': ('11/PHOTO-2018-11-04-12-23-28.jpg', [0]),
    'com-cafe-3': ('11/PHOTO-2018-11-04-12-23-28_1.jpg', [0]), 'com-cafe-4': ('11/PHOTO-2018-11-04-12-23-28_2.jpg', [0]),
    'com-cafe-5': ('11/PHOTO-2018-11-04-12-23-29.jpg', [0]), 'com-cafe-6': ('11/PHOTO-2018-11-04-12-23-29_1.jpg', [0]),
    'com-cafe-7': ('11/PHOTO-2018-11-04-12-23-30.jpg', [0]), 'com-cafe-8': ('11/PHOTO-2018-11-04-12-23-31.jpg', [0]),
    'com-cafe-9': ('11/PHOTO-2018-11-04-12-23-31_1.jpg', [0]), 'com-cafe-10': ('11/PHOTO-2018-11-04-12-23-32.jpg', [0]),
    'office-sign': ('10/PHOTO-2018-10-15-13-08-28.jpg', [0]), 'office-lounge': ('10/IMG_0106.jpg', [0]),
    'office-meeting': ('10/IMG_0116.jpg', [0]), 'office-open': ('10/IMG_0118.jpg', [0]),
    'office-glass': ('10/IMG_0055.jpg', [0]),
}

man = {}
for name, (src, ws) in jobs.items():
    im = Image.open(f'{SRC}/{src}').convert('RGB')
    W, H = im.size
    man[name] = {'w': W, 'h': H, 'sizes': []}
    for w in ws:
        tw = min(w, W) if w else W
        th = round(H * tw / W)
        suffix = f'-{tw}' if w else ''
        r = im.resize((tw, th), Image.LANCZOS) if tw != W else im
        fn = f'{name}{suffix}.webp'
        r.save(f'{OUT}/{fn}', 'WEBP', quality=80, method=6)
        man[name]['sizes'].append([fn, tw])

# Brand mark (gold "n" on transparent) -> small web sizes + favicons
raw = Image.open(f'{SRC}/10/n.png').convert('RGBA')
bb = raw.getbbox()
raw = raw.crop(bb)


def square(im, s, pad=0.14):
    c = Image.new('RGBA', (s, s), (0, 0, 0, 0))
    k = s * (1 - 2 * pad) / max(im.size)
    r = im.resize((round(im.width * k), round(im.height * k)), Image.LANCZOS)
    c.paste(r, ((s - r.width) // 2, (s - r.height) // 2), r)
    return c


mark = raw.copy()
mark.thumbnail((240, 240), Image.LANCZOS)
mark.save(f'{OUT}/mark.webp', 'WEBP', quality=90)
man['mark'] = {'w': mark.width, 'h': mark.height}
for s, fn in [(32, 'favicon-32.png'), (180, 'apple-touch-icon.png'), (512, 'icon-512.png')]:
    square(raw, s).save(f'{OUT}/{fn}')

# Open Graph share image 1200x630 (bedroom visualisation crop + brand mark)
b = Image.open(f'{SRC}/09/1-1.jpg').convert('RGB')
w = 1200
h = round(b.height * w / b.width)
b = b.resize((w, h), Image.LANCZOS)
top = max(0, (h - 630) // 2 - 40)
og = b.crop((0, top, 1200, top + 630)).convert('RGBA')
og.alpha_composite(square(raw, 120, 0.1), (48, 462))
og.convert('RGB').save(f'{OUT}/og-share.jpg', quality=84)

json.dump(man, open(f'{ROOT}/tools/manifest.json', 'w'), indent=1)
print(sum(os.path.getsize(f'{OUT}/{f}') for f in os.listdir(OUT)) // 1024, 'KB images')

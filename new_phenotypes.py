#!/usr/bin/env python3

import sys
from PIL import Image, ImageDraw, ImageFont

mainfont = ImageFont.truetype('DejaVuSansMono.ttf', 18)
sidefont = ImageFont.truetype('DejaVuSansMono-Oblique.ttf', 18)

def base_image(code):
    code = code.strip('\n')
    prefix = " ... other lines of code"
    suffix = " ... other lines of code"
    img = Image.new('RGB', (500, 200), color='white')
    d = ImageDraw.Draw(img)
    tc,oc,cc = 'black','darkgray','indianred'
    sx, sy = 5, 15
    cw, ch = 11, 18             # char width, char height
    lh = 18 + 3                 # line height
    d.text((sx, sy),text=prefix, fill=oc, font=sidefont)
    d.text((sx, sy+1*lh),text=' ...', fill=oc, font=sidefont)
    d.text((sx, sy+2*lh),text=' else:', fill=tc, font=mainfont)
    d.text((sx+6*cw, sy+2*lh),text=' # ")tipple', fill=cc, font=mainfont)
    d.text((sx, sy+3*lh),text='  print("silliness")', fill=tc, font=mainfont)
    d.text((sx+20*cw,sy+3*lh),text='# fd',fill=cc, font=mainfont)
    d.text((sx, sy+5*lh),     text=suffix, fill=oc, font=sidefont)
    return img

def narration(img, text):
    d = ImageDraw.Draw(img)
    _, _, width, _ = d.textbbox((0,0), text=text, font=mainfont, align='left')
    nx, ny = (img.width - width) // 2, 160
    d.text((nx,ny), text=text, font=mainfont, fill='blue', align='left')
    return img

def save(img, filename):
    img.save(filename)
    print(filename)

if __name__ == '__main__':
    code = ''' else:#  ") tipple
  print("silliness")# print("friend")'''
    img = base_image(code)
    save(img, 'sample0.gif')
    n1 = narration(img.copy(), 'an initial state')
    save(n1, 'sample1.gif')
    n2 = narration(img.copy(), 'comment line, locus for neutral mutations')
    save(n2, 'sample2.gif')

## new_phenotypes.py ends here

#!/usr/bin/env python3

import sys
from PIL import Image, ImageDraw, ImageFont
from mutation_simulator import mutation_simulator

mainfont = ImageFont.truetype('DejaVuSansMono.ttf', 18)
sidefont = ImageFont.truetype('DejaVuSansMono-Oblique.ttf', 18)

sx, sy = 5, 15
tc, oc, cc = 'black', 'darkgray', 'indianred'
sx, sy = 5, 15
cw, ch = 11, 18             # char width, char height
lh = 18 + 3                 # line height

def base_image(comment=''):
    if not comment: comment = '# pt'
    prefix = " ... other lines of code elided"
    suffix = prefix
    img = Image.new('RGB', (560, 200), color='white')
    d = ImageDraw.Draw(img)
    d.text((sx, sy+0*lh), prefix, fill=oc, font=sidefont)
    d.text((sx, sy+1*lh), ' else:', fill=tc, font=mainfont)
    d.text((sx+6*cw, sy+1*lh), ' ... elided', fill=oc, font=sidefont)
    d.text((sx, sy+2*lh), '  print("dissent")', fill=tc, font=mainfont)
    d.text((sx+20*cw, sy+2*lh), comment, fill=cc, font=mainfont)
    d.text((sx, sy+4*lh), suffix, fill=oc, font=sidefont)
    return img

def narration(img, text, d):
    d.rectangle((0, 159, img.width, img.height), outline='white', fill='white')
    nx, ny = 5, 160
    d.text((nx, ny), ' '+text, font=mainfont, fill='blue', align='left')

def draw(img, msg, *lambdas):
    d = ImageDraw.Draw(img)
    narration(img, msg, d)
    for lambd_ in lambdas:
        lambd_(d)

if __name__ == '__main__':
    imgs = [(base_image(), 500)]

    imgs.append((imgs[-1][0].copy(), 1000))
    draw(imgs[-1][0], 'an initial state')

    imgs.append((imgs[-1][0].copy(), 1000))
    draw(imgs[-1][0], 'comment section',
         lambda d: d.line((59, 158, 232, 67), fill='green', width=2))

    imgs.append((imgs[0][0].copy(), 2000))
    draw(imgs[-1][0], 'suppose the following mutations occur')

    imgs.append((base_image('#  print("instill") #"de f)t:)'), 2000))
    draw(imgs[-1][0], 'suppose the following mutations occur')

    target = '#  print("instill") #"de f)t:)'
    start  = '# _p___t______________________'
    ms = mutation_simulator(target, start)

    mutations = []
    durations = []
    for val in ms.animate():
        img = base_image(val)
        draw(img, 'suppose the following mutations occur')
        mutations.append(img)
        durations.append(500)

    durations[-1] *= 10
    mutations[0].save(
        'result.gif',
        save_all=True,
        append_images=mutations[1:],
        duration=durations,
        include_color_table=False,
        loop=2)

    imgs.append((base_image('#'), 2000))
    draw(imgs[-1][0], 'A mutation adds a newline',
         lambda d: d.text((sx,sy+3*lh),'  print("instill")', fill=tc, font=mainfont),
         lambda d: d.text((sx+19*cw,sy+3*lh),'#"de f)t:)', fill=cc, font=mainfont))

    imgs.append((base_image('#  print("instill") #"de f)t:)'), 2000))
    draw(imgs[-1][0], 'A mutation adds a newline')

    imgs.append((base_image('#↲ print("instill") #"de f)t:)'), 2000))
    draw(imgs[-1][0], 'A mutation adds a newline')

    for i, (img, delay) in enumerate(imgs):
        filename = f'behavior_{i:03d}.gif'
        img.save(filename)
        print(filename)
    
## new_phenotypes.py ends here

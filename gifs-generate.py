#!/usr/bin/env python3

from generate import corpus, get_category, get_catprefix
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

def read_results(resultsin):
    data0 = defaultdict(lambda: dict())
    data1 = defaultdict(lambda: dict())
    for line in resultsin.readlines():
        cat, idx, res0, res1 = line.strip().split(',')
        data0[cat][int(idx)-1] = (res0 == 'SUCCESS')
        data1[cat][int(idx)-1] = (res1 == 'SUCCESS')
    return data0, data1

def save(coretext, index, char, imgdims, saveas, font, color, spacing=1):
    sx, sy = 5, 10
    img = Image.new('RGB', imgdims, color='white')
    d = ImageDraw.Draw(img)
    draw = lambda txt: d.multiline_text(
                xy=(sx, sy), text=txt,
                font=font, fill='black', spacing=spacing)
    draw(coretext[:index] + ' ' + coretext[index:])
    wid, hei = d.textsize('x', font=font)
    row, col = 0, 0
    for i, c in enumerate(coretext):
        if i == index: break
        col += 1
        if c == '\n':
            row, col = row + 1, 0
    ox, oy = col*wid, row*(hei+spacing)
    #print(f'idx,c,(row,col),color={index},"{char}",{(row,col)},{color}')
    d.text(xy=(ox + sx, oy + sy), text=char, fill=color, font=font)
    img.save(saveas)

def gifs_generate(corpus, category, chars, font, results):
    valiter = iter(infinite(chars))
    for i in range(len(corpus)):
        char = next(valiter)
        save(
            coretext=corpus,
            index=i,
            char=char,
            imgdims=(200, 280),
            saveas=f'imgs/{category}_{i:#03d}.png',
            font=font,
            color='green' if results[i] else 'red')

class infinite(object):
    def __init__(self, iterable):
        self._iterable = iterable
    def __iter__(self):
        self._iterator = iter(self._iterable)
        return self
    def __next__(self):
        try:
            val = next(self._iterator)
        except StopIteration:
            self._iterator = iter(self._iterable)
            val = next(self._iterator)
        return val
        
if __name__ == '__main__':
    import sys
    category = sys.argv[1]
    results_strm = open(sys.argv[2]) if len(sys.argv) > 2 else sys.stdin
    fontfile = 'DejaVuSansMono.ttf'
    font = ImageFont.truetype(fontfile, 18)
    code = corpus('code.py')
    imgsize = (200, 280)
    table = defaultdict(lambda: set())
    for c in set(code):
        cat = get_category(c)
        prefix = get_catprefix(cat)
        if c == ' ': c = '█'
        if c == '\n': c = '↲'
        table[prefix].add(c)
    data0, data1 = read_results(results_strm)
    gifs_generate(code, category, table[category], font, data0[category])

## gifs-generate.py ends here

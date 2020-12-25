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

def index_coords(text, idx):
    row, col = (0, 0)
    for i, c in enumerate(text):
        if i == idx: break
        col += 1
        if c == '\n': row, col = row+1, 0
    return row, col

def save(coretext, index, char, imgdims, saveas, font, color, chardims, footer):
    spacing = 1
    sx, sy = 5, 10
    img = Image.new('RGB', imgdims, color='white')
    d = ImageDraw.Draw(img)
    draw = lambda txt: d.multiline_text(
                xy=(sx, sy), text=txt,
                font=font, fill='black', spacing=spacing)
    draw(coretext[:index] + ' ' + coretext[index:])
    wid, hei = chardims
    row, col = index_coords(coretext, index)
    ox, oy = col*wid, row*(hei+spacing)
    d.text(xy=(ox + sx, oy + sy), text=char, fill=color, font=font)
    ## write footer
    fx, fy = sx, imgdims[-1] - sy - chardims[-1]
    d.text(xy=(fx, fy), text=footer, fill=color, font=font)
    img.save(saveas)

def gifs_generate(corpus, imgdims, filenamefn, chars, font, results, footerfn):
    chardims = canvas_size('x', font)
    for i in range(len(corpus)):
        save(
            coretext=corpus,
            index=i,
            char=next(chars),
            imgdims=imgdims,
            saveas=filenamefn(i),
            font=font,
            color='green' if results[i] else 'red',
            chardims=chardims,
            footer=footerfn(i))

def canvas_size(text, font):
    img = Image.new('RGB', (1, 1), color='white')
    d = ImageDraw.Draw(img)
    bbox = d.multiline_textbbox(xy=(0, 0), text=text, font=font, align="left")
    return bbox[2:]

class infinite(object):
    '''Infinite stream over the given iterable.  Throws exception if
iterable is empty otherwise continues streaming it forever.

    >>> inf = infinite([1,2,3])
    >>> [i for i, j in zip(inf, range(10))]
    [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]
    '''
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
    width, height = canvas_size(code, font)
    nearest_mult = lambda x, n: x + (n - x % n)
    width = nearest_mult(width, 100)
    height = nearest_mult(height, 100)
    imgsize = (width, height)
    table = defaultdict(lambda: set())
    for c in set(code):
        cat = get_category(c)
        prefix = get_catprefix(cat)
        if c == ' ': c = '█'
        if c == '\n': c = '↲'
        table[prefix].add(c)
    data0, data1 = read_results(results_strm)
    filenamer0 = lambda i: f'imgs/{category}_0_{i:#03d}.png'
    footer0 = lambda i: f'n=0    pos: {i}'
    chars = iter(infinite(table[category]))
    gifs_generate(code, imgsize, filenamer0, chars, font, data0[category], footer0)
    filenamer1 = lambda i: f'imgs/{category}_1_{i:#03d}.png'
    footer1 = lambda i: f'n=1    pos: {i}'
    gifs_generate(code, imgsize, filenamer1, chars, font, data1[category], footer1)

## gifs-generate.py ends here

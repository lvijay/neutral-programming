#!/usr/bin/env python3

from generate import corpus, get_category, get_catprefix
from collections import defaultdict
from PIL import Image, ImageDraw, ImageFont

class infinite(object):
    '''Infinite stream over the given iterable.  Throws exception if
iterable is empty otherwise continues streaming it forever.

    >>> inf = infinite([1,2,3])
    >>> [i for i, j in zip(inf, range(10))]
    [1, 2, 3, 1, 2, 3, 1, 2, 3, 1]
    '''
    @staticmethod
    class iinfinite(object):
        def __init__(self, iterable):
            self._iterable = iterable
            self._iterator = iter(iterable)
        def __next__(self):
            try:
                return next(self._iterator)
            except StopIteration:
                self._iterator = iter(self._iterable)
                return next(self._iterator)
    def __init__(self, iterable): self._iterable = iterable
    def __iter__(self): return infinite.iinfinite(self._iterable)

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

def nearest_mult(x, n):
    '''same as math.ceil but for ints'''
    return x + (n - x % n)

class Animate(object):
    def __init__(self, text, font):
        self._text = text
        self._font = font
        self._chardims = self._size('x')
        w, h = self._size(self._text)
        self._xgap = 30
        self._text_width = nearest_mult(w, 100)
        self._width = self._xgap + 2 * self._text_width
        self._height = nearest_mult(h, 100)
        self._line_spacing = 1
    def _size(self, text):
        img = Image.new('RGB', (1, 1), color='white')
        d = ImageDraw.Draw(img)
        bbox = d.multiline_textbbox((0,0), text, font=self._font, align="left")
        w, h = bbox[2:]
        return w, h
    def generate(self, outfile, chars, results, footerfns):
        # hack
        clrs0 = ['green' if results[0][i] else 'red' for i in range(len(results[0]))]
        clrs1 = ['green' if results[1][i] else 'red' for i in range(len(results[1]))]
        imgs = [self.save(i, char, (clr0, clr1), (footerfns[0](i), footerfns[1](i)))
                for i, (char, clr0, clr1) in enumerate(zip(chars, clrs0, clrs1))]
        return imgs[0].save(outfile,
                            save_all=True,
                            append_images=imgs[1:],
                            optimize=False,
                            duration=200,
                            loop=0)
    def save(self, index, char, colors, footers):
        img = Image.new('RGB', (self._width, self._height), color='white')
        offsetfn = lambda i: 5 + self._xgap + self._text_width * i
        yoff = 10
        for i, (clr, footer) in enumerate(zip(colors, footers)):
            self.draw(img, index, char, clr, footer, (offsetfn(i), yoff))
        return img
    def draw(self, img, index, char, color, footer, offset):
        sx, sy = offset
        d = ImageDraw.Draw(img)
        d.multiline_text(
            xy=(sx, sy),
            text=self._text[:index] + ' ' + self._text[index:],
            font=font,
            fill='black',
            spacing=self._line_spacing)
        wid, hei = self._chardims
        row, col = index_coords(self._text, index)
        ox, oy = sx + col*wid, sy + row*(hei+self._line_spacing)
        d.text(xy=(ox, oy), text=char, fill=color, font=font)
        ## write footer
        fx, fy = sx, self._height - sy - self._chardims[-1]
        d.text(xy=(fx, fy), text=footer, fill=color, font=font)
        return img

if __name__ == '__main__':
    import sys
    results_strm = open(sys.argv[1]) if len(sys.argv) > 2 else sys.stdin
    categories = sys.argv[2:]

    fontfile = 'DejaVuSansMono.ttf'
    font = ImageFont.truetype(fontfile, 18)

    code = corpus('code.py')

    table = defaultdict(lambda: set())
    for c in set(code):
        cat = get_category(c)
        prefix = get_catprefix(cat)
        if c == ' ': c = '▢'
        if c == '\n': c = '↲'
        table[prefix].add(c)
    data = read_results(results_strm)
    animater = Animate(code, font)
    for category in categories:
        chars = infinite(table[category])
        outfile = f'animate_{category}.gif'
        results = data[0][category], data[1][category]
        footerfns = (lambda i: f'n=0    pos: {i}'), (lambda i: f'n=1    pos: {i}')
        animater.generate(outfile, chars, results, footerfns)
        print(outfile)

### Run Instructions ###
# time -p ./gifs-generate.py py_results.data `ls python | cut -f1 -d '_' | sort | uniq` | xargs -t -n1 -I{} gifsicle -l0 -d50 -O3 {} -o o{}

## gifs-generate.py ends here

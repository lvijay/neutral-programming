#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import random

class randomizer(object):
    def __init__(self, target, start, r=random.Random()):
        if len(target) != len(start):
            raise ValueError('lengths should be equal')
        self._target = target
        self._rand = r
        self._placeholder = [('' if c == '_' else c) for i,c in enumerate(start)]
        self._shuffled    = list(range(len(start)))
    def shuffled(self):
        shuffled = self._shuffled[::]
        placeholder = self._placeholder[::]
        self._rand.shuffle(shuffled)
        tos = lambda: ''.join(placeholder)
        yield tos()
        for i in shuffled:
            placeholder[i] = self._target[i]
            yield tos()

def get_size(text, offset, font):
    img = Image.new('RGB', (1, 1), color='white')
    d = ImageDraw.Draw(img)
    size = d.multiline_textbbox(offset, text, font=font)[2:]
    return size

def generate(text, size, mainfont, offset):
    oimg = Image.new('RGB', size, color='white')
    rander = randomizer(target, '_' * len(text))
    values = [val for val in rander.shuffled()]
    imgs = [oimg.copy() for _ in values]
    for img, val in zip(imgs, values):
        ImageDraw.Draw(img).text(offset, val, fill='black', font=mainfont)
    return imgs

def intervals(images, total_time_ms, last_frame_ms):
    frame_ms = (total_time_ms - last_frame_ms - 1) // len(images)
    remainder = total_time_ms - last_frame_ms - frame_ms * (len(target) - 1)
    durations = [frame_ms] * (len(images) - 1) + [last_frame_ms + remainder]
    return durations

if __name__ == '__main__':
    import sys
    total_time_ms = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    last_frame_ms = int(sys.argv[2]) if len(sys.argv) > 2 else 1000
    target = sys.stdin.read()
    start  = '_' * len(target)
    nearest_mult = lambda x, n: x + (n - x % n)
    mainfont = ImageFont.truetype('DejaVuSansMono.ttf', 18)
    offset = (5, 5)
    size = tuple([nearest_mult(x, 15) for x in get_size(target, offset, mainfont)])
    images = generate(target, size, mainfont, offset)
    durations = intervals(images, total_time_ms, last_frame_ms)
    images[0].save(
        'result.gif',
        save_all=True,
        append_images=images[1:],
        duration=durations,
        include_color_table=False,
        loop=2)

## Generate emerging GIF images
## Usage:
## echo -e 'the quick\nbrown fox\njumps' | ./emergif.py 10000 2000
##
## emergif reads the text from stdin
## - argument 1 is total time (in ms) for the gif to run
## - argument 2 is the time for the final image that shows the text

## emergif.py ends here

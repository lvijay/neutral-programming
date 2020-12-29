#!/usr/bin/env python3

from collections import defaultdict
from generate import corpus
import importlib
gifs_generate = importlib.import_module('gifs-generate')

class linecounter(object):
    def __init__(self, corpus):
        self._linenums = [i for i, c in enumerate(corpus) if c == '\n']
    def linenum(self, index):
        for i, linechar in enumerate(self._linenums):
            if index <= linechar:
                return i+1      # because line numbers start at 1
        raise ValueError('Exceeds corpus')

if __name__ == '__main__':
    import sys
    with open('py_results.data') as results_strm:
        data0, data1 = gifs_generate.read_results(results_strm)
    code = corpus('code.py')
    lc = linecounter(code)
    linemap = dict([(i, lc.linenum(i)) for i in range(len(code))])

    successes = defaultdict(lambda: 0)
    failures  = defaultdict(lambda: 0)
    alldata = ([(k, '0', v) for k, v in data0.items()]
            + [(k, '1', v) for k, v in data1.items()])
    keyfn = lambda c, v, j: f'{c} | {linemap[j]:02d}'
    #keyfn = lambda c, v, j: f'{c} | {v} | {linemap[j]:02d}'
    allkeys = set()
    for category, value, runresults in alldata:
        for i, rr in runresults.items():
            key = keyfn(category, value, i)
            allkeys.add(key)
            ## unreadability alert
            (successes if rr else failures)[key] += 1
    for catline in allkeys:
        print(f'| {catline} | {failures[catline]} | {successes[catline]} |')

## Run instructions
# ./errors-by-line.py | sort | sed -Ee 's/0([0-9])/ \1/g' > line_results.org

## errors-by-line.py ends here

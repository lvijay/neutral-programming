#!/usr/bin/env python3

CATEGORIES = {'␠': set(' '),
              '␤': set('\n'),
              'α': set('s p l i n t e r f d'.split()),
              '#': set('#'),
              '(': set('('),
              ')': set(')'),
              '"': set('"'),
              ':': set(':')}

CAT_PREFIX = {'␠': 'space',
              '␤': 'nline',
              'α': 'alpha',
              '#': 'pound',
              '(': 'preno',
              ')': 'prenc',
              '"': 'dquot',
              ':': 'colon'}

def corpus(filename):
    with open(filename) as fn:
        return fn.read()

def generate(filename):
    data = corpus(filename)
    width = len(str(len(data) * len(CATEGORIES)))
    for k, v in CATEGORIES.items():
        fileprefix = CAT_PREFIX[k]
        candidate = next(iter(v))
        for i in range(len(data)):
            prefix, suffix = data[:i], data[i:]
            filename = fileprefix + f'{i:#0{width}d}.py'
            with open(filename, 'w') as out:
                out.write(prefix + candidate + suffix)

if __name__ == '__main__':
    import sys
    generate(sys.argv[1])

## generate.py ends here

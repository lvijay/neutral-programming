#!/usr/bin/env python3

import os.path

def corpus(filename):
    with open(filename) as fn:
        return fn.read()

def get_category(char):
    if char.isalpha(): return 'α'
    if char.isdigit(): return '𝓃'
    if char in ' ': return '␠'
    if char in '\n': return '␤'
    return char              # other characters are their own category

def get_catprefix(category):
    return {
        'α': 'alphabet',
        '𝓃': 'digit',
        '␠': 'space',
        '␤': 'newline',
        '(': 'paren-open',
        ')': 'paren-close',
        '_': 'underscore',
        '"': 'dquote',
        "'": 'squote',
        '#': 'hash',
        ':': 'colon'
    }[category]

def generate(filename, odir, vals, exec_content_fn):
    data = corpus(filename)
    categories = dict(map(lambda c: (get_category(c), c), data))
    ext = filename[filename.index('.')+1:] # extension
    for k, v in categories.items():
        fileprefix = get_catprefix(k)
        candidate = next(iter(v))
        for i in range(1, 1+len(data)):
            prefix, suffix = data[:i], data[i:]
            filename = lambda c, v: f'{fileprefix}_{c}_{v}.{ext}'
            content = prefix + candidate + suffix
            for val in vals:
                fname = filename(i, val)
                exec_content = exec_content_fn(val)
                with open(os.path.join(odir, fname), 'w') as out:
                    print(prefix + candidate + suffix, file=out)
                    print(exec_content, file=out)

if __name__ == '__main__':
    import sys
    i = 1
    inputfile, i = sys.argv[i], i+1
    outputdir, i = (sys.argv[i], i+1) if len(sys.argv) >= 2 else ('.', i)
    ispy = inputfile.endswith('.py')
    vals = '01' if ispy else ('nil', '1')
    efn = (lambda x: f'\ndin({x})') if ispy else (lambda x: f'\ndeed {x}')
    generate(inputfile, outputdir, vals, efn)

## generate.py ends here

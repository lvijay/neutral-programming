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
    if char in '{([])}': return '⌶'
    return char              # other characters are their own category

def get_catprefix(category):
    return {
        'α': 'alphabet',
        '𝓃': 'digit',
        '␠': 'space',
        '␤': 'newline',
        '_': 'underscore',
        '"': 'dquote',
        "'": 'squote',
        '#': 'hash',
        ':': 'colon',
        ';': 'semicolon',
        '?': 'qmark',
        '/': 'slash',
        '\\': 'backslash',
        '⌶': 'enclosed'         # all paren family chars
    }[category]

def get_category_representative(categories, k):
    if k == '/': return '//'    # should be mode specific...
    return next(iter(categories[k]))

def generate(filename, odir, vals, exec_content_fn):
    data = corpus(filename)
    categories = dict(map(lambda c: (get_category(c), c), data))
    ext = filename[filename.index('.')+1:] # extension
    for k in categories.keys():
        fileprefix = get_catprefix(k)
        candidate = get_category_representative(categories, k)
        for i in range(len(data)):
            prefix, suffix = data[:i], data[i:]
            filename = lambda c, v: f'{fileprefix}_{c}_{v}.{ext}'
            content = prefix + candidate + suffix
            for val in vals:
                fname = filename(i+1, val)
                exec_content = exec_content_fn(val)
                with open(os.path.join(odir, fname), 'w') as out:
                    print(prefix + candidate + suffix, file=out)
                    print(exec_content, file=out)

if __name__ == '__main__':
    import sys
    i = 1
    inputfile, i = sys.argv[i], i+1
    outputdir, i = (sys.argv[i], i+1) if len(sys.argv) >= 2 else ('.', i)
    vals, efn = None, None
    extension = inputfile[inputfile.find('.'):]
    if extension == '.py':
        vals = '01'
        efn = lambda x: f'\ndin({x})'
    elif extension == '.rb':
        vals = ('nil', '1')
        efn = lambda x: f'\ndeed {x}'
    elif extension == '.c':
        vals = '01'
        efn = lambda x: '\nmain(){pees(' + f'{x}' + ');}'
    else:
        raise ValueError('Unknown filetype: ' + extension)
    generate(inputfile, outputdir, vals, efn)

## generate.py ends here

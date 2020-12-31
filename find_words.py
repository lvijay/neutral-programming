#!/usr/bin/env python3

from collections import defaultdict
from itertools import takewhile

def build(filename):
    words = defaultdict(lambda: [])
    with open(filename) as inf:
        while (line := inf.readline()):
            word = line.strip()
            if any((not (c.isalpha() and c.islower()) for c in word)):
                continue
            key = ''.join(set(word))
            words[key] += [word]
    return [(set(k), w) for k, w in words.items()]

if __name__ == '__main__':
    import sys
    dictfile = '/usr/share/dict/words'
    dictionary = build(dictfile)
    chars = sys.argv[1]
    scars = set(chars)
    for k, words in dictionary:
        if k <= scars: print('\n'.join(words))

## Run instructions
# for word in `./find_words.py ifelseprintdef`; do printf "%d %s\n" `echo -n $word | wc -c` "$word"; done | sort -n -k1 | tee possible_words

## find_words.py ends here

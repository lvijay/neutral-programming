import random

class mutation_simulator(object):
    def __init__(self, target, start, r=random.Random()):
        if len(target) != len(start):
            raise ValueError('lengths should be equal')
        self._target = target
        self._rand = r
        self._placeholder = [('' if c == '_' else c) for i,c in enumerate(start)]
        self._shuffled    = [(i if s == '_' else -1) for i,s in enumerate(start)]
    def animate(self):
        shuffled = self._shuffled[::]
        placeholder = self._placeholder[::]
        self._rand.shuffle(shuffled)
        tos = lambda: ''.join(filter(None, placeholder))
        yield tos()
        for i in shuffled:
            if i == -1: continue
            placeholder[i] = self._target[i]
            yield tos()

if __name__ == '__main__':
    target = ' print("instill") #"de f)t:)'
    start  = ' p___t______________________'
    ms = mutation_simulator(target, start)
    for val in ms.animate():
        print(val)

## mutation_simulator.py ends here

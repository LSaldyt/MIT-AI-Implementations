from ..util   import timedblock, timeout, sign
from ..search.methods import *

from .systems     import logic
from .theoremnode import TheoremNode
from .            import heuristics

from pprint      import pprint
from random      import choice
from collections import OrderedDict
from functools   import partial

def produce_theorems(start, branches, depth):
    theorems = {start}
    for i in range(depth):
        new_theorems = set()
        for t in theorems:
            new_theorems.update(set(branches(t)))
        theorems.update(new_theorems)

    to_show = set()
    for t in theorems:
        if isinstance(t, tuple):
            to_show.add(t[-1])
        else:
            to_show.add(t)
    pprint(to_show)

def create_random_proof(start, branches, depth):
    last = start
    for i in range(depth):
        last = choice(list(branches(last)))
    return last 

def test_algo(a, start, end):
    from inspect import getfullargspec
    args = getfullargspec(a).args
    if 'distance' not in args:
        with timedblock(a.__name__):
            result = a(logic.branches, start, end)
    else:
        with timedblock(a.__name__):
            result = a(logic.branches, start, end, 
                    distance=heuristics.hamming_len_dist)
    for i, step in enumerate(result):
        print('{:>5}: {}'.format(i + 1, step))

def compare_algos():
    start = TheoremNode('R.(~P⊃Q)')
    end   = TheoremNode('(QvP).R')
    print('Difference engine demonstration:')
    with timedblock('proof'):
        result = logic.prove(start, end)
    for i, step in enumerate(result):
        print('{:>5}: {}'.format(i + 1, step))
    test = partial(test_algo, start=start, end=end)
    test(branch_and_bound)
    test(depth_first)
    test(breadth_first)
    test(breadth_first_2)
    test(hill_climbing)
    test(beam_search)
    test(branch_and_bound)
    test(astar)

def demo():
    compare_algos()

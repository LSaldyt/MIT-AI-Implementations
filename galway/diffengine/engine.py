from ..search   import branch_and_bound, astar
from ..util     import timedblock, timeout, sign

from .diff_search import alt_astar, diff_search
from .systems     import logic
from .problem     import Problem, solve
from .            import heuristics

from .compare_heuristics import compare_heuristics

from pprint      import pprint
from random      import choice
from collections import OrderedDict

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

'''
def create_random_proof(start, branches, depth):
    last = start
    for i in range(depth):
        last = choice(list(branches(last)))
    return last 

def random_compare(amount, depth=3):
    seen = set()
    start = 'R.(~P⊃Q)'
    problems = []
    for i in range(amount):
        last = create_random_proof(start, logic.branches, depth)
        while last in seen:
            last = create_random_proof(start, logic.branches, depth)
        problems.append(Problem(start, last, logic))
        seen.add(last)
    pprint(problems)
    compare_heuristics(problems)
'''

#print(diff_search(start, end, diffList, transformers))

def demo():
    produce_theorems('P⊃Q', logic.branches, 4)
    #diff_search('P⊃Q', 'Qv~P', logic)
    print('Difference engine demonstration:')
    p = Problem('P⊃Q', 'Qv~P', logic)
    v = heuristics.hamming_dist
    with timedblock('proof'):
        result = solve(p, v)
    for i, step in enumerate(result):
        print('{:>5}: {}'.format(i + 1, step))

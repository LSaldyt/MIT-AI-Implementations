from ..search   import branch_and_bound, astar
from ..util     import timedblock, timeout, sign

from .diff_search import diff_search
from .mu          import mu
from .logic       import logic
from .problem     import Problem
from .system      import System
from .            import heuristics

from .compare_heuristics import compare_heuristics

from pprint      import pprint

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

def demo():
    print('Difference engine demonstration:')
    p = Problem('R.(~P⊃Q)', '(QvP).R', logic)
    #v = heuristics.alt_theorem_dist
    v = heuristics.hamming_dist
    with timedblock('proof'):
        result = astar(logic.branches, p.start, p.goal, distance=v)
    for i, step in enumerate(result):
        print('{:>5}: {}'.format(i + 1, step))

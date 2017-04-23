from ..search   import branch_and_bound, breadth_first, breadth_first_2, astar 
from ..util     import timedblock, ztest, to_p, timeout

from .mu import mu_branches
from .logic import logic_branches, subterms

from . import heuristics

from statistics import mean
from pprint     import pprint

def produce_theorems(start, branches, depth):
    theorems = {start}
    for i in range(depth):
        new_theorems = set()
        for t in theorems:
            new_theorems.update(set(branches(t)))
        theorems.update(new_theorems)
    pprint(theorems)

distanceDict = { name : f for name, f in heuristics.__dict__.items() if callable(f) and name.endswith('dist')}

def test_heuristics():
    for f in distanceDict.values():
        assert(f('aaa', 'abc') > f('aaa', 'aaa'))

def demo():
    test_heuristics()
    sampleSize = 30

    start = 'MI'
    goal  = 'M' + ('I' * 2**10)

    timeDict = {'no_heuristic' : []}
    for key in distanceDict:
        timeDict[key] = []

    for i in range(sampleSize):
        print('.', end='', flush=True)
        with timedblock('no_heuristic', timeDict):
            result = branch_and_bound(mu_branches, start, goal)
        for k, v in distanceDict.items():
            with timeout(1):
                with timedblock(k, timeDict):
                    result = astar(mu_branches, start, goal, distance=v)

    print('')
    keys = sorted(distanceDict.keys())
    u = mean(timeDict['no_heuristic'])
    print('p-values for z test from no_heuristic mean:')
    print('_' * 80)
    print('{:<28}| {:f}s'.format('no_heuristic', u))
    for key in keys:
        print('{:<28}| {:f}s'.format(key, mean(timeDict[key])))
    print('_' * 80)
    for key in keys:
        z = ztest(timeDict[key], u)
        p = to_p(z)
        print('{:<28}| {:>5}% confidence'.format(key, p * 100))
    #produce_theorems('AvB', logic_branches, 2)


from ..search   import branch_and_bound, breadth_first, breadth_first_2, astar 
from ..util     import timedblock, ztest, to_p, timeout, sign

from .mu import mu_branches
from .logic import logic_branches, subterms 

from . import heuristics

from statistics  import mean, stdev
from pprint      import pprint
from collections import namedtuple

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

distanceDict = { name : f for name, f in heuristics.__dict__.items() if callable(f) and name.endswith('dist')}

def test_heuristics():
    for f in distanceDict.values():
        assert(f('aaa', 'abc') > f('aaa', 'aaa'))
        f('', '')

def show_results(timeDict):
    print('')
    keys = sorted(distanceDict.keys())
    u = mean(timeDict['no_heuristic'])
    print('p-values for z test from no_heuristic mean:')
    print('_' * 80)
    print('{:<28}| {:+f}s | sdev {:+f}'.format('no_heuristic', u, stdev(timeDict['no_heuristic'])))
    for key in keys:
        m = mean(timeDict[key])
        print('{:<28}| {:+f}s | {:+f}s | sdev {:+f}'.format(key, m, m - u, stdev(timeDict[key])))
    print('_' * 80)
    for key in keys:
        z = ztest(timeDict[key], u)
        p = to_p(z)
        print('{:<28}| {} | {:<10}%'.format(key, sign(z), round(p * 100, 4)))

def run_tests(timeDict, sampleSize, start, goal, branches, maxTime=1):
    for i in range(sampleSize):
        print('.', end='', flush=True)
        with timeout(maxTime):
            with timedblock('no_heuristic', timeDict):
                result = branch_and_bound(branches, start, goal)
        for k, v in distanceDict.items():
            with timeout(maxTime):
                with timedblock(k, timeDict):
                    result = astar(branches, start, goal, distance=v)

Theorem = namedtuple('Theorem', ['start', 'goal', 'branches'])

def demo():
    produce_theorems(('R.(~P⊃Q)',), logic_branches, 3)
    test_heuristics()
    sampleSize = 30

    theorems = [Theorem('MI', 'M' + 'I' * 2**8,  mu_branches),
                Theorem('MI', 'M' + 'IU' * 2**8, mu_branches),
                Theorem('MI', 'MIIUIIU',         mu_branches)]
    #,Theorem(('AvB',), ('~(~A.~B)',), logic_branches)]

    with timedblock('demo'):
        for theorem in theorems:
            print('')
            print('{} to {}'.format(theorem.start, theorem.goal))
            print('')
            timeDict = {'no_heuristic' : []}
            for key in distanceDict:
                timeDict[key] = []
            run_tests(timeDict, sampleSize, theorem.start, theorem.goal, theorem.branches, maxTime=1)
            show_results(timeDict)
        print('\n\n')



from ..search   import branch_and_bound, astar
from ..util     import timedblock, ztest, to_p, timeout, sign

from .diff_search import diff_search
from .mu          import mu_branches
from .logic       import logic_branches, subterms 

from . import heuristics

from statistics  import mean, stdev
from pprint      import pprint
from collections import namedtuple

import time

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
        if f('AAA', 'ABC') <= f('AAA', 'AAA'):
            print('Warning, {} does not distinguish by variable'.format(f.__name__))
        f('', '')

def show_results(timeDict, maxTime=.1):
    correct = lambda t : float('inf') if t > maxTime else t
    print('')
    keys = sorted(distanceDict.keys(), key = lambda k : mean(timeDict[k]) if timeDict[k] is not None else float('inf'))
    if timeDict['no_heuristic'] is not None:
        u = mean(timeDict['no_heuristic'])
        print('p-values for z test from no_heuristic mean:')
        print('({:d} iterations)'.format(len(timeDict['no_heuristic'])))
        print('_' * 80)
        print('{:<28}| {:+f}s | sdev +/- {:f}'.format('no_heuristic', u, stdev(timeDict['no_heuristic'])))
    else:
        u = 0
    for key in keys:
        if timeDict[key] is not None:
            m = mean(timeDict[key])
            print('{:<28}| {:+f}s | {:+f}s | sdev +/- {:f}'.format(key, correct(m), correct(m) - u, stdev(timeDict[key])))
        else:
            print('{:<28}| timeout'.format(key))
    print('_' * 80)
    for key in keys:
        if timeDict[key] is not None:
            z = ztest(timeDict[key], u)
            p = to_p(z)
            print('{:<28}| {} | {:<10}%'.format(key, sign(z), round(p * 100, 4)))
        else:
            print('{:<28}| timeout'.format(key))

    best = sorted(keys, key=lambda k : mean(timeDict[k]) if timeDict[k] is not None else float('inf'))
    print('\nFastest algorithm was {}'.format(best[0]))
    print('Followed by {}'.format(best[1]))
    print('Worst: {}'.format(best[-1]))

def run_tests(timeDict, sampleSize, start, goal, branches, maxTime=1):
    startTime = time.perf_counter()
    for i in range(sampleSize):
        with timedblock('no_heuristic', timeDict, maxTime):
            result = branch_and_bound(branches, start, goal)
        for k, v in distanceDict.items():
            with timedblock(k, timeDict, maxTime):
                result = astar(branches, start, goal, distance=v)
        if i == 0:
            perIter = time.perf_counter() - startTime
            print('Time estimate for {} iterations: {}'.format(sampleSize, sampleSize * perIter))
        print('.', end='', flush=True)
        if (i + 1) % 10 == 0:
            print(' ({})'.format(i + 1))
        if i + 1 == sampleSize:
            print('\nSolution:')
            pprint(result)


Problem = namedtuple('Problem', ['start', 'goal', 'branches'])

def demo():
    test_heuristics()
    sampleSize = 30
    maxTime    = 1

    problems = [Problem('MI', 'M' + 'IU' * 2**8, mu_branches),
                Problem('R.(~P⊃Q)', '(QvP).R', logic_branches),
                Problem('(R⊃~P).(R⊃Q)', '~Rv(~P.Q)', logic_branches)]

    with timedblock('demo'):
        for p in problems:
            print('')
            print('{} to {}'.format(p.start, p.goal))
            print('')
            timeDict = {'no_heuristic' : []}
            for key in distanceDict:
                timeDict[key] = []
            run_tests(timeDict, sampleSize, p.start, p.goal, p.branches, maxTime=maxTime)
            show_results(timeDict, maxTime=maxTime)
        print('\n\n')



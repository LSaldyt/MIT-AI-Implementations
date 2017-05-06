from ..search   import branch_and_bound, astar
from ..util     import timedblock, ztest, to_p, sign

from .systems import logic
from .problem import Problem
from .plot    import vplot, heatplot
from .        import heuristics

from pprint      import pprint
from statistics  import mean, stdev
from collections import OrderedDict

import time

def test_heuristics():
    distanceDict = { name : f for name, f in heuristics.__dict__.items() if callable(f) and name.endswith('dist')}
    for f in distanceDict.values():
        if f('AAA', 'ABC') <= f('AAA', 'AAA'):
            print('Warning, {} does not distinguish by variable'.format(f.__name__))
        f('', '')

def show_results(timeDict, distanceDict, maxTime=.1):
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

def run_tests(timeDict, sampleSize, problem, distanceDict, maxTime=1):
    startTime = time.perf_counter()
    result = None
    for i in range(sampleSize):
        with timedblock('no_heuristic', timeDict, maxTime):
            result = branch_and_bound(problem.system.branches, problem.start, problem.goal)
        for k, v in distanceDict.items():
            with timedblock(k, timeDict, maxTime):
                result = astar(problem.system.branches, problem.start, problem.goal, distance=v)
        if i == 0:
            perIter = time.perf_counter() - startTime
            print('Time estimate for {} iterations: {}'.format(sampleSize, sampleSize * perIter))
        print('.', end='', flush=True)
        if (i + 1) % 10 == 0:
            print(' ({})'.format(i + 1))
        if i + 1 == sampleSize:
            print('\nSolution:')
            pprint(result)


def compare_heuristics(problems=None):
    distanceDict = { name : f for name, f in heuristics.__dict__.items() if callable(f) and name.endswith('dist')}
    test_heuristics()

    sampleSize = 30
    maxTime    = .1

    if problems is None:
        problems = [Problem('MI', 'M' + 'IU' * 2**8, mu),
                    Problem('R.(~P⊃Q)', '(QvP).R', logic),
                    Problem('(R⊃~P).(R⊃Q)', '~Rv(~P.Q)', logic)]

    results = dict()
    with timedblock('demo'):
        for i, p in enumerate(problems):
            print('')
            print('{} to {}'.format(p.start, p.goal))
            print('')
            timeDict = {'no_heuristic' : []}
            for key in distanceDict:
                timeDict[key] = []
            run_tests(timeDict, sampleSize, p, distanceDict, maxTime=maxTime)
            show_results(timeDict, distanceDict, maxTime=maxTime)
            preD = {k:v for k, v in timeDict.items() if v is not None}
            d = OrderedDict()
            pairs = sorted(preD.items(), key=lambda x : mean(x[1]))
            for k, v in pairs:
                d[k] = v
            if len(d) > 0:
                vplot(d, 'output/violin_%s.png' % i)
            u = 1 if timeDict['no_heuristic'] is None else mean(timeDict['no_heuristic'])
            results[p.start[:10] + ', ' + p.goal[:10]] = {k : (-1 if v is None else mean(v)/u) for k, v in timeDict.items()}
        print('\n\n')
    heatplot(results, 'output/heat.png')

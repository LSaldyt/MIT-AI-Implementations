from ..search   import branch_and_bound, breadth_first, breadth_first_2, astar 
from ..util     import timedblock, ztest, to_p

from .mu import mu_branches
from .logic import logic_branches, subterms

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


def hamming_dist(a, b):
    score = 0
    for ca, cb in zip(min(a, b), max(a, b)):
        if ca != cb:
            score += 1
    return score

def levenshtein_dist(a, b, weight=1):
    return hamming_dist(a, b) + abs(len(a) - len(b)) * weight

distanceDict = {
        'levenshtein_dist' : levenshtein_dist,
        'hamming_dist'     : hamming_dist
        }

def demo():
    sampleSize = 30

    start = 'MI'
    goal  = 'M' + ('I' * 2**10)

    timeDict = {'no_heuristic' : []}
    for key in distanceDict:
        timeDict[key] = []

    for _ in range(sampleSize):
        with timedblock('no_heuristic', timeDict):
            result = branch_and_bound(mu_branches, start, goal)
        for k, v in distanceDict.items():
            with timedblock(k, timeDict):
                result = astar(mu_branches, start, goal, distance=v)

    u = mean(timeDict['no_heuristic'])
    print('p-values for z test from no_heuristic mean:')
    print('{:<20}: {:f}s'.format('no_heuristic', u))
    for key in distanceDict:
        print('{:<20}: {:f}s'.format(key, mean(timeDict[key])))
    print('_' * 80)
    for key in distanceDict:
        z = ztest(timeDict[key], u)
        p = to_p(z)
        print('{:<20}: {:>5}% confidence'.format(key, p * 100))
    #produce_theorems('AvB', logic_branches, 2)


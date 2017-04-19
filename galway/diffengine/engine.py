from ..search   import branch_and_bound, breadth_first, breadth_first_2, astar 
from ..util     import timedblock

from .mu import mu_branches
from .logic import logic_branches

from pprint import pprint

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

def demo():
    iterations = 500
    start = 'MI'
    goal  = 'M' + ('I' * 2**10)
    with timedblock('levenshtein dist'):
        for i in range(iterations):
            result = astar(mu_branches, start, goal, distance=levenshtein_dist)
    with timedblock('hamming dist'):
        for i in range(iterations):
            result = astar(mu_branches, start, goal, distance=hamming_dist)
    produce_theorems('AvB', logic_branches, 10)

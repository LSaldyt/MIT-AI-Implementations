#!/usr/bin/env python3
from ..search   import branch_and_bound, breadth_first, breadth_first_2, astar 
from ..util     import timedblock

def mu_branches(node):
    options = []
    if node.endswith('I'):
        options.append(node + 'U')
    options.append(node + node[1:])
    options.append(node.replace('III', 'U'))
    options.append(node.replace('UU', ''))
    return options

def gen_theorems(depth):
    theorems = {'MI'}

    for i in range(depth):
        new_theorems = set()
        for t in theorems:
            for s in mu_branches(t):
                new_theorems.add(s)
        theorems.update(new_theorems)

    return theorems

def theorem_dist(a, b):
    score = 0
    for ca, cb in zip(min(a, b), max(a, b)):
        if ca != cb:
            score += 1
    return score + abs(len(a) - len(b))
    #return abs(a.count('I') - b.count('I')) + abs(a.count('U') - b.count('U'))

def timed_theorem_search(f, iterations=1):
    with timedblock(f.__name__):
        for i in range(iterations):
            result = f(mu_branches, 'MI', 'MIIIIIIIIIIIIIIII')
    print(result)

def demo():
    iterations = 10000
    timed_theorem_search(breadth_first,    iterations)
    timed_theorem_search(breadth_first_2,  iterations)
    timed_theorem_search(branch_and_bound, iterations)
    with timedblock('astar'):
        for i in range(iterations):
            result = astar(mu_branches, 'MI', 'MIIIIIIIIIIIIIIII', distance=theorem_dist)
    print(result)

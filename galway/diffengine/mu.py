#!/usr/bin/env python3
from ..search import branch_and_bound

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

#def astar(branches, start, end):

def demo():
    print(gen_theorems(4))
    print(branch_and_bound(mu_branches, 'MI', 'MUI'))

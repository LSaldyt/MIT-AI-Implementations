#!/usr/bin/env python3
from time import time

def branches(node):
    options = []
    if node.endswith('I'):
        options.append(node + 'U')
    options.append(node + node[1:])
    options.append(node.replace('III', 'U'))
    options.append(node.replace('UU', ''))
    return options

theorems = {'MI'}

for i in range(3):
    new_theorems = set()
    for t in theorems:
        for s in branches(t):
            new_theorems.add(s)
    theorems.update(new_theorems)

print(theorems)


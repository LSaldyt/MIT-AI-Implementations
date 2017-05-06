
def var_dist(a, b):
    dist = 0
    for c in 'ABCDEFGHIJKLMNOPQRSTUV':
        if bool(c in a) != bool(c in b): # xor
            dist += 1
    return dist

def numvar_dist(a, b):
    dist = 0
    for c in 'ABCDEFGHIJKLMNOPQRSTUV':
        dist += abs(a.count(c) - b.count(c))
    return dist

def sign_dist(a, b):
    dist = 0
    a_neg = a.count('~') % 2 == 0
    b_neg = b.count('~') % 2 == 0
    if a_neg != b_neg: # xor
        dist += 1
    return dist

def binary_connective_dist(a, b):
    dist = 0
    connectives = '⊃.v'
    l = min(len(a), len(b))
    for i in range(l):
        if a[i] in connectives and a[i] == b[i]:
            dist += 1
    return dist

def position_dist(a, b):
    dist = 0
    for i, ca in enumerate(a):
        for j, cb in enumerate(b):
            if ca == cb and i != j:
                dist += 1
    return dist

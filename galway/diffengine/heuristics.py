import numpy as np
from collections import namedtuple

def transpositions(a, b):
    n = 0
    l = min(len(a), len(b))
    for i in range(l):
        if (i < l - 1    and 
            a[i] != b[i] and 
            a[i] == b[i+1]):
            n += 1
    return n

def len_dist(a, b):
    if a == b:
        return 0
    n = abs(len(a) - len(b)) 
    if n == 0: return 1 
    else: return n

def hamming_dist(a, b):
    score = 0
    for ca, cb in zip(min(a, b), max(a, b)):
        if ca != cb:
            score += 1
    return score

def hamming_len_dist(a, b):
    return hamming_dist(a, b) + len_dist(a, b)

def jaro(a, b):
    l = min(len(a), len(b))
    m = max(1, l - hamming_dist(a, b))
    t = transpositions(a, b)
    la = max(1, len(a))
    lb = max(1, len(b))
    return 1/3 * (m /la + m/lb + (m-t)/m)

def jaro_dist(a, b):
    return 1 / jaro(a, b)

def jaro_winkler(a, b):
    d = jaro(a, b)

    l = 0
    for ca, cb in zip(min(a, b), max(a, b)):
        if ca != cb or l > 4:
            break
        else:
            l += 1
    p = .1
    return d + l * p * (1-d)

def jaro_winkler_dist(a, b):
    return 1 / jaro_winkler(a, b)

def jaro_len_dist(a, b):
    return jaro_dist(a, b) * len_dist(a, b) 

def jaro_winkler_len_dist(a, b):
    return jaro_winkler_dist(a, b) * len_dist(a, b) 

CharInfo = namedtuple('CharInfo', ['indices', 'count'])

def _build_summary_dict(s):
    d = dict()
    for i, c in enumerate(s):
        if c in d:
            indices, count = d[c]
            d[c] = CharInfo(indices + [i], count + 1)
        else:
            d[c] = CharInfo([i], 1)
    return d

'''
Distance function in the spirit of the original GPS paper
Should account for (in order of importance):
    Difference in variable          (V)
    Difference in num variables     (N)
    Difference in sign              (T)
    Difference in binary connective (C)
    Difference in grouping          (G)
    Difference in position          (P)
'''
def theorem_dist(a, b, variables=set('ABCDEFGHIJKLMNOPQRSTUV'), negation='~'):
    a_dict = _build_summary_dict(a) # Form (item : indices, count)
    b_dict = _build_summary_dict(b) # Form (item : indices, count)
    V = 0
    N = 0
    T = 0
    C = 0
    I = 0 # Based on G and P
    #G = 0 Important but currently left out
    #P = 0
    for c, (indices, count) in a_dict.items():
        if c in variables:
            if c not in b_dict:
                V += 1
            else:
                N += abs(count - b_dict[c].count)
                char_I = len(indices)
                for i in indices:
                    for j in b_dict[c].indices:
                        if i == j:
                            char_I -= 1
                I += char_I
        elif c == negation:
            if c not in b_dict:
                T += 1
        else: # c is operator
            for i in indices:
                if len(b) < i + 1 or b[i] != c:
                    C += 1
    return V * 10000 + N * 1000 + T * 100 + C * 10 + I

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


def alt_theorem_dist(a, b):
    return var_dist(a, b) * 10000 + numvar_dist(a, b) * 1000 + sign_dist(a, b) * 100 + binary_connective_dist(a, b) * 10 + position_dist(a, b)

'''
Difference in grouping          (G) !!!
'''

def lev_dist(a, b):
    m = len(a)
    n = len(b)

    if m == 0 or n == 0:
        return 0

    d = np.zeros((m, n))
 
    # source prefixes can be transformed into empty string by
    # dropping all characters
    for i in range(m):
        d[i, 0] = i
 
    # target prefixes can be reached from empty source prefix
    # by inserting every character
    for j in range(n):
        d[0, j] = j
 
    for j in range(n):
        for i in range(m):
            if a[i] == b[j]:
                substitutionCost = 0
            else:
                substitutionCost = 1
            d[i, j] = min(d[i-1, j] + 1,                   # deletion
                          d[i, j-1] + 1,                   # insertion
                          d[i-1, j-1] + substitutionCost)  # substitution
 
    return d[m - 1, n - 1]

def opt_align_dist(a, b):
    m = len(a)
    n = len(b)

    if m == 0 or n == 0:
        return 0

    d = np.zeros((m, n))
 
    # source prefixes can be transformed into empty string by
    # dropping all characters
    for i in range(m):
        d[i, 0] = i
 
    # target prefixes can be reached from empty source prefix
    # by inserting every character
    for j in range(n):
        d[0, j] = j
 
    for j in range(n):
        for i in range(m):
            if a[i] == b[j]:
                substitutionCost = 0
            else:
                substitutionCost = 1
            d[i, j] = min(d[i-1, j] + 1,                   # deletion
                          d[i, j-1] + 1,                   # insertion
                          d[i-1, j-1] + substitutionCost)  # substitution
            if i > 1 and j > 1 and a[i] == b[j - 1] and a[i - 1] == b[j]:
                d[i, j] = min(d[i, j],
                              d[i-2, j-2] + substitutionCost)
 
    return d[m - 1, n - 1]

def dam_lev_dist(a, b):
    m = len(a)
    n = len(b)

    if m == 0 or n == 0:
        return 0
 
    # From psuedocode, inaccurate
    #let d[−1..length(a), −1..length(b)] be a 2-d array of integers, dimensions length(a)+2, length(b)+2
    # note that d has indices starting at −1, while a, b and da are one-indexed.
    # Actually, d is zero indexed, but the same dimensions as described above
    d = np.zeros((m + 2, n + 2))
    da = np.zeros((26, 26))

    maxdist = m + n
    d[0, 0] = maxdist 
    for i in range(m): 
        d[i, 0] = maxdist
        d[i, 1] = i
    for j in range(n): 
        d[0, j] = maxdist
        d[1, j] = j

    for i in range(1, m + 1):
        db = 0
        for j in range(1, n + 1):
            k = 0 #da[b[j]]
            l = db
            if a[i - 1] == b[j - 1]:
                cost = 0
                db   = j
            else:
                cost = 1
            d[i, j] = min(d[i-1, j-1] + cost,  #substitution
                          d[i,   j-1] + 1,     #insertion
                          d[i-1, j  ] + 1,     #deletion
                          d[k-1, l-1] + (i-k-1) + 1 + (j-l-1)) #transposition
        #da[a[i]] = i
        da[0] = i
    return d[m, n]


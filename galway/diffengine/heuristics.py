import numpy as np

def transpositions(a, b):
    n = 0
    l = min(len(a), len(b))
    for i in range(l):
        if (i < l - 1    and 
            a[i] != b[i] and 
            a[i] == b[i+1]):
            n += 1
    return n

def hamming_dist(a, b):
    score = 0
    for ca, cb in zip(min(a, b), max(a, b)):
        if ca != cb:
            score += 1
    return score

def hamming_len_dist(a, b, weight=1):
    return hamming_dist(a, b) + abs(len(a) - len(b)) * weight

def hamming_len_trans_dist(a, b):
    return hamming_len_dist(a, b) - transpositions(a, b)

def hamming_trans_dist(a, b):
    return hamming_dist(a, b) - transpositions(a, b)

def jaro_dist(a, b):
    l = min(len(a), len(b))
    m = l - hamming_dist(a, b)
    t = transpositions(a, b)
    return 1 / (1/3 * (m /len(a) + m/len(b) + (m-t)/m))


'''
def lev_dist(s, t):
    m = len(s)
    n = len(t)

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
            if s[i] == t[j]:
                substitutionCost = 0
            else:
                substitutionCost = 1
            d[i, j] = min(d[i-1, j] + 1,                   # deletion
                          d[i, j-1] + 1,                   # insertion
                          d[i-1, j-1] + substitutionCost)  # substitution
 
    return d[m-1, n-1]
'''

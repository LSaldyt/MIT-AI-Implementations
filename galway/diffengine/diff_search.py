from collections import namedtuple

Path = namedtuple('Path', ['len', 'path'])

'''
Specialized graph search for difference engine:

    Given a set of heuristics that define differences, and corresponding transformations:
        Evaluate each heuristic, apply the transformation corresponding to the largest heuristic
        (Weight heuristics by importance)

    { 'V' : var_diff_heuristic, var_diff_transform}

    heuristics = sorted([h(node) for h in heuristics])
    for transform in generate_transformers(heuristics):
        #.. test transform
'''

def diff_search(start, end, heuristics, transformers):
    paths = { start : Path(0, [start])}

    while end not in paths:
        # min element of keys sorted by heuristic:
        shortestKey = min([key for key in paths], key=lambda point : paths[point].len)
        scoredKeys  = sorted([h(start) for h in heuristics])

        for transform in (transformers[key] for key in scoredKeys):
            adj = transform(shortestKey)
            l = paths[shortestKey].len + 1
            # add the path if it doesn't exist, update it if a shorter one is found:
            if adj not in paths or paths[adj].len > l:
                paths[adj] = Path(l, paths[shortestKey].path + [adj])
        del paths[shortestKey] # the path to the previously shortest node is now unneeded
    return paths[end].path 

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
from collections import namedtuple

Path = namedtuple('Path', ['len', 'path'])

def alt_astar(branches, start, end, distance, axioms=None):
    if axioms is None:
        axioms = []
    paths = { start : Path(0, axioms + [start])}

    heuristic = lambda point : paths[point].len * distance(point, end)

    while end not in paths:
        # min element of keys sorted by heuristic:
        shortestKey = min([key for key in paths], key=heuristic)

        for adj in branches(shortestKey, paths[shortestKey].path):
            l = paths[shortestKey].len + 1
            # add the path if it doesn't exist, 
            # update it if a shorter one is found:
            if adj not in paths or paths[adj].len > l:
                paths[adj] = Path(l, paths[shortestKey].path + [adj])
        # the path to the previously shortest node is now unneeded
        del paths[shortestKey] 
    return paths[end].path 

class NoPathException(Exception):
    pass

def diff_search(start, end, diffList, transformers):
    if start == end:
        return [end]
    for hueristic, transKeys in diffList:
        try:
            if hueristic(start):
                for key in transKeys:
                    return ([start] + 
                            diff_search(transformers[key](start), 
                                end, diffList, transformers))
        except NoPathException as e:
            # Continue to the next hueristic, or fail if none work
            pass
    raise NoPathException(
            'The theorem {} cannot be proven from {}'.format(start, end))

'''
Distance function in the spirit of the original GPS paper
Should account for (in order of importance):
    Difference in variable          (V)
    Difference in num variables     (N)
    Difference in sign              (T)
    Difference in binary connective (C)
    Difference in grouping          (G)
    Difference in position          (P)

Needed: transformer-heuristic associations
heuristics: dictionary of functions
transformers: dictionary of functions
'''

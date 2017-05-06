from collections import namedtuple

Path = namedtuple('Path', ['len', 'path'])

def alt_astar(branches, start, end, distance):
    print(start, end)
    paths = { start : Path(0, [start])}

    heuristic = lambda point : paths[point].len * distance(point, end)

    while end not in paths:
        # min element of keys sorted by heuristic:
        shortestKey = min([key for key in paths], key=heuristic)

        for adj in branches(shortestKey):
            l = paths[shortestKey].len + 1
            # add the path if it doesn't exist, 
            # update it if a shorter one is found:
            if adj not in paths or paths[adj].len > l:
                paths[adj] = Path(l, paths[shortestKey].path + [adj])
        # the path to the previously shortest node is now unneeded
        del paths[shortestKey] 
    return paths[end].path 

'''
def diff_search(start, end, system):
    1/0
    if start == end:
        return [end]

    paths = { start : Path(0, [start])}

    while end not in paths:
        for hueristic, transKeys in system.diffList:
            if hueristic(start, end):
                for key in transKeys:
                    options = system.transformers[key](start, 
                                                       system.subterms(start))
                    for option in options:
                        return ([start] + 
                                diff_search(option, 
                                            end, 
                                            system))


'''

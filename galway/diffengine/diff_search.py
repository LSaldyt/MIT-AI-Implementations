from collections import namedtuple

Path = namedtuple('Path', ['len', 'path'])

def astar(branches, start, end, distance):
    paths = { start : Path(0, [start])}

    heuristic = lambda point : paths[point].len * distance(point, end)

    while end not in paths:
        # min element of keys sorted by heuristic:
        shortestKey = min([key for key in paths], key=heuristic)

        for adj in branches(shortestKey):
            l = paths[shortestKey].len + 1
            # add the path if it doesn't exist, update it if a shorter one is found:
            if adj not in paths or paths[adj].len > l:
                paths[adj] = Path(l, paths[shortestKey].path + [adj])
        del paths[shortestKey] # the path to the previously shortest node is now unneeded
    return paths[end].path 

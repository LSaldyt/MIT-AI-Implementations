from .graph import Graph, to_obstacles
from math  import sqrt

from collections import namedtuple

Path = namedtuple('Path', ['len', 'path'])

def depth_first(branches, seen, current, end):
    if end in branches(current):
        return (True, seen + [end])
    else:
        possible = [point for point in branches(current) if point not in seen]
        for next_point in possible:
            result = depth_first(branches, seen + [next_point], next_point, end)
            if(result[0]):
                return (True, result[1])
        return (False, [])

def breadth_first(branches, start, end):
    if start == end:
         return [end]
    extend  = lambda paths : [path + [p] for path in paths for p in branches(path[-1]) if p not in path]
    paths   = extend([[start]])
    results = [path for path in paths if path[-1] == end]

    while len(results) < 1:
        results = [path for path in paths if path[-1] == end]
        paths = extend(paths)

    if len(results) > 0:
        return results[0]
    else:
        return []

def breadth_first_2(branches, start, end):
    if start == end:
         return [end]
    seen    = []
    extend  = lambda paths : [path + [p] for path in paths for p in branches(path[-1]) if p not in path and p not in seen]
    paths   = extend([[start]])
    results = [path for path in paths if path[-1] == end]

    while len(results) < 1:
        results = [path for path in paths if path[-1] == end]
        paths   = extend(paths)
        seen    = set([path[-1] for path in paths])

    if len(results) > 0:
        return results[0]
    else:
        return []

point_distance = lambda current, end : sqrt((end[0] - current[0]) ** 2 + (end[1] - current[1]) ** 2)

def hill_climbing(branches, seen, current, end, distance=point_distance):
    if end in branches(current):
        return (True, seen + [end])
    else:
        possible = sorted([point for point in branches(current) if point not in seen],
                        key=lambda p : distance(p, end))
        for next_point in possible:
            result = hill_climbing(branches, seen +[next_point], next_point, end, distance=distance)
            if(result[0]):
                return (True, result[1])
        return (False, [])


def beam_search(branches, start, end, width=2, distance=point_distance):
    if start == end:
         return [end]
    seen    = []
    extend  = lambda paths : [path + [p] for path in paths for p in branches(path[-1]) if p not in path and p not in seen]
    limit   = lambda paths : sorted(paths, key=lambda path : distance(path[-1], end))[:width]
    paths   = limit(extend([[start]]))
    results = [path for path in paths if path[-1] == end]

    while len(results) < 1:
        results = [path for path in paths if path[-1] == end]
        paths   = limit(extend(paths))
        seen    = seen + [path[-1] for path in paths]

    if len(results) > 0:
        return results[0]
    else:
        return []

def branch_and_bound(branches, start, end):
    if start == end:
         return [end]
    paths = { start : Path(0, [start])}

    while end not in paths:
        shortest = min([(paths[key][0], key) for key in paths])
        for p in branches(shortest[1]):
            if p not in paths:
                paths[p] = (shortest[0]+1, paths[shortest[1]][1] + [p])
            elif paths[p][0] > shortest[0]+1:
                paths[p] = (shortest[0]+1, paths[shortest[1]][1] + [p])
        del paths[shortest[1]]

    return paths[end][1]



def astar(branches, start, end, distance=point_distance):
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

mazeString = """
......o...
ooo.o.....
....o.oooo
.o.oo.o...
.o..o.o.o.
.oooo...o.
....ooooo.
o.o.o.....
o.o.o.....
..o.......
"""
def demo():
    maze = to_obstacles(mazeString)
    print(maze)
    graph = Graph(10, 10, maze)

    """
    print(depth_first(graph, [], (0, 0), (1, 9)))
    
    print(breadth_first(graph, (0, 0), (1, 9)))
    
    print(breadth_first_2(graph, (0, 0), (1, 9)))
    
    print(hill_climbing(graph, [], (0, 0), (1, 9)))
    
    print(beam_search(graph, (0, 0), (1, 9)))
    
    print(branch_and_bound(graph, (0, 0), (1, 9)))
    """

    print("Path using a*:")
    path = astar(lambda l : graph.points[l], (0, 0), (9, 9))
    print(path)

    graph.show(path)

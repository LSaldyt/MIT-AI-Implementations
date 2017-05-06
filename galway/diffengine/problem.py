from collections import namedtuple

from .diff_search import alt_astar

Problem = namedtuple('Problem', ['start', 'goal', 'system', 'axioms'])
Problem.__new__.__defaults__ = (None, None, None, None) 

def solve(problem, d):
    return alt_astar(problem.system.branches, 
                     problem.start, 
                     problem.goal, 
                     distance=d)

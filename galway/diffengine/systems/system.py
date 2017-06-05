from .transform import build_transformers
from ...util.subterms  import build_subterm_function
from .path      import Path

from ...search.methods import *

class System():
    def __init__(self, 
                 name,
                 strReplacements, 
                 operators, 
                 heuristics, 
                 special_transformers=None):
        self.name = name

        if special_transformers is None:
            special_transformers = []
        self.special_transformers = special_transformers

        self.transformers = build_transformers(strReplacements)
        self.subterms     = build_subterm_function(operators)

        self.diffList = []
        for heuristic in heuristics:
            transformKeys = []
            i = 0
            for line in strReplacements.split('\n'):
                terms = line.split()
                if len(terms) == 3:
                    a, _, b = terms 
                    if heuristic(a, b):
                        transformKeys.append(i)
                    i += 1
            self.diffList.append((heuristic, transformKeys))


    def _find_replacements(self, node):
        options = set()
        terms = self.subterms(node)
        for t in self.transformers:
            options.update(t(node, terms))
        return options

    def branches(self, theorem):
        options = set()
        for t in self._find_replacements(theorem):
            options.add(theorem + t)
        return options


    def __repr__(self):
        return 'System({})'.format(self.name)

    def prove(self, start, end, distance=lambda a, b : 0):
        return astar(self._branches, start, end, distance)

    def _branches(self, current, end):
        options = set()
        for hueristic, transKeys in self.diffList:
            if hueristic(current, end):
                for key in transKeys:
                    options |= (self.transformers[key](current,
                                                      self.subterms(current))
                               | self.special_transformers(current))
        return options



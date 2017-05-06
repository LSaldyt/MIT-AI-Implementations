from .transform import build_transformers
from .subterms  import build_subterm_function

class System():
    def __init__(self, strReplacements, operators, heuristics):
        self.transformers = build_transformers(strReplacements)
        self.subterms     = build_subterm_function(operators)
        self.diffList = []
        for heuristic in heuristics:
            transformKeys = []
            for i, line in enumerate(strReplacements.split('\n')):
                terms = line.split()
                if len(terms) == 3:
                    a, _, b = terms 
                    if heuristic(a, b):
                        transformKeys.append(i)
            self.diffList.append((heuristic, transformKeys))

    '''
    def diff_search(start, end, diffList, transformers):
        if start == end:
            return [end]
        for hueristic, transKeys in diffList:
            try:
                if hueristic(start):
                    for key in transKeys:
    '''

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
        return 'System()'



from .transform import build_transformers
from .subterms  import build_subterm_function
from .path      import Path

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

    def prove(self, start, end):
        if end in start.theorems:
            return []
        paths = { start : Path(0, [start])}
        heuristic = lambda point : paths[point].len

        while end not in paths:
            # min element of keys sorted by heuristic:
            current = min([key for key in paths], key=heuristic)
            for hueristic, transKeys in self.diffList:
                if hueristic(current, end):
                    for key in transKeys:
                        options = (self.transformers[key](current,
                                                          self.subterms(current))
                                   | self.special_transformers(current))
                        for option in options:
                            l = paths[current].len + 1
                            # add the path if it doesn't exist, 
                            # update it if a shorter one is found:
                            if option not in paths or paths[option].len > l:
                                paths[option] = Path(l, paths[current].path + [option])
            del paths[current]
        return paths[end].path

    def branches(self, current, end):
        options = set()
        for hueristic, transKeys in self.diffList:
            if hueristic(current, end):
                for key in transKeys:
                    options |= (self.transformers[key](current,
                                                      self.subterms(current))
                               | self.special_transformers(current))
        return options



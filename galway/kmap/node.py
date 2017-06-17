from collections import defaultdict, namedtuple

EndNode = namedtuple('EndNode', ['node', 'causes', 'conditions'])
EndNode.__str__ = lambda self : '{} (because {}) (when {})'.format(*self)
EndNode.__repr__ = EndNode.__str__

class Node():
    def __init__(self):
        self.relations = defaultdict(set)

    def add(self, relation, node, causes=None, conditions=None):
        if causes is None:
            causes = tuple()
        else:
            causes = tuple(sorted(causes))
        if conditions is None:
            conditions = tuple()
        else:
            conditions = tuple(sorted(conditions))
        self.relations[relation].add(EndNode(node, causes, conditions))

    def current_state(self):
        current = dict()
        for k, v in self.relations.items():
            for elem in v:
                for cond in elem.conditions:
                    if cond not in self.relations:
                        continue
            current[k] = v
        return current

    def __repr__(self):
        return str(self)

    def __str__(self):
        prettify = lambda kv : '{}:{}'.format(*kv)
        return '\n    '.join(map(prettify, self.relations.items()))

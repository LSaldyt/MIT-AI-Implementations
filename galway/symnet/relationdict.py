from collections import defaultdict

class RelationDict():
    def __init__(self):
        self.relations = defaultdict(set)

    def __getitem__(self, key):
        return self.relations[key]

    def __contains__(self, key):
        return key in self.relations

    def __str__(self):
        if len(self.relations.keys()) == 0:
            l = 1
        else:
            l = max(len(s) for s in self.relations.keys())
        prettify = lambda kv : ('{:<' + str(l) + '} : {}').format(*kv)
        return '\n    '.join(map(prettify, self.relations.items()))

    def remove(key, node):
        assert key in self.relations
        assert node in self.relations[key]
        self.relations[key].remove(node)

    def items(self):
        return self.relations.items()

    def update(self, other):
        self.relations.update(other.relations)



class TheoremNode():
    def __init__(self, end, axioms=None):
        if axioms is None:
            self.axioms = set()
        else:
            self.axioms = set(axioms)
        self.end = end 
        self._theorems = self.axioms | {self.end}

    def substitute(self, left, right, clean=lambda s : s):
        return self + clean(self.end.replace(left, right))
    
    def __hash__(self):
        return hash(self.end)

    def __eq__(self, other):
        return self.end == other.end

    def __add__(self, other):
        return TheoremNode(str(other), self.theorems)

    def __lt__(self, other):
        return self.end < other.end

    def __getitem__(self, item):
        return self.end.__getitem__(item)

    def __str__(self):
        return self.end

    def __repr__(self):
        return 'TheoremNode({})'.format(self.end)

    def __len__(self):
        return len(self.end)

    def count(self, n):
        return self.end.count(n)

    @property
    def theorems(self):
        return self._theorems

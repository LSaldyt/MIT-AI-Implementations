from collections import defaultdict, Counter

from ..util.orderedset import OrderedSet

from .clause       import Clause
from .relationdict import RelationDict

class SymbolNet():
    '''
    X --relation--> Y

    SymbolNet:
        Dictionary {name : {relation : set(connected nodes)}}
        Each of connected nodes is in Dictionary
        An item is atomic is it has no relations (terminal)

    def __getitem__(self, key):
        return self.symbolDict[key]

    def __contains__(self, key):
        return key in self.symbolDict

    Relations : {(relation, node) : set()}

    causedict: {(relation, node) : cause}

    '''
    reserved = {'__atomic__'}
    
    def __init__(self):
        self.symbolDict   = defaultdict(RelationDict)
        self.causeDict    = defaultdict(list)
        self.concludeDict = defaultdict(list)
        self.relations    = defaultdict(set)
        self.relationTypes = set()

    def __str__(self):
        prettify = lambda kv : '{}:\n    {}'.format(*kv)
        return '\n'.join(map(prettify, self.symbolDict.items()))

    def _add_cause(self, key, relation, node, cause):
        self.causeDict[(relation, node)].append(cause)
        if cause != '__atomic__':
            self.concludeDict[(cause.relation, cause.node)] = (relation, node)

            ckey, crelation, cnode = cause
            if ckey not in self.symbolDict:
                self.add(ckey, crelation, cnode)

    def add(self, key, relation, node, cause='__atomic__', causes=None):
        self.symbolDict[key][relation].add(node)
        self.relations[(relation, node)].add(key)
        self.relationTypes.add(relation)
        if causes is None:
            causes = []
        if cause != '__atomic__':
            causes.append(cause)
        for c in causes:
            self._add_cause(key, relation, node, c)

    def find_that(self, relation, node):
        return self.relations[(relation, node)]

    def find_close(self, relationPairs):
        counter = Counter()
        for pair in relationPairs:
            for element in self.find_that(*pair):
                counter[element] += 1
        best = counter.most_common()
        if len(best) > 0 and best[0][1] == len(relationPairs):
            return best[:1]
        else:
            return best

    def find_by(self, relation, *nodes):
        return self.find_close([(relation, node) for node in nodes])

    def find_reasons(self, clause):
        if clause == '__atomic__':
            return clause
        return self.causeDict[clause.relation, clause.node]

    def trace_reasons(self, clause):
        print('Tracing reasons for {}'.format(clause))
        seen = OrderedSet()
        reasons = self.find_reasons(clause)
        while '__atomic__' not in seen:
            if len(reasons) == 0:
                break
            for reason in reasons:
                seen.add(reason)
                reasons = self.find_reasons(reason)
        return seen

    def _conclude(self, key):
        queue = []
        for relation, nodes in self.symbolDict[key].items():
            for node in nodes:
                if (relation, node) in self.concludeDict:
                    concludedRelation, concludedNode = self.concludeDict[(relation, node)]
                    queue.append((key, concludedRelation, concludedNode, Clause(key, relation, node)))
        for args in queue:
            self.add(*args)

    def show(self, a, b):
        self._conclude(a)
        aRelations = self.symbolDict[a]
        causes = []
        for relation, nodes in self.symbolDict[b].items():
            for node in nodes:
                if relation not in aRelations or \
                       node not in aRelations[relation]:
                    print('{} does not supersede {}'.format(a, b))
                causes.append(Clause(a, relation, node))
        self.add(a, 'supersedes', b, causes=causes)
        print('Proof for {} superseding {}:'.format(a, b))
        print(self.trace_reasons(Clause(a, 'supersedes', b)))


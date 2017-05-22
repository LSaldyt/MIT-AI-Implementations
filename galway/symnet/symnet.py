from collections import defaultdict, Counter
from pprint      import pprint

from ..util.orderedset import OrderedSet

from .clause       import Clause
from .relationdict import RelationDict

class SymbolNet():
    '''
    Maps relations and relation causes of objects
    symbolDict:
        Dictionary {name : {relation : set(connected nodes)}}
        Each of connected nodes is in Dictionary
        An item is relationally atomic is it has no relations (terminal)
        An item is causally atomic if its cause is atomic: cause = '__atomic__'
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
        self.concludeDict[(cause.relation, cause.node)].append((relation, node))

        ckey, crelation, cnode = cause
        if crelation not in self.symbolDict[ckey]:
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

    def query(self, clause):
        return clause.name in self.symbolDict and\
               clause.relation in self.symbolDict[clause.name] and\
               clause.node in self.symbolDict[clause.name][clause.relation]

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
        seen = OrderedSet([clause])
        reasons = self.find_reasons(clause)
        pprint(reasons)
        while '__atomic__' not in seen:
            if len(reasons) == 0:
                break
            queue = []
            for reason in reasons:
                seen.add(reason)
                subreasons = self.find_reasons(reason)
                if subreasons:
                    print('Reasons for {}:'.format(reason))
                    pprint(subreasons)
                queue += subreasons
            reasons = queue
        return seen

    def _conclude(self, key):
        queue = []
        for relation, nodes in self.symbolDict[key].items():
            for node in nodes:
                if (relation, node) in self.concludeDict:
                    concludePairs = self.concludeDict[(relation, node)]
                    for cr, cn in concludePairs:
                        queue.append((key, cr, cn, Clause(key, relation, node)))
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
        self.trace_reasons(Clause(a, 'supersedes', b))

    def likely(self, key, endrelation, endnode):
        self._conclude(key)
                     
        reasonDict = defaultdict(set)
        for relation, nodes in self.symbolDict[key].items():
            for node in nodes:
                close = self.find_that(relation, node)
                for item in close:
                    if item != key:
                        reasonDict[item].add((relation, node))
        close = self.find_that(endrelation, endnode)
        for similarity, reasons in reasonDict.items():
            supersedes = self.query(Clause(similarity, 'supersedes', key))
            if similarity in close:
                if supersedes:
                    print('Because {} supersedes {}, it is certain that:'.format(key, similarity))
                    print('{} {} {}'.format(key, endrelation, endnode))
                else:
                    print('Because a {} is similar to a {}, a {} likely:'.format(key, similarity, key))
                    print(endrelation, endnode)
                    print('    {} and {} share:'.format(key, similarity))
                    for reason in reasons:
                        print('        {}'.format(reason))




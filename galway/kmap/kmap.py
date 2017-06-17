from collections import defaultdict, Counter
from pprint      import pprint
from copy        import deepcopy

from ..util.orderedset import OrderedSet

from .node import Node

class KnowledgeMap():
    
    def __init__(self):
        self.symbolDict = defaultdict(Node)

    def __copy__(self):
        newmap = KnowledgeMap()
        for k, v in self.__dict__.items():
            newmap.__dict__[k] = deepcopy(v)
        return newmap

    def __repr__(self):
        return str(self)

    def __str__(self):
        prettify = lambda kv : '{}:\n    {}'.format(*kv)
        return '\n'.join(map(prettify, self.symbolDict.items()))

    def add(self, key, relation, node, **kwargs):
        '''
        Add a piece of knowledge to the network

        Each piece of knowledge might have conditions and causes
        Conditions rely on states of instance objects
        '''
        self.symbolDict[key].add(relation, node, **kwargs)

    def current_state(self, key):
        return self.symbolDict[key].current_state()

    def rel_items(self, key):
        return self.symbolDict[key].relations.items()

    def inherit(self):
        newmap = self.__copy__()
        for key in self.symbolDict.keys():
            for relation, endnode in self.rel_items(key):
                if relation == 'isa':
                    for item in endnode:
                        for rel, e in self.rel_items(item.node):
                            for i in e:
                                newmap.add(key, rel, i.node, 
                                        causes=i.causes + (('isa', item.node),), 
                                        conditions=i.conditions)
        return newmap



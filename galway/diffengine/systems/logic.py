from pprint import pprint

from .system   import System
from .subterms import build_splitter, _strip_parens

from .. import logic_heuristics


'''
Objects:
    Expressions built recursively from:
        variables: P, Q, R
        binary connectives: ., ⊃, v
        unary: ~

Operators:
'''
strReplacements = '''
    AvB            <-> BvA
    A.B            <-> B.A
    A⊃B             -> ~B⊃~A
    AvA             -> A
    A.A             -> A
    Av(BvC)        <-> (AvB)vC
    A.(B.C)        <-> (A.B).C
    AvB            <-> ~(~A.~B)
    A⊃B            <-> ~AvB
    Av(B.C)        <-> (AvB).(AvC)
    A.(BvC)        <-> (A.B)v(A.C)
    A.B             -> A
    B.A             -> B
    '''
advanced = '''
    A               -> AvX
    [A, B]          -> A.B
    [A ⊃ B, A]      -> B
    [A ⊃ B, B ⊃ C]  -> A ⊃ C
''' 

'''
def deductions(theorems):
    options = set()
    for i, a in enumerate(theorems):
        for j, b in enumerate(theorems):
            if i != j:
                options.add(a + '.' + b)
    return options
'''

_imp_splitter = build_splitter(['⊃'])

def get_implications(t):
    implications = dict()
    terms = list(_imp_splitter(t))
    l = len(terms)
    for i, term in enumerate(terms):
        if term.startswith('('):
            pass
            #implications.update(get_implications(_strip_parens(term)))
        elif i + 2 < l:
            if terms[i + 1] == '⊃':
                implications[terms[i]] = terms[i + 2]
    return implications

def advanced_deductions(t):
    options = set()
    implications = dict()
    for subt in t.theorems:
        implications.update(get_implications(subt))
    for a, b in implications.items():
        if a in t.theorems:
            options.add(t + b)
        if b in implications:
            # A -> B, B -> C, therefore, A -> C
            options.add(t + (a + '⊃' + implications[b]))  
    return options

_heuristics = [f for f in logic_heuristics.__dict__.values() if callable(f)]
logic = System('logic', 
        strReplacements, ['.', 'v', '⊃'], _heuristics, advanced_deductions)

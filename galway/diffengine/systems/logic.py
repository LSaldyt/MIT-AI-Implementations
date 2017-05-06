from pprint import pprint

from .system    import System
from .transform import build_transformers
from .subterms  import build_subterm_function

'''
Objects:
    Expressions built recursively from:
        variables: P, Q, R
        binary connectives: ., ⊃, v
        unary: ~

Operators:
'''
strReplacements = '''
    ~(~A)           -> A
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

transformers = build_transformers(strReplacements)
subterms     = build_subterm_function(['.', 'v', '⊃'])

def find_replacements(node):
    options = set()
    terms = subterms(node)
    for t in transformers:
        t(node, terms, options)
    return options

def logic_branches(theorem):
    options = set()
    for t in find_replacements(theorem):
        options.add(t)
    return options

logic = System(logic_branches)


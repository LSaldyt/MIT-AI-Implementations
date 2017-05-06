from pprint import pprint

from .system    import System

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

heuristics = [f for f in logic_heuristics.__dict__.values() if callable(f)]
logic = System(strReplacements, ['.', 'v', '⊃'], heuristics)


'''
Objects:
    Expressions built recursively from:
        variables: P, Q, R
        binary connectives: ., ⊃, v
        unary: ~

Operators:
'''
replacements = '''
    AvB             -> BvA
    A.B             -> B.A
    A⊃B             -> ~B⊃~A
    AvA            <-> A
    A.A            <-> A
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

def build_transformers():
    transformers = dict()
    for line in replacements.split('\n'):
        terms = line.split()
        if len(terms) > 0:
            transformers[terms[0]] = terms[2]
    return transformers

transformers = build_transformers()

def logic_branches(node):
    options = []
    for a, b in transformers.items():
        options.append(node.replace(a, b))
    return options


import re

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

operators = ['v', '.', '⊃', '~']

pattern = '(%s)' % ')|('.join(map(re.escape, operators))

def subterms(formula):
    formula_terms = []
    items = [item for item in re.split(pattern, formula) if item is not None]
    for i, item in enumerate(items):
        if item not in operators:
            formula_terms.append(item)
            if i != len(items) - 1:
                formula_terms.append(item + ''.join(items[i + 1:]))
    return [term for term in formula_terms if len(term) > 0]


def logic_branches(node):
    options = set()
    formula_terms = subterms(node)
    for a, b in transformers.items():
        for i, term_a in enumerate(formula_terms):
            for term_b in formula_terms:
                a_pattern = a.replace('A', term_a).replace('B', term_b)
                b_pattern = b.replace('A', term_a).replace('B', term_b)

                next_formula = node.replace(a_pattern, b_pattern)
                next_formula = next_formula.replace('~~', '')
                options.add(next_formula)

    return options


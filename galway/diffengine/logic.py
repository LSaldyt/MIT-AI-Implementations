from pyparsing import *
from pprint import pprint
import string, re

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

def build_transformers():
    transformers = [] 
    for line in strReplacements.split('\n'):
        terms = line.split()
        if len(terms) > 0:
            transformers.append((terms[0], terms[2], terms[1] == '<->'))
    return transformers

transformers = build_transformers()

operators = ['v', '.', '⊃']#, '~']

split_ops = '(%s)' % ')|('.join(map(re.escape, operators))

split_imps = '(%s)' % ')|('.join(map(re.escape, ['⊃']))

def split_implications(formula):
    for item in re.split(split_imps, formula):
        if item is not None and item != '':
            yield item

def split_operators(formula):
    for item in re.split(split_ops, formula):
        if item is not None and item != '':
            if item not in operators and item != '~':
                yield item

def strip_parens(term):
    assert len(term) >= 2
    return term[1:-1]

def nested_matcher (n):
    # poor man's matched paren scanning, gives up after n+1 levels.
    # Matches any string with balanced parens or brackets inside; add
    # the outer parens yourself if needed.  Nongreedy.  Does not
    # distinguish parens and brackets as that would cause the
    # expression to grow exponentially rather than linearly in size.
    return "[^][()]*?(?:[([]"*n+"[^][()]*?"+"[])][^][()]*?)*?"*n

parens = re.compile('[^][()]+|[([]' + nested_matcher(100) + '[])]')

def split_parens(formula):
    return parens.findall(formula)

def subterms(formula, impsonly=False):
    terms = []
    
    items = split_parens(formula)
    for item in items:
        if item.startswith('('):
            terms.append(item)
            terms += subterms(strip_parens(item))
        else:
            if impsonly:
                for token in split_implications(item):
                    terms.append(token)
            else:
                for token in split_operators(item):
                    terms.append(token)
    return terms

def extensions(node):
    options = set()
    for char in 'DEFGHIJKLMNOPQRSTUVWXYZ':
        if char not in node:
            if len(node) > 1:
                options.add('(' + node + ')v' + char)
            else:
                options.add(node + 'v' + char)
            break
    return options

def replacements(node):
    options = set()
    def add_theorem(l_pattern, r_pattern):
        next_formula = node.replace(l_pattern, r_pattern)
        next_formula = next_formula.replace('~~', '')
        options.add(next_formula)
    formula_terms = subterms(node)
    for term_a in formula_terms:
        for term_b in formula_terms:
            for term_c in formula_terms:
                for left, right, inverse in transformers:
                    l_pattern = left.replace('A', term_a).replace('B', term_b).replace('C', term_c)
                    r_pattern = right.replace('A', term_a).replace('B', term_b).replace('C', term_c)

                    add_theorem(l_pattern, r_pattern)
                    if inverse:
                        add_theorem(r_pattern, l_pattern)
    return options


def deductions(theorems):
    options = set()
    for i, a in enumerate(theorems):
        for j, b in enumerate(theorems):
            if i != j:
                options.add(a + '.' + b)
    return options

def get_implications(t):
    implications = dict()
    terms = subterms(t, impsonly=True)
    l = len(terms)
    for i, term in enumerate(terms):
        if term.startswith('('):
            implications.update(get_implications(strip_parens(term)))
        elif i + 2 < l:
            if terms[i + 1] == '⊃':
                implications[terms[i]] = terms[i + 2]
    return implications

def advanced_deductions(theorems):
    options = set()
    implications = dict()
    for t in theorems:
        implications.update(get_implications(t))
    for a, b in implications.items():
        if a in theorems:
            options.add(b)
        if b in implications:
            options.add(a + '⊃' + implications[b]) # A -> B, B -> C, therefore, A -> C 
    return options

def logic_branches(theorems):
    options = set()

    for theorem in theorems:
        for t in replacements(theorem):#extensions(theorem) | replacements(theorem):
            if t not in theorems:
                options.add(theorems + (t,))
    for t in deductions(theorems) | advanced_deductions(theorems):
        if t not in theorems:
            options.add(theorems + (t,))
    return options


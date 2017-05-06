from collections import namedtuple
from functools   import partial

Replacement = namedtuple('Replacement', ['left', 'right', 'reversible'])

def _build_replacements(replacementStr):
    replacements = []
    for line in replacementStr.split('\n'):
        terms = line.split()
        if len(terms) > 0:
            replacements.append(Replacement(
                terms[0], terms[2], terms[1] == '<->'))
    return replacements

def _apply_replacement(node, terms, options, replacement):
    for term_a in terms:
        for term_b in terms:
            for term_c in terms:
                l_pattern = replacement.left.replace('A', term_a).replace('B', term_b).replace('C', term_c)
                r_pattern = replacement.right.replace('A', term_a).replace('B', term_b).replace('C', term_c)
                next_formula = node.replace(l_pattern, r_pattern).replace('~~','')
                options.add(next_formula)
                if replacement.reversible:
                    next_formula = node.replace(r_pattern, l_pattern).replace('~~','')
                    options.add(next_formula)

def build_transformers(replacementStr):
    replacements = _build_replacements(replacementStr)
    return [partial(_apply_replacement, replacement=r) for r in replacements]



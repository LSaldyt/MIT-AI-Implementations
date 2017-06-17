import string, re

def build_splitter(terms):
    splitRegex = '(%s)' % ')|('.join(map(re.escape, terms))
    splitRegex = re.compile(splitRegex)
    def splitter(line):
        for item in re.split(splitRegex, line):
            if item is not None and item != '':
                yield item
    return splitter

def alt_build_splitter(terms):
    discard = set()
    for term, keep in terms:
        if not keep:
            discard.add(term)
    terms = [term for term, keep in terms]
    inner_splitter = build_splitter(terms)
    def splitter(line):
        return (item for item in inner_splitter(line) if item not in discard)
    return splitter

def _strip_parens(term):
    a = len(term) >= 2
    b = term[0]  == '('
    c = term[-1] == ')'
    if a and b and c:
        return term[1:-1]
    else:
        return term

def _nested_matcher (n):
    '''
    Poor man's matched paren scanning, gives up after n+1 levels.
    Matches any string with balanced parens or brackets inside; add
        the outer parens yourself if needed.  Nongreedy.  Does not
        distinguish parens and brackets as that would cause the
        expression to grow exponentially rather than linearly in size.
    '''
    return "[^][()]*?(?:[([]"*n+"[^][()]*?"+"[])][^][()]*?)*?"*n

_parens = re.compile('[^][()]+|[([]' + _nested_matcher(100) + '[])]')

def _split_parens(formula):
    return _parens.findall(str(formula))

def build_subterm_function(splitby):
    splitter = build_splitter(splitby)
    def subterms(formula):
        terms = []
        items = _split_parens(formula)
        for item in items:
            if item.startswith('('):
                terms.append(item)
                terms += subterms(_strip_parens(item))
            else:
                for token in splitter(item):
                    terms.append(token)
        return terms
    return subterms

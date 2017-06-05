from ..util.subterms import alt_build_splitter
from .symnet         import SymbolNet, Clause

natural_language_splitter = alt_build_splitter(
       [(' ', False),
        ('?', True), 
        ('\n', False)])


def read_natural_language(filename):
    net = SymbolNet()
    '''
    net.add('firetruck', 'isa', 'vehicle')
    net.find_that('is', 'weak')
    net.find_close([('is', 'weak'), ('is', 'greedy'), ('isa', 'noble')])
    net.find_by('is', 'weak', 'tired')
    net.trace_reasons(Clause('macbeth', 'is', 'weak'))
    net.show('mystery-object', 'cup')
    net.likely('glass', 'hasa', 'concavity')
    net.analogize('cup', 'drinking', 'briefcase')
    '''
    with open(filename, 'r') as infile:
        for line in infile:
            terms = list(natural_language_splitter(line))
            assert len(terms) > 0
            if terms[-1] == '?':
                net.likely(*(terms[:-1]))
            else:
                assert len(terms) == 3
                net.add(*terms)
    print(net)

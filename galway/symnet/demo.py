from .symnet import SymbolNet, Clause

def description_matching():
    net = SymbolNet()
    net.add('firetruck', 'isa', 'vehicle')
    net.add('firetruck', 'is', 'red')
    net.add('firetruck', 'is', 'metal')
    net.add('apple', 'isa', 'fruit')
    net.add('apple', 'is', 'red')
    net.add('apple', 'is', 'round')

    print(net.find_by('is', 'red', 'round'))

def macbeth():
    net = SymbolNet()
    net.add('macbeth', 'murder', 'duncan')
    net.add('duncan', 'isa', 'king')
    net.add('macbeth', 'isa', 'noble')
    net.add('macbeth', 'has-spouse', 'lady macbeth')
    net.add('lady-macbeth', 'is', 'greedy')
    net.add('lady-macbeth', 'is', 'domineering')
    net.add('macbeth', 'is', 'tired', cause=Clause('lady-macbeth', 'is', 'domineering'))
    net.add('macbeth', 'is', 'weak', cause=Clause('macbeth', 'is', 'tired'))
    print(net)
    print('* is weak:')
    print(net.find_that('is', 'weak'))
    print('* is weak, greedy, and a noble:')
    print(net.find_close([('is', 'weak'), ('is', 'greedy'), ('isa', 'noble')]))
    print('* is weak and tired:')
    print(net.find_by('is', 'weak', 'tired'))
    print('macbeth is weak because:')
    print(net.trace_reasons(Clause('macbeth', 'is', 'weak')))

def cup():
    net = SymbolNet()
    net.add('brick', 'is', 'stable', cause=Clause('brick', 'hasa', 'flatbottom'))
    net.add('brick', 'is', 'heavy')
    net.add('glass', 'enables', 'drinking', causes=[Clause('glass', 'hasa', 'handle'), Clause('glass', 'carries', 'liquid')])
    net.add('glass', 'is', 'pretty')
    net.add('briefcase', 'is', 'liftable', causes=[Clause('briefcase', 'has', 'handle'), Clause('briefcase', 'is', 'light')])
    net.add('briefcase', 'is', 'useful', cause=Clause('briefcase', 'holds', 'papers'))
    net.add('bowl', 'carries', 'liquid', cause=Clause('bowl', 'has', 'concavity'))
    net.add('bowl', 'contains', 'cherry-soup')

    net.add('cup', 'is', 'stable')
    net.add('cup', 'enables', 'drinking')

    net.add('mystery-object', 'madeof', 'porcelain')
    net.add('mystery-object', 'hasa', 'decoration')
    net.add('mystery-object', 'hasa', 'concavity')
    net.add('mystery-object', 'hasa', 'handle')
    net.add('mystery-object', 'hasa', 'flatbottom')

    print(net)
    net.show('mystery-object', 'cup')
    print(net.relationTypes)

    net.likely('glass', 'hasa', 'concavity')
    net.likely('cup', 'hasa', 'concavity')
    net.likely('mystery-object', 'is', 'heavy')

def demo():
    #description_matching()
    #macbeth()
    cup()

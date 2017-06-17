from .kmap import KnowledgeMap
from pprint import pprint

def demo():
    '''
    Why can you pull something with a string but not push it?
    '''
    km = KnowledgeMap()
    km.add('string', 'can', 'force-transfer', conditions=['taut'])
    km.add('string', 'is', 'taut',            conditions=['pulling'])
    km.add('push', 'isa', 'movement')
    km.add('pull', 'isa', 'movement')
    km.add('movement', 'requires', 'force-transfer')
    km.add('string', 'is', 'pulling')
    '''
    Because pulling is a movement, it requires force-transfer
    Because pushing is a movement, it requires force-transfer
    Strings can only transfer force when taut
    Strings are not taut when pushing 
    Strings can only pull, not push
    '''
    current = km.inherit()
    print(current.current_state('string')['can'])

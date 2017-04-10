from symbol     import Symbol
from countstore import CountStorage

class SymbolStorage(dict):
    def __init__(self):
        super().__init__()

        self.substorages = {
                'kind'       : CountStorage(),
                'char'       : CountStorage(),
                'origin'     : CountStorage(),
                'components' : CountStorage()
                    }
        self.undefined = []

    def _sub(self, storename):
        return self.substorages[storename]

    def add(self, *args, **kwargs):
        if len(args) == 1 and len(kwargs) == 0:
            symbol = args[0]
        else:
            symbol = Symbol(*args, **kwargs)
        self[symbol.name] = symbol
        
        self.undefined.append(symbol.name)
        self.update()

    def update(self):
        pending = []
        for name in self.undefined:
            if name not in self:
                pending.append(name)
            else:
                sym = self[name]
                for char in self.chars_of(name):
                    self._sub('char').add(name, char)
                for component in sym.components:
                    self._sub('components').add(name, component.name)
                if sym.origin is not None:
                    self._sub('origin').add(name, sym.origin)
                if sym.kind is not None:
                    self._sub('kind').add(name, sym.origin)

        self.undefined = pending

    def chars_of(self, name):
        '''
        Recursively retrieve the characteristics of a symbol "name"
        Stops once atomic symbols (no parents) are found
        '''
        chars = []
        if name not in self: 
            if name not in self.undefined:
                self.undefined.append(name)
            return chars
        sym   = self[name]

        chars += sym.characteristics
        for component in sym.components:
            # Components are atomic, no recursion needed
            chars += component.characteristics
        if sym.kind is not None:
            chars += self.chars_of(sym.kind)
        return chars

    def find_by(self, items, storename):
        print('%s best matched the %s items %s' % (self._sub(storename).find(items), storename, items))


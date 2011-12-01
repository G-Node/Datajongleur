import numpy as np

class Bunch(dict):

    def __init__(self, dic={}, **kw):
        #also works if dic is a Bunch - XXX write tests
        here = dict(dic).copy() # avoid data sharing!
        here.update(kw) # kw overrides dic
        bunchified = self._bunchify(here) # convert deep to Bunch
        dict.__init__(self, bunchified)
        self.__dict__.update(bunchified)


    def _bunchify(self, dic):
        """Take a dictionary and return an (item, value) list where
        all dict-like values have been turned into bunches,
        recursively."""
        return [(k, Bunch(v))
                if hasattr(v,'keys') else (k, v) for k,v in dic.items()]

    
    def __setattr__(self, name, val):
        """Make dictionary keys available as class attributes."""
        if hasattr(val, 'keys'):
            val = Bunch(val)
        self[name] = val
        self.__dict__[name] = val


    def update(self, dic={}, **kw):
        dic.update(kw)
        dict.update(self, dic)
        self.__dict__.update(dic)

    def __add__(self, b2):
        #XXX implement exception raise if key collision
        #(if update semantics meant, use update method (or << operator (TBD)?)
        #do it with set intersection between keys
        return Bunch(self, **b2)

    def copy(self):
        """Return a copy.
        """
        return Bunch(self)


    __repr__ = dict.__repr__


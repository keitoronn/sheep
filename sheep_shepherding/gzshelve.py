# -*- coding: utf-8 -*-
import shelve
import dbm
from pickle import Pickler, Unpickler
from io import BytesIO
from zlib import compress, decompress
__all__ = ['gzShelf', 'open']

class gzShelf(shelve.Shelf) :
    def __init__(self, dict, protocol=None, writeback=False, keyencoding="utf-8") :
        shelve.Shelf.__init__(self, dict, protocol, writeback, keyencoding)

    def __getitem__(self, key) :
        try:
            value = self.cache[key]
        except KeyError:
            f = BytesIO(decompress(self.dict[key.encode(self.keyencoding)]))
            value = Unpickler(f).load()
            if self.writeback:
                self.cache[key] = value
        return value

    def __setitem__(self, key, value):
        if self.writeback:
            self.cache[key] = value
        f = BytesIO()
        p = Pickler(f, self._protocol)
        p.dump(value)
        self.dict[key.encode(self.keyencoding)] = compress(f.getvalue())

class DbfilenameShelf(gzShelf):
    """Shelf implementation using the "dbm" generic dbm interface.

    This is initialized with the filename for the dbm database.
    See the module's __doc__ string for an overview of the interface.
    """

    def __init__(self, filename, flag='c', protocol=None, writeback=False):
        import dbm
        gzShelf.__init__(self, dbm.open(filename, flag), protocol, writeback)

def open(filename, flag='c', protocol=None, writeback=False) :
    return DbfilenameShelf(filename, flag, protocol, writeback)
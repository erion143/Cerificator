import shelve as sh
from copy import copy


class FewArgsException(Exception):
    pass


class Creator:
    name = 'Creator'
    is_empty = False
    batch = None
    customer = None
    analyser = None

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        if not self.verify() and not self.is_empty:
            raise FewArgsException
        elif not self.is_empty:
            with sh.open(self.__class__.name) as store:
                store[self.batch] = self.__dict__

    def verify(self):
        for val in self.__dict__.values():
            if val is None:
                return False
        return True

    def get_batches(self):
        with sh.open(self.__class__.name) as store:
            return [i for i in store.keys()]

    def get_batch_date(self, batch):
        cur_batch = self.get_obj_from_store(batch)
        if cur_batch is None:
            return None
        else:
            return cur_batch['date']

    def get_obj_from_store(self, batch):
        with sh.open(self.__class__.name) as store:
            return store.get(batch, None)

    def save(self):
        if not self.is_empty:
            d = copy(self.__dict__)
            #d.pop('is_empty')
            with sh.open(self.__class__.name) as store:
                store[self.batch] = d

    def rm(self, batch):
        with sh.open(self.__class__.name) as store:
            store.pop(batch)

    def __call__(self, **kwargs):
        if self.is_empty:
            return self.__class__(**kwargs)


class Emulsion0(Creator):
    name = 'Emulsion'
    brand = 'Umacoll 83M'
    batch = None
    date = None
    nvc = None
    brookf = None
    dens = None
    ph = None
    thermastab = None


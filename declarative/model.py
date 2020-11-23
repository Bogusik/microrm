import inspect
import asyncpg
from . import Query

class Model:

    __table__ = ''
    __conn__ = None

    def __init__(self, record=None, **k):

        if record:
            self.set_record(record)

        for k,v in k.items():
            getattr(self, k).value = v

    @classmethod
    def columns(cls):
        t = []
        for i, v in inspect.getmembers(cls):
            if v.__class__.__name__ == "Column":
                t.append((i, v))
        return dict(t)
    
    @classmethod
    def columns_vals(cls):
        t = []
        for i, v in inspect.getmembers(cls):
            if v.__class__.__name__ == "Column":
                t.append((i, v.value))
        return dict(t)

    @classmethod
    def query(cls):
        return Query.set_model(cls) 

    def is_empty(self):
        return len(self._data) == 0


    def not_empty(self):
        return not self.is_empty()

    @classmethod
    def conn(cls, conn):
        cls.__conn__ = conn
        return cls


    def set_record(self, record):
        for k in record.keys():
            getattr(self, k).value = record[k]
        return self

    def __str__(self):
        return self.__table__

    def validate(self):
        return all([v.validate() for v in self.columns().values()])

    @classmethod
    def _get_name(cls):
        return cls.__name__.lower()

    def insert(self):
        return Query().set_model(self.__class__).insert(**self.columns())
    
    def update(self):
        return Query().set_model(self).update(**self.columns()).where(self.id==self.id.value)

    def delete(self):
        return Query().set_model(self).delete().where(self.id==self.id.value)
    
    @classmethod
    def find(cls, expr=None):
        return Query().set_model(cls).select().where(expr)

    @classmethod
    def join(cls, model, on=None, type='INNER'):
        Query().set_model(cls).add_model(model).join(model, on, type)
        return cls
    
    @classmethod
    def get(cls, id):
        return Query().set_model(cls).select().where(cls.id == id)
    
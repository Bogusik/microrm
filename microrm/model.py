import inspect
import asyncpg
from microrm.declarative import Query

class Model:

    __table__ = ''
    __conn__ = None
    id=None

    def __init__(self, record=None, **k):

        for v in inspect.getmembers(self):
            if v[1].__class__.__name__ == "Column":
                v[1].value = None

        if record:
            self.set_record(record)

        for k,v in k.items():
            try:
                getattr(self, k).value = v
            except AttributeError:
                continue

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
        return Query().set_model(cls) 


    @classmethod
    def conn(cls, conn):
        cls.__conn__ = conn
        return cls


    def set_record(self, record):
        for k in record.keys():
            try:
                getattr(self, k).value = record[k]
            except AttributeError:
                pass
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
        return Query().set_model(self.__class__).update(**self.columns()).where(self.id==self.id.value)

    def delete(self):
        return Query().set_model(self.__class__).delete().where(self.id==self.id.value)

    @classmethod
    def find(cls, expr=None):
        return Query().set_model(cls).select().where(expr)

    @classmethod
    def join(cls, model, on=None, type='INNER'):
        return Query().set_model(cls).add_model(model).join(model, on, type)

    @classmethod
    def get(cls, id):
        return Query().set_model(cls).select().where(cls.id == id)

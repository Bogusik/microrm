import re, datetime
import inspect
import asyncpg
from ..columns import Column, Expression


SQL_KEYWORDS = [
        "AND",
        "OR",
    ]

def _construct_for_list(item, *models):
    ls = []
    for i in item:
        if isinstance(i, Column):
            ls.append(_construct_for_column(i, *models))
        else:
            ls.append(str(i))

    return ls

def _construct_for_column(item, *models):
    for model in models:
        for name, field in inspect.getmembers(model):
            if item is field:
                return f"{model.__table__}.{name}"

class Query(object):


    sql = []

    __model__ = None

    __models = []

    def set_model(self, model):
        self.__model__ = model
        return self

    def __getattr__(self, name):
        if name in SQL_KEYWORDS:
            self.sql.append(name)
        return self
    
    def add_model(self, model):
        self.__models.append(model)
        return self

    def select(self, *argv):
        l = []
        if argv:
            l = list(argv)
        else:
            l = '*'

        self.sql = ["SELECT", l, "FROM", self.__model__.__table__] + self.sql
        
        return self
        
    
    def update(self, **argv):
        values = []
        for k, v in argv.items():
            if v.value and v.primary == False:
                if isinstance(v.value, int):
                    t = str(v.value)
                else:
                    t = f"'{v.value}'"
                values.append(f"{k} = {t}")
        if argv:
            self.sql = ["UPDATE", self.__model__.__table__, "SET", values] + self.sql

        return self

    
    def insert(self, **argv):
        keys = []
        values = []
        for k, v in argv.items():
            if v.value and v.primary == False:
                if isinstance(v.value, int):
                    t = str(v.value)
                else:
                    t = f"'{v.value}'"
                keys.append(k)
                values.append(t)


        self.sql = ["INSERT INTO", self.__model__.__table__, "(", ', '.join(keys), ") VALUES (", values, ")"] + self.sql

        return self


    def delete(self):      
        self.sql = ["DELETE FROM", self.__model__.__table__] + self.sql

        return self
    
    def returning(self, *argv):      
        self.sql.extend(["RETURNING", list(argv)])

        return self

    def where(self, expr):
        if expr:
            if expr:
                self.sql.extend(["WHERE", expr])
        return self
    

    def order_by(self, *k, asc=[]):
        if k:
            if len(asc) < len(k):
                asc.extend([True]*(len(k)-len(asc)))


        return self


    def join(self, model, on, type='INNER'):
        self.__models.append(model)
        self.sql.extend([f"{type} JOIN", model, "ON", on])
        return self

    def __str__(self):
        return "(" + self._construct_sql() + ")"


    def _construct_sql(self):
        sql_ = ''
        for item in self.sql:
            if isinstance(item, str):
                sql_ += f"{item}"
            elif issubclass(item.__class__, self.__model__.__class__):
                sql_ += f"{item.__table__}"
            elif isinstance(item, list):
                sql_ += ', '.join(_construct_for_list(item, self.__model__, *self.__models))
            elif isinstance(item, Column):
               sql_ += _construct_for_column(item)
            elif isinstance(item, Expression):
                sql_ += ' '.join(_construct_for_list(item.expr, self.__model__, *self.__models))
            sql_ += ' '
        return sql_[:-1]


    async def execute(self, conn):
        print(self._construct_sql())
        await conn.execute(self._construct_sql())
        self.sql = []
    
    async def fetch(self, conn):
        records = await conn.fetch(self._construct_sql())

        self.sql = []
        return [self.__model__(record) for record in records]
    

    async def fetchval(self, conn):
        value = await conn.fetchval(self._construct_sql())

        self.sql = []
        return value
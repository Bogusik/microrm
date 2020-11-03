import re
import inspect
from microrm.column import Column
from microrm.model import Model
from microrm.expression import Expression

SQL_KEYWORDS = [
        "AND",
        "OR",
    ]

class Query(object):

    sql = []

    def __init__(self, model):
        self.models = [model]

    def __getattr__(self, name):
        if name in SQL_KEYWORDS:
            self.sql.append(name)
        return self

    def select(self, *argv):
        if argv:
            self.sql = ["SELECT", list(argv), "FROM", self.models[0]]
        else:
            self.sql = ["SELECT", ['*'], "FROM", self.models[0]]

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

    def join(self, model, on=None, using=None, type='INNER'):
        self.models.append(model)
        if on:
            end = ["ON", on]
        else:
            end = ["USING", using]
        self.sql.extend([f"{type} JOIN ", model, *end])
        return self

    def __str__(self):
        return "(" + " ".join([str(t) for t in self.sql]) + ")"


    def _construct_sql(self):
        sql = ''
        for item in self.sql:
            if isinstance(item, str):
                sql += f"{item} "
            elif issubclass(item.__class__, Model.__class__):
                sql += f"{item.__table__} "
            elif isinstance(item, list):
               sql += ', '.join(self.__construct_for_list(item))
            elif isinstance(item, Column):
               sql += self.__construct_for_column(item)
            elif isinstance(item, Expression):
                sql += ' '.join(self.__construct_for_list(item.expr))
        return sql


    def __construct_for_list(self, item):
        ls = []
        for i in item:
            print(i, isinstance(i, Column))
            if isinstance(i, Column):
                for model in self.models:
                    for name, field in inspect.getmembers(model):
                        if i is field:
                            ls.append(f"{model.__table__}.{name} ")
            elif isinstance(i, str):
                ls.append(i)

        return ls

    def __construct_for_column(self, i):
        for model in self.models:
            for name, field in inspect.getmembers(model):
                if id(i) == id(field):
                    return f"{model.__table__}.{name} "
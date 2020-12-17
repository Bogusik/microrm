import re
import inspect
import asyncpg


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
        if model not in self.__models:
            self.__models.append(model)
        return self

    def __getattr__(self, name):
        if name in SQL_KEYWORDS:
            self.sql.append(name)
        return self

    def add_model(self, model):
        if model not in self.__models:
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
                values.append(f"{k} = '{v.value}'")
        if argv:
            self.sql = ["UPDATE", self.__model__.__table__, "SET", values] + self.sql

        return self


    def insert(self, **argv):
        keys = []
        values = []
        for k, v in argv.items():
            if v.value and v.primary == False:
                keys.append(k)
                values.append(f"'{v.value}'")


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
        await conn.execute(self._construct_sql())
        self.sql = []

    async def fetch(self, conn, md=None):
        if not md:
            md = self.__model__()
        else:
            md = md()
            for model in self.__models:
                for c, v in model.columns().items():
                    setattr(md, c, v)
        records = await conn.fetch(self._construct_sql())

        self.sql = []
        return ModelList(md, [record for record in records])


    async def fetchval(self, conn):
        value = await conn.fetchval(self._construct_sql())

        self.sql = []
        return value


class ModelList:

    def __init__(self, model, models=[]):
        self.model = model
        self.models = models[:]

    def first(self):
        if self.models:
            return self.model.set_record(self.models[0])
        else:
            return None

    def last(self):
        if self.models:
            return self.model.set_record(self.models[-1])
        else:
            return None

    def __iter__(self):
        return ModelListIterator(self)


class ModelListIterator:

    def __init__(self, model_list):
        self.model_list = model_list
        self.index = 0

    def __next__(self):
        if self.index < len(self.model_list.models) :
            res = self.model_list.model.set_record(self.model_list.models[self.index])
            self.index +=1
            return res
        raise StopIteration

class Column:

    def __init__(self, type=None, primary=False, validators=[], null=True):
        self.value = None
        self.validators = validators
        self.type = type
        self.primary = primary
        self.null = null

    def _validate_val(self, val=None):
        if self.validators:
            return all([v.validate(val) for v in self.validators])
        else:
            return True

    def validate(self, val=None):
        if not val:
            val = self.value
        if val:
            return self._validate_val(val)
        else:
            if self.null:
                return True
            else:
                return False

    def __eq__(self, other):
        if other:
            return Expression(self, "=", other)
        else:
            return Expression(self, "IS", other)

    def __lt__(self, other) :
        return Expression(self, "<", other)

    def __le__(self, other) :
        return Expression(self, "<=", other)

    def __gt__(self, other) :
        return Expression(self, ">", other)

    def __ge__(self, other) :
        return Expression(self, ">=", other)

    def __ne__(self, other) :
        if other:
            return Expression(self, "!=", other)
        else:
            return Expression(self, "IS NOT", other)

    def __and__(self, other) :
        return Expression(self, "AND", other)

    def __or__(self, other) :
        return Expression(self, "OR", other)

    def __rshift__(self, other):
        return Expression(self, "IN", other)

    def __lshift__(self, other):
        return Expression(self, "NOT IN", other)


class Expression:

    def __init__(self, obj=None, operator=None, other=None):
        self.expr = []
        self.obj = obj
        if operator:
            self.__operator(operator, other)

    def __eq__(self, other):
        return self.__operator("=", other)

    def __lt__(self, other):
        return self.__operator("<", other)

    def __rshift__(self, other):
        return self.__operator("IN", other)

    def __lshift__(self, other):
        return self.__operator("NOT IN", other)

    def __le__(self, other):
        return self.__operator("<=", other)

    def __gt__(self, other):
        return self.__operator(">", other)

    def __ge__(self, other):
        return self.__operator(">=", other)

    def __ne__(self, other):
        return self.__operator("!=", other)

    def __and__(self, other):
        return self.__operator("AND", other)

    def __or__(self, other):
        return self.__operator("OR", other)

    def __repr__(self):
        return repr(self.expr)

    def __str__(self):
        return " ".join([str(e) for e in self.expr])

    def __operator(self, operator, other):
        last_str = ""
        if isinstance(other, self.__class__):
            self.expr.extend([operator, *other.expr])
            return self
        elif not other:
            last_str = "NULL"
        elif isinstance(other, Query):
            last_str = other
        elif isinstance(other, str):
            last_str = "'" + other + "'"
        else:
            last_str = "'" + str(other) + "'"

        self.expr.extend([self.obj, operator, last_str])

        return self
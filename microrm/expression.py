import microrm.column

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
        elif isinstance(other, str):
            last_str = "'" + str(other) + "'"
        elif not other:
            last_str = "NULL"
        elif isinstance(other, microrm.column.Column):
            last_str = other
        else:
            last_str = str(other)

        self.expr.extend([self.obj, operator, last_str])

        return self
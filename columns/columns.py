
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
        elif isinstance(other, Column):
            last_str = other
        else:
            last_str = "'" + str(other) + "'"

        self.expr.extend([self.obj, operator, last_str])

        return self
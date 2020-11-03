
from microrm.expression import Expression

class Column:

    def __init__(self, value=None, type=None, validators=[]):
        self.validators = validators
        self.validate_val(value)
        self.value = value
        self.type = type

    def validate_val(self, val=None):
        return all([v.validate(val) for v in self.validators])

    def validate(self):
        return self.validate_val(self.value)

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

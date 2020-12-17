import re


class Validator:

    @staticmethod
    def length(string, min_val=0, max_val=100):
        if not string:
            return True

        return min_val <= len(string) <= max_val

    @staticmethod
    def re(string, r):
        if not string:
            return True

        if re.search(r, string):
            return True
        else:
            return False


class LengthValidator(Validator):

    def __init__(self, min_val=0, max_val=100):
        self.min = min_val
        self.max = max_val

    def validate(self, value):
        return self.length(value, self.min, self.max)


class ReValidator(Validator):

    def __init__(self, r):
        self.r = r

    def validate(self, value):
        return self.re(value, self.r)


class EmailValidator(ReValidator):

    def __init__(self):
        self.r = r"(^[a-z0-9_.+-]+@[a-z0-9-]+\.[a-z0-9-.]+$)"


class UsernameValidator(ReValidator):

    def __init__(self):
        self.r = r"(^[a-z0-9_.-]+$)"


class NameValidator(ReValidator):

    def __init__(self):
        self.r = r"(^[a-zA-Z0-9\s_.-]+$)"
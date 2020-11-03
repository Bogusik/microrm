import inspect

from microrm.column import Column


class Model:

    __table__ = ''


    def __init__(self, record=None, **k):
        self._data = {
            'id': None
        }

        if record:
            self.set_record(record)

        for k,v in k.items():
            self._data[k] = v


    def __getattribute__(self, key):
        _data = object.__getattribute__(self, '_data')
        if key in _data:
            return _data[key]
        return object.__getattribute__(self, key)

    def is_empty(self):
        return len(self._data) == 0

    def not_empty(self):
        return not self.is_empty()

    def set_record(self, record):
        for k, v in record:
            self._data[k] = v
        return self

    def __str__(self):
        return self.__table__


    def validate(self, *args):
        if args:
            return all([v.validate() for v in args])

        return all([getattr(self, v).validate() for k, v in self._data.items() if issubclass(v.__class__, Column)])

    @classmethod
    def _get_name(cls):
        return cls.__name__.lower()

    @classmethod
    async def add(cls, request):
        async with request.app.config['db'].acquire() as conn:
            columns = ", ".join(cls.__dict__.keys())
            values = ", ".join([f"${i+1}" for i in range(len(cls.__dict__.values()))])
            sql = f'''
                INSERT INTO {cls.__table__}({columns})
                VALUES
                    ({values})
                RETURNING id
            '''
            cls.id = await conn.fetchval(
                sql,
                *cls.__dict__.values()
            )
            return cls

    @classmethod
    async def update(cls, request):
        async with request.app.config['db'].acquire() as conn:

            row = ''
            for i, k in enumerate(cls.__dict__.keys()):
                row += f"{k}=${i+1},"

            sql = f'''
                UPDATE users
                SET
                    {row[:-1]}
                WHERE
                    id = {cls.id}
            '''
            await conn.execute(sql, *cls.__dict__.values())
            return cls

    @classmethod
    async def delete(cls, request, **k):
        async with request.app.config['db'].acquire() as conn:
            sql = f'''
                DELETE FROM {cls.__table__} WHERE
            '''

            values = []
            variables = []

            for i, (name, value) in enumerate(k.items()):
                variables.append(f" {name}=${i+1}")
                values.append(value)

            sql += "AND ".join(variables)

            await conn.execute(sql, cls.id)
            return cls

    @classmethod
    async def find(cls, request, **k):
        async with request.app.config['db'].acquire() as conn:
            sql = '''
                    SELECT * FROM users WHERE
            '''

            values = []
            variables = []

            for i, (k, v) in enumerate(k.items()):
                variables.append(f"{k}=${i+1}")
                values.append(v)

            sql += " AND ".join(variables)

            cls.records = await conn.fetch(sql, *values)
            return cls
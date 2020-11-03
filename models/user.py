import secrets
from microrm.model import Model
from microrm.column import Column
from microrm.validator import LengthValidator, UsernameValidator, NicknameValidator, EmailValidator

class User(Model):

    __table__ = 'users'

    id = Column()
    username = Column(validators=[LengthValidator(max_val=50), UsernameValidator()])
    nickname = Column(validators=[LengthValidator(max_val=50), NicknameValidator()])
    status = Column(validators=[LengthValidator(max_val=50)])
    avatar = Column(validators=[LengthValidator(max_val=50)])
    email = Column(validators=[LengthValidator(max_val=50), EmailValidator()])
    verified = Column()
    verification_token = Column(value=secrets.token_urlsafe(16), validators=[LengthValidator(max_val=50)])
    password = Column(validators=[LengthValidator(max_val=256)])
    registration_date = Column()

    def to_dict(self):
        return {
            'id': self.id.value,
            'username': self.username.value,
            'status': self.status.value,
            'nickname': self.nickname.value,
            'avatar': self.avatar.value,
            'email': self.email.value
        }

    async def delete(self, request):
        async with request.app.config['db'].acquire() as conn:
            sql = '''
                DELETE FROM users WHERE id = $1
            '''
            await conn.execute(sql, self.id)
            return self


    async def get(self, request, _id):
        async with request.app.config['db'].acquire() as conn:
            sql = '''
                SELECT * FROM users WHERE id = $1
            '''
            self.set_record(await conn.fetchrow(sql, _id))
            return self

    def to_lower(self):
        self.username = self.username.lower() if self.username else None
        self.email = self.username.lower() if self.email else None

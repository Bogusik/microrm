import secrets
from microrm.model import Model
from microrm.column import Column
from microrm.validator import LengthValidator, UsernameValidator, NicknameValidator, EmailValidator


class UserRoles(Model):

    __table__ = 'user_roles'

    role_id = Column(validators=[LengthValidator(max_val=50), UsernameValidator()])
    user_id = Column(validators=[LengthValidator(max_val=50), UsernameValidator()])
    workspace_id = Column(validators=[LengthValidator(max_val=50), NicknameValidator()])

    def to_dict(self):
        return {
            'id': self.id.value,
            'username': self.username.value,
            'status': self.status.value,
            'nickname': self.nickname.value,
            'avatar': self.avatar.value,
            'email': self.email.value
        }

    def to_lower(self):
        self.username = self.username.lower() if self.username else None
        self.email = self.username.lower() if self.email else None

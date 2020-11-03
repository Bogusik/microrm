from microrm.query import Query
from models.user import User
from models.user_roles import UserRoles

q = Query(User).select(User.username, User.id).where(User.username == User.id).join(UserRoles, on=(UserRoles.user_id==User.id))


print(q.sql)
print(q._construct_sql())
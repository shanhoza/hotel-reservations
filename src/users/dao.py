from dao.base import BaseDAO
from users.models import Users


class UserDAO(BaseDAO):
    model = Users

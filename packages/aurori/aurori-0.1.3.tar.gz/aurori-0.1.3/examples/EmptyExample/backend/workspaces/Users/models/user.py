from aurori import db
from sqlalchemy_utils import ArrowType
import arrow
from aurori.users.basemodels import UserBase

class User(UserBase):
    global_user_id = db.Column(db.String(255), default='')
    home_server = db.Column(db.String(255), default='')

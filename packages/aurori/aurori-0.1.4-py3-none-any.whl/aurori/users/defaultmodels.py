"""
The aurori project

Copyright (C) 2022  Marcus Drobisch,

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

__authors__ = ["Marcus Drobisch"]
__contact__ = "aurori@fabba.space"
__credits__ = []
__license__ = "AGPLv3+"

from aurori import db, bcrypt
from aurori.users.basemodels import UserBase
import hashlib
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
from sqlalchemy_utils import ArrowType
import arrow

class User(UserBase):
    def __init__(self, email, password, isAdmin=False, skip_password=False):
        self.email = email
        if skip_password is False:
            self.password = password
        self.admin = isAdmin

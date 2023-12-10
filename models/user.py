#!/usr/bin/python3
""" this module is for creating User model"""

from models.base_model import BaseModel


class User(BaseModel):
    """ User class that inherit from BaseModel """

    email = " "
    password = " "
    first_name = " "
    last_name = " "

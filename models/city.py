#!/usr/bin/python3
""" this module is for creating City model"""

from models.base_model import BaseModel


class City(BaseModel):
    """ City class that inherit from BaseModel """
    state_id = ""
    name = ""

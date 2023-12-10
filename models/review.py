#!/usr/bin/python3
""" this module is for creating Review model"""
from models.base_model import BaseModel


class Review(BaseModel):
    """ Review class that inherit from BaseModel """
    place_id = ""
    user_id = ""
    text = ""

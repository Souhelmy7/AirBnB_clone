 a `FileStorage` class for serializing instances to a JSON file
and deserializing a JSON file to instances.
"""

import json
import os
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Class for serializing instances and deserializing a JSON file"""
    __file_path = os.path.abspath("file.json")
    __objects = {}

    @property
    def objects(self):
        """Get the dictionary of objects."""
        return self.__objects

    @objects.setter
    def objects(self, value):
        """Set the dictionary of objects."""
        self.__objects = value

    @property
    def file_path(self):
        """Get the file path."""
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        """Set the file path."""
        self.__file_path = value

    def all(self):
        """Get the dictionary of objects."""
        return self.objects

    def new(self, obj):
        """Set in __objects the obj with key <obj class name>.id."""
        key = f"{obj.__class__.__name__}.{obj.id}"
        self.__objects[key] = obj

    def save(self):
        """Serialize __objects to the JSON file (path: __file_path)."""
        json_object = {}
        for key, value in self.__objects.items():
            json_object[key] = value.to_dict()
        with open(self.__file_path, "w") as outfile:
            json.dump(json_object, outfile)

    def reload(self):
        """Deserialize the JSON file to objects only if the JSON file exists"""
        try:
            with open(self.__file_path, "r") as file:
                jsonData = json.load(file)
                for o in jsonData.values():
                    cls_name = o["__class__"]
                    del o["__class__"]
                    self.new(eval(cls_name)(**o))
        except FileNotFoundError:
            pass

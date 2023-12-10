#!/usr/bin/python3
"""this module is for BaseModel class"""

import uuid
from datetime import datetime


class BaseModel():
    """class that defines common attributes and methods for other classes."""

    def __init__(self, *args, **kwargs):
        """Initialize instance attributes."""
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    if key == 'created_at' or key == 'updated_at':
                        value = datetime.strptime(value,
                                                  '%Y-%m-%dT%H:%M:%S.%f')
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            from models import storage
            storage.new(self)

    def __str__(self):
        """Return a string representation of the instance."""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"

    def save(self):
        """Update the date and time of modification and save to storage."""
        self.updated_at = datetime.now()
        from models import storage
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of the instance."""
        dict = self.__dict__.copy()
        dict['__class__'] = self.__class__.__name__
        dict['created_at'] = self.created_at.isoformat()
        dict['updated_at'] = self.updated_at.isoformat()
        return dict

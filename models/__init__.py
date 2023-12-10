#!/usr/bin/python3

"""Script to initialize and reload a FileStorage instance."""
from models.engine.file_storage import FileStorage

storage = FileStorage()
storage.reload()

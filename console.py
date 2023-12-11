#!/usr/bin/python3
"""this module is Write a program called console.py
that contains the entry point of the command interpreter"""

import cmd
import sys
import json
import re
import os
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models import storage
from models.user import User
from models.state import State
from models.place import Place
from models.city import City
from models.amenity import Amenity
from models.review import Review
import shlex
from datetime import datetime
import models


class HBNBCommand(cmd.Cmd):
    """class HBNBCommand that inherit from cmd module"""

    prompt = "(hbnb) "
    allowed_classes = ['BaseModel', 'User', 'State', 'City',
                       'Amenity', 'Place', 'Review']

    def json_to_obj(self):
        """ this function to deserializes the JSON file to __objects"""
        jsonData = {}
        with open(os.path.abspath("file.json"), "r") as file:
            jsonData = json.load(file)
        return jsonData

    def error_msg(self, arg):
        """ this function to show error messages"""
        jsonData = self.json_to_obj()
        if arg:
            args = arg.split(' ')
            if len(args) == 1:
                class_name = args[0]
                class_exist = False
                instance_found = False
                for key in jsonData:
                    if class_name == jsonData[key].get("__class__"):
                        class_exist = True
                if not class_exist:
                    print("** class doesn't exist **")
                if class_exist and len(args) == 1:
                    print("** instance id missing **")
            if len(args) == 2:
                class_name = args[0]
                instance_id = args[1]
                class_exist = False
                for key, value in jsonData.items():
                    if (
                        class_name == value.get("__class__") and
                        instance_id == value.get("id")
                            ):
                        class_exist = True
                        filtered_dict = {key: value[key]
                                         for key in value
                                         if key != '__class__'}
                        obj = (
                            f"[{value['__class__']}] "
                            f"({value['id']}) "
                            f"{filtered_dict}"
                            )
                        key = f"{value.get('__class__')}.{value.get('id')}"
                        return key, obj
                    elif (
                        class_name != value.get("__class__") and
                        instance_id == value.get("id")
                            ):
                        print("** class doesn't exist **")
                    elif (
                        class_name == value.get("__class__") and
                        instance_id != value.get("id")
                            ):
                        print("** no instance found **")
        else:
            print("** class name missing **")

    def do_quit(self, arg):
        """Quit command to exit the program \n"""
        sys.exit()

    def do_EOF(self, arg):
        """Exit the interpreter when EOF (Ctrl-D) is encountered \n"""
        print("")
        return True

    def emptyline(self):
        """this funcion to an empty line + ENTER should not execute anything"""
        pass

    def do_create(self, arg):
        """
        Creates a new instance of class, saves it, and prints the id.
        """
        if arg:
            if arg in self.allowed_classes:
                class_obj = globals()[arg]
                instance = class_obj()
                instance.save()
                print(instance.id)
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_show(self, arg):
        """Prints the string representation of instance based on class name"""
        obj = self.error_msg(arg)
        if obj:
            strings = obj[0].split(".")
            match = re.search(r'\{.*\}', obj[1])
            if match:
                extracted_dict_str = match.group(0)
                extracted_dict_str = extracted_dict_str.replace("'", "\"")
                extracted_dict = json.loads(extracted_dict_str)
                for key, value in extracted_dict.items():
                    created_at = "created_at"
                    updated_at = "updated_at"
                    created_date_str = extracted_dict[created_at]
                    updated_date_str = extracted_dict[updated_at]
                    extracted_dict[created_at] = datetime.fromisoformat(str(
                        created_date_str))
                    extracted_dict[updated_at] = datetime.fromisoformat(
                        str(updated_date_str))
            result = f"[{strings[0]}] ({strings[1]}) {extracted_dict}"
            print(result)

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id .
        """
        obj = self.error_msg(arg)
        if obj:
            objects = storage.all()
            del objects[obj[0]]
            storage.save()

    def do_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name"""
        jsonData = self.json_to_obj()
        list = []
        if arg:
            args = arg.split(' ')
            if len(args) == 1:
                class_name = args[0]
                class_exist = False
                for key, value in jsonData.items():
                    if class_name == value.get("__class__"):
                        class_exist = True
                        object = (
                            f"[{value['__class__']}] "
                            f"({value['id']}) "
                            f"{value}"
                            )
                        list.append(object)
                print(list)
                if not class_exist:
                    print("** class doesn't exist **")
        else:
            for key, value in jsonData.items():
                object = (
                            f"[{value['__class__']}] "
                            f"({value['id']}) "
                            f"{jsonData.items()}"
                            )
            list.append(object)
            print(list)

    def analyze_parameter_value(self, value):
        """Checks a parameter value for an update
        """
        if value.isdigit():
            return int(value)
        elif value.replace('.', '', 1).isdigit():
            return float(value)

        return value

    def do_update(self, line):
        """Updates an instance based on the class name and id
            by adding or updating attribute.
        """
        args = shlex.split(line)
        args_size = len(args)
        if args_size == 0:
            print('** class name missing **')
        elif args[0] not in self.allowed_classes:
            print("** class doesn't exist **")
        elif args_size == 1:
            print('** instance id missing **')
        else:
            key = args[0] + '.' + args[1]
            inst_data = models.storage.all().get(key)
            if inst_data is None:
                print('** no instance found **')
            elif args_size == 2:
                print('** attribute name missing **')
            elif args_size == 3:
                print('** value missing **')
            else:
                attribute_name = args[2]
                if attribute_name in ['id', 'created_at', 'updated_at']:
                    pass
                else:
                    args[3] = self.analyze_parameter_value(args[3])
                    setattr(inst_data, args[2], args[3])
                    models.storage.save()

    def class_all(self, arg):
        """Prints all string representation of all
        instances based or not on the class name"""
        jsonData = self.json_to_obj()
        obj = []
        if arg:
            args = arg.split(' ')
            if len(args) == 1:
                class_name = args[0]
                class_exist = False
                for key, value in jsonData.items():
                    if class_name == jsonData[key].get("__class__"):
                        class_exist = True
                        item = f"[{value['__class__']}]({value['id']}) {value}"
                        obj.append(item)
                print(obj)
                if not class_exist:
                    print("** class doesn't exist **")

    def class_count(self, class_name):
        """function to to retrieve the number of instances of a class"""
        jsonData = self.json_to_obj()
        count = 0
        for key, value in jsonData.items():
            if class_name == value.get("__class__"):
                count += 1
        return count

    def default(self, line):
        """called on an input line when the command prefix is not recognized"""
        args = []
        args = line.split('.')
        jsonData = self.json_to_obj()
        class_name = args[0]
        class_exist = False
        for key, value in jsonData.items():
            if class_name == jsonData[key].get("__class__"):
                class_exist = True
        if class_exist:
            if len(args) == 2:
                if args[1] == "count()":
                    count = self.class_count(class_name)
                    print(count)
                elif args[1] == "all()":
                    self.class_all(class_name)
                elif re.match(r'show\("([^"]+)"\)', args[1]):
                    self.class_show(args)
                elif re.match(r'destroy\("([^"]+)"\)', args[1]):
                    self.class_destroy(args)
                else:
                    return cmd.Cmd.default(self, line)
            else:
                return cmd.Cmd.default(self, line)
        else:
            return cmd.Cmd.default(self, line)

    def class_show(self, arg):
        """Show the string representation of an instance based
        on the class id"""
        jsonData = self.json_to_obj()
        id = re.compile(r'show\("([^"]+)"\)')
        match = id.match(arg[1])
        id_found = False
        if match:
            class_name = arg[0]
            id_value = match.group(1)
            for key, value in jsonData.items():
                if (
                    class_name == value.get("__class__") and
                    id_value == value.get("id")
                        ):
                    id_found = True
                    obj = (
                        f"[{value['__class__']}] "
                        f"({value['id']}) "
                        f"{value}"
                        )
                    print(obj)
        if not id_found:
            pass

    def class_destroy(self, arg):
        """Show the string representation of an instance based
        on the class id"""
        jsonData = self.json_to_obj()
        id = re.compile(r'destroy\("([^"]+)"\)')
        match = id.match(arg[1])
        id_found = False
        if match:
            class_name = arg[0]
            id_value = match.group(1)
            for key, value in jsonData.items():
                if (
                    class_name == value.get("__class__") and
                    id_value == value.get("id")
                        ):
                    id_found = True
                    obj = (
                        f"[{value['__class__']}] "
                        f"({value['id']}) "
                        f"{value}"
                        )
                    objects = storage.all()
                    del objects[key]
                    storage.save()
        if not id_found:
            print("ok")


if __name__ == '__main__':
    HBNBCommand().cmdloop()

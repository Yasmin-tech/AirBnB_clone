#!/usr/bin/python3
"""This module contain the class that is use for the console
    i.e, the entry point for the command intepreter
    """
import cmd
from models.base_model import BaseModel
from models import storage
import json
import os
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review

classes = ["BaseModel", "User", "Place", "State", "City", "Amenity", "Review"]
class HBNBCommand(cmd.Cmd):
    """This class is a command intepreter"""
    prompt = "(hbnb) "
    def do_quit(self, line):
        """quit command to exit the program"""
        return True

    def do_EOF(self, line):
        """quit command to exit the program"""
        print()
        return True

    def emptyline(self):
        """do nothing when the line is empty"""
        pass
    def do_create(self, line):
        """create an instance of BaseModel"""
        if not line:
            print("** class name missing **")
        else:
            if line in classes:
                b1 = eval(line + "()")
                b1.save()
                print(b1.id)
            else:
                print("** class doesn't exist **")

    def do_show(self, line):
        """print the string implementation of an instance based
        on the class name and the id
        """
        all_objects = {}
        if not line:
            print("** class name missing **")
        else:
             command_list = line.split()
             class_name = command_list[0]
             if class_name in classes:
                 if len(command_list) == 1:
                     print("** instance id missing **")
                 else:
                     try:
                         with open("file.json", "r") as f:
                             if os.path.getsize("file.json") != 0:
                                all_objects = json.load(f)
                     except(IOError):
                         pass
                     id_value = command_list[1]
                     obj = all_objects.get(class_name + "." + id_value, -1)
                     if obj == -1:
                         print("** no instance found **")
                     else:
                         instance = eval(class_name + "(**obj)")
                         print(instance)
             else:
                 print("** class doesn't exist **")

    def do_destroy(self, line):
        """Deletes an instance based on the class name and id"""

        all_objects = {}
        if not line:
            print("** class name missing **")
        else:
            command_list = line.split()
            class_name = command_list[0]
            if class_name in classes:
                if len(command_list) == 1:
                     print("** instance id missing **")
                else:
                    try:
                         with open("file.json", "r") as f:
                             if os.path.getsize("file.json") != 0:
                                all_objects = json.load(f)
                    except(IOError):
                         pass
                    id_value = command_list[1]
                    obj = all_objects.get(class_name + "." + id_value, -1)
                    if obj == -1:
                        print("** no instance found **")
                    else:
                        del(all_objects[class_name + "." +id_value])
                        with open("file.json", "w") as f:
                            json.dump(all_objects, f)
            else:
                print("** class doesn't exist **")

    def do_all(self, line):
        """Prints all string representation of all instances\
        based or not on the class name. Ex: $ all BaseModel or $ all"""
        all_objects = {}
        list_objects = []

        if line and line not in classes:
            print("** class doesn't exist **")
        else:
            try:
                with open("file.json", "r") as f:
                        if os.path.getsize("file.json") != 0:
                                all_objects = json.load(f)

                for obj in all_objects.keys():
                    class_name = all_objects[obj]["__class__"]
                    created_instance = eval(class_name + "(**all_objects[obj])")
                    if line:
                        if line == class_name:
                                list_objects.append(str(created_instance))
                    else:
                        list_objects.append(str(created_instance))
            except(IOError):
                pass
            finally:
                print(list_objects)
        
    def do_update(self, line):
        """Updates an instance based on the class name and id
                by adding or updating attribute
                Usage:
                update <class name> <id> <attribute> "<attribute value>"
        """
        all_objects = {}
        if not line:
            print("** class name missing **")
        else:
             command_list = line.split()
             class_name = command_list[0]
             if class_name in classes:
                 if len(command_list) == 1:
                     print("** instance id missing **")
                 else:
                     try:
                         with open("file.json", "r") as f:
                            if os.path.getsize("file.json") != 0:
                                all_objects = json.load(f)
                     except(IOError):
                         pass
                     id_value = command_list[1]
                     obj = all_objects.get(class_name + "." + id_value, -1)
                     if obj == -1:
                         print("** no instance found **")
                     else:
                        if len(command_list) == 2:
                            print("** attribute name missing **")
                        elif len(command_list) == 3:
                            print("** value missing **")
                        else:
                            instance = eval(class_name + "(**obj)")
                            command_list[2] = command_list[2].strip("\"\'")
                            setattr(instance, command_list[2], eval(command_list[3]))
                            instance.save()
                    
             else:
                 print("** class doesn't exist **")

        

                     




if __name__ == '__main__':
    HBNBCommand().cmdloop()

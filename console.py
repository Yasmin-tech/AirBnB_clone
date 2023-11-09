#!/usr/bin/python3
"""This module contain the class that is use for the console
    i.e, the entry point for the command intepreter
    """
import cmd
from models.base_model import BaseModel
from models import storage

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

    def emptyline(self, line):
        """do nothing when the line is empty"""
        pass
    def do_create(self, line):
        """create an instance of BaseModel"""
        if not line:
            print("** class name missing **")
        else:
            if line == "BaseModel":
                b1 = BaseModel()
                b1.save()
                print(b1.id)
            else:
                print("** class doesn't exist **")

    def do_show(self, line):
        """print the string implementation of an instance based
        on the class name and the id
        """
        if not line:
            print("** class name missing **")
        else:
            class_name, id_value = line.splits()
            if class_name != "BaseModel":
                print("** class doesn't exist **")
            elif not id_value:
                print("** instance id missing **")
            else:
                with open("file.json", "r", encoding="utf-8") as f:
                    all_obj = json.load(f)
            if all_obj[


if __name__ == '__main__':
    HBNBCommand().cmdloop()

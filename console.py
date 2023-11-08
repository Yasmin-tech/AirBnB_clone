#!/usr/bin/python3
"""This module contain the class that is use for the console
    i.e, the entry point for the command intepreter
    """
import cmd


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

if __name__ == '__main__':
    HBNBCommand().cmdloop()

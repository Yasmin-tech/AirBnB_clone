#!/usr/bin/python3
""" Unittest for the console """


import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
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

obj = HBNBCommand()


class Test_Console(unittest.TestCase):
    """ The class that contains test cases for the console"""


    @staticmethod
    def get_stdout(command):
        """ get the content printed to stdout"""

        with patch('sys.stdout', new=StringIO()) as f:
            HBNBCommand().onecmd(command)
            file = f.getvalue()
        return file

    def test_help(self):
        """test the help command to print everythin available"""
        file = Test_Console.get_stdout("help")
        expected_output = ("\nDocumented commands (type help <topic>):\n" +
                            "========================================\n" +
                            "EOF  all  create  destroy  help  quit  show  update\n\n")
        self.assertEqual(file, expected_output)

    def test_help_with_class(self):
        """test the help command with all methods available"""
        file = Test_Console.get_stdout("help EOF")
        expected_output = "quit command to exit the program\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("help all")
        expected_output = obj.do_all.__doc__ + "\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("help create")
        expected_output = "create an instance of BaseModel\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("help destroy")
        expected_output = "Deletes an instance based on the class name and id\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("help help")
        expected_output = ("List available commands with \"help\" or detailed " +
                            "help with \"help cmd\".\n")
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("help quit")
        expected_output = "quit command to exit the program\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("help show")
        expected_output = obj.do_show.__doc__ + "\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("help update")
        expected_output = obj.do_update.__doc__ + "\n"
        self.assertEqual(file, expected_output)

    def test_EOF(self):
        """test the EOF command"""
        file = Test_Console.get_stdout("EOF")
        expected_output = "\n"
        self.assertEqual(file, expected_output)

    def test_emptyline(self):
        """test when the input is an emptyline"""
        file = Test_Console.get_stdout("")
        expected_output = ""
        self.assertEqual(file, expected_output)

    def test_prompt(self):
        """test the prompt printed in the console"""
        file = obj.prompt
        expected_output = "(hbnb) "
        self.assertEqual(file, expected_output)

    def test_create(self):
        """test the create method"""
        file = Test_Console.get_stdout("create BaseModel")
        self.assertTrue(file)

        file = Test_Console.get_stdout("create")
        expected_output = "** class name missing **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("create hotel")
        expected_output = "** class doesn't exist **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("create User")
        self.assertTrue(file)
        file = Test_Console.get_stdout("create Amenity")
        self.assertTrue(file)
        file = Test_Console.get_stdout("create Place")
        self.assertTrue(file)
        file = Test_Console.get_stdout("create State")
        self.assertTrue(file)
        file = Test_Console.get_stdout("create Review")
        self.assertTrue(file)

    def test_show(self):
        """test the show command"""
        file = Test_Console.get_stdout("show")
        expected_output = "** class name missing **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("show Hotel")
        expected_output = "** class doesn't exist **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("show BaseModel")
        expected_output = "** instance id missing **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("show BaseModel 245")
        expected_output = "** no instance found **\n"
        self.assertEqual(file, expected_output)

        id_value = Test_Console.get_stdout("create User")
        file = Test_Console.get_stdout("show User " + id_value)
        self.assertTrue("[User]" in file)

        id_value = Test_Console.get_stdout("create BaseModel")
        file = Test_Console.get_stdout("show BaseModel " + id_value)
        self.assertTrue("[BaseModel]" in file)

        id_value = Test_Console.get_stdout("create Place")
        file = Test_Console.get_stdout("show Place " + id_value)
        self.assertTrue("[Place]" in file)

        id_value = Test_Console.get_stdout("create Amenity")
        file = Test_Console.get_stdout("show Amenity " + id_value)
        self.assertTrue("[Amenity]" in file)

        id_value = Test_Console.get_stdout("create State")
        file = Test_Console.get_stdout("show State " + id_value)
        self.assertTrue("[State]" in file)

        id_value = Test_Console.get_stdout("create Review")
        file = Test_Console.get_stdout("show Review " + id_value)
        self.assertTrue("[Review]" in file)

    def test_destroy(self):
        """test the destroy command"""
        file = Test_Console.get_stdout("destroy")
        expected_output = "** class name missing **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("destroy Hotel")
        expected_output = "** class doesn't exist **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("destroy BaseModel")
        expected_output = "** instance id missing **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("destroy BaseModel 245")
        expected_output = "** no instance found **\n"
        self.assertEqual(file, expected_output)

        id_value = Test_Console.get_stdout("create BaseModel")
        file = Test_Console.get_stdout("destroy BaseModel " + id_value)
        show_output = Test_Console.get_stdout("show BaseModel " + id_value)
        expected_output = "** no instance found **\n"
        self.assertEqual(show_output, expected_output)

        id_value = Test_Console.get_stdout("create User")
        file = Test_Console.get_stdout("destroy User " + id_value)
        show_output = Test_Console.get_stdout("show User " + id_value)
        expected_output = "** no instance found **\n"
        self.assertEqual(show_output, expected_output)

        id_value = Test_Console.get_stdout("create Place")
        file = Test_Console.get_stdout("destroy Place " + id_value)
        show_output = Test_Console.get_stdout("show Place " + id_value)
        expected_output = "** no instance found **\n"
        self.assertEqual(show_output, expected_output)

        id_value = Test_Console.get_stdout("create Review")
        file = Test_Console.get_stdout("destroy Review " + id_value)
        show_output = Test_Console.get_stdout("show Review " + id_value)
        expected_output = "** no instance found **\n"
        self.assertEqual(show_output, expected_output)

        id_value = Test_Console.get_stdout("create State")
        file = Test_Console.get_stdout("destroy State " + id_value)
        show_output = Test_Console.get_stdout("show State " + id_value)
        expected_output = "** no instance found **\n"
        self.assertEqual(show_output, expected_output)

        id_value = Test_Console.get_stdout("create Review")
        file = Test_Console.get_stdout("destroy Review " + id_value)
        show_output = Test_Console.get_stdout("show Review " + id_value)
        expected_output = "** no instance found **\n"
        self.assertEqual(show_output, expected_output)

    def test_update(self):
        """test the update command of the console"""
        id_value = Test_Console.get_stdout("create State")

        file = Test_Console.get_stdout("update")
        expected_output = "** class name missing **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("update Hotel")
        expected_output = "** class doesn't exist **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("update State")
        expected_output = "** instance id missing **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("update State 38")
        expected_output = "** no instance found **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("update State " + id_value)
        expected_output = "** attribute name missing **\n"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("update State " + id_value + "Ho")
        expected_output = "** value missing **\n"
        self.assertEqual(file, expected_output)




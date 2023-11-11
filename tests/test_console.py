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
        """ test the help method of the console """

        file  = Test_Console.get_stdout("all")
        expected_output = ("[\"[User] (af471e7f-2d40-41ed-9cb4-4ea28f0b26f2) " +
        "{'id': 'af471e7f-2d40-41ed-9cb4-4ea28f0b26f2', " +
        "'created_at': datetime.datetime(2023, 11, 11, 21, 42, 32, 134002), " +
        "'updated_at': datetime.datetime(2023, 11, 11, 21, 42, 32, 134196)}\"]\n")
        self.assertEqual(file, expected_output)

            


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
from models.engine.file_storage import FileStorage

obj = HBNBCommand()


class Test_Console(unittest.TestCase):
    """The class that contains test cases for the console"""

    @staticmethod
    def get_stdout(command):
        """get the content printed to stdout"""

        with patch("sys.stdout", new=StringIO()) as f:
            HBNBCommand().onecmd(command)
            file = f.getvalue()
        return file

    def test_help(self):
        """test the help command to print everythin available"""
        file = Test_Console.get_stdout("help")
        expected_output = (
            "\nDocumented commands (type help <topic>):\n"
            + "========================================\n"
            + "EOF  all  create  destroy  help  quit  show  update\n\n"
        )
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

        file = Test_Console.get_stdout("help destroy").strip()
        expected_output = "Deletes an instance based on the class name and id"
        self.assertEqual(file, expected_output)

        file = Test_Console.get_stdout("help help")
        expected_output = (
            'List available commands with "help" or detailed '
            + 'help with "help cmd".\n'
        )
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


class Test_Console_show_with_dot_notation(unittest.TestCase):
    """A class that contains unittests for testing show from
    the HBNB command interpreter"""

    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_show_dot_notations_missing_id(self):
        """Test show command of the console when is id is missing"""
        output = Test_Console.get_stdout("BaseModel.show('')").strip()
        expected_output = "** instance id missing **"
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('BaseModel.show("")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('BaseModel.show(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('User.show("")').strip()
        output = Test_Console.get_stdout('User.show(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Place.show("")').strip()
        output = Test_Console.get_stdout('Place.show(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('City.show("")').strip()
        output = Test_Console.get_stdout('City.show(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('State.show("")').strip()
        output = Test_Console.get_stdout('State.show(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Review.show("")').strip()
        output = Test_Console.get_stdout('Review.show(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Amenity.show("")').strip()
        output = Test_Console.get_stdout('Place.show(" ")').strip()
        self.assertEqual(output, expected_output)

    def test_show_dot_notations_instance_not_found(self):
        """Test show command of the console when is instance not found"""
        output = Test_Console.get_stdout("BaseModel.show('Bar')").strip()
        expected_output = "** no instance found **"
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('BaseModel.show("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('BaseModel.show("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('BaseModel.show("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('BaseModel.show("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('User.show("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('User.show("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('User.show("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('User.show("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('State.show("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('State.show("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('State.show("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('State.show("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Place.show("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Place.show("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Place.show("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Place.show("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('City.show("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('City.show("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('City.show("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('City.show("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Amenity.show("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Amenity.show("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Amenity.show("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Amenity.show("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Review.show("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Review.show("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Review.show("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Review.show("{}")').strip()
        self.assertEqual(output, expected_output)

    def test_show_dot_notations_class_doesnt_exist(self):
        """Test show command of the console when is id is missing"""
        output = Test_Console.get_stdout("MyModel.show('')").strip()
        expected_output = "** class doesn't exist **"
        self.assertEqual(output, expected_output)

    def test_show_dot_notations_valid_id(self):
        """Test show command of the console with valid id"""

        b1 = BaseModel()
        b1.save()
        b1_id = '"' + b1.id + '"'
        output = Test_Console.get_stdout("BaseModel.show({})".format(b1_id))
        expected_output = "[BaseModel] ({}) {}".format(b1.id, b1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        u1 = User()
        u1.first_name = "Yasmin"
        u1.last_name = "Abdu"
        u1.email = "user@user.com"
        u1.save()
        u1_id = '"' + u1.id + '"'
        output = Test_Console.get_stdout("User.show({})".format(u1_id))
        expected_output = "[User] ({}) {}".format(u1.id, u1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        p1 = Place()
        p1.city_id = "123"
        p1.save()
        p1_id = '"' + p1.id + '"'
        output = Test_Console.get_stdout("Place.show({})".format(p1_id))
        expected_output = "[Place] ({}) {}".format(p1.id, p1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        c1 = City()
        c1.name = "city"
        c1.save()
        c1_id = '"' + c1.id + '"'
        output = Test_Console.get_stdout("City.show({})".format(c1_id))
        expected_output = "[City] ({}) {}".format(c1.id, c1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        s1 = State()
        s1.name = "state"
        s1.save()
        s1_id = '"' + s1.id + '"'
        output = Test_Console.get_stdout("State.show({})".format(s1_id))
        expected_output = "[State] ({}) {}".format(s1.id, s1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        a1 = Amenity()
        a1.name = "empty"
        a1.save()
        a1_id = '"' + a1.id + '"'
        output = Test_Console.get_stdout("Amenity.show({})".format(a1_id))
        expected_output = "[Amenity] ({}) {}".format(a1.id, a1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        r1 = Review()
        r1.place_id = "111"
        r1.save()
        r1_id = '"' + r1.id + '"'
        output = Test_Console.get_stdout("Review.show({})".format(r1_id))
        expected_output = "[Review] ({}) {}".format(r1.id, r1.__dict__)
        self.assertEqual(output.strip(), expected_output)

    def test_show_dot_notations_invalid_syntax(self):
        """Test show command of the console with invalid syntax"""
        output = Test_Console.get_stdout("BaseModel.show()").strip()
        expected_output = "*** Unknown syntax: {}.show()".format("BaseModel")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("User.show()").strip()
        expected_output = "*** Unknown syntax: {}.show()".format("User")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Place.show()").strip()
        expected_output = "*** Unknown syntax: {}.show()".format("Place")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Amenity.show()").strip()
        expected_output = "*** Unknown syntax: {}.show()".format("Amenity")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("City.show()").strip()
        expected_output = "*** Unknown syntax: {}.show()".format("City")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("State.show()").strip()
        expected_output = "*** Unknown syntax: {}.show()".format("State")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Review.show()").strip()
        expected_output = "*** Unknown syntax: {}.show()".format("Review")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("BaseModel.show").strip()
        expected_output = "*** Unknown syntax: {}.show".format("BaseModel")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("User.show").strip()
        expected_output = "*** Unknown syntax: {}.show".format("User")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Place.show").strip()
        expected_output = "*** Unknown syntax: {}.show".format("Place")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Amenity.show").strip()
        expected_output = "*** Unknown syntax: {}.show".format("Amenity")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("City.show").strip()
        expected_output = "*** Unknown syntax: {}.show".format("City")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("State.show").strip()
        expected_output = "*** Unknown syntax: {}.show".format("State")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Review.show").strip()
        expected_output = "*** Unknown syntax: {}.show".format("Review")
        self.assertEqual(output, expected_output)

        b1 = BaseModel()
        b1.id = "1235"
        b1.save()
        output = Test_Console.get_stdout("BaseModel.show({})"
                                         ).format(b1.id).strip()
        expected_output = "*** Unknown syntax: {}.show(1235)".format(
            "BaseModel")
        self.assertEqual(output, expected_output)

        u1 = User()
        u1.id = "1235"
        u1.save()
        output = Test_Console.get_stdout("User.show({})").format(u1.id).strip()
        expected_output = "*** Unknown syntax: {}.show(1235)".format("User")
        self.assertEqual(output, expected_output)

        p1 = Place()
        p1.id = "1235"
        p1.save()
        output = Test_Console.get_stdout("Place.show({})").format(
            p1.id).strip()
        expected_output = "*** Unknown syntax: {}.show(1235)".format("Place")
        self.assertEqual(output, expected_output)

        a1 = Amenity()
        a1.id = "1235"
        a1.save()
        output = Test_Console.get_stdout(
            "Amenity.show({})").format(a1.id).strip()
        expected_output = "*** Unknown syntax: {}.show(1235)".format("Amenity")
        self.assertEqual(output, expected_output)

        c1 = City()
        c1.id = "1235"
        c1.save()
        output = Test_Console.get_stdout("City.show({})").format(c1.id).strip()
        expected_output = "*** Unknown syntax: {}.show(1235)".format("City")
        self.assertEqual(output, expected_output)

        s1 = State()
        s1.id = "1235"
        s1.save()
        output = Test_Console.get_stdout(
            "State.show({})").format(s1.id).strip()
        expected_output = "*** Unknown syntax: {}.show(1235)".format("State")
        self.assertEqual(output, expected_output)

        r1 = Review()
        r1.id = "1235"
        r1.save()
        output = Test_Console.get_stdout(
            "Review.show({})").format(r1.id).strip()
        expected_output = "*** Unknown syntax: {}.show(1235)".format("Review")
        self.assertEqual(output, expected_output)


class Test_Console_destroy_with_dot_notation(unittest.TestCase):
    """A class that contains unittests for testing destroy from
    the HBNB command interpreter"""

    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_destroy_dot_notations_missing_id(self):
        """Test destroy command of the console when is id is missing"""
        output = Test_Console.get_stdout("BaseModel.destroy('')").strip()
        expected_output = "** instance id missing **"
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('BaseModel.destroy("")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('BaseModel.destroy(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('User.destroy("")').strip()
        output = Test_Console.get_stdout('User.destroy(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Place.destroy("")').strip()
        output = Test_Console.get_stdout('Place.destroy(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('City.destroy("")').strip()
        output = Test_Console.get_stdout('City.destroy(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('State.destroy("")').strip()
        output = Test_Console.get_stdout('State.destroy(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Review.destroy("")').strip()
        output = Test_Console.get_stdout('Review.destroy(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Amenity.destroy("")').strip()
        output = Test_Console.get_stdout('Place.destroy(" ")').strip()
        self.assertEqual(output, expected_output)

    def test_destroy_dot_notations_instance_not_found(self):
        """Test destroy command of the console when instance not found"""
        output = Test_Console.get_stdout("BaseModel.destroy('Bar')").strip()
        expected_output = "** no instance found **"
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('BaseModel.destroy("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('BaseModel.destroy("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('BaseModel.destroy("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('BaseModel.destroy("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('User.destroy("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('User.destroy("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('User.destroy("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('User.destroy("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('State.destroy("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('State.destroy("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('State.destroy("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('State.destroy("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Place.destroy("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Place.destroy("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Place.destroy("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Place.destroy("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('City.destroy("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('City.destroy("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('City.destroy("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('City.destroy("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Amenity.destroy("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Amenity.destroy("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Amenity.destroy("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Amenity.destroy("{}")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Review.destroy("Bar")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Review.destroy("123")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Review.destroy("[]")').strip()
        self.assertEqual(output, expected_output)
        output = Test_Console.get_stdout('Review.destroy("{}")').strip()
        self.assertEqual(output, expected_output)

    def test_destroy_dot_notations_class_doesnt_exist(self):
        """Test destroy command of the console when class doesn't exist"""
        output = Test_Console.get_stdout("MyModel.destroy('')").strip()
        expected_output = "** class doesn't exist **"
        self.assertEqual(output, expected_output)

    def test_destroy_dot_notations_valid_id(self):
        """Test show command of the console with valid id"""

        b1 = BaseModel()
        b1.save()
        b1_id = '"' + b1.id + '"'
        output = Test_Console.get_stdout("BaseModel.show({})".format(b1_id))
        expected_output = "[BaseModel] ({}) {}".format(b1.id, b1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        output = Test_Console.get_stdout("BaseModel.destroy({})".format(b1_id))
        self.assertEqual(output.strip(), "")
        output = Test_Console.get_stdout("BaseModel.show({})".format(b1_id))
        expected_output = "** no instance found **"
        self.assertEqual(output.strip(), expected_output)

        output = Test_Console.get_stdout("BaseModel.destroy({})".format(b1_id))
        expected_output = "** no instance found **"
        self.assertEqual(output.strip(), expected_output)

        u1 = User()
        u1.first_name = "Yasmin"
        u1.last_name = "Abdu"
        u1.email = "user@user.com"
        u1.save()
        u1_id = '"' + u1.id + '"'
        output = Test_Console.get_stdout("User.show({})".format(u1_id))
        expected_output = "[User] ({}) {}".format(u1.id, u1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        output = Test_Console.get_stdout("User.destroy({})".format(u1_id))
        self.assertEqual(output.strip(), "")
        output = Test_Console.get_stdout("User.show({})".format(u1_id))
        expected_output = "** no instance found **"
        self.assertEqual(output.strip(), expected_output)

        p1 = Place()
        p1.city_id = "123"
        p1.save()
        p1_id = '"' + p1.id + '"'
        output = Test_Console.get_stdout("Place.show({})".format(p1_id))
        expected_output = "[Place] ({}) {}".format(p1.id, p1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        output = Test_Console.get_stdout("Place.destroy({})".format(p1_id))
        self.assertEqual(output.strip(), "")
        output = Test_Console.get_stdout("Place.show({})".format(p1_id))
        expected_output = "** no instance found **"
        self.assertEqual(output.strip(), expected_output)

        c1 = City()
        c1.name = "city"
        c1.save()
        c1_id = '"' + c1.id + '"'
        output = Test_Console.get_stdout("City.show({})".format(c1_id))
        expected_output = "[City] ({}) {}".format(c1.id, c1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        output = Test_Console.get_stdout("City.destroy({})".format(c1_id))
        self.assertEqual(output.strip(), "")
        output = Test_Console.get_stdout("City.show({})".format(c1_id))
        expected_output = "** no instance found **"
        self.assertEqual(output.strip(), expected_output)

        s1 = State()
        s1.name = "state"
        s1.save()
        s1_id = '"' + s1.id + '"'
        output = Test_Console.get_stdout("State.show({})".format(s1_id))
        expected_output = "[State] ({}) {}".format(s1.id, s1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        output = Test_Console.get_stdout("State.destroy({})".format(s1_id))
        self.assertEqual(output.strip(), "")
        output = Test_Console.get_stdout("State.show({})".format(s1_id))
        expected_output = "** no instance found **"
        self.assertEqual(output.strip(), expected_output)

        a1 = Amenity()
        a1.name = "empty"
        a1.save()
        a1_id = '"' + a1.id + '"'
        output = Test_Console.get_stdout("Amenity.show({})".format(a1_id))
        expected_output = "[Amenity] ({}) {}".format(a1.id, a1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        output = Test_Console.get_stdout("Amenity.destroy({})".format(a1_id))
        self.assertEqual(output.strip(), "")
        output = Test_Console.get_stdout("Amenity.show({})".format(a1_id))
        expected_output = "** no instance found **"
        self.assertEqual(output.strip(), expected_output)

        r1 = Review()
        r1.place_id = "111"
        r1.save()
        r1_id = '"' + r1.id + '"'
        output = Test_Console.get_stdout("Review.show({})".format(r1_id))
        expected_output = "[Review] ({}) {}".format(r1.id, r1.__dict__)
        self.assertEqual(output.strip(), expected_output)

        output = Test_Console.get_stdout("Review.destroy({})".format(r1_id))
        self.assertEqual(output.strip(), "")
        output = Test_Console.get_stdout("Review.show({})".format(r1_id))
        expected_output = "** no instance found **"
        self.assertEqual(output.strip(), expected_output)

    def test_destroy_dot_notation_invalid_syntax(self):
        """Test destroy command of the console with invalid syntax"""
        output = Test_Console.get_stdout("BaseModel.destroy()").strip()
        expected_output = "*** Unknown syntax: {}.destroy()".format(
            "BaseModel")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("User.destroy()").strip()
        expected_output = "*** Unknown syntax: {}.destroy()".format("User")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Place.destroy()").strip()
        expected_output = "*** Unknown syntax: {}.destroy()".format("Place")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Amenity.destroy()").strip()
        expected_output = "*** Unknown syntax: {}.destroy()".format("Amenity")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("City.destroy()").strip()
        expected_output = "*** Unknown syntax: {}.destroy()".format("City")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("State.destroy()").strip()
        expected_output = "*** Unknown syntax: {}.destroy()".format("State")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Review.destroy()").strip()
        expected_output = "*** Unknown syntax: {}.destroy()".format("Review")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("BaseModel.destroy").strip()
        expected_output = "*** Unknown syntax: {}.destroy".format("BaseModel")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("User.destroy").strip()
        expected_output = "*** Unknown syntax: {}.destroy".format("User")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Place.destroy").strip()
        expected_output = "*** Unknown syntax: {}.destroy".format("Place")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Amenity.destroy").strip()
        expected_output = "*** Unknown syntax: {}.destroy".format("Amenity")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("City.destroy").strip()
        expected_output = "*** Unknown syntax: {}.destroy".format("City")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("State.destroy").strip()
        expected_output = "*** Unknown syntax: {}.destroy".format("State")
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout("Review.destroy").strip()
        expected_output = "*** Unknown syntax: {}.destroy".format("Review")
        self.assertEqual(output, expected_output)

        b1 = BaseModel()
        b1.id = "1235"
        b1.save()
        output = Test_Console.get_stdout("BaseModel.destroy({})").format(
            b1.id).strip()
        expected_output = "*** Unknown syntax: {}.destroy(1235)".format(
            "BaseModel")
        self.assertEqual(output, expected_output)

        u1 = User()
        u1.id = "1235"
        u1.save()
        output = Test_Console.get_stdout("User.destroy({})").format(
            u1.id).strip()
        expected_output = "*** Unknown syntax: {}.destroy(1235)".format(
            "User")
        self.assertEqual(output, expected_output)

        p1 = Place()
        p1.id = "1235"
        p1.save()
        output = Test_Console.get_stdout("Place.destroy({})").format(
            p1.id).strip()
        expected_output = "*** Unknown syntax: {}.destroy(1235)".format(
            "Place")
        self.assertEqual(output, expected_output)

        a1 = Amenity()
        a1.id = "1235"
        a1.save()
        output = Test_Console.get_stdout("Amenity.destroy({})").format(
            a1.id).strip()
        expected_output = "*** Unknown syntax: {}.destroy(1235)".format(
            "Amenity")
        self.assertEqual(output, expected_output)

        c1 = City()
        c1.id = "1235"
        c1.save()
        output = Test_Console.get_stdout("City.destroy({})").format(
            c1.id).strip()
        expected_output = "*** Unknown syntax: {}.destroy(1235)".format(
            "City")
        self.assertEqual(output, expected_output)

        s1 = State()
        s1.id = "1235"
        s1.save()
        output = Test_Console.get_stdout("State.destroy({})").format(
            s1.id).strip()
        expected_output = "*** Unknown syntax: {}.destroy(1235)".format(
            "State")
        self.assertEqual(output, expected_output)

        r1 = Review()
        r1.id = "1235"
        r1.save()
        output = Test_Console.get_stdout("Review.destroy({})").format(
            r1.id).strip()
        expected_output = "*** Unknown syntax: {}.destroy(1235)".format(
            "Review")
        self.assertEqual(output, expected_output)


class Test_Console_update_with_dot_notation(unittest.TestCase):
    """A class that contains unittests for testing update from
    the HBNB command interpreter"""

    def setUp(self):
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage.__objects = {}

    def tearDown(self):
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass

    def test_update_dot_notations_missing_id(self):
        """Test update command of the console when id is missing"""
        output = Test_Console.get_stdout("BaseModel.update('')").strip()
        expected_output = "** instance id missing **"
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('BaseModel.update("")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('BaseModel.update(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('User.update("")').strip()
        output = Test_Console.get_stdout('User.update(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Place.update("")').strip()
        output = Test_Console.get_stdout('Place.update(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('City.update("")').strip()
        output = Test_Console.get_stdout('City.update(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('State.update("")').strip()
        output = Test_Console.get_stdout('State.update(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Review.update("")').strip()
        output = Test_Console.get_stdout('Review.update(" ")').strip()
        self.assertEqual(output, expected_output)

        output = Test_Console.get_stdout('Amenity.update("")').strip()
        output = Test_Console.get_stdout('Place.update(" ")').strip()
        self.assertEqual(output, expected_output)

    def test_update_dot_notation_attribute_name_missing(self):
        """Test update command of the console when attribute
           name is missing"""

        b1 = BaseModel()
        b1.id = "555"
        b1.save()
        output = Test_Console.get_stdout('BaseModel.update("555")').strip()
        expected_output = "** attribute name missing **"
        self.assertEqual(output, expected_output)

        u1 = User()
        u1.id = "555"
        u1.save()
        output = Test_Console.get_stdout('User.update("555")').strip()
        self.assertEqual(output, expected_output)

        p1 = Place()
        p1.id = "555"
        p1.save()
        output = Test_Console.get_stdout('Place.update("555")').strip()
        self.assertEqual(output, expected_output)

        c1 = City()
        c1.id = "555"
        c1.save()
        output = Test_Console.get_stdout('City.update("555")').strip()
        self.assertEqual(output, expected_output)

        s1 = State()
        s1.id = "555"
        s1.save()
        output = Test_Console.get_stdout('State.update("555")').strip()
        self.assertEqual(output, expected_output)

        r1 = Review()
        r1.id = "555"
        r1.save()
        output = Test_Console.get_stdout('Review.update("555")').strip()
        self.assertEqual(output, expected_output)

        a1 = Amenity()
        a1.id = "555"
        a1.save()
        output = Test_Console.get_stdout('Amenity.update("555")').strip()
        self.assertEqual(output, expected_output)

    def test_update_dot_notation_attribute_value_missing(self):
        """Test update command of the console when attribute value
           is missing"""

        b1 = BaseModel()
        b1.id = "555"
        b1.save()
        output = Test_Console.get_stdout(
            'BaseModel.update("555", "name")').strip()
        expected_output = "** value missing **"
        self.assertEqual(output, expected_output)

        u1 = User()
        u1.id = "555"
        u1.save()
        output = Test_Console.get_stdout('User.update("555", "name")').strip()
        self.assertEqual(output, expected_output)

        p1 = Place()
        p1.id = "555"
        p1.save()
        output = Test_Console.get_stdout('Place.update("555", "name")').strip()
        self.assertEqual(output, expected_output)

        c1 = City()
        c1.id = "555"
        c1.save()
        output = Test_Console.get_stdout('City.update("555", "name")').strip()
        self.assertEqual(output, expected_output)

        s1 = State()
        s1.id = "555"
        s1.save()
        output = Test_Console.get_stdout('State.update("555", "name")').strip()
        self.assertEqual(output, expected_output)

        r1 = Review()
        r1.id = "555"
        r1.save()
        output = Test_Console.get_stdout(
            'Review.update("555", "name")').strip()
        self.assertEqual(output, expected_output)

        a1 = Amenity()
        a1.id = "555"
        a1.save()
        output = Test_Console.get_stdout(
            'Amenity.update("555", "name")').strip()
        self.assertEqual(output, expected_output)

    def test_update_dot_notation_instance_not_found(self):
        """Test destroy command of the console when instance is not found"""

        b1 = BaseModel()
        b1.id = "555"
        b1.save()
        output = Test_Console.get_stdout(
            'BaseModel.update("554", "name", "new_name")'
        ).strip()
        expected_output = "** no instance found **"
        self.assertEqual(output, expected_output)

        u1 = User()
        u1.id = "555"
        u1.save()
        output = Test_Console.get_stdout(
            'User.update("554", "name", "new_name")'
        ).strip()
        self.assertEqual(output, expected_output)

        p1 = Place()
        p1.id = "555"
        p1.save()
        output = Test_Console.get_stdout(
            'Place.update("554", "name", "new_name")'
        ).strip()
        self.assertEqual(output, expected_output)

        c1 = City()
        c1.id = "555"
        c1.save()
        output = Test_Console.get_stdout(
            'City.update("554", "name", "new_name")'
        ).strip()
        self.assertEqual(output, expected_output)

        s1 = State()
        s1.id = "555"
        s1.save()
        output = Test_Console.get_stdout(
            'State.update("554", "name", "new_name")'
        ).strip()
        self.assertEqual(output, expected_output)

        r1 = Review()
        r1.id = "555"
        r1.save()
        output = Test_Console.get_stdout(
            'Review.update("554", "name", "new_name")'
        ).strip()
        self.assertEqual(output, expected_output)

        a1 = Amenity()
        a1.id = "555"
        a1.save()
        output = Test_Console.get_stdout(
            'Amenity.update("554", "name", "new_name")'
        ).strip()
        self.assertEqual(output, expected_output)

    # def test_update_dot_notation_valid_syntax(self):
    #     """Test update command does update the instace attribute"""

    #     b1 = BaseModel()
    #     b1.id = "555"
    #     b1.save()
    #     output = Test_Console.get_stdout(
    #         'BaseModel.update("555", "name", "new_name")'
    #     ).strip()
    #     self.assertEqual(output, "")
    #     output = Test_Console.get_stdout('BaseModel.show("555")').strip()
    #     expected_output = "[BaseModel] (555) {}".format(b1.__dict__)
    #     self.assertEqual(output, expected_output)

    #     u1 = User()
    #     u1.id = "555"
    #     u1.save()
    #     output = Test_Console.get_stdout(
    #         'User.update("554", "name", "new_name")'
    #     ).strip()
    #     self.assertEqual(output, expected_output)

    #     p1 = Place()
    #     p1.id = "555"
    #     p1.save()
    #     output = Test_Console.get_stdout(
    #         'Place.update("554", "name", "new_name")'
    #     ).strip()
    #     self.assertEqual(output, expected_output)

    #     c1 = City()
    #     c1.id = "555"
    #     c1.save()
    #     output = Test_Console.get_stdout(
    #         'City.update("554", "name", "new_name")'
    #     ).strip()
    #     self.assertEqual(output, expected_output)

    #     s1 = State()
    #     s1.id = "555"
    #     s1.save()
    #     output = Test_Console.get_stdout(
    #         'State.update("554", "name", "new_name")'
    #     ).strip()
    #     self.assertEqual(output, expected_output)

    #     r1 = Review()
    #     r1.id = "555"
    #     r1.save()
    #     output = Test_Console.get_stdout(
    #         'Review.update("554", "name", "new_name")'
    #     ).strip()
    #     self.assertEqual(output, expected_output)

    #     a1 = Amenity()
    #     a1.id = "555"
    #     a1.save()
    #     output = Test_Console.get_stdout(
    #         'Amenity.update("554", "name", "new_name")'
    #     ).strip()
    #     self.assertEqual(output, expected_output)

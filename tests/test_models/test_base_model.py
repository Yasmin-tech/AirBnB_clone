#!/usr/bin/python3
"""This module contains the unittest test cases for the class
    named <BaseModel>
    """
from models.base_model import BaseModel
import unittest
import datetime


class Test_Base_Model(unittest.TestCase):
    """This class contains several methods to test
        the Base_Model class
        """
    def test_create_instance(self):
        """confirm the instatiation of an instance"""
        b1 = BaseModel()
        self.assertEqual(type(b1), BaseModel)
        with self.assertRaises(TypeError):
            b2 = BaseModel(2)

    def test_unique_id(self):
        """test for unique id among instances"""
        b1 = BaseModel()
        b2 = BaseModel()
        self.assertNotEqual(b1.id, b2.id)

    def test_string_id(self):
        """test if the id is a string"""
        b1 = BaseModel()
        self.assertEqual(type(b1.id), str)
        b2 = BaseModel()
        self.assertEqual(type(b2.id), str)

    def test_created_at(self):
        """test the created_at attribute"""
        b1 = BaseModel()
        self.assertEqual(type(b1.created_at), datetime.datetime)
        self.assertEqual(b1.created_at, b1.updated_at)
        b2 = BaseModel()
        self.assertLess(b1.created_at, b2.created_at)

    def test_updated_at(self):
        """test the updated_at attribute"""
        b1 = BaseModel()
        self.assertEqual(type(b1.updated_at), datetime.datetime)
        self.assertEqual(b1.created_at, b1.updated_at)
        b2 = BaseModel()
        self.assertLess(b1.updated_at, b2.updated_at)

    def test_str_method(self):
        """test the string implementation of the instance"""
        b1 = BaseModel()
        b1.id = "89"
        b1.name = "Yasmin"
        expected_out = "[BaseModel] (89) {}".format(b1.__dict__)
        self.assertEqual(str(b1), expected_out)

    def test_save(self):
        """test if the updated_at is truly updated"""
        b1 = BaseModel()
        temp_updated_at = b1.updated_at
        b1.save()
        self.assertLess(temp_updated_at, b1.updated_at)
        self.assertNotEqual(b1.updated_at, b1.created_at)
        temp_updated_at = b1.updated_at
        b1.save()
        self.assertLess(temp_updated_at, b1.updated_at)

    def test_to_dict(self):
        """test all the attribute stored in the dictionary"""
        b1 = BaseModel()
        obj_dict = b1.to_dict()
        self.assertEqual(type(obj_dict), dict)
        self.assertEqual(obj_dict["__class__"], "BaseModel")
        self.assertEqual(type(obj_dict["created_at"]), str)
        self.assertEqual(type(obj_dict["updated_at"]), str)
        convert_isoformat = datetime.datetime.fromisoformat(obj_dict["created_at"])
        self.assertEqual(type(convert_isoformat), datetime.datetime)
        convert_isoformat = datetime.datetime.fromisoformat(obj_dict["updated_at"])
        self.assertEqual(type(convert_isoformat), datetime.datetime)
        self.assertEqual(b1.id, obj_dict["id"])

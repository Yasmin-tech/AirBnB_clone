#!/usr/bin/python3
""" This Model will be used for serialization-deserialization
    purposes of BaseModel objects and all of its subclasses
"""
import json
import os


class FileStorage():
        """ a class FileStorage that serializes instances to a JSON file
        and deserializes JSON file to instances

        class 'BaseModel' -> to_dict() <class 'dict'>
          -> JSON dump <class 'str'> -> FILE <class 'str'>
            -> JSON load <class 'dict'> -> <class 'BaseModel'
        
        constructor -> __init__(self)
        -----------------------------

        Private class attributes
        ------------------------
                __file_path: string - path to the JSON file (ex: file.json)
                __objects: dictionary - empty but will store all objects
                by <class name>.id as a key

        Public instance methods
        -----------------------
                all(self): returns the dictionary __objects
                new(self, obj): sets in __objects the obj
                        with key <obj class name>.id
                save(self): serializes __objects to the JSON file
                         (path: __file_path)
                reload(self): deserializes the JSON file to __objects
                        (only if the JSON file (__file_path) exists ;
                        otherwise, no exception should be raised)

        """

        __file_path = "file.json"
        __objects = {}

        def __init__(self):
                """ construct a new FileStorage object
                """
                pass

        def all(self):
                """returns the dictionary __objects"""
                return self.__objects
        
        def new(self, obj):
                """ sets in __objects the obj
                        with key <obj class name>.id
                """
                key = obj.__class__.__name__ + "." + obj.id
                self.__objects[key] = obj.to_dict()
                

        def save(self): 
                """ serializes __objects to the JSON file
                         (path: __file_path)"""
                with open(self.__file_path, "w") as f:
                        json.dump(self.__objects, f)

        def reload(self):
                """ deserializes the JSON file to __objects
                        (only if the JSON file (__file_path) exists ;
                        otherwise, no exception should be raised)
                """
                try:
                        with open(self.__file_path, "r") as f:
                                if os.path.getsize(self.__file_path) != 0:
                                        self.__objects = json.load(f)
                except(IOError):
                        pass
               

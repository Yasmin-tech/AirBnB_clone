#!/usr/bin/python3
""" A module that contains the Amenity class that

defines all  attributes/methods for a Amenity object
"""
import models.base_model


class Amenity(models.base_model.BaseModel):
    """ a class that defines a Amenity object that inherits from BaseModel

    Public class attributes:
    ------------------------

    name: string - empty string
    """
    name = ""

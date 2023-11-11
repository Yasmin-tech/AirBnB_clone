#!/usr/bin/python3
""" A module that contains the City class that

defines all  attributes/methods for a City object
"""

import models.base_model


class City(models.base_model.BaseModel):
    """ a class that defines a City object that inherits from BaseModel

    Public class attributes:
    ------------------------

    state_id: string - empty string: it will be the State.id
    name: string - empty string
    """
    name = ""
    state_id = ""

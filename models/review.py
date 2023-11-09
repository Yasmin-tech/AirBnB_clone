#!/usr/bin/python3
""" A module that contains the Review class that

defines all  attributes/methods for a Review object
"""

import models.base_model

class Review(models.base_model.BaseModel):
        """ a class that defines a Review object that inherits from BaseModel

        Public class attributes:
        ------------------------

        place_id: string - empty string: it will be the Place.id
        user_id: string - empty string: it will be the User.id
        text: string - empty string
        """
        place_id = ""
        user_id = ""
        text = ""
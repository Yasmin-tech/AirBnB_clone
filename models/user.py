#!/usr/bin/python3
""" A module that contains the User class that

defines all  attributes/methods for a user object
"""

import models.base_model



class User(models.base_model.BaseModel):
        """ a class User that inherits from BaseModel 

        Use the init from the parent class
        
        Public class attributes:
        -----------------------
        email: string - empty string
        password: string - empty string
        first_name: string - empty string
        last_name: string - empty string
        
        """
        email = ""
        password = ""
        first_name = ""
        last_name = ""
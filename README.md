Description of the project:
	The project named AirBnB clone focuses on clonning the AirBnB website which will be
	interact with by the console(command interpreter).
	
	The project uses file as the storage engine.
	Note: This is just like a partial clonning, other things to make it a full web
		application will be added later.


Description of the command interpreter:
	How to start the command interpreter:
		Enter ./console.py on the terminal to start it

	How to use it:
		After starting the command interpreter input any command to create, destroy
		show and update an instance.

	Examples:
		create BaseModel	------> this command create an instance from a BaseModel class
		create Place	------> this command create an instance from a Place class
		destroy BaseModel <id>	------> this command delete an instance of BaseModel with the specific id
		show BaseModel <id>	------> this command show the dictionary attribute of an instance of BaseModel
						with the specific id
		all	------> show all the dictionary attribute of all instances saved in the file(storage engine)

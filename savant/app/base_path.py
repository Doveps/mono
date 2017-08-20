import os

def get_path():
	return str(os.getcwd()).split("/mono", 1)[0]
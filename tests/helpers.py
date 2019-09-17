import os


def load_file(filename: str) -> str:
	absolute_path = os.path.join(os.path.dirname(__file__), filename)

	with open(absolute_path) as schema_file:
		return schema_file.read()

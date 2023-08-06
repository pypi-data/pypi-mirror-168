"""Testing utilities

"""
import sys


class PathManager():
	"""Context manager for temporarily modifying the PATH variable, used
	primarily for testing code that is outside package directory (scripts)
	"""

	def __init__(self, add_paths: list = None):
		self.add_paths = add_paths

	def __enter__(self):
		for path in self.add_paths:
			sys.path.insert(0, path)

	def __exit__(self, exc_type, exc_value, traceback):
		try:
			for path in self.add_paths:
				sys.path.remove(path)
		except ValueError:
			pass

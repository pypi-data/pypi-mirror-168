from . import miniPath
from . import isdir
from . import isfile
import pickle
from os import path
from pathlib import Path

class TypeHint:
	def __init__(s,object:"Any"):
			s.o = object
	__repr__ = lambda s:s.o.__name__


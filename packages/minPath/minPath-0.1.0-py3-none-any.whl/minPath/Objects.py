class DataType:
	def __init__(self,type):
		self.type = type
	def value(self):
		return self.type
	def __repr__(self):
		return repr(self.value()) if isinstance(self.type, str) else str(self.type)

class FolderType(DataType):
	pass
class FileType(DataType):
	pass

class walk_(object):
    def __init__(self, generators):
        super(walk_, self).__init__()
        self.generators = generators
    def __iter__(self):
        return iter(self.generators)
    def __repr__(self):
        memoryview = hex(id(self))
        return f"<generator {type(self).__name__} object at {memoryview}>"

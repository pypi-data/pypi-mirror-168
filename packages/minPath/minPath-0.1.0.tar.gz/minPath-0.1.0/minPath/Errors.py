class InvaildPatternError(Exception):
	pass
class InvaildNameError(InvaildPatternError):
	pass
class InvaildPathSyntex(InvaildPatternError):
	pass

class FileError(Exception):
	pass
class isNotaFileObject(FileError):
	pass
class UnknownFileError(FileError):
	pass
class MiniPathError(OSError):
    pass
class MPError(MiniPathError):
    pass


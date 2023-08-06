from dataclasses import dataclass
@dataclass
class Missing(object):
	data: object
	def __reprit__(self,isin=[str]): return self.data if not isinstance(self.data,*isin) else str(self.data) 
	def __repr__(self): return f"<Missing[object] data={self.__reprit__()}>"

class UnownObject(object):
	def __init__(self,*args,**kw): 
		self.__dict__=kw;self.__args__=args;__value__=args[0] if bool(args) else Missing(args)

def pathGet(dictionary, path):
    for item in path.split("/"):
        dictionary = dictionary[item]
    return dictionary

def filter_min_path(path):
	return Path if "\\" not in Path else "/".join(Path.split("\\"))

def find_path(object,path,replaced=None):
	return 

class MinPath(object):
	def __init__    (self,Path)  : self.path = Path
	def filter      (self)       : return filter_min_path(self.path)
	def __getattr__ (self,attr)  : return getattr(self.path,attr)
	def __call__    (self,object): 
	def __repr__    (self)       : return f"MinPath({repr(self.path)})"

object = {}
object["hi/n"]

class Dict(object):
	"""docstring for Dict"""
	def __init__(self, Dict=Missing({})):
		super(Dict, self).__init__()
		if isinstance(Dict,Missing):
			self.Dict={}
		else:
			self.Dict = dict(Dict)
	def __getattr__(self,other):
		return getattr(self.Dict,other)
	def __setattr__(self,name,other):
		self.Dict[name] = other
		return self.Dict[name]
	def __getitem__(self,path):
		return getItem(self.Dict,path)
	def __add__(self,other):
		attrs={"dict":dict,"Dict":getDict}
		self.Dict.\
		update(attrs[type(other).__name__])
"[0-2][0-9]:[0-6][0-9]:[0-6][0-9] ERROR|[0-2][0-9]:[0-6][0-9]:[0-6][0-9] WARN "
"""
╔═════════════════╗
║ 🡐 🡒 ↻ ⌂  　              🗕🗗🗙 ║
╠═════════════════╣
║ 𝕃𝕠𝕒𝕕𝕚𝕟𝕘...                               ║
╚═════════════════╝
"""


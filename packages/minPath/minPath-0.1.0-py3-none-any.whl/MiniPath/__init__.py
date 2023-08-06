# pickling.py
try:
    from StringIO import StringIO ## for Python 2
except ImportError:
    from io import StringIO ## for Python 3
import pickle
from threading import Thread
import time
import re
from io import TextIOWrapper
from typing import Any,Callable
from os.path import split as split_path
import sys
from .Objects import *
from .Errors  import *

InvaildChars = r"[\\/*?:<>|]"
Invaildsyntax = r"[*?<>|]"
InvaildName_pattern = re.compile(InvaildChars)
Invaildsynt_pattern = re.compile(Invaildsyntax)
nowtime = time.time

def parser_path(content):
	token = []
	tok   = ""
	for char in content:
		if char == "/" or char == "\\":
			token.append(tok)
			tok = ""
		else:
			tok+=char
	if tok.strip():
		token.append(tok)
	return token

def vaild_name(name:str):
    """ check if name is vaild. error if not """
	if not isinstance(name,str):
		raise ValueError(f"excepted str (not {type(name).__name__})")
	if InvaildName_pattern.search(name):
		raise InvaildNameError(f"Invalid char detected, ({repr(name)}). Invaild Chars: {(InvaildChars)}")
	elif name == "":
		raise InvaildNameError(f"Invalid name. name mustn't be empty")
	return name

def vaild_path(path:str):
    """ check if path is vaild. error if not """
	if not isinstance(path,str):
		raise ValueError(f"excepted str (not {type(path).__name__})")
	if Invaildsynt_pattern.search(path):
		raise InvaildPathSyntex(f"Invalid char detected, ({repr(path)}). Invaild Chars: {(Invaildsyntax)}")
	return path

def recreate_file(file):
    """ recreate a file """
	newfile = File(file.name,file.getvalue())
	newfile.time    = file.time
	newfile.created = file.created
	return newfile

def search(files,filename):
    """ search a file if found return file else None"""
    for file in files:
        if file.name == filename:
            return file
    return

def isfile(file):
    """ returns type(file.type) is FileType """
    return type(file.type) is FileType
def isdir(file):
    """ returns type(file.type) is FolderType """
    return type(file.type) is FolderType



class Folder_Array(object):
	"""docstring for Folder_Array"""
	def __init__(self, Files):
		super(Folder_Array, self).__init__()
		self.Files = {}
		self._Files(Files);self.name = None
	def _Files(self,Files):
		if not isinstance(Files,(list,dict)):
			raise ValueError(f"excepted a any(iter,list,dict) but get {type(Files).__name__}")
		my_files = Files if isinstance(Files,list) else list(Files.values())
		[self.append(file) for file in my_files] # append files/folders
		return self.Files
	def checkFileObject(self,file):
		if isinstance(file,File) or isinstance(file,Folder):
			return file
		else:
			raise isNotaFileObject(f"{file} is not a File object")
	def append(self,file):
		file = self.checkFileObject(file)
		if file.name in self.Files:
			raise FileExistsError(f"file already Exists {file.name}:{file}")
		self.Files[file.name] = file
	def replace(self,file):
		file = self.checkFileObject(file)
		if file.name not in self.Files:
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
		self.Files[file.name] = file
	def remove(self,file,byname=False):
		if byname:
			if not isinstance(file,str):
				raise ValueError(f"excepted str (not {type(file).__name__})")
			if file not in self.Files:
				raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
			del self.Files[file]
			return
		# find file object
		if file not in self.Files.values():
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
		try:
			file = self.checkFileObject(file).name
			file = list(self.Files.keys())[list(self.Files.values()).index(file)]
			self.remove(file,byname=True)
		except ValueError:
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
		return
	def find(self,file,byname=False):
		if byname:
			if not isinstance(file,str):
				raise ValueError(f"excepted str (not {type(file).__name__})")
			if file not in self.Files:
				raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
			return self.Files[file]
		# find file object
		if file not in self.Files.values():
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
		try:
			file = self.checkFileObject(file).name
			file = self.list()[self.listObj().index(file)]
			return file
		except ValueError:
			raise FileNotFoundError(f"The system cannot find the file specified: {repr(file)}")
	def list(self):
		return list(self.Files.keys())
	def listObj(self):
		return list(self.Files.values())
	def __iter__(self):
		return iter(self.Files.items())



class File(StringIO):
	def __init__(self,name,*args,**kw):
		super(File, self).__init__(*args,**kw)
		self.name = self.rename(name)

		self.time = nowtime()
		self.created = time.strftime("%Y/%m/%d - %I:%M:%S~%p")
	def rename(self,name):
		self.name = vaild_name(name)
		try:
			if "." in name:
				self.type = FileType(name.split(".").pop())
			else:
				self.type = FileType(None)
		except IndexError:
			self.type = FileType(None)
		return name
	def copy(self,seek=True):
		if seek and self.seekable() and self.readable():self.seek(0); content = self.read()
		else: content = self.getvalue()
		file = self.__class__(self.name,content)
		file.time = self.time
		file.created = self.created
		return file
	def __repr__(self):
		return f"{type(self).__name__}({repr(self.name)})"


class Folder(Folder_Array):
	def __init__(self,name,Files={}):
		super(Folder, self).__init__(Files = Files)
		self.name = vaild_name(name)
		try:
			if "." in name:
				self.type = FolderType(name.split(".").pop())
			else:
				self.type = FolderType(None)
		except IndexError:
			self.type = FolderType(None)
		self.time = nowtime()
		self.created = time.strftime("%Y/%m/%d - %I:%M:%S~%p")
	def copy(self,copy_files=False):
		file = self.__class__(name = self.name, Files = (self.Files.copy() if copy_files else self.Files))
		file.time = self.time
		file.created = self.created
		return file
	def open(self,name,mode="rw"):
		byname=True
		if any((all(( "w" in (mode) , "r" in (mode) )),mode in ["w","x","a","+"])):
			if all(( "w" in (mode) , "r" in (mode) )) or mode == "+":
				file = self.find(name,byname=byname)
			elif mode == "w":
				wfile = self.find(name,byname=byname)
				file = wfile.copy()
				self.replace(file)
			else:
				try:
					self.append(File(name))
				except FileExistsError as error:
					if mode == "x":
						raise error
				file = self.find(name,byname=byname)
		else:
			raise ValueError(f"Unknown mode {mode}")
		file.closeit = file.close
		file.close = lambda : None
		if mode=="a" and file.seekable():
			file.seek(0)
			file.read()
		elif file.seekable():
			file.seek(0)
		return file
	def __refreah(self,recreate=False):
		if recreate:
			print("recreate is a test code. that may break something")
			for name,file in self:
				try:
					newfile = file.copy()
					self.replace(newfile)
				except FileNotFoundError:
					pass
				except AttributeError:
					pass
			return
		for name,file in self:
			try:
				if not type(file.type) is FileType:
					continue
				if file.seekable():
					file.seek(0)
			except AttributeError:
				pass
	def refreah(self):
		return self.__refreah()
	def __repr__(self):
		return f"{type(self).__name__}({repr(self.name)})"

class Drive(object):
    def __init__(self,letter,name,echo=True):
        super(Drive, self).__init__()
        if echo : print("the class still in development or it will be removed in the new update")
        if len(letter) > 1:
            raise ValueError("letter len must be 1")
        if not isinstance(letter,str):
            raise ValueError("letter must be a str")
        if not isinstance(name,str):
            raise ValueError("name must be a str")
        self.letter = letter
        self.name = name
        self.lets = letter+":"
    def __repr__(self):
        return "<"+type(self).__name__+"({}) object at ".format(repr(f"{self.name} ({self.lets})"))+hex(id(self))+">"

class MiniPath(object):
    def __init__(self,name="C:",Files=[],path_sep="/"):
        super(MiniPath, self).__init__()
        self.path_sep = path_sep
        self.paths = [ name ]
        self.path = self.path_sep.join(self.paths)
        self.parent = Folder_Array(Files)
        self.parent_dir = self.parent.list()
        self.parents = []
        self.name = name

        self.last_parent = self.parent
        self.last_dir = self.parent_dir

        self.time = nowtime()
        self.created = time.strftime("%Y/%m/%d - %I:%M:%S~%p")
    def chdir(self,path):
        """ Change the current working directory to the specified path """
        if vaild_path(path) == "":
            raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
        elif path == ".":
            return self.paths
        elif path=="..":
            if len(self.parents)==0:
                self.last_parent = self.parent
                self.last_dir = self.parent.list()
                self.path = self.path_sep.join(self.paths)
                return self.paths
            self.parents.pop()
            name = self.paths.pop()
            try:
                parent = self.parents[-1]
            except IndexError: # if len(self.parents)==0:
                self.last_parent = self.parent
                self.last_dir = self.parent.list()
                self.path = self.path_sep.join(self.paths)
                return self.paths
            dirlist  = parent.list()
            self.last_parent = parent
            self.last_dir = dirlist
            self.path = self.path_sep.join(self.paths)
            return self.paths
        children = self.last_parent.listObj()
        dirlist = self.last_parent.list()
        pathing = parser_path(path)
        parents = []
        paths = []
        for sep in pathing:
            if sep in dirlist:
                folder = search(children,sep)
                if isdir(folder):
                    parent = folder
                    children = parent.listObj()
                    dirlist = parent.list()
                    parents.append(parent)
                    paths.append(parent.name)
                else:
                    raise NotADirectoryError(f"The directory name is invalid: {repr(sep)}")
            else:
                raise FileNotFoundError(f"The MiniPath cannot find the file specified: {repr(path)}.")
        self.parents.extend(parents)
        self.paths.extend(paths)
        self.last_parent = parent
        self.last_dir = dirlist
        self.path = self.path_sep.join(self.paths)
        return self.paths
    def get(self,path):
        """ get (a file or a folder) with path """
        if vaild_path(path) == "":
            raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
        pathing = parser_path(path)
        children = self.last_parent.listObj()
        dirlist = self.last_parent.list()
        index = 0
        while len(pathing)>index:
            sep = pathing[index]
            if sep in dirlist:
                file = search(children,sep)
                if index==len(pathing)-1:
                    return file
                else:
                    if not isdir(file):
                        raise NotADirectoryError(f"The directory name is invalid: {repr(sep)}")
                    children = file.listObj()
                    dirlist = file.list()
            else:
                raise FileNotFoundError(f"The MiniPath cannot find the file specified: {repr(path)}.")
            index += 1
        raise FileNotFoundError(f"The MiniPath cannot find the file specified: {repr(path)}.")
    def get_parent(self,path):
        """ get a folder with path """
        if path is None:
            return self.last_parent
        elif vaild_path(path) == "":
            raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
        pathing = parser_path(path)
        children = self.last_parent.listObj()
        dirlist = self.last_parent.list()
        for sep in pathing:
            if sep in dirlist:
                folder = search(children,sep)
                if isdir(folder):
                    parent = folder
                    children = parent.listObj()
                    dirlist = parent.list()
                else:
                    raise NotADirectoryError(f"The directory name is invalid: {repr(sep)}")
            else:
                raise FileNotFoundError(f"The MiniPath cannot find the file specified: {repr(path)}.")
        return parent
    def listdir(self,path=None):
        """ list a folder with the specified path """
        return self.get_parent(path).list()
    def walk(self,top,sep="\\"):
        """ Directory tree generator """
        def list_(parent):
            list_dirs    = []
            list_files   = []
            parent_dirs  = []
            parent_files = []
            for name,file in parent:
                if isdir(file):
                    parent_dirs .append(file)
                    list_dirs .append(name)
                else:
                    parent_files .append(file)
                    list_files.append(name)
            return list_files,list_dirs,parent_files,parent_dirs
        if top == "" or top == None:
            parent = self.last_parent
        else:
            parent = self.get_parent(top)
        root = parent.name
        list_files,list_dirs,_,parent_dirs = list_(parent)
        listed = [(root,list_dirs,list_files)]
        def walk_wrapper(old_root,dir):
            old_root = root = ((old_root+sep)if old_root else "")+dir.name
            list_files,list_dirs,_,parent_dirs = list_(dir)
            listed = [(root,list_dirs,list_files)]
            if bool(parent_dirs):
                for dir_ in parent_dirs:
                    listed += walk_wrapper(old_root,dir_)
            return listed
        for dir in parent_dirs:
            listed += walk_wrapper(None,dir)
        return walk_(listed)
    def find(self,*args,**kw):
        """ find a file/folder in the current parent """
        return self.last_parent.find(*args,**kw)
    def list(self,*args,**kw):
        """ list the current parent """
        return self.last_parent.list(*args,**kw)
    def isdir(self,path):
        """ is folder with path"""
        return isdir(self.get(path))
    def isfile(self,path):
        """ is file with path"""
        return isfile(self.get(path))
    def makedirs(self,path,exist_ok=False):
        if vaild_path(path) == "":
            raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
        pathing = parser_path(path)
        path = ""
        for sep in pathing:
            if path:
                path += "\\"+sep
            else:
                path = sep
            try:
                self.mkdir(path)
            except FileExistsError as error:
                if not exist_ok: raise error
        return 
    def mkdir(self,path):
        """ create a folder """
        if vaild_path(path) == "":
            raise MPError(f"The filename, directory name syntax is incorrect: {repr(path)}")
        path,name = split_path(path)
        parent = self.get_parent(path if path!="" else None)
        return parent.append(Folder(name))
    def isexists(self,path):
        """ returns False when (file not found) or (not a directory) """
        try:
            self.get(path)
        except (FileNotFoundError,NotADirectoryError):
            return False
        return True
    def getcwd(self):
        """ get the current path """
        return str(self)
    @property
    def current_parent(self):
        """ get last_parent """
        return self.last_parent
    @property
    def current_dir(self):
        """ get last_dir """
        return self.last_dir
    def join(path,*paths):
        """ join one (or more) paths """
        paths = list(paths)
        return self.path_sep.join([path]+paths)
    def __str__(self):
        """ get the cwd """
        self.path = self.path_sep.join(self.paths)
        return self.path


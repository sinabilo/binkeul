import os ,pdb ,fnmatch ,re ,sys
def getfiles (targetdir =".",fnpat ="*",regpat =None ):
	files =[]
	if not regpat :
		for file in os .listdir (targetdir ):
			if fnmatch .fnmatch (file ,fnpat ):
				files .append (file )
	else :
		pat =re .compile (regpat ,re .IGNORECASE )
		for file in os .listdir (targetdir ):
			fname =os .path .basename (file )
			if pat .search (fname ):
				files .append (file )
	return files
def godir (todir =None ,olddirs =[]):
	if todir ==None :
		os .chdir (olddirs .pop ())
	else :
		olddirs .append (os .getcwd ())
		os .chdir (todir )
	return os .getcwd ()
import tempfile
class tmfopen (tempfile ._TemporaryFileWrapper ):
	def __init__ (self ,**kws ):
		kws ["dir"]=os .getcwd ()
		kws ["delete"]=False
		tf =tempfile .NamedTemporaryFile (**kws )
		super ().__init__ (tf ,tf .name ,delete =False )
	def __enter__ (self ):
		return self
	def __exit__ (self ,exc_ty ,exc_val ,exc_tb ):
		super ().__exit__ (exc_ty ,exc_val ,exc_tb )
		os .remove (self .name )
def isurl (urlstr ):
	for w in ("file:","http:","https:","ftp:"):
		if urlstr .startswith (w ):
			return True
import hashlib
def hash_file (filename ):
	h =hashlib .sha1 ()
	with open (filename ,'rb')as file :
		chunk =0
		while chunk !=b'':
			chunk =file .read (1024 )
			h .update (chunk )
	return h .hexdigest ()

import os ,pdb ,fnmatch ,re ,sys
def dataroot (realpath =False ):
	if getattr (sys ,"frozen",False ):
		dataroot =os .path .dirname (sys .executable )
	else :
		dataroot =os .path .dirname (__file__ )
	if realpath :
		return os .path .realpath (dataroot )
	else :
		return dataroot
def datapath (*filename ,realpath =False ):
	return os .path .join (dataroot (realpath ),*filename )
import configparser
from collections import ChainMap
from binkeul .betl .pubcls import SizeStyle
class Conf (dict ):
	__cfgfile ='binkeul.cfg'
	cfg =configparser .ConfigParser ()
	cfg .read (datapath (__cfgfile ))
	def __init__ (self ):
		super ().__init__ (self .setItemsFromFile ())
	def chainmap (slef ,*dics ):
		return ChainMap (*dics ,slef )
	def setItemsFromFile (self ):
		raise NotImplementedError
class MainConf (Conf ):
	def setItemsFromFile (self ):
		cfg =self .cfg
		root =cfg ["main"].get ("root","data")
		return {
		"db-file":datapath (root ,cfg ["main"].get ("db-file")),
		"i18n-usefile":datapath (root ,"i18n",cfg ["i18n"].get ("usefile")),
		"ukode-channel":int (cfg ['ukode'].get ('channel',16 )),
		"ukode-size-style":
		SizeStyle [cfg ['ukode'].get ('size-style',"fix")],
		"dics-default":list (map (str .strip ,cfg ['main'].get ('dics-default',"").split (',')))
		}
class SvgConf (Conf ):
	def setItemsFromFile (self ):
		cfg =self .cfg
		return cfg ["svg"]
CONF =MainConf ()
SVGCONF =SvgConf ()
from binkeul .tools .cachefunc import fcached ,pcached ,PCache
from functools import partial
fCached =partial (fcached ,datapath ('data','cache'))
_PCacheMain_PATH =datapath ('data','-pcache')
_PCacheMain =PCache (_PCacheMain_PATH )
pCached =partial (pcached ,_PCacheMain )

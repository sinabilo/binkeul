import pickle ,os
import atexit
from binkeul .base import pCached ,_PCacheMain
def end_main ():
	_PCacheMain .dump ()
atexit .register (end_main )

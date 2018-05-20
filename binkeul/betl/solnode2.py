from binkeul .betl .kode import Kode
from binkeul .betl .keul import Keul
SOL_ROOT =Kode (0 ,0 )
SOL_ONE =Kode (0 ,2 )
SOL_START =Kode (1 ,2 )
SOL_MID =Kode (2 ,2 )
SOL_END =Kode (3 ,2 )
SolNodes =(SOL_ROOT ,SOL_ONE ,SOL_START ,SOL_MID ,SOL_END )
class TreeItem (object ):
	def __init__ (self ,data ,parent =None ):
		self .parentItem =parent
		self .itemData =data
		self .childItems =[]
	def appendChild (self ,item ):
		self .childItems .append (item )
	def child (self ,row ):
		return self .childItems [row ]
	def childCount (self ):
		return len (self .childItems )
	def columnCount (self ):
		if self .childItems :
			return max (len (ch .itemData )for ch in self .childItems )
		else :
			return 0
	def data (self ,column ):
		try :
			return self .itemData [column ]
		except IndexError :
			return None
	def parent (self ):
		return self .parentItem
	def row (self ):
		if self .parentItem :
			return self .parentItem .childItems .index (self )
		return 0
class SolItem (TreeItem ):
	def __init__ (self ,sol ,data ,parent =None ):
		super ().__init__ (data ,parent )
		self .sol =sol
	def __repr__ (self ):
		return "SolItem({},{})".format (repr (self .sol ),self .itemData )
	def isopen (self ):
		if self .isempty ():
			return False
		return not self .isclose ()
	def isclose (self ):
		if self .isempty ():
			return False
		if self .childItems [-1 ].sol in (SOL_START ,SOL_MID ):
			return False
		elif self .childItems [-1 ].sol in (SOL_END ,SOL_ONE ):
			return True
	def isempty (self ):
		if self .childItems ==[]:
			return True
		else :
			return False
	def isroot (self ):
		return False if self .parentItem else True
	def showTree (self ,top =False ,prt =True ):
		import io
		outstr =io .StringIO ()
		def callfunc (item ,lev =0 ):
			print (lev *"    ",repr (item .sol ),": ",item .itemData ,sep ='',file =outstr )
		if top :
			callfunc (self )
			print ("-"*30 ,file =outstr )
		self .walk (callfunc )
		outstr .seek (0 )
		if prt :
			print (outstr .read ())
		else :
			return outstr .read ()
	def walk (self ,call ,level =0 ):
		for item in self .childItems :
			call (item ,level )
			item .walk (call ,level +1 )
	def toKeul (self ):
		assert self .sol ==SOL_ROOT
		return Keul (self .serialize ())
	def serialize (self ):
		ls =[]
		ls .append (self .sol )
		ls .extend (self .itemData )
		for ch in self .childItems :
			ls .extend (ch .serialize ())
		return ls
	@staticmethod
	def fromKeul (keul ):
		sollines =[]
		for kd in keul :
			if kd in SolNodes :
				solln =[kd ,]
				sollines .append (solln )
			else :
				solln .append (kd )
		return makeSolTree (sollines )
def makeSolTree (sollines ):
	def createRoot (sollines ):
		if sollines [0 ][0 ]==SOL_ROOT :
			solroot =sollines .pop (0 )
			return SolItem (SOL_ROOT ,solroot [1 :])
		return SolItem (SOL_ROOT ,[])
	def addnext (prev ,next ):
		assert type (next )==SolItem
		sol =next .sol
		if sol in (SOL_START ,SOL_ONE ):
			prev .childItems .append (next )
			next .parentItem =prev
		elif sol in (SOL_MID ,SOL_END ):
			par =find_open_node (prev )
			par .childItems .append (next )
			next .parentItem =par
		else :
			raise UserWarning ()
	def find_open_node (prev ):
		node =prev .parentItem
		while 1 :
			if node .isclose ():
				if node .parentItem ==None :
					raise UserWarning ("더이상 상위노드가 없음")
				node =node .parentItem
				continue
			else :
				return node
	def main (sollines ):
		root =createRoot (sollines )
		prev =root
		for next in sollines :
			sol =next [0 ]
			next =SolItem (sol ,next [1 :])
			addnext (prev ,next )
			prev =next
		return root
	return main (sollines )

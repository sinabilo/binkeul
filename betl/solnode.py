from binkeul .betl .kode import Kode
from binkeul .betl .keul import Keul
from binkeul .betl .pubcls import Rect
class SKode (Kode ):
	def __new__ (cls ,kode ):
		assert kode .channel in (0 ,2 )
		return super ().__new__ (cls ,kode )
	def __init__ (self ,kode ):
		pass
	def __getnewargs__ (self ):
		return (Kode (self .numerator ),)
	def getHxs (self ):
		return {
		Kode (0 ,0 ):HxSet ({0 ,4 ,6 ,11 ,13 ,16 ,18 ,23 ,25 }),
		Kode (0 ,2 ):HxSet ({0 ,3 ,4 ,6 ,7 ,11 ,12 ,13 ,16 ,17 ,18 ,19 ,22 ,23 ,24 ,25 }),
		Kode (1 ,2 ):HxSet ({0 ,3 ,4 ,6 ,7 ,11 ,13 ,14 ,16 ,17 ,18 ,19 ,23 ,24 ,25 }),
		Kode (2 ,2 ):HxSet ({0 ,3 ,4 ,6 ,11 ,13 ,14 ,15 ,16 ,18 ,19 ,23 ,24 ,25 }),
		Kode (3 ,2 ):HxSet ({0 ,3 ,4 ,6 ,11 ,12 ,13 ,15 ,16 ,18 ,19 ,22 ,23 ,24 ,25 }),
		}[self ]
	def __repr__ (self ):
		return {
		Kode (0 ,0 ):"SOL_ROOT",
		Kode (0 ,2 ):"SOL_ONE",
		Kode (1 ,2 ):"SOL_START",
		Kode (2 ,2 ):"SOL_MID",
		Kode (3 ,2 ):"SOL_END",
		}[self ]
	@property
	def rect (self ):
		return Rect (-5 -1 ,-5 -1 ,5 +1 ,5 +1 )
SOL_ROOT =SKode (Kode (0 ,0 ))
SOL_ONE =SKode (Kode (0 ,2 ))
SOL_START =SKode (Kode (1 ,2 ))
SOL_MID =SKode (Kode (2 ,2 ))
SOL_END =SKode (Kode (3 ,2 ))
SolNodes =(SOL_ROOT ,SOL_ONE ,SOL_START ,SOL_MID ,SOL_END )
class TreeItem (object ):
	def __init__ (self ,data ,parent =None ):
		self .parentItem =parent
		self .itemData =data
		self .childItems =[]
	def child (self ,row ):
		return self .childItems [row ]
	def childCount (self ):
		return len (self .childItems )
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
	def walk (self ,call ,level =0 ,byChild =False ):
		Items =self .childItems if byChild else self .subNodes
		for item in Items :
			call (item ,level )
			item .walk (call ,level +1 ,byChild )
class SolData (SolItem ):
	def __init__ (self ,data ,parent =None ):
		super ().__init__ (data ,parent )
	def columnCount (self ):
		return 0
	def rowCount (self ):
		return 0
	def __repr__ (self ):
		return "SolData({})".format (self .itemData )
class SolNode (SolItem ):
	def __init__ (self ,data ):
		self .subNodes =[]
		self .upnode =None
		super ().__init__ (data ,parent =None )
	def sublen (self ,sidx =None ):
		subNodes =self .subNodes [:sidx ]
		return len (self .subNodes )+sum (sb .sublen ()for sb in self .subNodes )
	@property
	def rootItem (self ):
		return self .parentItem if self .parentItem else self
	def reSol (self ,sidxs =[]):
		subs =self .subNodes
		slast =len (subs )-1
		for i in sidxs :
			if i >slast :break
			elif i ==slast :
				if slast ==0 :subs [i ].sol =SOL_ONE
				else :subs [i ].sol =SOL_END
			elif i ==0 :
				subs [i ].sol =SOL_START
			else :
				subs [i ].sol =SOL_MID
	def popNode (self ,sidx ):
		popitem =self .subNodes .pop (sidx )
		self .rootItem .childItems .remove (popitem )
		self .reSol ([sidx -1 ,sidx ])
	def appendNode (self ,node ,resol =False ):
		sidx =len (self .subNodes )
		self .insertNode (sidx ,node ,resol )
	def insertNode (self ,sidx ,node ,resol =False ):
		assert type (node )==SolNode
		idx =(self .subNodes [-1 ].row ()+1 )if self .subNodes else (self .row ()+1 )
		idx +=self .sublen (sidx )
		self .subNodes .append (node )
		node .upnode =self
		rootItem =self .rootItem
		rootItem .childItems .insert (idx ,node )
		node .parentItem =rootItem
		if resol :self .reSol ([sidx -1 ,sidx ,sidx +1 ])
	def columnCount (self ):
		return len (self .childItems [0 ].itemData )
	def rowCount (self ):
		return 1
	def get_sol (self ):
		return self .itemData [0 ]
	def set_sol (self ,sol ):
		self .itemData [0 ]=sol
	sol =property (get_sol ,set_sol )
	def __repr__ (self ):
		return "SolNode([{}])".format (repr (self .sol ))
	def isopen (self ):
		if self .isempty ():
			return False
		return not self .isclose ()
	def isclose (self ):
		if self .isempty ():
			return True
		if self .subNodes [-1 ].sol in (SOL_START ,SOL_MID ):
			return False
		elif self .subNodes [-1 ].sol in (SOL_END ,SOL_ONE ):
			return True
	def isempty (self ):
		if self .subNodes ==[]:
			return True
		else :
			return False
	def isroot (self ):
		return False if self .parentItem else True
	def showTree (self ,prt =True ):
		assert self ==self .rootItem
		import io
		outstr =io .StringIO ()
		return self .showNodes (prt =prt ,byChild =True )
	def showNodes (self ,top =False ,prt =True ,byChild =False ):
		import io
		outstr =io .StringIO ()
		def callfunc (item ,lev =0 ):
			print (
			lev *"    ",
			repr (item ),
			sep ='',
			file =outstr )
		if top :
			callfunc (self )
			print ("-"*30 ,file =outstr )
		self .walk (callfunc ,byChild =byChild )
		outstr .seek (0 )
		if prt :
			print (outstr .read ())
		else :
			return outstr .read ()
	def toKeul (self ):
		assert self .sol ==SOL_ROOT
		return Keul (self .serialize ())
	def serialize (self ):
		ls =[]
		ls .extend (self .itemData )
		if type (self )==SolNode :
			ls .extend (self .child (0 ).itemData )
		for ch in self .subNodes :
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
class SolRoot (SolNode ):
	def __init__ (self ):
		super ().__init__ ([SOL_ROOT ])
	def columnCount (self ):
		return 10
	def rowCount (self ):
		return self .childCount ()
	def __repr__ (self ):
		return "SolRoot()"
def makeSolTree (sollines ):
	def createRoot (sollines ):
		if sollines [0 ][0 ]==SOL_ROOT :
			solroot =sollines .pop (0 )
			assert len (solroot )==1
		return SolRoot ()
	def addnext (prev ,next ):
		assert type (next )==SolNode
		sol =next .sol
		if sol in (SOL_START ,SOL_ONE ):
			prev .appendNode (next )
		elif sol in (SOL_MID ,SOL_END ):
			par =find_open_node (prev )
			par .appendNode (next )
		else :
			raise UserWarning ()
	def find_open_node (prev ):
		node =prev .upnode
		while 1 :
			if node .isclose ():
				if node .upnode ==None :
					raise UserWarning ("더이상 상위노드가 없음")
				node =node .upnode
				continue
			else :
				return node
	def main (sollines ):
		root =createRoot (sollines )
		prev =root
		for line in sollines :
			sol =line [0 ]
			data =line [1 :]
			next =SolNode ([sol ])
			next .childItems =[SolData (data ,next )]
			addnext (prev ,next )
			prev =next
		return root
	return main (sollines )

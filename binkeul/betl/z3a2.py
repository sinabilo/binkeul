import re ,io ,array ,struct ,pprint ,__main__
import pdb
from binkeul .excepts import *
class Z3a2 :
	DIV =896
	MAX =65792
	ec9dc =lambda ls :(ls ,dict ([(c ,i )for i ,c in enumerate (ls )]));
	ec_Z ,dc_Z =ec9dc ("OoPpQqRrSsTtUuVvWwXxYyZz")
	ec_N ,dc_N =ec9dc ("AaBbCcDdEeFfGgHhIiJjKkLlMmNn")
	ec_A ,dc_A =ec9dc ("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")
	PAT =r"([A-N][A-P])|([O-Z][A-Z][A-Z])"
	REGPAT =re .compile (PAT ,re .I )
	@classmethod
	def split (cls ,z3a2s ,strict =False ):
		zlist =[]
		mpos =0
		g =True
		while g :
			g =cls .REGPAT .match (z3a2s ,mpos )
			if g :
				z =g .group (0 )
				zlist .append (z )
				mpos +=len (z )
		else :
			if strict :
				assert z3a2s [:mpos ]==z3a2s
			elif z3a2s [:mpos ]!=z3a2s :
				return None
		return zlist
	@classmethod
	def pack (cls ,val ,div0 =True ):
		if div0 :val +=256
		assert 0 <=val <cls .MAX ,"0 <= {} < {}".format (val ,cls .MAX )
		if 0 <=val <cls .DIV :
			mv ,mr =divmod (val ,32 )
			return cls .ec_N [mv ]+cls .ec_A [mr ]
		elif cls .DIV <=val <cls .MAX :
			val -=cls .DIV
			mv ,mr =divmod (val ,2704 )
			nv ,nr =divmod (mr ,52 )
			return cls .ec_Z [mv ]+cls .ec_A [nv ]+cls .ec_A [nr ]
	@classmethod
	def unpack (cls ,z3a2 ,div0 =True ):
		DIVV =256 if div0 else 0
		m =re .match (cls .PAT +"$",z3a2 ,re .I )
		assert m
		if m .group (1 ):
			mv ,mr =m .group (1 )
			return cls .dc_N [mv ]*32 +cls .dc_A [mr ]-DIVV
		elif m .group (2 ):
			mv ,nv ,nr =m .group (2 )
			return cls .dc_Z [mv ]*2704 +cls .dc_A [nv ]*52 +cls .dc_A [nr ]+cls .DIV -DIVV
class Z3a2s (str ):
	REGPAT =re .compile (r"({})*".format (Z3a2 .PAT ),re .I )
	b2z =staticmethod (lambda mode ,bts :Z3a2 .pack (struct .unpack (mode ,bts )[0 ]-{"H":0 ,"B":256 }[mode ]))
	@staticmethod
	def Z2B (zs ):
		zlist =Z3a2 .split (zs )
		bts =io .BytesIO ()
		for z in zlist :
			zv =Z3a2 .unpack (z )
			if zv <0 :
				bts .write (struct .pack ("B",zv +256 ))
			else :
				bts .write (struct .pack ("H",zv ))
		bts .seek (0 )
		return bts .read ()
	def __new__ (cls ,st ,check =False ):
		return super ().__new__ (cls ,st )
	def __init__ (self ,st ,check =False ):
		if check :self .check ()
		super ().__init__ ()
	def toBytes (self ):
		return Z3a2s .Z2B (self )
	def check (self ):
		if not Z3a2s .REGPAT .fullmatch (self ):
			raise BinkeulError ("Z3a2s 는 {} 에 매치되어야 합니다.".format (str (Z3a2 .REGPAT )))
		return True
class Z3a2sIO (io .StringIO ):
	def toStringIO (self ):
		return io .StringIO (self .readall ())
	def __init__ (self ,bts =b""):
		super ().__init__ ("")
		self .end =b""
		self .endWrite (bts )
	def replaceAll (self ,zts ):
		assert re .fullmatch (r"({}){}".format (Z3a2 .PAT ,"*"),zts ,re .I )
		self .seek (0 )
		super ().write (zts )
	def endJoin (self ,bts ):
		if not bts :return
		self .seek (0 ,2 )
		self .write (Z3a2s .b2z (self .end ))
		self .end =b''
		self .write (Z3a2sIO (bts ),readAll ())
	def endWrite (self ,bts ,endrepl =True ):
		self .seek (0 ,2 )
		bts =self .end +bts
		bts_len =(len (bts )//2 )*2
		self .end =bts [bts_len :]
		super ().write ("".join ([Z3a2s .b2z ('H',bts [i :i +2 ])for i in range (0 ,bts_len ,2 )]))
	def readAll (self ):
		self .seek (0 )
		return super ().read ()+(Z3a2s .b2z ('B',self .end )if self .end else '')
	def check (self ):
		Z3a2s (self .readAll (),check =True )
		return True
	def write (self ,bts ):
		raise NotImplementedError ('write 함수는 사용할 수 없음')
	def toBytes (self ):
		return Z3a2s .Z2B (self .readAll ())
	def seek (self ,*arg ):
		if not arg in ((0 ,),(0 ,0 ),(0 ,2 )):
			raise UserWarning ("Z3a2sIO seek is not run")
		super ().seek (*arg )

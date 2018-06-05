from collections import namedtuple
FfcMap =[
(40 ,41 ,42 ,43 ,44 ),
(35 ,36 ,37 ,38 ,39 ),
(20 ,15 ,0 ,5 ,10 ),
(21 ,16 ,1 ,6 ,11 ),
(22 ,17 ,2 ,7 ,12 ),
(23 ,18 ,3 ,8 ,13 ),
(24 ,19 ,4 ,9 ,14 ),
(30 ,31 ,32 ,33 ,34 ),
(25 ,26 ,27 ,28 ,29 ),
]
class Ffc (namedtuple ("_Ffc",['u',"v"])):
	@property
	def x (self ):return (self .u *2 )
	@property
	def y (self ):return (self .v *2 )
FfcOrd =list (range (45 ))
for v ,ln in enumerate (FfcMap ):
	for u ,idx in enumerate (ln ):
		FfcOrd [idx ]=Ffc (u -2 ,v -4 )
rmidx =(0 ,1 ,2 ,3 ,6 ,7 ,8 ,12 ,15 ,16 ,18 ,22 ,31 )
hmidx =(0 ,1 ,3 ,7 ,15 ,31 )
assert len (rmidx )==13
class FfcSet :
	def __init__ (self ,data ):
		assert data .bit_length ()<=32
		self .data =data
		bitls =[]
		j =0
		for i in range (45 ):
			if i in rmidx :
				bitls .append (None )
			else :
				if (1 <<j )&data :
					bitls .append (1 )
				else :
					bitls .append (0 )
				j +=1
		fv =sum (n for i ,n in enumerate (bitls )if n !=None )
		fb =fv %4
		bitls [6 ]=fb &1
		bitls [18 ]=(fb &2 )>>1
		bitls [2 ]=0
		bitls [8 ]=bitls [16 ]=1
		for idx ,ls in [
		(12 ,(44 ,39 ,10 ,11 ,13 ,14 ,34 ,29 )),
		(22 ,(40 ,35 ,20 ,21 ,23 ,24 ,30 ,25 ))]:
			s =sum (n for i ,n in enumerate (bitls )if i in ls )
			bitls [idx ]=(s +1 )%2
		for n in range (6 ):
			h =(2 **n )
			s =sum (m for i ,m in enumerate (bitls )if i !=h -1 and (i +1 )&h )
			bitls [h -1 ]=1 if s %2 else 0
		self .bitls =bitls
	def __repr__ (self ):
		return "{}({})".format (self .__class__ .__name__ ,self .data )
	def __eq__ (self ,other ):
		assert isinstance (other ,self .__class__ )
		return self .bitls ==other .bitls
	@property
	def bitset (self ):
		return "".join (reversed (list (map (str ,self .bitls ))))
	def gen (self ):
		for idx ,n in enumerate (self .bitls ):
			if n ==1 :
				yield FfcOrd [idx ]
	@classmethod
	def sample (cls ):
		import random
		data =random .randint (0 ,2 **32 -1 )
		return cls (data )
	@classmethod
	def fromBitSet (cls ,bitls ):
		assert len (bitls )==45
		if isinstance (bitls ,str ):
			bitls =list (map (int ,reversed (bitls )))
		eh =[]
		for n in range (6 ):
			h =(2 **n )
			s =sum (m for i ,m in enumerate (bitls )if (i +1 )&h )
			if s %2 !=0 :
				eh .append (h -1 )
		if eh :
			eidx =sum (h +1 for h in eh )-1
			if eidx >=45 :return False
			bitls [eidx ]^=1
		if bitls [2 ]!=0 :return False
		if bitls [8 ]!=1 or bitls [16 ]!=1 :return False
		for idx ,ls in [
		(12 ,(44 ,39 ,10 ,11 ,13 ,14 ,34 ,29 )),
		(22 ,(40 ,35 ,20 ,21 ,23 ,24 ,30 ,25 ))]:
			s =sum (n for i ,n in enumerate (bitls )if i in ls )
			if (bitls [idx ]+s )%2 ==0 :return False
		fv =sum (n for i ,n in enumerate (bitls )if not i in rmidx )
		fb =fv %4
		if bitls [6 ]!=(fb &1 ):return False
		if bitls [18 ]!=((fb &2 )>>1 ):return False
		data =0
		j =0
		for i in range (45 ):
			if i in rmidx :continue
			data |=bitls [i ]<<j
			j +=1
		obj =cls (data )
		assert obj .bitls ==bitls
		return obj

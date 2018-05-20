from binkeul .betl .z3a2 import Z3a2
import re
HxBitsetRe =re .compile ("[01]{97}$")
class HxBaseZ3a2 :
	@staticmethod
	def encode (bitset ):
		assert HxBitsetRe .match (bitset )
		bm =0
		za =[]
		b1 =int (bitset [:1 ],2 )
		for n ,i in enumerate (range (1 ,97 ,16 )):
			v =int (bitset [i :i +16 ],2 )
			if v :
				bm |=1 <<n +1
				za .append (Z3a2 .pack (v ))
		za .insert (0 ,Z3a2 .pack ((b1 |bm )-256 ))
		return "".join (za )
	@staticmethod
	def decode (za ):
		bitset =[]
		zas =Z3a2 .split (za )
		bm =Z3a2 .unpack (zas .pop (0 ))+256
		b1 ='1'if bm &1 else '0'
		for n in range (6 ):
			if (bm >>n )&2 :
				bitset .append (
				"{:0>16b}".format (Z3a2 .unpack (zas .pop (0 )))
				)
			else :
				bitset .append ("0"*16 )
		return b1 +"".join (bitset )

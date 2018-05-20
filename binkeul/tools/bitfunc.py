import hashlib
def bits (number ):
	bit =1
	while number >=bit :
		if number &bit :
			yield 1
		else :
			yield 0
		bit <<=1
def msb (x ):
	return x .bit_length ()-1
def lsb (x ):
	return msb (x &-x )
def onbitcount (x ):
	b =0
	bit =1
	while bit <=x :
		b +=int (x &bit >0 )
		bit =bit <<1
	return b
def R1bit (x ):
	if x ==0 :return -1
	x =((-x )^-abs (~x )).bit_length ()
	return x -1
def L1bit (x ):
	if x ==0 :return -1
	x =x .bit_length ()
	return x -1
def bytes2int (b ,limit =4 ):
	x =0
	for i in range (min (len (b ),limit )):
		x +=b [i ]<<(i *8 )
	return x
def bytes2hashint (bts ):
	hashint =hashlib .md5 (bts ).digest ()
	return bytes2int (hashint ,16 )

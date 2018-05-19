from PIL import Image
import os ,tempfile
import pdb
def OGX (num ):
	if num ==255 :
		return 100
	elif num ==0 :
		return 0
	elif num >=128 :
		return 10
	elif num <128 :
		return 1
class FillcheckImage :
	def __init__ (self ,bitmap ):
		line_px2
		round_px2
		pass
def linetype (px ,x ,y ,psum4set =True ):
	p1 ,p2 ,p3 ,p4 =(
	OGX (px [x -1 ,y -1 ]),
	OGX (px [x ,y -1 ]),
	OGX (px [x -1 ,y ]),
	OGX (px [x ,y ]))
	psum =sum ([p1 ,p2 ,p3 ,p4 ])
	if psum ==200 :
		if p1 ==p4 ==0 :
			return "R"
		elif p2 ==p3 ==0 :
			return "L"
	elif psum ==100 :
		return "C"
	elif psum ==4 :
		if psum4set :
			px [x ,y ]=0
			px [x -1 ,y ]=0
			px [x ,y -1 ]=0
			px [x -1 ,y -1 ]=0
		return "G"
	return psum
def checkRL (px ,x ,y ):
	if not linetype (px ,x +1 ,y +1 )in (0 ,400 ):return True
	if not linetype (px ,x -1 ,y +1 )in (0 ,400 ):return True
	if not linetype (px ,x +1 ,y -1 )in (0 ,400 ):return True
	if not linetype (px ,x -1 ,y -1 )in (0 ,400 ):return True
	return False
def set_linepx (linepx ,px ,x ,y ):
	subLR =lambda x ,y :linepx .append ((x ,y ))if (linetype (px ,x ,y )=="C")else None
	lnt =linetype (px ,x ,y )
	if lnt in ('R','L','G'):
		if not checkRL (px ,x ,y ):return
		if lnt =='R':
			subLR (x -1 ,y -1 )
			subLR (x +1 ,y +1 )
		elif lnt =='L':
			subLR (x -1 ,y +1 )
			subLR (x +1 ,y -1 )
		elif lnt =='G':
			print ("G:",x ,y )
			linepx .append ((x -1 ,y -1 ))
			linepx .append ((x +1 ,y +1 ))
			linepx .append ((x +1 ,y -1 ))
			linepx .append ((x -1 ,y +1 ))
		linepx .append ((x ,y ))
def drawline_im2 (linepx ,im2 ):
	print (linepx )
	px2 =im2 .load ()
	for p in linepx :
		x ,y =p [0 ]*2 ,p [1 ]*2
		px2 [x ,y ]=px2 [x -1 ,y ]=px2 [x ,y -1 ]=px2 [x -1 ,y -1 ]=0
def fillchecker (im ):
	linepx =list ()
	im =im .convert ('L')
	mx ,my =im .size
	px =im .load ()
	for y in range (1 ,my -1 ):
		for x in range (1 ,mx -1 ):
			set_linepx (linepx ,px ,x ,y )
	mx2 ,my2 =mx *2 ,my *2
	im2 =im .resize ([mx2 ,my2 ]).convert ('1')
	drawline_im2 (linepx ,im2 )
	return im2 ,linepx
def bmp_round (im2 ):
	px2 =im2 .load ()
	mx2 ,my2 =im2 .size
	px2list =[]
	for y in range (2 ,my2 -1 ):
		for x in range (2 ,mx2 -1 ):
			if 400 ==linetype (px2 ,x ,y ,psum4set =False ):
				px2list .append ((x ,y ))
	for x ,y in px2list :
		px2 [x ,y ]=px2 [x -1 ,y -1 ]=px2 [x -1 ,y ]=px2 [x ,y -1 ]=255
	return im2
def fillck2x (bmpfile ,savefile =None ,svgfile =None ,round =True ):
	im =Image .open (bmpfile )
	im2 ,linepx =fillchecker (im )
	if savefile :
		if round :
			im2 =bmp_round (im2 )
		im2 .save (savefile )
	if svgfile :
		pass
	else :
		pass
	return im2 ,linepx

from PIL import Image
import os ,tempfile
from enum import Enum ,IntEnum
import pdb
OX =lambda num :1 if num else 0
class Color (IntEnum ):
	white =1000
	lightgray =100
	drakgray =10
	black =1
CW =Color .white
CL =Color .lightgray
CD =Color .drakgray
CB =Color .black
CW2CB2 =CW *2 +CB *2
CW1CB3 =CW +CB *3
CW3CB1 =CW *3 +CB
CD4 =CD *4
CB4 =CB *4
CW4 =CW *4
def OGX (num ):
	if num ==255 :
		return Color .white
	elif num ==0 :
		return Color .black
	elif num >=128 :
		return Color .white
	elif num <128 :
		return Color .drakgray
def type2x2px (px ,x ,y ,replpx ={'G':0 }):
	p1 ,p2 ,p3 ,p4 =(
	OGX (px [x -1 ,y -1 ]),
	OGX (px [x ,y -1 ]),
	OGX (px [x -1 ,y ]),
	OGX (px [x ,y ]))
	psum =sum ([p1 ,p2 ,p3 ,p4 ])
	if psum ==CW2CB2 :
		if p1 ==p4 ==CB :
			psum ="R"
		elif p2 ==p3 ==CB :
			psum ="L"
	elif psum ==CW1CB3 :
		psum ="C"
	elif psum ==CD4 :
		psum ="G"
	if replpx :
		if replpx .get (psum ,None ):
			px [x ,y ]=px [x -1 ,y ]=px [x ,y -1 ]=px [x -1 ,y -1 ]=replpx [psum ]
	return psum
def checkRL (px ,x ,y ):
	if not type2x2px (px ,x +1 ,y +1 )in (CB4 ,CW4 ):return True
	if not type2x2px (px ,x -1 ,y +1 )in (CB4 ,CW4 ):return True
	if not type2x2px (px ,x +1 ,y -1 )in (CB4 ,CW4 ):return True
	if not type2x2px (px ,x -1 ,y -1 )in (CB4 ,CW4 ):return True
	return False
def set_linepx (linepx ,px ,x ,y ):
	subLR =lambda x ,y :linepx .append ((x ,y ))if (type2x2px (px ,x ,y )=="C")else None
	lnt =type2x2px (px ,x ,y )
	if lnt in ('R','L','G'):
		if not checkRL (px ,x ,y ):return
		if lnt =='R':
			subLR (x -1 ,y -1 )
			subLR (x +1 ,y +1 )
		elif lnt =='L':
			subLR (x -1 ,y +1 )
			subLR (x +1 ,y -1 )
		elif lnt =='G':
			linepx .append ((x -1 ,y -1 ))
			linepx .append ((x +1 ,y +1 ))
			linepx .append ((x +1 ,y -1 ))
			linepx .append ((x -1 ,y +1 ))
		linepx .append ((x ,y ))
def drawline_im2 (linepx ,im2 ):
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
	im2 =im .resize ([mx2 ,my2 ]).convert ('1',dither =Image .NONE )
	drawline_im2 (linepx ,im2 )
	return im2 ,linepx
def get_round_info (im ):
	im =im .convert ('L')
	px =im .load ()
	mx ,my =im .size
	replpx ={CB4 :128 }
	px2round =[]
	CW3CL1 =CW *3 +CL
	def set_round_info (x ,y ):
		if CB4 !=type2x2px (px ,x ,y ,replpx =replpx ):
			return
		if type2x2px (px ,x -1 ,y -1 ,{})==CW3CL1 :
			px2round .append ((x *2 -2 ,y *2 -2 ))
		if type2x2px (px ,x +1 ,y +1 ,{})==CW3CL1 :
			px2round .append ((x *2 +1 ,y *2 +1 ))
		if type2x2px (px ,x -1 ,y +1 ,{})==CW3CL1 :
			px2round .append ((x *2 -2 ,y *2 +1 ))
		if type2x2px (px ,x +1 ,y -1 ,{})==CW3CL1 :
			px2round .append ((x *2 +1 ,y *2 -2 ))
	for y in range (2 ,my -1 ):
		for x in range (2 ,mx -1 ):
			set_round_info (x ,y )
	return px2round
def img_round (im2 ,px2round ):
	px2 =im2 .load ()
	mx2 ,my2 =im2 .size
	for x ,y in px2round :
		px2 [x ,y ]=255
	return im2
def fillck2x (bmpfile ,savefile =None ,round =False ):
	if type (bmpfile )==str :
		im =Image .open (bmpfile )
	else :
		im =bmpfile
	if round :
		px2round =get_round_info (im )
	im2 ,linepx =fillchecker (im )
	if round :
		im2 =img_round (im2 ,px2round )
	if savefile :
		im2 .save (savefile )
	return im ,im2 ,linepx

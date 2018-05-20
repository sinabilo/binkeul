import random ,pdb ,collections ,enum
from PySide .QtCore import *
from PySide .QtGui import *
from binkeul .qkui .fodata import *
from binkeul .betl .bkode import BKode
from binkeul .betl .solnode import SKode
class QkFoGrpItem (QAbstractGraphicsShapeItem ):
	def __init__ (self ,*a ):
		super ().__init__ (*a )
		self .setFlag (QGraphicsItem .ItemIsSelectable )
		self ._pen =QPen (Qt .NoPen )
		self .setPen (self ._pen )
		self ._sel_pen =QPen (Qt .NoPen )
	def rect (self ):
		return self ._rect
	def setRect (self ,*a ):
		if len (a )==4 :
			x ,y ,w ,h =a
			self ._rect =QRect (x ,y ,w ,h )
			self .update ()
		elif len (a )==1 and type (a [0 ])==QRect :
			self ._rect =a [0 ]
			self .update ()
		else :
			raise TypeError ("")
	def setSelected (self ,selected ):
		super ().setSelected (selected )
		if self .isSelected ():
			self .setBrush (self ._sel_brush )
		else :
			self .setBrush (self ._brush )
	@staticmethod
	def extendRect (r ,w ):
		return QRect (r .x ()-w ,r .y ()-w ,r .width ()+w *2 ,r .height ()+w *2 )
	def setPaint (self ,painter ):
		pass
		painter .setPen (self .pen ())
		painter .setBrush (self .brush ())
class QkFoI (QkFoGrpItem ):
	exw =3
	def __init__ (self ):
		super ().__init__ ()
		self ._hover =False
		self .setAcceptsHoverEvents (True )
		self .setRect (-18 ,-18 ,36 ,36 )
		self .setBrush (self ._brush )
		self ._sel_brush =QBrush (Qt .red )
		self .setOpacity (0.6 )
		self .setZValue (201 )
	def mousePressEvent (self ,event ):
		pass
	def setHover (self ,hover =True ):
		if self ._hover !=hover :
			if hover ==True :
				self .setRect (self .extendRect (self .rect (),self .exw ))
			elif hover ==False :
				self .setRect (self .extendRect (self .rect (),-self .exw ))
			self ._hover =hover
	def hoverEnterEvent (self ,e ):
		self .setHover (True )
	def hoverLeaveEvent (self ,e ):
		self .setHover (False )
	def boundingRect (self ):
		penw =2
		return QRectF (self .extendRect (self .rect (),penw ))
class QkFoIEllips (QkFoI ):
	def __init__ (self ,x ,y ):
		self .Fo =Foint (x ,y ,Fo .IE )
		self ._brush =QBrush (Qt .lightGray )
		super ().__init__ ()
		self .moveBy (x *30 ,y *30 )
		self ._chk_brush =QBrush (Qt .green )
		self ._checked =False
	def setChecked (self ,chk =True ):
		self ._checked =chk
	def isChecked (self ):
		return self ._checked
	def paint (self ,painter ,option ,widget ):
		self .setPaint (painter )
		painter .drawEllipse (self .rect ())
class QkFoIMrect (QkFoI ):
	def __init__ (self ,x ,y ):
		self .Fo =Foint (x ,y ,Fo .IM )
		self ._brush =QBrush (Qt .green )
		super ().__init__ ()
		self .moveBy (x *30 ,y *30 )
		self .rotate (45 )
	def paint (self ,painter ,option ,widget ):
		self .setPaint (painter )
		painter .drawRoundedRect (self .rect (),5 ,5 )
class QkFoD (QkFoGrpItem ):
	def __init__ (self ,x ,y ,w ,h ,parent =None ):
		super ().__init__ ()
		self .setAcceptsHoverEvents (True )
		self .setRect (x ,y ,w ,h )
		self ._brush =QBrush (Qt .black )
		self .setBrush (self ._brush )
		self ._sel_brush =QBrush (Qt .red )
		self .setZValue (101 )
	def vtoggle (self ):
		self .setVisible (not self .isVisible ())
	def isSet (self ):
		return self .isVisible ()
	def boundingRect (self ):
		return QRectF (self .rect ())
	def setSelected (self ,tf ):
		if tf :
			self .setZValue (102 )
		else :
			self .setZValue (101 )
		super ().setSelected (tf )
	def paint (self ,painter ,option ,widget ):
		self .setPaint (painter )
		painter .drawRect (self .rect ())
class QkFoDRect (QkFoD ):
	def __init__ (self ,x ,y ,parent =None ):
		if x %2 ==y %2 ==0 :
			self .Fo =Foint (x ,y ,Fo .DP )
		elif x %2 ==0 :
			self .Fo =Foint (x ,y ,Fo .DV )
		else :
			self .Fo =Foint (x ,y ,Fo .DH )
		super ().__init__ (-15 ,-15 ,30 ,30 ,parent )
		self .moveBy (x *30 ,y *30 )
class QkFoDRay (QkFoD ):
	'''사선'''
	def __init__ (self ,x ,y ,k ,parent =None ):
		self .Fo =Foint (x ,y ,k )
		super ().__init__ (-9 ,-40 ,18 ,80 ,parent )
		dx =1 if k ==Fo .DR else 0
		self .rotate (45 +dx *-90 )
		self .moveBy (x *30 ,y *30 )
class QkFoG (QkFoGrpItem ):
	def __init__ (self ,x ,y ,w ,h ,parent =None ):
		super ().__init__ ()
		self .setRect (x ,y ,w ,h )
		self ._brush =QBrush (Qt .yellow )
		self .setBrush (self ._brush )
		self .setZValue (91 )
	def boundingRect (self ):
		return QRectF (self .rect ())
	def paint (self ,painter ,option ,widget ):
		self .setPaint (painter )
		painter .drawRect (self .rect ())
class QkFoGRect (QkFoG ):
	def __init__ (self ,x ,y ,parent =None ):
		if x %2 ==y %2 ==0 :
			self .Fo =Foint (x ,y ,Fo .DP )
		elif x %2 ==0 :
			self .Fo =Foint (x ,y ,Fo .DV )
		else :
			self .Fo =Foint (x ,y ,Fo .DH )
		super ().__init__ (-20 ,-20 ,40 ,40 ,parent )
		self .moveBy (x *30 ,y *30 )
class QkFoGRay (QkFoG ):
	def __init__ (self ,x ,y ,k ,parent =None ):
		self .Fo =Foint (x ,y ,k )
		super ().__init__ (-14 ,-45 ,28 ,90 ,parent )
		dx =1 if k ==Fo .DR else 0
		self .rotate (45 +dx *-90 )
		self .moveBy (x *30 ,y *30 )
class QkFopadScene (QGraphicsScene ):
	def __init__ (self ):
		super ().__init__ ()
		self .initFo ()
		self .setupState ()
	def setupState (self ):
		machine =self .machine =QStateMachine (self )
	def setShowAllItem (self ,bo ,mode =Fo .I ):
		dic ={Fo .I :self .foidic ,
		Fo .D :self .foddic ,
		Fo .G :self .fogdic ,
		}[mode ]
		for i in dic .values ():
			i .show ()if bo else i .hide ()
	def unsetSelectedFoOItems (self ):
		for i in self .foddic .values ():
			i .setSelected (False )
	def initFo (self ):
		self .foidic ={}
		self .foddic ={}
		self .fogdic ={}
		self .fosdic ={}
		for x in range (-4 ,5 ):
			for y in range (-4 ,5 ):
				if x %2 or y %2 :continue
				i =QkFoIMrect (x ,y )
				self .foidic [i .Fo ]=i
				self .addItem (i )
		for x in range (-4 ,5 ):
			for y in range (-4 ,5 ):
				if x %2 and y %2 :
					continue
				o =QkFoDRect (x ,y )
				o .hide ()
				self .foddic [o .Fo ]=o
				self .addItem (o )
				g =QkFoGRect (x ,y )
				g .hide ()
				self .fogdic [g .Fo ]=g
				self .addItem (g )
		for x in range (-3 ,4 ):
			for y in range (-3 ,4 ):
				if not (x %2 and y %2 ):continue
				i =QkFoIEllips (x ,y )
				self .foidic [i .Fo ]=i
				self .addItem (i )
		for x in range (-3 ,4 ):
			for y in range (-3 ,4 ):
				if not (x %2 and y %2 ):continue
				for k in (Fo .DL ,Fo .DR ):
					o =QkFoDRay (x ,y ,k )
					o .hide ()
					self .foddic [o .Fo ]=o
					self .addItem (o )
					g =QkFoGRay (x ,y ,k )
					g .hide ()
					self .fogdic [g .Fo ]=g
					self .addItem (g )
class QkFopad (QGraphicsView ):
	sg_input_step =Signal ((Fodata ,Fodata ))
	def __init__ (self ,parent =None ):
		super ().__init__ (parent )
		self .setObjectName ("fopad")
		self .fodraw_stack =FodrawStack ()
		self .setRenderHints (QPainter .Antialiasing |QPainter .SmoothPixmapTransform )
		self .setHorizontalScrollBarPolicy (Qt .ScrollBarAlwaysOff )
		self .setVerticalScrollBarPolicy (Qt .ScrollBarAlwaysOff )
		self .setViewportMargins (0 ,0 ,0 ,0 )
		self .setFixedSize (300 ,300 )
		self .setSceneRect (-150 ,-150 ,300 ,300 )
		self .setBackgroundBrush (QBrush (Qt .white ))
		self .foscene =QkFopadScene ()
		self .setScene (self .foscene )
		self .foidrag =None
		self .sg_input_step [Fodata ,Fodata ].connect (self .draw )
	def enterEvent (self ,e ):
		self .foscene .setShowAllItem (True ,Fo .I )
		self .setBackgroundBrush (QBrush (Qt .white ))
	def leaveEvent (self ,e ):
		self .foscene .setShowAllItem (False ,Fo .I )
		self .setBackgroundBrush (QImage ("fopad-bg.png"))
	def fodrag_start (self ,e ):
		if self .foidrag :
			raise UserWarning ()
		self .foidrag =FoMInputs (self )
		i =self .itemAt (e .pos ())
		if i and Fo .DI (i .Fo .k )==Fo .I .value :
			self .foidrag .append (i .Fo )
			return True
		return False
	def fodrag_append (self ,e ):
		if not self .foidrag :
			return None
		i =self .itemAt (e .pos ())
		if i and Fo .DI (i .Fo .k )==Fo .I .value and self .foidrag [-1 ]!=i .Fo :
			self .foidrag .append (i .Fo )
			return True
		return False
	def fodrag_end (self ):
		if not self .foidrag :
			return None
		self .foidrag .appendEnd ()
		self .foscene .unsetSelectedFoOItems ()
	def undoDraw (self ):
		self .fodraw_stack .undo ()
		self .sg_input_step [Fodata ,Fodata ].emit (*self .getFoDG ())
	def redoDraw (self ):
		self .fodraw_stack .redo ()
		self .sg_input_step [Fodata ,Fodata ].emit (*self .getFoDG ())
	def keyPressEvent (self ,e ):
		if e .key ()==Qt .Key_Backspace :
			if bool (e .modifiers ()&Qt .SHIFT ):
				self .redoDraw ()
			else :
				self .undoDraw ()
		elif e .key ()==Qt .Key_Delete :
			self .foscene .setShowAllItem (False ,Fo .G )
			for g in self .fodraw_stack .sumw ().getFoD (False ):
				self .foscene .fogdic [g ].show ()
		elif e .key ()==Qt .Key_Return :
			pass
		elif e .key ()==Qt .Key_Insert :
			pass
		elif e .key ()in (
		Qt .Key_Left ,
		Qt .Key_Up ,
		Qt .Key_Right ,
		Qt .Key_Down ,):
			pass
	def mousePressEvent (self ,e ):
		self .fodrag_start (e )
	def mouseMoveEvent (self ,e ):
		if self .fodrag_append (e ):
			pass
		super ().mouseMoveEvent (e )
	def getFoDG (self ):
		return self .fodraw_stack .getFoGD ()
	def mouseReleaseEvent (self ,e ):
		self .fodrag_append (e )
		self .fodrag_end ()
		fow =self .foidrag .getFoW ()
		self .sg_input_step [Fodata ,Fodata ].emit (*self .getFoDG ())
	def mouseDoubleClickEvent (self ,e ):
		self .resetDraw ()
	def draw (self ,fod ,fog ):
		self .foscene .setShowAllItem (False ,Fo .D )
		self .foscene .setShowAllItem (False ,Fo .G )
		for o in fod :
			self .foscene .foddic [o ].show ()
		for g in fog :
			self .foscene .fogdic [g ].show ()
	def resetDraw (self ,kode =None ):
		if kode and not isinstance (kode ,(BKode ,SKode )):
			return
		self .foscene .setShowAllItem (False ,Fo .D )
		self .foscene .setShowAllItem (False ,Fo .G )
		self .fodraw_stack =FodrawStack (kode )
		self .sg_input_step [Fodata ,Fodata ].emit (*self .getFoDG ())

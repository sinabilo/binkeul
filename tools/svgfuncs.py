from lxml import etree
import re ,os
def svgskew (svgfile ,angle =5 ,xmove =0 ,leftrev =0 ,rightrev =0 ):
	def svgskewrepl (xstr ,delviewbox =False ):
		root =etree .XML (xstr )
		if leftrev :
			newvb =re .sub (
			"^\d+([.]\d+)?(?= )",
			lambda g :str (float (g .group (0 ))+leftrev ),
			root .get ("viewBox"))
			root .set ("viewBox",newvb )
		if rightrev :
			root .set ("width",
			re .sub (r"\d+([.]\d+)?(?=pt)",
			lambda g :str (float (g .group (0 ))+rightrev ),
			root .get ("width")
			)
			)
			def viewbox_replace (values ):
				vals =values .split (" ")
				vals [2 ]=str (float (vals [2 ])+rightrev )
				return " ".join (vals )
			root .set ("viewBox",viewbox_replace (root .get ("viewBox")))
		nm =root .nsmap [None ]
		g =root .find ('{%s}g'%nm )
		if delviewbox :
			del root .attrib ["width"]
			del root .attrib ["height"]
			del root .attrib ["viewBox"]
		re_call =lambda g :str (float (g .group (0 ))+xmove )
		newtrset =re .sub (r"(?<=translate\()\d+[.]\d+(?=[,])",re_call ,g .get ("transform"))
		newtrset =re .sub (r'''skewX[(]\d+[)]''',
		"",newtrset ).strip ()+" skewX({})".format (angle )
		g .set ("transform",newtrset )
		return etree .tostring (root )
	if type (svgfile )==str :
		if svgfile [0 ]=="<":
			return svgskewrepl (xstr )
		elif os .path .isfile (svgfile ):
			with open (svgfile ,"rb+")as f :
				xstr =f .read ()
				f .truncate (0 )
				f .seek (0 )
				f .write (svgskewrepl (xstr ))
		else :
			raise IOError ()
	else :
		f =svgfile
		f .truncate (0 )
		f .seek (0 )
		f .write (svgskewrepl (xstr ))

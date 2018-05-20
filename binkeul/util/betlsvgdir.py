import runpy ,sys ,os ,functools
print ("--BETLSVGDIR--")
def newer (pngf ):
	svgf =os .path .splitext (pngf )[0 ]+".svg"
	if not os .path .isfile (svgf ):
		return False
	else :
		if os .path .getmtime (pngf )>os .path .getmtime (svgf ):
			return True
	return False
def makesvg (root ,pngf ):
	sys .argv =["",pngf ]
	_ =runpy .run_module ("binkeul.utils.betlsvg",run_name ="__main__")
CWD =os .getcwd ()
for root ,dirs ,files in os .walk (os .curdir ):
	print ("-- DIR :",root )
	os .chdir (root )
	for pngf in filter ((lambda f :os .path .splitext (f )[1 ].lower ()==".png"),files ):
		if newer (pngf ):
			makesvg (root ,pngf )
			print (pngf )
	os .chdir (CWD )

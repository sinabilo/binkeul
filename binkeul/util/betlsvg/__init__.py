from PIL import Image
import os ,tempfile
from .roughimg import roughimg
from .fillck2x import fillck2x ,drawline_im2
from binkeul .tools .potraceconv import img2svg ,svg2png
from binkeul .tools .which import which
from binkeul .utils .solfuncs import appendSolns
def betlsvg_main (bmpfile ,
save_svg =None ,
ck2x =True ,
save_ck2x_bmp =None ,
save_nosie_bmp =None ,
round_bmp =False ,
roughlevel =1 ,
alphamax =0.1 ,
resolution =150 ,
skew =[0.0 ,0 ,0.0 ,0.0 ],
solns ="",
prtout =False ):
	linepx =None
	im1x =None
	if ck2x :
		im1x ,im2x ,linepx =fillck2x (
		bmpfile ,
		savefile =save_ck2x_bmp ,
		round =round_bmp )
	else :
		if type (bmpfile )==str :
			im2x =Image .open (bmpfile )
		else :
			im2x =bmpfile
		im2x =im2x .convert ('1')
	im2x =roughimg (im2x ,roughlevel ,save_nosie_bmp )
	if linepx :drawline_im2 (linepx ,im2x )
	tmpbmp =tempfile .NamedTemporaryFile (
	suffix =".bmp",
	dir =os .getcwd (),
	delete =False )
	im2x .save (tmpbmp ,format ='bmp')
	tmpbmp .close ()
	if not save_svg :
		save_svg =os .path .splitext (bmpfile )[0 ]+'.svg'
	if (which ("potrace")or which ("potrace.exe"))is None :
		raise SystemError ("potrace 프로그램을 찾을수 없습니다.")
	if im1x and solns :
		appendSolns (solns ,im1x ,save_svg )
	os .system ('potrace "{}" -a {} -r {} -s -o "{}"'.format (
	tmpbmp .name ,alphamax ,resolution ,save_svg ))
	if prtout :
		with open (save_svg ,'r')as f :
			print (f .read ())
	if skew !=[0.0 ,0 ,0.0 ,0.0 ]:
		skewangle ,xmove ,leftrev ,rightrev =skew
		from binkeul .tools .svgfuncs import svgskew
		svgskew (save_svg ,skewangle ,xmove ,leftrev ,rightrev )
	os .remove (tmpbmp .name )

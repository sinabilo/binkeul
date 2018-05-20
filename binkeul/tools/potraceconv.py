import cairosvg
import io ,os
import subprocess
import tempfile
from PIL import Image
import svgwrite
from .which import which
from lxml import etree
if (which ("potrace")or which ("potrace.exe"))is None :
	raise SystemError ("potrace 프로그램을 찾을수 없습니다.")
def potrace_exe (tfbmp ,outsvg ,alphamax ):
	subprocess .call (
	['potrace','-s','-a',str (alphamax )],
	stdin =tfbmp ,
	stdout =outsvg
	)
def img2svg (im ,svgfileobj =None ,alphamax =0.1 ):
	if im .mode !='1':
		im =im .convert ('1')
	tfbmp =tempfile .TemporaryFile ()
	im .save (tfbmp ,'ppm')
	tfbmp .seek (0 )
	outsvg =svgfileobj if svgfileobj else tempfile .TemporaryFile ()
	potrace_exe (tfbmp ,outsvg ,alphamax )
	tfbmp .close ()
def svgscale (svgfileobj ,scale =1.0 ):
	if scale ==1.0 :return
	svgfileobj .seek (0 )
	xml_data =etree .fromstring (svgfileobj .read ())
	width =float (xml_data .get ('width').rstrip ('pt'))
	height =float (xml_data .get ('height').rstrip ('pt'))
	xml_data .set ('width','{}pt'.format (width *scale ))
	xml_data .set ('height','{}pt'.format (height *scale ))
	svgfileobj .truncate (0 )
	svgfileobj .seek (0 )
	svgfileobj .write (etree .tostring (xml_data ))
def svg2png (svgfileobj ,pngfileobj =None ,scale =1.0 ,ret =False ):
	svgscale (svgfileobj ,scale )
	svgfileobj .seek (0 )
	if pngfileobj ==None :
		pngfileobj =tempfile .TemporaryFile ()
	cairosvg .svg2png (
	bytestring =svgfileobj .read (),
	write_to =pngfileobj ,
	dpi =72 )
	if ret :
		pngfileobj .seek (0 )
		im =Image .open (pngfileobj )
		im .load ()
		return im

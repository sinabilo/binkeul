import inspect
from enum import Enum ,IntEnum ,auto
__ofs__ =20
_KIND ={"표의문자":"A","표음문자":"B",
"숫자":"C","알파벳":"D","격조사":"E",
"후치사":"F","용언부호":"G","칸부호":"H",
"부호":"I","불합성자":"J"}
kind_dic ={m [1 ]:(i +1 )<<__ofs__ for i ,m in enumerate (_KIND .items ())}
_OPT ={
"좌항":"k","우항":"l","이항":"m","무항":"n",
"독립소":"p","의존소":"q",
"대문자":"r","소문자":"s","음절":"t",
"좌":"u","우":"v","한점":"w","두점":"x","무점":"y","칸막":"z"}
assert len (_OPT )<__ofs__
opt_dic ={m [1 ]:1 <<i for i ,m in enumerate (_OPT .items ())}
from functools import reduce
KodeKind ={}
for k ,vs in {
"표의문자":("독립소","의존소"),
"표음문자":("대문자","소문자","음절","독립소"),
"숫자":("독립소","의존소"),
"알파벳":("독립소","의존소"),
"격조사":("좌","우"),
"후치사":("좌","우"),
"용언부호":("독립소","의존소"),
"칸부호":("좌|한점","좌|두점","좌|무점","우|한점","우|두점","우|무점","칸막"),
"부호":("좌항","우항","이항","무항"),
"불합성자":("좌항","우항","이항","무항")
}.items ():
	for v in vs :
		vn =[_OPT [a ]for a in v .split ("|")]
		vm =[opt_dic [a ]for a in vn ]
		key =reduce (lambda a ,b :a |b ,vm )|kind_dic [_KIND [k ]]
		KodeKind [key ]=(_KIND [k ]+"".join (vn ),"|".join ([k ,v ]))
KindVal ={k :val for val ,(k ,_ )in KodeKind .items ()}

from ColorCraft.Print import * #import Everything and import print func
from ColorCraft import * #import Everything
try
	activeColor() #trun on the Colors
except NameError:
	init()
try:
	printColors
except NameError:
	printColors = printableColors

print("normal COLOR",color="normal") # 'normal' means no colors
normal = "normal"
for LOF in printColors:
	print("Hello, World",LOF,sep=": ",bg=None,color=LOF)
print("random Color:",repr(Color(type='random')),color=normal)
# dum="_" make random colors from the <Colors class> =:= Colors.random() ; default Color(type="random")
array = ColorArray(range(0,10),dum="_")
for color in array:
	print(repr(color))
	#print((color.__dict__),color=None),bg=Colors.random().color

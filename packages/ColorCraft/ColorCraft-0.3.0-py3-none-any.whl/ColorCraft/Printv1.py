from .Errors import *
from .Color  import Color
from .Color  import Colors
import sys

terminalColors = Colors.terminalColors
DefaultColor = "LOG"
def isinstances(object,*objects):
	if len(objects) == 0:
		raise TypeError("at last pass one object -:= for object")
	tnf = [] # true and false
	for obj in objects:
		tnf.append(isinstance(object,obj))
	return tnf

class Fruit(object):
	# Fruit trun class to sub
	def __init__(self, args):
		for k,v in args.items():
			if any(isinstances(v,str,int,list)):
				setattr(self, k, args[k])
	def __getitem__(self, item):
		return getattr(self, item)
	def __repr__(self):
		return f"<Fruit<{(self).__dict__}>>"


TerminalColors = Fruit(terminalColors.__dict__)
logs = {"LOG":terminalColors.OKGREEN,"LOGB":terminalColors.OKBLUE,"LOGC":terminalColors.OKCYAN,"NORMAL":None}
printColors   = ['FAIL', 'HEADER', 'OKBLUE', 'OKCYAN', 'OKGREEN', 'WARNING']
formated = {"negative": "\033[5m","bold": "\033[1m", "underline": "\033[4m"}

def getrgb(color):
	""" extrect color from the passed color :-: return (Color object, rgb color) """
	if isinstance(color,Color):
		color_rgb = Colors.hex2rgb(color.Hexcolor)
	elif isinstance(color,str):
		color = Color(color,type="hex")
		color_rgb = Colors.hex2rgb(color.Hexcolor)
	elif isinstance(color,tuple):
		color = Color(color,type="rgb")
		color_rgb = Colors.hex2rgb(color.Hexcolor)
	elif color is None:
		return None,None
	else:
		raise UnknownObject(f"Unown object expected str/Color() but got {color.__class__.__name__} instead")
	return (color , color_rgb)

class printer(object):
	def SubString(*args,start="",end="\n",sep=" "): #SS = SubString
		""" Substring the default print handler; substr return str : SubString("obj1","obj two",end="") == 'obj1 obj two'"""
		string = ""
		string+=str(start)
		if len(args) != 0:
			string += str(args[0])
			for obj in list(args[1::]):
				string += sep+str(obj)
		else:
			string += ""
		string+=str(end)
		return string
	def colorzieBG(r,g,b):
		""" color bg text return str : f"\\033[48;2;{r};{g};{b}m" """
		return f"\033[48;2;{r};{g};{b}m"
	def colorzieCO(r,g,b):
		""" color text return str : "\\033[38;2;{r};{g};{b}m" """
		return f"\033[38;2;{r};{g};{b}m"

	def colorzie(substring,bg=None,color=None):
		""" the default print handler;
		get substring, bg and a color and return (colorful str) :
		colorzie("Hello World",bg=None,color="000ff") == "\\033[38;2;0;0;255mHello World" \033[0m
	   \033[38;2;255;237;72m Warning the colorzie doesn't add ENDC by default; you must add ENDC(end color value) by youself ENDC = "\\033[0m" \033[0m""" 
		newsub = ""
		if not isinstance(substring,str):
			raise TypeError(f"unvaild substring {type(substring)}")
		if bg is not None:
			newsub += printer.colorzieBG(*bg)
		if color is not None:
			newsub += printer.colorzieCO(*color)
		newsub+=substring
		return newsub
	def upper(object):
		try:
			return object.upper()
		except AttributeError:
			return object
	def is_Color_object(color):
		if not isinstance(color,Color):
			if   color          is  None       : pass
			elif color          in  logs       : color = logs[color]
			elif color          in  printColors: color = TerminalColors[color]
		return color
	def format(formats,string):
		s = ""
		if isinstance(formats,str):
			if formats in formated:
				s+=formated[formats]
		else:
			for format in formats:
				if format in formated:
					s+=formated[format]
		return s+string

def print(*objs,start="",sep=" ",end="\n",file=sys.stdout,flush=False,bg=None,color=DefaultColor,formats=[]):
	"""
    print(*objs,start="",sep=" ",end="\\n",file=sys.stdout,flush=False,bg=None,color="LOG",,formats=[])

    Prints colors to the terminal, it writes into sys.stdout by default.
    Optional keyword arguments:
    file : a file-like object (stream); defaults to the current sys.stdout.
    sep  : string inserted between values, default a space.
    end  : string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
    color: the text color, by default 'OKGREEN'|'LOG'.
    bg   : the text background, by default None .
	"""
	color  = getrgb(printer.is_Color_object(printer.upper( color )))[1]
	bg     = getrgb(printer.is_Color_object(printer.upper(   bg  )))[1]
	string = printer.SubString(*objs,sep=sep,start=start,end="\033[0m"+str(end))
	output = printer.format(formats,printer.colorzie(string,bg=bg,color=color))
	file.write(output)
	if flush: file.flush()

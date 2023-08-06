from .Errors import *
from .Color  import Color
from .Color  import Colors
import sys


DefaultColor = "LOG"

class Fruit(object):
	# Fruit trun class to sub
	def __init__(self, args):
		copyed = vars(args).copy()
		for k,v in copyed.items():
			try:
				setattr(self, k, copyed[k])
			except (TypeError,AttributeError):
				pass
	def __getitem__(self, item):
		return getattr(self, item)
	def __iter__(self):
		return iter(vars(self).keys())
	def __repr__(self):
		return f"<Fruit<{vars(self)}>>"


#TerminalColors = Colors.terminalColors
TerminalColors = Fruit(Colors.terminalColors)
logs = {"LOG":TerminalColors.OKGREEN,"LOGB":TerminalColors.OKBLUE,"LOGC":TerminalColors.OKCYAN,"NORMAL":None}
printableColors   = ['FAIL', 'HEADER', 'OKBLUE', 'OKCYAN', 'OKGREEN', 'WARNING']
formated = {"negative": "\033[5m","negative2": "\033[3m","bold": "\033[1m", "underline": "\033[4m","italic": "\033[3m"}


class PrintHelper:
	def SubString(string="",*args,start="",end="\n",sep=" "): #SS = SubString
		""" Substring the default print handler; substr return str : SubString("obj1","obj two",end="") == 'obj1 obj two'"""
		string = str(string)
		string+=str(start)
		for obj in list(args):
			string += sep+str(obj)
		string+=str(end)
		return string

	def colorzie_text(text,color,end="\033[0m",is_bg=False):
		if color is None:
			return text
		if isinstance(color,str):
			if color.upper() in logs:
				if logs[color.upper()] is None:
					return text
				color = Color(logs[color.upper()])
			elif color.upper() in TerminalColors:
				color = Color(TerminalColors[color.upper()])
			else:
				raise KeyError(f"color key is not found {color}")
		if not isinstance(color,Color):
			raise TypeError(f"colorzie_text() color argument must be Color, not {color}")
		return color.colorize(str(text),end=end,is_bg=is_bg)
	
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
def print(*objs,start="",sep=" ",end="\033[0m\n",file=sys.stdout,flush=False,bg=None,color=DefaultColor,formats=[]):
	"""
    print(*objs,start="",sep=" ",end="\\033[0m\\n",file=sys.stdout,flush=False,bg=None,color="LOG",,formats=[])

    Prints colors to the terminal, it writes into sys.stdout by default.
    Optional keyword arguments:
    file : a file-like object (stream); defaults to the current sys.stdout.
    sep  : string inserted between values, default a space.
    end  : string appended after the last value, default a newline.
    flush: whether to forcibly flush the stream.
    color: the text color, by default 'OKGREEN'|'LOG'.
    bg   : the text background, by default None .
	"""
	output = PrintHelper.colorzie_text(
		PrintHelper.colorzie_text(
			PrintHelper.SubString(
				*objs,sep=str(sep),start=start,end=end),
			color=color,end=""),
		color=bg,is_bg=True)
	file.write(PrintHelper.format(formats,output))
	if flush: file.flush()

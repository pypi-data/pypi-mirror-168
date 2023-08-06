from .Color import *
from .Print import *
from .Errors import *
class TColor(object):
	""" Terminal Colors class Contain 'OKGREEN','WARNING','HEADER',etc and ENDC,BOLD,UNDERLINE; just simple name for Termainal Color Class"""
	HEADER = 'HEADER'
	OKBLUE = 'OKBLUE'
	OKCYAN = 'OKCYAN'
	OKGREEN = 'OKGREEN'
	WARNING = 'WARNING'
	FAIL = 'FAIL'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	LOGC = "LOGC"
	LOGB = "LOGB"
	LOG = "LOG"
	NORMAL = None

__all__ = ["Colors","Color","ColorArray","BasicColor","init","TerminalColors","logs","print","TColor","Blank"]
#print(f"\033[48;2;{r};{g};{b}m"+f"\033[38;2;{r};{g+100};{b}m{text}\033[0m")
__author__ = 'Alawi Hussein Adnan Al Sayegh'
__description__ = 'simplest and coolest color Library. print and menaged colors in Python!'
__license__ = """
Copyright 2022 "Alawi Hussein Adnan Al Sayegh"

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
and the names are copyrighted
"""
name = "ColorCraft"
names = {"Craft Color":"CraftColor","Crafter Color":"CrafterColor","Color Craft":"ColorCraft"}
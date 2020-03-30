from ctypes import *

def convert(s):
	i = int(s,16)
	cp = pointer(c_int(i))
	fp = cast(cp,POINTER(c_float))
	value = round(float(fp.contents.value),3)
	return value

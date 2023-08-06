
import os
from ctypes import *
lib1 = cdll.LoadLibrary(os.path.dirname(__file__) + '/lib/libgtknodes-0.1.so')

os.environ["GI_TYPELIB_PATH"] = os.path.dirname(__file__) + '/lib/girepository-1.0/'


print("pygtknodes!!")

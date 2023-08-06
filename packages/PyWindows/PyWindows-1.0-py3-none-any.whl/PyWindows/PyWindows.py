from ctypes import *
import ctypes
from ctypes.wintypes import *
import os

libPath = os.path.abspath(__file__).replace("PyWindows.py", "lib")

ctypes.windll.kernel32.SetDllDirectoryW(None)

cdll.LoadLibrary(f'{libPath}/SDL2.dll')
theDLL = cdll.LoadLibrary(f"{libPath}/C-Python-Window-Lib.dll")

class types:
    info = 0x00000040
    warning = 0x00000030
    question = 0x00000020
    error = 0x00000010

    openGL = 2
    vulkan = 268435456

class Window:
    def __init__(self, x: int, y: int, width: int, height: int, flag: int):
        theDLL.newWindow.argtypes = [c_int, c_int, c_int, c_int, c_int]
        theDLL.newWindow.restype = c_void_p

        theDLL.windowInit.argtypes = [c_void_p]
        theDLL.windowInit.restype = c_void_p

        theDLL.getRenderer.argtypes = [c_void_p]
        theDLL.getRenderer.restype = c_void_p

        theDLL.windowQuit.argtypes = [c_void_p]
        theDLL.windowQuit.restype = c_void_p

        theDLL.windowClear.argtypes = [c_void_p]
        theDLL.windowClear.restype = c_void_p

        theDLL.createRect.argtypes = [c_void_p]
        theDLL.createRect.restype = c_void_p

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.flag = flag

        self.obj = theDLL.newWindow(x, y, width, height, flag)

    def create(self):
        theDLL.windowInit(self.obj)

    def loop(self):
        return theDLL.windowLoop()

    def quit(self):
        theDLL.windowQuit(self.obj) 

    def clear(self):
        theDLL.windowClear(self.obj)     

    def createRect(self, x: int, y: int , width: int, height: int, r: int = 255, g: int = 255, b: int = 255, a: int = 255):
        theDLL.createRect(self.obj, x, y, width, height, r, g, b, a)          

    def getRenderer(self):
        return theDLL.getRenderer(self.obj)  
       

def createMessageBox(title: str, desc: str, icon: int): # The icon param can be used to add buttons
    msgBox = theDLL.createMessageBox(title, desc, icon)
    return msgBox # Returns 1 for Ok and 2 for cancel        
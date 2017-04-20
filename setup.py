__author__ = 'gustavosmc'

from distutils.core import setup
import py2exe

setup(windows=[{'script' :'gui/view.py'}],
      options={"py2exe":{'includes' : ["tkinter","pyautogui", "netifaces","qrcode"],
               "packages":["controll", "gui", "connection"]}}
                         
            )


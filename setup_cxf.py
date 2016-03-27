__author__ = 'gustavosmc'

from cx_Freeze import setup, Executable
import sys

base = None
if sys.platform == "win32":
    base = "Win32GUI"


executable = Executable(
    "gui/view.py",
    icon="icon.png",
    base=base    
    )

setup(
    name='SMC-PC',
    version="1.0.0",
    executables = [executable]
)

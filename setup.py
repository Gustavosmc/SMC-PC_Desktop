__author__ = 'gustavosmc'

from cx_Freeze import setup, Executable

executable = Executable(
    "gui/view.py",
    icon="icon.png",
    )

setup(
    name='SMC-PC',
    version="1.0",
    executables = [executable],
    packages=['img'],
    package_data={'img': ['*']},
    include_package_data = True
)

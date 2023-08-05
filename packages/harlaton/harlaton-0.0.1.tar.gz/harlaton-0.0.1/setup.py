from tkinter import W
from setuptools import setup 
setup(
    name='harlaton',
    version = '0.0.1',
    description='Say Hello!',
    pymodules=["helloworld"],
    package_dir = {'': 'src'},
)

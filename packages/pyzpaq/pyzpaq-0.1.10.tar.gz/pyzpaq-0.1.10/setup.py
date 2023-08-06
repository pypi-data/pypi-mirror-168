import sys
import platform

from setuptools import setup, Extension

ss = ['pyzpaq.cpp', 'zpaq/libzpaq.cpp']
if 'sdist' in sys.argv:
    ss += ['zpaq/libzpaq.h']

defines = []
if sys.platform.startswith('darwin'):
    defines += [('unix', '1'), ('BSD', 1)]

if platform.machine() not in ['i386', 'x86_64']:
    defines += [('NOJIT', 1)]

zpaq = Extension('zpaq',
                 define_macros=[('unix', '1'), ('BSD', 1), ('NOJIT', 1)] if sys.platform.startswith("darwin") else [],
                 sources=ss,
                 libraries=['advapi32'] if sys.platform.startswith("win") else [])

setup(name='pyzpaq',
      version='0.1.10',
      description='Python zpaq bindings',
      url='https://github.com/CPB9/pyzpaq.git',
      ext_modules=[zpaq])

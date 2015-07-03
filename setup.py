'''
Copyright (c) Pysapp 2015  - Alberto Lorenzo (alorenzo.md@gmail.com)

Distributed under the MIT License.
(See accompanying file "copying" or copy at
http://opensource.org/licenses/MIT)
'''

from distutils.core import setup, Extension
from distutils.command.build import build
from distutils.command.build_ext import build_ext
import os

import numpy

version = '0.8.2'
base_name = 'pysapp'
include_path = './include'

copt = {'msvc': ['/openmp', '/Ox'],
        'mingw32': ['-fopenmp', '-O3'],
        'mingw64': ['-fopenmp', '-O3'],
        'cygwin': ['-fopenmp', '-O3'],
        'unix': ['-fopenmp', '-O3']}
lopt = {'mingw32': ['-lgomp'],
        'mingw64': ['-lgomp'],
        'cygwin': ['-lgomp'],
        'unix': ['-lgomp']}


class build_subclass(build):
    sub_commands = [
        ('build_ext', build.has_ext_modules), 
        ('build_py', build.has_pure_modules),
        ('build_clib', build.has_c_libraries), 
        ('build_scripts', build.has_scripts),
    ]


class build_ext_subclass(build_ext):

    def build_extensions(self):
        c = self.compiler.compiler_type
        if c in copt:
            for e in self.extensions:
                e.extra_compile_args = copt[c]
        if c in lopt:
            for e in self.extensions:
                e.extra_link_args = lopt[c]
        build_ext.build_extensions(self)

ext_name = 'isacpp'
ext_folder = os.path.join(base_name, ext_name)
extension = Extension(base_name + '.' + ext_name + '._' + ext_name,
                      language='c++',
                      sources=[os.path.join(ext_folder, ext_name + '.i'),
                               os.path.join(ext_folder, ext_name + '.cpp'),
                               os.path.join(ext_folder, 'cstmath.cpp')],
                      swig_opts=['-c++', '-py3', '-I' + include_path],
                      include_dirs=[numpy.get_include()],)

setup(name=base_name,
      version=version,
      author='Alberto Lorenzo',
      description='ISA Model computed in C++',
      ext_modules=[extension],
      cmdclass={'build': build_subclass,
                'build_ext': build_ext_subclass},
      packages=[base_name, base_name + '.' + ext_name],)

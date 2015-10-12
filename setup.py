'''
Copyright (c) Pyaisa 2015  - Alberto Lorenzo (alorenzo.md@gmail.com)

Distributed under the MIT License.
(See accompanying file "copying" or copy at
http://opensource.org/licenses/MIT)
'''

from distutils.core import setup, Extension
from distutils.command.build import build
from distutils.command.build_ext import build_ext

import os
import re
import requests

import numpy

version = '0.8.5'
base_name = 'pyaisa'

# Compiler flags
copt = {'mingw32': ['-fopenmp', '-O3'],
        'mingw64': ['-fopenmp', '-O3'],
        'cygwin': ['-fopenmp', '-O3'],
        'msvc': ['/openmp', '/Ox'],
        'unix': ['-fopenmp', '-O3']}
lopt = {'mingw32': ['-lgomp'],
        'mingw64': ['-lgomp'],
        'cygwin': ['-lgomp'],
        'unix': ['-lgomp']}

# Parallel computing disabled on CI builds
auto_build_ids = ['BINSTAR_BUILD', 'TRAVIS_BUILD_ID', 'APPVEYOR_BUILD_ID']
build_ids = {}
for build_id in auto_build_ids:
    build_ids[build_id] = False
    if build_id in os.environ:
        if os.environ[build_id] != '<UNDEFINED>':
            build_ids[build_id] = True
if any(build_ids.values()):
    copt = {}
    lopt = {}
    filedata = None
    with open('pyaisa/isa.py', 'r') as file:
        filedata = file.read()
    filedata = filedata.replace('__default_parallel = get_opt_parallel()',
                                '__default_parallel = -1')
    with open('pyaisa/isa.py', 'w') as file:
        file.write(filedata)

# Download numpy.i file
np_version = re.compile(r'(?P<MAJOR>[0-9]+)\.'
                        '(?P<MINOR>[0-9]+)') \
                        .search(numpy.__version__)
np_version_string = np_version.group()
np_version_info = {key: int(value)
                   for key, value in np_version.groupdict().items()}

np_file_name = 'numpy.i'
np_file_url = 'https://raw.githubusercontent.com/numpy/numpy/maintenance/' + \
              np_version_string + '.x/tools/swig/' + np_file_name
if(np_version_info['MAJOR'] == 1 and np_version_info['MINOR'] < 9):
    np_file_url = np_file_url.replace('tools', 'doc')

chunk_size = 8196
with open(np_file_name, 'wb') as file:
    for chunk in requests.get(np_file_url,
                              stream=True).iter_content(chunk_size):
        file.write(chunk)


# Build steps must be reordered to include python generated files in the
# final package
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

# Set up
ext_name = 'isacpp'
ext_folder = os.path.join(base_name, ext_name)
extension = Extension(base_name + '.' + ext_name + '._' + ext_name,
                      language='c++',
                      sources=[os.path.join(ext_folder, ext_name + '.i'),
                               os.path.join(ext_folder, ext_name + '.cpp'),
                               os.path.join(ext_folder, 'cstmath.cpp')],
                      swig_opts=['-c++', '-py3', '-I .'],
                      include_dirs=[numpy.get_include()],)

setup(name=base_name,
      version=version,
      author='Alberto Lorenzo',
      author_email='alorenzo.md@gmail.com',
      home_page='https://github.com/newlawrence/Pysapp',
      license='MIT',
      description='ISA Model computed in C++',
      ext_modules=[extension],
      cmdclass={'build': build_subclass,
                'build_ext': build_ext_subclass},
      packages=[base_name, base_name + '.' + ext_name,
                base_name + '.' + 'test'])

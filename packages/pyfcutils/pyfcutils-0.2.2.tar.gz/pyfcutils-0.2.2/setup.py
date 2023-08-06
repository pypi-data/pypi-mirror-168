from sys import platform

import numpy
from setuptools import setup
from setuptools.extension import Extension

try:
    from Cython.Build import cythonize
except ImportError:
    print('Cython not available, compiling C++ sources')
    USE_CYTHON = False
else:
    print('Cython available, compiling .pyx sources')
    USE_CYTHON = True

fcio_libs = 'src/libs'

if platform.startswith('freebsd') or platform.startswith('linux'):
    extra_objects = [f'{fcio_libs}/fcio_linux.a', f'{fcio_libs}/tmio-0.93_linux.a']
elif platform.startswith('darwin'):
    extra_objects = [f'{fcio_libs}/fcio_mac.a', f'{fcio_libs}/tmio-0.93_mac.a']
elif platform.startswith('win32'):
    raise Exception('Windows not supported!')

ext = '.pyx' if USE_CYTHON else '.cpp'

extensions = [
    Extension(
        'fcutils',
        sources=['src/fcutils/fcutils' + ext],
        include_dirs=[fcio_libs, 'src/fcutils', numpy.get_include()],
        extra_objects=extra_objects,
    )
]

if USE_CYTHON:
    extensions = cythonize(extensions, language_level=3)

setup(ext_modules=extensions)

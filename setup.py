import sys

import distutils.sysconfig
from setuptools import setup, find_packages
from setuptools.extension import Extension


# Cython extension.
source_files = [
    "jpeg_ls/_CharLS.pyx",
    "jpeg_ls/CharLS_src/interface.cpp",
    "jpeg_ls/CharLS_src/jpegls.cpp",
    "jpeg_ls/CharLS_src/header.cpp",
]

include_dirs = ["jpeg_ls/CharLS_src", distutils.sysconfig.get_python_inc()]

# Platform-specific arguments
if sys.platform == "win32":
    extra_compile_args = []  # ['/EHsc']
    extra_link_args = []
elif sys.platform == "darwin":
    extra_compile_args = []
    extra_link_args = []
else:
    extra_compile_args = []
    extra_link_args = []

# These next two lines are left over from when I was playing with MinGW64 on my Windows PC.
# extra_compile_args = ['-m64'] #, '-nostdlib', '-lgcc']
# extra_link_args = ['-m64'] #, '-nostdlib', '-lgcc']


# https://luminousmen.com/post/resolve-cython-and-numpy-dependencies
# https://stackoverflow.com/questions/54117786/add-numpy-get-include-argument-to-setuptools-without-preinstalled-numpy
def create_build_ext(*args, **kwargs):
    # Delay imports until setup requirements can be processed
    # from setuptools.command.build_ext import build_ext
    from Cython.Distutils import build_ext

    class cython_numpy_build_ext(build_ext):
        def finalize_options(self):
            super().finalize_options()
            # Prevent numpy from thinking it is still in its setup process:
            __builtins__.__NUMPY_SETUP__ = False
            import numpy as np

            self.include_dirs.append(np.get_include())

    return cython_numpy_build_ext(*args, **kwargs)


# Do it.
version = "1.0.3"

setup(
    name="CharPyLS",
    packages=find_packages(),
    package_data={"": ["*.txt", "*.cpp", "*.h", "*.pyx"]},
    cmdclass={"build_ext": create_build_ext},
    ext_modules=[
        Extension(
            "_CharLS",
            source_files,
            language="c++",
            include_dirs=include_dirs,
            extra_compile_args=extra_compile_args,
            extra_link_args=extra_link_args,
        )
    ],
    setup_requires=["setuptools>=18.0", "cython", "numpy"],

    # Metadata
    version=version,
    license="MIT",
    author="Pierre V. Villeneuve",
    author_email="pierre.villeneuve@gmail.com",
    description="JPEG-LS for Python via CharLS C++ Library",
    url="https://github.com/Who8MyLunch/CharPyLS",
)

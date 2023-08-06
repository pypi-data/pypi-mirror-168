

import sys
from pybind11 import get_cmake_dir
# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import setup
long_desc = open("README.md").read()

__version__ = "0.0.4"

cp = Pybind11Extension("CheatPy",
    ["Cheat.cpp"],
    define_macros = [('VERSION_INFO', __version__)],
    extra_compile_args=['-O2','/D','NDEBUG'],
    include_dirs = []
)


ext_modules = [
    cp,
]

setup(
    name="CheatPy",
    version=__version__,
    author="Maury Dev",
    author_email="maurygta2@gmail.com",
    url="https://github.com/",
    description="Cheat.Py",
    long_description=long_desc,
    long_description_content_type= "text/markdown",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
    install_requires=['pybind11>=1.7'],
    python_requires=">=3.6",
    package_data={"CheatPy": ["py.typed", "__init__.pyi"]},
    packages=["CheatPy"]
)

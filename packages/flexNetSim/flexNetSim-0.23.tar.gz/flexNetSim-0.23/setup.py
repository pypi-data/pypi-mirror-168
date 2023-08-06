import pathlib
from setuptools import find_packages, setup
from distutils.core import setup, Extension
from Cython.Build import cythonize

SETUP_REQUIRES = ["setuptools", "wheel", "Cython"]

INSTALL_REQUIRES = [
    'numpy',
    'enum34'
]

setup(name='flexNetSim',
      version='0.23',
      license='MIT',
      description='Python Package of Event-Oriented Simulation for Flexible Grid Optical Networks',
      author='Gonzalo España, Danilo Bórquez-Paredes',
      author_email='danilo.borquez.p@uai.cl',
      url='https://gitlab.com/DaniloBorquez/flex-net-sim-python/',
      packages=['flexnetsim'],
      install_requires=INSTALL_REQUIRES,
      include_package_data=True,
      zip_safe=False,  # to prevent Cython fail: Note also that if you use setuptools instead of distutils, the default action when running python setup.py install is to create a zipped egg file which will not work with cimport for pxd files when you try to use them from a dependent package
      ext_modules=cythonize([
          Extension(
                    name="flexnetsim.random.pyunivariable",
                    sources=["flexnetsim/random/pyunivariable.pyx"
                             ],
                    include_dirs=["flexnetsim/random"],
                    language="c++"),
          Extension(
                    name="flexnetsim.random.pyexpvariable",
                    sources=["flexnetsim/random/pyexpvariable.pyx"
                             ],
                    include_dirs=["flexnetsim/random"],
                    language="c++")
      ],
          compiler_directives={'language_level': "3"},
      ),
    #   package_data={"flexnetsim/random": ["*.hpp"]},
      )

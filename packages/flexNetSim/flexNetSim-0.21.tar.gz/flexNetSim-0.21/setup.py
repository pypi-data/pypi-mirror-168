import pathlib
from setuptools import find_packages, setup
from distutils.core import setup, Extension
from Cython.Build import cythonize
from distutils.command.build import build as build_orig

SETUP_REQUIRE = ["setuptools", "wheel", "cython"]

INSTALL_REQUIRES = [
    'numpy',
    'enum34'
]



class build(build_orig):

    def finalize_options(self):
        super().finalize_options()
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        for extension in self.distribution.ext_modules:
            extension.include_dirs.append(numpy.get_include())
        self.distribution.ext_modules = cythonize(self.distribution.ext_modules,
                                                  language_level=3)

setup(name='flexNetSim',
      version='0.21',
      license='MIT',
      description='Python Package of Event-Oriented Simulation for Flexible Grid Optical Networks',
      author='Gonzalo España, Danilo Bórquez-Paredes',
      author_email='danilo.borquez.p@uai.cl',
      url='https://gitlab.com/DaniloBorquez/flex-net-sim-python/',
    #   packages=['flexnetsim'],
      packages=find_packages(),
      
      setup_requires= SETUP_REQUIRE,
      install_requires=INSTALL_REQUIRES,
      include_package_data=True,
      
      zip_safe=False,
      
      package_data={"flexNetSim.random": ["exp_variable.hpp", "pyexpvariable.pyx","uniform_variable.hpp", "pyunivariable.pyx"]}, 
      cmdclass={"build": build}, 
      # to prevent Cython fail: Note also that if you use setuptools instead of distutils, the default action when running python setup.py install is to create a zipped egg file which will not work with cimport for pxd files when you try to use them from a dependent package
      ext_modules=cythonize([
          Extension("flexnetsim.random.pyunivariable",
                    sources=["flexnetsim/random/pyunivariable.pyx"],
                    # include_dirs=["flexnetsim"],
                    language="c++"),
          Extension("flexnetsim.random.pyexpvariable",
                    sources=["flexnetsim/random/pyexpvariable.pyx"],
                    # include_dirs=["flexnetsim"],
                    language="c++")
      ],
          compiler_directives={'language_level': "3"},
      )
      
      )

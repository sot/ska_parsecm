from setuptools import setup

from Ska.ParseCM import __version__

setup(name='Ska.ParseCM',
      author = 'CXC Aspect',
      description='Parse MP command management files',
      maintainer_email = 'aldcroft@head.cfa.harvard.edu',
      py_modules = ['Ska.ParseCM'],
      version=__version__,
      test_suite='test',
      zip_safe=False,
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )

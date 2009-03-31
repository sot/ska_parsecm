from setuptools import setup
setup(name='Ska.ParseCM',
      author = 'CXC Aspect',
      description='Parse MP command management files',
      maintainer_email = 'aldcroft@head.cfa.harvard.edu',
      py_modules = ['Ska.ParseCM'],
      version='0.03',
      test_suite='test',
      zip_safe=False,
      namespace_packages=['Ska'],
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )

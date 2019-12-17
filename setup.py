from setuptools import setup

setup(name='Ska.ParseCM',
      author = 'CXC Aspect',
      description='Parse MP command management files',
      maintainer_email = 'aldcroft@head.cfa.harvard.edu',
      py_modules = ['Ska.ParseCM'],
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      test_suite='test',
      zip_safe=False,
      packages=['Ska'],
      package_dir={'Ska' : 'Ska'},
      package_data={}
      )

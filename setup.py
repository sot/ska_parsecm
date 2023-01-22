from setuptools import setup
from ska_helpers.setup_helper import duplicate_package_info

name = "ska_parsecm"
namespace = "Ska.ParseCM"

packages = ["ska_parsecm"]
package_dir = {name: name}

duplicate_package_info(packages, name, namespace)
duplicate_package_info(package_dir, name, namespace)


setup(name=name,
      author = 'CXC Aspect',
      description='Parse MP command management files',
      maintainer_email = 'taldcroft@cfa.harvard.edu',
      use_scm_version=True,
      setup_requires=['setuptools_scm', 'setuptools_scm_git_archive'],
      test_suite='test',
      zip_safe=False,
      packages=packages,
      package_dir=package_dir,
      )

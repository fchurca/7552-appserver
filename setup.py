from pip.req import parse_requirements
from setuptools import setup, find_packages

requirements = parse_requirements('./requirements.txt', session=False)
requirements = [str(r.req) for r in requirements]

package_dir = {'', 'src'}

setup(name='appserver', 
      version='0.1', 
      packages=find_packages(),
      install_requires=requirements)
from pip.req import parse_requirements
from setuptools import setup, find_packages

requirements = parse_requirements('requirements.txt', session=False)
requirements = [str(r.req) for r in requirements]


setup(name='appserver', 
      version='0.1',
      package_dir = {'': 'src'}, 
      packages=find_packages('src'),
      data_files=[('', ['requirements.txt'])],
      install_requires=requirements)

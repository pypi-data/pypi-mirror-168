from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(name='torrs_hammers',
      version='0.2.2',
      description='useful tools',
      url='https://github.com/PyTorr/torrs_hammers/archive/refs/tags/v02.tar.gz',
      author='PyTorr',
      author_email='',
      license='MIT',
      packages=['torrs_hammers'],
      zip_safe=False,
      long_description=long_description,
      long_description_content_type='text/markdown'
      )

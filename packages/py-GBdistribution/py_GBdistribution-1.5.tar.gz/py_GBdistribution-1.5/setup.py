from setuptools import setup
from pathlib import Path

# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(name='py_GBdistribution',
      version='1.5',
      description='Gaussian and Binomial distributions package',
      packages=['py_GBdistribution'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)

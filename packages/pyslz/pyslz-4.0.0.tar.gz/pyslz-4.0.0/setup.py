from setuptools import setup, find_packages

VERSION = '4.0.0'
DESCRIPTION = 'Usefull functions'

setup(name="pyslz",
      version=VERSION,
      author="Eduardo Maia",
      author_email="<maia@pessoalize.com>",
      description=DESCRIPTION,
      long_description_content_type="text/markdown",
      packages=find_packages(),
      keywords=['pyslz'],
      classifiers=["Development Status :: 1 - Planning",
                   "Intended Audience :: Developers",
                   "Programming Language :: Python :: 3",
                   "Operating System :: Unix",
                   "Operating System :: MacOS :: MacOS X",
                   "Operating System :: Microsoft :: Windows"])

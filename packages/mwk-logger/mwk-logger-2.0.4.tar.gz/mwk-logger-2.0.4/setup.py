from setuptools import setup
from setuptools.config import read_configuration
from mwk_logger import __version__ as ver

conf_dict = read_configuration('setup.cfg')
setup(version=ver)

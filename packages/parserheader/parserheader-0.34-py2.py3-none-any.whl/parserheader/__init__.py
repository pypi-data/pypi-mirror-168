from .parserheader import *

from . import __version__ as version
if isinstance(version, float):
	__version__ 	= version
else:
	__version__ 	= version.version
__email__		= "licface@yahoo.com"
__author__		= "licface@yahoo.com"
'''
making it really easy to run cli with logging configured to debug
'''

try:
    from . import fomuser
except ImportError:
    import fomuser

import logging
LOGGER = logging.getLogger()
LOGGER.setLevel(logging.DEBUG)
hndlr = logging.StreamHandler()
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
hndlr.setFormatter(formatter)
LOGGER.addHandler(hndlr)

cli = fomuser.CLI()
cli.defineParser()

import logging

"""
TODO : make this class able to read the configuration files and be able to log into an debug.log file
? Use FileHandle() for this from logging module, during initialing of the class logMessage, read the config value and add or dont add the file handler for the created instance.
"""

class logMessage:

    def __init__(self, name):
        log_format = "%(asctime)s %(levelname)s:%(name)s:%(message)s (%(filename)s:%(lineno)d [pid %(process)d:tid %(thread)d])"
        logging.basicConfig(format=log_format, level=logging.DEBUG)
        self.logger = logging.getLogger(name)

logger = logMessage(__name__)
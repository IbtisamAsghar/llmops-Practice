# this file identifies logger as the module and we can use the method present in the logger

from .custom_logger import CustomLogger  # assuming your logger class is in custom_logger.py

# create a global logger object
GLOBAL_LOGGER = CustomLogger().get_logger()

import os
from configparser import ConfigParser


class AppProperties:
    """
        Utility class for reading application properties from a file
    """

    def __init__(self):
        """
           Initializes a config parser reading properties from file
        """
        self._parser = ConfigParser()
        self._parser.read(os.path.join(os.getcwd(), 'app.properties'))

    def get_work_directory(self):
        """
           returns the directory where data resides and
           figures are extracted
        """
        return self._parser.get('data_section', 'work.directory')

    def get_workers(self):
        """
           The number of worker processes that this server
           should keep alive for handling requests
        """
        return self._parser.get('service_section', 'workers')

    def get_timeout(self):
        """
           If a worker does not notify the master process in this
           number of seconds it is killed and a new worker is spawned
           to replace it.
        """
        return self._parser.get('service_section', 'timeout')

    def get_log_level(self):
        """
           The log-level
        """
        return self._parser.get('service_section', 'log.level')

    @property
    def parser(self):
        return self._parser

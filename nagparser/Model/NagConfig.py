import os
import types


class NagConfig(object):
    """Configuration class for NagParser.
    
    Stores configuration settings for parsing Nagios data files and controlling
    how status information is interpreted. This includes file paths, thresholds,
    API keys, and various behavioral options.
    
    Attributes:
        files (list): List of file paths to parse (status.dat and/or objects.cache)
        STALE_THRESHOLD (int): Number of seconds after which data is considered stale (default: 240)
        IGNORE_STALE_DATA (bool): If True, stale data won't affect status calculations (default: False)
        NAGIOS_CMD_FILE (str): Path to Nagios command file (default: '/var/lib/nagios3/rw/nagios.cmd')
        IMPORTANTSERVICEGROUPS (dict): Dictionary of important service groups
        DATETIME_FORMAT (str): Format string for datetime output (default: '%Y-%m-%d %H:%M:%S')
        REQUIRE_HARD_SERVICE_STATUS (bool): If True, only consider hard states for status (default: False)
        basicAPIKEYS (list): List of API keys for basic authentication
    
    Args:
        files (list): List of file paths to Nagios data files
    
    Raises:
        IOError: If any of the specified files don't exist
    
    Example:
        >>> config = NagConfig(files=['/var/lib/nagios3/objects.cache',
        ...                           '/var/lib/nagios3/status.dat'])
        >>> config.STALE_THRESHOLD = 300
        >>> config.APIKEYS = ['secret-key-123']
    """
    def __init__(self, files):
        self.STALE_THRESHOLD = 240
        self.IGNORE_STALE_DATA = False
        self.NAGIOS_CMD_FILE = '/var/lib/nagios3/rw/nagios.cmd'
        self.IMPORTANTSERVICEGROUPS = {}
        self.basicAPIKEYS = []
        self.DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        self.REQUIRE_HARD_SERVICE_STATUS = False

        allfilesexist = True
        for temp in files:
            if not os.path.exists(temp):
                allfilesexist = False

        if allfilesexist:
            self.files = files
        else:
            raise IOError('File(s) not found')

    def _get_basicapikeys(self):
        return self.basicAPIKEYS

    def _set_basicapikeys(self, apikeys):
        if type(apikeys) is not list:
            apikeys = [apikeys]
        self.basicAPIKEYS = apikeys

    APIKEYS = property(_get_basicapikeys, _set_basicapikeys)


    def getpermissions(self, apikey):
        """Check if an API key is valid and return permissions.
        
        Basic API key validation function. Can be overridden in subclasses to provide
        custom API key validation functionality. Currently returns a simple list with
        'access granted' for valid keys or an empty list for invalid keys.
        
        Args:
            apikey (str): The API key to validate
        
        Returns:
            list: List of permission strings. Returns ['access granted'] for valid keys,
                  empty list [] for invalid keys. Future versions may use more granular
                  permissions to restrict access to specific operations.
        
        Example:
            >>> config = NagConfig(files=['status.dat'])
            >>> config.APIKEYS = ['valid-key']
            >>> config.getpermissions('valid-key')
            ['access granted']
            >>> config.getpermissions('invalid-key')
            []
        """

        if apikey in self.basicAPIKEYS:
            return ['access granted']
        else:
            return []

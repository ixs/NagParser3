import time
import types
import json

from datetime import datetime

from .NagCommands import NagCommands
from .NagList import NagList
from .NagConfig import NagConfig


class Base(object):
    """Base class for all Nagios objects providing common functionality.
    
    This is the base class that Nag, Host, Service, and ServiceGroup inherit from.
    It provides common functionality for all Nagios objects including attribute
    access, output generation, status calculations, and command execution.
    
    This class should not be directly instantiated - use the specific subclasses
    (Nag, Host, Service, ServiceGroup) instead.
    
    Attributes:
        nag (Nag): Reference to the root Nag object containing all data
    
    Properties:
        commands (NagCommands): Command execution interface for this object
        attributes (list): List of (name, value) tuples for this object's attributes
    """
    def getnowtimestamp(self):
        """Get the current Unix timestamp.
        
        Returns:
            float: Current time as Unix timestamp
        """
        return time.time()

    def __init__(self, nag=None):
        if nag == None:
            self.nag = self
            self._nagcreated = datetime.now()
        else:
            self.nag = nag

    @property
    def commands(self):
        return NagCommands(self)

    @property
    def attributes(self):
        """Get all simple attributes of this object as a list of tuples.
        
        Returns only non-complex attributes (excludes lists, NagLists, NagConfig,
        tuples, and other Base objects). Useful for serialization and debugging.
        
        Returns:
            list: List of (attribute_name, value) tuples for simple attributes
        
        Example:
            >>> host = nag.hosts.first
            >>> for name, value in host.attributes:
            ...     print(f"{name}: {value}")
        """

        output = []
        for attr in self.__dict__:
            attrtype = type(self.__dict__[attr])
            if attrtype is not list and attrtype is not NagList and attrtype is not NagConfig \
                and attrtype is not tuple and not issubclass(attrtype, Base) and not attr == '_nagcreated':
                output.append((attr, self.__dict__[attr]))

        return output

    def getbad(self, objtype=None, items=None):
        """Get objects with non-OK status.
        
        Filters a collection of objects to return only those with a non-OK status.
        Can work with hosts, services, or any collection of Nagios objects.
        
        Args:
            objtype (type, optional): Type of objects to filter (e.g., Host, Service)
            items (list, optional): Specific list of items to filter. If not provided,
                                   uses objtype to determine which collection to filter.
        
        Returns:
            NagList: List of objects with non-OK status
        
        Raises:
            Exception: If neither objtype nor items is provided
        """
        if objtype is None and items is None:
            raise Exception("objtype or items must be passed")

        if items == None:
            items = getattr(self, self.classname(objtype) + 's')
        else:
            return NagList([x for x in items if x.status[0] != 'ok'])

    def getbadservices(self):
        """Get all services with non-OK status.
        
        Returns:
            NagList: List of Service objects with status other than 'ok'
        """
        return self.getbad(items=self.services)

    def classname(self, classname=None):
        """Get the lowercase class name of this object or another class.
        
        Args:
            classname (type, optional): Class to get the name of. If not provided,
                                       uses this object's class.
        
        Returns:
            str: Lowercase class name (e.g., 'host', 'service', 'nag')
        """
        if classname:
            classbase = classname
        else:
            classbase = self.__class__

        parts = str(classbase).split("'")[1].lower().split('.')
        return parts[len(parts) - 1]

    def genoutput(self, outputformat='json', items=None, finaloutput=True):
        """Generate output in the specified format (currently only JSON).
        
        Creates a serialized representation of this object and optionally its
        child objects. Useful for creating APIs or exporting data.
        
        Args:
            outputformat (str): Output format, currently only 'json' is supported
            items (list, optional): Specific items to include in output
            finaloutput (bool): If True, return JSON string; if False, return dict
        
        Returns:
            str or dict: JSON string if finaloutput=True, otherwise dict structure
        """
        outputformat = outputformat.lower()

        #Setup
        output = {}
        if outputformat == 'json':
            output['objtype'] = self.classname()
            output['attributes'] = {}
        else:
            return 'Invalid Output'

        #Attributes
        for attr in self.attributes:
            output['attributes'][attr[0]] = attr[1]

        order = ['host', 'service', 'servicegroup']
        if items is None:
            if order[0] == self.classname():
                items = getattr(self, order[1] + 's')
            else:
                try:
                    items = getattr(self, order[0] + 's')
                except Exception:
                    items = []

        for obj in items:
            temp = obj.genoutput(outputformat=outputformat, finaloutput=False)
            if outputformat == 'json':
                if obj.classname() + 's' not in list(output.keys()):
                    output[obj.classname() + 's'] = []
                output[obj.classname() + 's'].append(temp)

        if outputformat == 'json' and finaloutput:
            output = json.dumps(output)

        return output

    def getservice(self, service_description):
        """Get a service by its description name.
        
        Args:
            service_description (str): The service description to look for
        
        Returns:
            Service or None: The matching Service object, or None if not found
        """
        try:
            return getattr(self.services, service_description)
        except AttributeError:
            return None

    def gethost(self, host_name):
        """Get a host by its name.
        
        Args:
            host_name (str): The host name to look for
        
        Returns:
            Host or None: The matching Host object, or None if not found
        """
        try:
            return getattr(self.hosts, host_name)
        except AttributeError:
            return None

    def getservicegroup(self, servicegroup_name):
        """Get a service group by its name.
        
        Args:
            servicegroup_name (str): The service group name to look for
        
        Returns:
            ServiceGroup or None: The matching ServiceGroup object, or None if not found
        """
        try:
            return [x for x in self.nag.getservicegroups() if x.__dict__['servicegroup_name'] == servicegroup_name][0]
        except Exception:
            return None


def servicesstatus(services):
    """Calculate aggregated status across multiple services.
    
    This is a utility function that determines the overall status of a collection
    of services following Nagios priority rules: critical > warning > downtime > unknown > ok.
    
    Args:
        services (list): List of Service objects to aggregate status from
    
    Returns:
        tuple: (status_str, has_downtime_bool) where:
               - status_str is one of: 'critical', 'warning', 'downtime', 'unknown', 'ok', 'stale'
               - has_downtime_bool indicates if any service is in scheduled downtime
    
    Status Priority (highest to lowest):
        1. stale - Any service with stale data
        2. critical - Any non-downtime service in critical state
        3. warning - Any non-downtime service in warning state  
        4. downtime - All problem services are in scheduled downtime
        5. unknown - Any service in unknown state
        6. ok - All services are OK
    
    Example:
        >>> from nagparser.Model.Base import servicesstatus
        >>> status, in_downtime = servicesstatus(host.services)
        >>> print(f"Host status: {status}")
    """
    if services:
        hasdowntime = max([x.status[1] for x in services])
    else:
        hasdowntime = 0

    if len([x for x in services if x.status[0] == 'stale']):
        return 'unknown', hasdowntime

    if len([x for x in services if x.status[0] == 'critical' and x.status[1] is False]):
        return 'critical', hasdowntime

    elif len([x for x in services if x.status[0] == 'warning' and x.status[1] is False]):
        return 'warning', hasdowntime

    elif len([x for x in services if x.status[0] in ['ok', 'unknown'] and x.status[1] is True]):
        return 'downtime', hasdowntime

    elif len([x for x in services if x.status[0] == 'unknown']):
        return 'unknown', hasdowntime
    else:
        return 'ok', hasdowntime

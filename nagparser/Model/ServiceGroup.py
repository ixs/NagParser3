from .NagList import NagList
from .Base import Base, servicesstatus

from nagparser.Services.nicetime import getnicetimefromdatetime


class ServiceGroup(Base):
    """Represents a service group definition from Nagios objects.cache.
    
    A ServiceGroup is a logical grouping of services, typically used to organize
    related services for easier monitoring and reporting. Service groups can span
    multiple hosts and contain any number of services.
    
    Attributes:
        servicegroup_name (str): Unique identifier for this service group
        alias (str): Human-readable name for this service group
        members (str): Comma-separated list of host,service pairs
        nag (Nag): Reference to the parent Nag object
    
    Properties:
        name (str): Alias for the alias attribute
        services (NagList): All services in this group
        hosts (NagList): All hosts that have services in this group
        status (tuple): Aggregated status tuple (status_str, in_downtime_bool)
    
    Example:
        >>> for sg in nag.servicegroups:
        ...     status, in_downtime = sg.status
        ...     print(f"{sg.name}: {status} ({len(sg.services)} services)")
    """

    def __init__(self, nag):
        super(ServiceGroup, self).__init__(nag=nag)

        self._hostsandservices = None
        self.members = None
        self.alias = None

    def gethostsandservices(self):
        """Parse the members string to extract hosts and services.
        
        The members attribute is a comma-separated string of alternating host names
        and service descriptions. This method parses that string and returns the
        corresponding Host and Service objects. Results are cached for performance.
        
        Returns:
            tuple: (services_list, hosts_list) where both are lists of unique objects
        """
        def _gethostsandservices():
            tempservices = []
            temphosts = []
            if self.members is not None and self.members != '':
                members = self.members.split(',')
                for i in range(len(members)):
                    if i % 2 == 0:
                        host = self.nag.gethost(members[i])
                        if host is not None:
                            temphosts.append(host)
                            service = host.getservice(members[i + 1])
                            if service is not None:
                                tempservices.append(service)

            return (list(set(tempservices)), list(set(temphosts)))
        if self._hostsandservices == None:
            self._hostsandservices = _gethostsandservices()

        return self._hostsandservices

    @property
    def services(self):
        """Get all services in this service group.
        
        Returns:
            NagList: List of Service objects that belong to this group
        """
        return NagList(self.gethostsandservices()[0])

    @property
    def hosts(self):
        """Get all hosts that have services in this service group.
        
        Returns:
            NagList: List of unique Host objects with services in this group
        """
        return NagList(self.gethostsandservices()[1])

    @property
    def name(self):
        """Get the name of this service group.
        
        Returns:
            str: The alias attribute (human-readable name)
        """
        return self.alias

    def getstatus(self, *arg):
        return servicesstatus(self.services)
    status = property(getstatus)

    def laststatuschange(self, returntimesincenow=True):
        """Get the most recent status change time among services in this group.
        
        Args:
            returntimesincenow (bool): If True, return human-readable time difference.
                                      If False, return datetime object.
        
        Returns:
            str or datetime: Human-readable time string (e.g., "2h 30m") if 
                            returntimesincenow is True, otherwise datetime object.
        """
        lastchange = max(self.services, key=lambda x: x.laststatuschange(returntimesincenow=False)). \
                        laststatuschange(returntimesincenow=False)

        if returntimesincenow:
            return getnicetimefromdatetime(lastchange)
        else:
            return lastchange

from .Base import Base, servicesstatus
from .NagList import NagList

from nagparser.Services.nicetime import getnicetimefromdatetime


class Host(Base):
    """Represents a host definition from Nagios status.dat.
    
    A Host object contains information about a single monitored host and provides
    access to all services running on that host. It inherits from Base, which
    provides common functionality like status aggregation and command execution.
    
    Attributes:
        host_name (str): The unique name of this host
        nag (Nag): Reference to the parent Nag object
    
    Properties:
        services (NagList): All services associated with this host
        name (str): Alias for host_name
        status (tuple): Aggregated status tuple (status_str, in_downtime_bool)
    
    Example:
        >>> host = nag.hosts.first
        >>> print(f"Host: {host.name}")
        >>> for service in host.services:
        ...     print(f"  Service: {service.name}, Status: {service.status[0]}")
    """

    def __init__(self, nag):
        super(Host, self).__init__(nag=nag)
        self.host_name = ''

    @property
    def services(self):
        """Get all services associated with this host.
        
        Returns:
            NagList: List of Service objects running on this host
        """
        # pylint: disable=E1103
        return NagList([x for x in self.nag.services if x.host_name == self.host_name])

    @property
    def name(self):
        """Get the name of this host.
        
        Returns:
            str: The host_name attribute
        """
        return self.host_name

    def getstatus(self, *arg):
        return servicesstatus(self.services)
    status = property(getstatus)

    def laststatuschange(self, returntimesincenow=True):
        """Get the most recent status change time among this host's services.
        
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

from datetime import datetime

from .NagList import NagList
from .Base import Base, servicesstatus
from nagparser.Model import Host, ServiceGroup
from nagparser.Services.nicetime import getnicetimefromdatetime


class Nag(Base):
    """Top-level container object for all parsed Nagios data.
    
    The Nag object is the main entry point for accessing parsed Nagios data.
    It contains all hosts, services, and service groups parsed from the Nagios
    status.dat and objects.cache files. It inherits from Base, which provides
    common functionality shared across all Nagios objects.
    
    Attributes:
        hosts (NagList): List of Host objects parsed from the data files
        services (NagList): List of Service objects parsed from the data files
        servicegroups (NagList): List of ServiceGroup objects (read-only property)
        config (NagConfig): Configuration object used for parsing
        importantservicegroups: Dictionary of service groups marked as important
        last_command_check (int): Timestamp of the last command check
    
    Properties:
        generated (datetime): When the Nagios data was generated
        lastupdated (datetime): When the Nagios data was last updated
        status (tuple): Aggregated status across all service groups
        servicegroups (NagList): All service groups including synthetic groups
    
    Example:
        >>> from nagparser import parse, NagConfig
        >>> config = NagConfig(files=['objects.cache', 'status.dat'])
        >>> nag = parse(config)
        >>> print(f"Hosts: {len(nag.hosts)}, Services: {len(nag.services)}")
        >>> print(f"Data generated: {nag.generated}")
        >>> status, in_downtime = nag.status
        >>> print(f"Overall status: {status}")
    """

    def __init__(self, nag=None):
        super(Nag, self).__init__(nag=nag)

        self.__servicegroups = [None, None]
        self.hosts = None
        self.services = None
        self._servicegroups = []
        self.last_command_check = 0
        self.importantservicegroups = None

    name = ''

    @property
    def generated(self):
        """Get the datetime when this Nagios data was generated.
        
        Returns:
            datetime: The generation timestamp from the Nagios data file
        """
        return datetime.fromtimestamp(float(self.created))

    @property
    def lastupdated(self):
        """Get the datetime when Nagios last checked commands.
        
        Returns:
            datetime: The last command check timestamp from the Nagios data
        """
        return datetime.fromtimestamp(float(self.last_command_check))


    def getstatus(self, onlyimportant=False):
        return servicesstatus(self.getservicegroups(onlyimportant))
    status = property(getstatus)

    def getbadhosts(self):
        """Get all hosts with non-OK status.
        
        Returns:
            NagList: List of Host objects that have a non-OK status
        """
        return self.getbad(Host)

    def laststatuschange(self, returntimesincenow=True):
        """Get the most recent status change time across all services.
        
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

    def getservicegroups(self, onlyimportant=False):
        """Get service groups, optionally filtered to only important ones.
        
        This method returns service groups from the Nagios data. When onlyimportant
        is False, it also creates two synthetic service groups: 'noservicegroup' for
        services not in any group, and 'allservices' containing all services.
        Results are cached for performance.
        
        Args:
            onlyimportant (bool): If True, return only service groups marked as important
                                 in the configuration. If False, return all service groups
                                 plus synthetic groups for ungrouped and all services.
        
        Returns:
            NagList: List of ServiceGroup objects
        
        Example:
            >>> nag = parse(config)
            >>> all_groups = nag.getservicegroups(onlyimportant=False)
            >>> important_groups = nag.getservicegroups(onlyimportant=True)
        """

        def _getservicegroups(onlyimportant=onlyimportant):
            if onlyimportant:
                servicegroups = NagList([x for x in self._servicegroups if x.servicegroup_name in self.importantservicegroups])
            else:
                servicegroups = self._servicegroups

                # Build up a servicegroup instance that will have all services NOT in a servicegroup
                noservicegroup = ServiceGroup(self.nag)
                noservicegroup.alias = 'No Service Group'
                noservicegroup.nag = self.nag
                noservicegroup.servicegroup_name = 'noservicegroup'
                noservicegroup.members = ''

                servicesinservicegroup = []
                for servicegroup in self._servicegroups:
                    servicesinservicegroup.extend(servicegroup.services)

                for services in list(set(self.services) - set(servicesinservicegroup)):
                    noservicegroup.members = noservicegroup.members + services.host.host_name + ',' + services.name + ','

                noservicegroup.members = noservicegroup.members.strip(',')
                servicegroups.append(noservicegroup)

                # Build "allservices" sudo servicegroup
                allservicesservicegroup = ServiceGroup(self.nag)
                allservicesservicegroup.alias = 'All Services'
                allservicesservicegroup.nag = self.nag
                allservicesservicegroup.servicegroup_name = 'allservices'
                allservicesservicegroup.members = ''

                for services in self.services:
                    allservicesservicegroup.members = allservicesservicegroup.members + services.host.host_name + ',' + services.name + ','

                allservicesservicegroup.members = allservicesservicegroup.members.strip(',')
                servicegroups.append(allservicesservicegroup)

                servicegroups = NagList(servicegroups)

            return servicegroups

        if onlyimportant and self.__servicegroups[0] is None:
            self.__servicegroups[0] = _getservicegroups(onlyimportant)
        elif not onlyimportant and self.__servicegroups[1] is None:
            self.__servicegroups[1] = _getservicegroups(onlyimportant)

        if onlyimportant:
            return self.__servicegroups[0]
        else:
            return self.__servicegroups[1]

    @property
    def servicegroups(self):
        """Get all service groups including synthetic groups.
        
        This is a convenience property that calls getservicegroups(onlyimportant=False).
        
        Returns:
            NagList: All service groups plus 'noservicegroup' and 'allservices' groups
        """
        return self.getservicegroups()

if __name__ == "__main__":
    pass

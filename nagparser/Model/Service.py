from .NagList import NagList
from .Base import Base

from nagparser.Services.nicetime import getnicetimefromdatetime

import time
from datetime import datetime


class Service(Base):
    """Represents a service definition from Nagios status.dat.
    
    A Service object contains detailed information about a monitored service,
    including its current state, check status, and scheduling information.
    Services are associated with a Host and can belong to multiple ServiceGroups.
    
    Attributes:
        host_name (str): Name of the host this service runs on
        service_description (str): Description of this service
        last_state_change (int): Timestamp of the last status change
        active_checks_enabled (int): Whether active checks are enabled (1/0)
        current_state (int): Current state code (0=OK, 1=WARNING, 2=CRITICAL, 3+=UNKNOWN)
        next_check (int): Timestamp of the next scheduled check
        scheduled_downtime_depth (int): Depth of scheduled downtime (>0 means in downtime)
        state_type (int): State type (0=SOFT, 1=HARD)
        nag (Nag): Reference to the parent Nag object
    
    Properties:
        host (Host): The Host object this service belongs to
        name (str): Alias for service_description
        status (tuple): Status tuple (status_str, in_downtime_bool) where status_str is one of: 'ok', 'warning', 'critical', 'unknown', 'stale'
        servicegroups (NagList): List of ServiceGroup objects this service belongs to
    
    Example:
        >>> service = nag.services.first
        >>> print(f"Service: {service.name} on {service.host.name}")
        >>> status, in_downtime = service.status
        >>> print(f"Status: {status}, In downtime: {in_downtime}")
    """

    def __init__(self, nag):
        super(Service, self).__init__(nag=nag)

        self.host_name = None
        self.last_state_change = None
        self.service_description = None
        self.active_checks_enabled = None
        self.current_state = None
        self.next_check = None
        self.scheduled_downtime_depth = None
        self.state_type = None

    @property
    def host(self):
        """Get the Host object this service runs on.
        
        Returns:
            Host: The Host object with matching host_name, or None if not found
        """
        # pylint: disable=E1103
        return NagList([x for x in self.nag.hosts if x.host_name == self.host_name]).first

    @property
    def name(self):
        """Get the name of this service.
        
        Returns:
            str: The service_description attribute
        """
        return self.service_description

    def getstatus(self, *arg):
        """Calculate the current status of this service.
        
        Determines the service status based on current_state, taking into account
        configuration options like STALE_THRESHOLD, REQUIRE_HARD_SERVICE_STATUS,
        and scheduled downtime.
        
        Returns:
            tuple: (status_str, in_downtime_bool) where:
                   - status_str is one of: 'ok', 'warning', 'critical', 'unknown', 'stale'
                   - in_downtime_bool is True if scheduled_downtime_depth > 0
        
        Note:
            - A service is 'stale' if it hasn't been checked recently (based on STALE_THRESHOLD)
            - Soft states are treated as 'ok' if REQUIRE_HARD_SERVICE_STATUS is True
            - State codes: 0=OK, 1=WARNING, 2=CRITICAL, >2=UNKNOWN
        """
        isdowntime = False
        if int(self.scheduled_downtime_depth) > 0:
            isdowntime = True
        # pylint: disable=E1103
        if ((time.time() - self.nag.config.STALE_THRESHOLD) > int(self.next_check) and
            self.active_checks_enabled == 1 and
            self.nag.config.IGNORE_STALE_DATA == False):
            return 'stale', isdowntime

        if self.nag.config.REQUIRE_HARD_SERVICE_STATUS and int(self.state_type) != 1:
            return 'ok', isdowntime
        if int(self.current_state) == 2:
            return 'critical', isdowntime
        elif int(self.current_state) == 1:
            return 'warning', isdowntime
        elif int(self.current_state) > 2 or int(self.current_state) < 0:
            return 'unknown', isdowntime
        else:
            return 'ok', isdowntime
    status = property(getstatus)

    def laststatuschange(self, returntimesincenow=True, timestamp=None):
        """Get the time of the last status change for this service.
        
        Args:
            returntimesincenow (bool): If True, return human-readable time difference.
                                      If False, return datetime object.
            timestamp (int, optional): Unix timestamp to use instead of last_state_change.
                                      Useful for calculating time from a specific point.
        
        Returns:
            str or datetime: Human-readable time string (e.g., "2h 30m") if 
                            returntimesincenow is True, otherwise datetime object.
        """
        if timestamp:
            lastchange = datetime.fromtimestamp(float(timestamp))
        else:
            lastchange = datetime.fromtimestamp(float(self.last_state_change))

        if returntimesincenow:
            return getnicetimefromdatetime(lastchange)
        else:
            return lastchange

    @property
    def servicegroups(self):
        """Get all service groups this service belongs to.
        
        Returns:
            NagList: List of ServiceGroup objects that contain this service
        """
        servicegroups = []
        # pylint: disable=E1103
        for servicegroup in self.nag.getservicegroups():
            if self in servicegroup.services:
                servicegroups.append(servicegroup)
        return NagList(servicegroups)

#!/usr/bin/env python

import re

from nagparser.Model.NagList import NagList
from nagparser.Model import Nag, Host, Service, ServiceGroup


def parse(config):
    """Parse Nagios status and cache files into a Nag object.
    
    This is the main entry point for NagParser. It reads Nagios runtime data from
    status.dat and objects.cache files and constructs a hierarchical object structure
    containing hosts, services, and service groups.
    
    Args:
        config (NagConfig): Configuration object containing file paths and options.
                           Must have a 'files' attribute with paths to status.dat
                           and/or objects.cache files.
    
    Returns:
        Nag: A Nag object containing all parsed hosts, services, and service groups.
             The returned object provides access to:
             - nag.hosts: NagList of Host objects
             - nag.services: NagList of Service objects
             - nag.servicegroups: NagList of ServiceGroup objects
    
    Raises:
        Exception: If an invalid filename is detected (must contain '.cache' or '.dat')
        IOError: If specified files don't exist (raised by NagConfig)
    
    Example:
        >>> from nagparser import parse, NagConfig
        >>> config = NagConfig(files=['/var/lib/nagios3/objects.cache',
        ...                           '/var/lib/nagios3/status.dat'])
        >>> nag = parse(config)
        >>> print(f"Found {len(nag.hosts)} hosts and {len(nag.services)} services")
    """
    tempobjs = []
    files = config.files
    importantservicegroups = config.IMPORTANTSERVICEGROUPS

    nag = None
    for filename in files:
        tempfile = open(filename)
        content = tempfile.read()
        tempfile.close()

        if nag == None:
            nag = Nag()
        if '.cache' in filename:
            sectionsnames = ['define servicegroup']
        elif '.dat' in filename:
            sectionsnames = ['hoststatus', 'servicestatus', 'programstatus', 'info']
        else:
            raise Exception('Invalid filename detected')

        for section in sectionsnames:
            pat = re.compile(section + r' \{([\S\s]*?)\t}', re.DOTALL)

            for sectioncontent in pat.findall(content):
                if section == 'hoststatus':
                    temp = Host(nag)
                elif section == 'servicestatus':
                    temp = Service(nag)
                elif section in ['programstatus', 'info']:
                    temp = nag
                elif section == 'define servicegroup':
                    temp = ServiceGroup(nag)

                for attr in sectioncontent.splitlines():
                    attr = attr.strip()
                    if len(attr) == 0 or attr.startswith('#'):
                        pass
                    else:
                        if section == 'define servicegroup':
                            delim = '\t'
                        else:
                            delim = '='

                        shortattr = attr.split(delim)[0].lower()
                        value = attr.replace(shortattr + delim, '')
                        try:
                            value = int(str(value))
                        except ValueError:
                            try:
                                value = float(str(value))
                            except ValueError:
                                pass

                        temp.__dict__[shortattr] = value
                tempobjs.append(temp)

    hosts = [x for x in tempobjs if isinstance(x, Host)]
    services = [x for x in tempobjs if isinstance(x, Service)]
    servicegroups = [x for x in tempobjs if isinstance(x, ServiceGroup)]

    nag.importantservicegroups = importantservicegroups
    nag.config = config

    if len(hosts):
        nag.hosts = NagList(hosts)
    if len(services):
        nag.services = NagList(services)
    if len(servicegroups):
        nag._servicegroups = NagList(servicegroups)

    return nag


if __name__ == "__main__":
    pass

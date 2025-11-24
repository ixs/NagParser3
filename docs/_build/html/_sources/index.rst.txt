.. NagParser documentation master file, created by
   sphinx-quickstart on Thu Dec 22 16:44:44 2011.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to NagParser's documentation!
=====================================

NagParser is a Python library for parsing Nagios runtime data from ``status.dat`` and 
``objects.cache`` files and presenting it as easy-to-use Python objects. It enables you to 
build custom monitoring dashboards, reporting tools, and automation scripts that integrate 
with your Nagios infrastructure.

Key Features
------------

* **Parse Nagios Runtime Data**: Read and interpret Nagios status data from status.dat files
* **Object-Oriented Interface**: Work with intuitive Python objects representing Hosts, Services, and ServiceGroups
* **Status Aggregation**: Automatically aggregate service statuses across hosts and service groups
* **Flexible Configuration**: Customize behavior with configuration options for stale data, hard states, and more
* **Time Utilities**: Built-in helpers for handling timestamps and human-readable time differences

Quick Start
-----------

Installation
^^^^^^^^^^^^

Install NagParser using pip::

    pip install NagParser

Basic Usage
^^^^^^^^^^^

Here's a simple example to get started:

.. code-block:: python

    from nagparser import parse, NagConfig
    
    # Configure file paths
    config = NagConfig(files=[
        '/var/lib/nagios3/objects.cache',
        '/var/lib/nagios3/status.dat'
    ])
    
    # Parse the files
    nag = parse(config)
    
    # Access hosts and services
    print(f"Total hosts: {len(nag.hosts)}")
    print(f"Total services: {len(nag.services)}")
    
    # Get the first host
    host = nag.hosts.first
    print(f"Host: {host.name}")
    print(f"Host status: {host.status}")
    
    # Iterate through services
    for service in host.services:
        status, in_downtime = service.status
        print(f"  Service: {service.name}, Status: {status}")

Working with Service Groups
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Service groups help organize related services:

.. code-block:: python

    from nagparser import parse, NagConfig
    
    config = NagConfig(files=[
        '/var/lib/nagios3/objects.cache',
        '/var/lib/nagios3/status.dat'
    ])
    nag = parse(config)
    
    # Get all service groups
    servicegroups = nag.getservicegroups(onlyimportant=False)
    
    for sg in servicegroups:
        status, in_downtime = sg.status
        print(f"{sg.name}: {status} ({len(sg.services)} services)")

Filtering Services by Status
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Find problematic services easily:

.. code-block:: python

    from nagparser import parse, NagConfig
    
    config = NagConfig(files=[
        '/var/lib/nagios3/objects.cache',
        '/var/lib/nagios3/status.dat'
    ])
    nag = parse(config)
    
    # Find all critical services
    critical_services = [s for s in nag.services 
                        if s.status[0] == 'critical']
    
    print(f"Critical services: {len(critical_services)}")
    for service in critical_services:
        print(f"  {service.host.name}: {service.name}")

Configuration Options
^^^^^^^^^^^^^^^^^^^^^

Customize NagParser behavior with configuration options:

.. code-block:: python

    from nagparser import NagConfig
    
    config = NagConfig(files=[
        '/var/lib/nagios3/objects.cache',
        '/var/lib/nagios3/status.dat'
    ])
    
    # Set stale data threshold (seconds)
    config.STALE_THRESHOLD = 300
    
    # Ignore stale data in status calculations
    config.IGNORE_STALE_DATA = True
    
    # Require hard service states (ignore soft states)
    config.REQUIRE_HARD_SERVICE_STATUS = True
    
    # Configure API keys for authentication
    config.APIKEYS = ['your-api-key']
    
    # Custom datetime format
    config.DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

Working with Timestamps
^^^^^^^^^^^^^^^^^^^^^^^

NagParser includes utilities for working with time data:

.. code-block:: python

    from nagparser import parse, NagConfig
    from nagparser import getnicetimefromdatetime
    from datetime import datetime, timedelta
    
    config = NagConfig(files=[
        '/var/lib/nagios3/objects.cache',
        '/var/lib/nagios3/status.dat'
    ])
    nag = parse(config)
    
    # Get human-readable time since generation
    print(f"Data generated: {nag.generated}")
    print(f"Last updated: {nag.lastupdated}")
    
    # Convert datetime to human-readable format
    some_time = datetime.now() - timedelta(hours=2, minutes=30)
    nice_time = getnicetimefromdatetime(some_time)
    print(f"Time ago: {nice_time}")  # Outputs: "2h 30m"

API Reference
-------------

Contents:

.. toctree::
   :maxdepth: 2

Main Classes
^^^^^^^^^^^^

.. automodule:: nagparser.Model.Nag
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: nagparser.Model.Host
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: nagparser.Model.Service
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: nagparser.Model.ServiceGroup
   :members:
   :undoc-members:
   :show-inheritance:

.. automodule:: nagparser.Model.NagList
   :members:
   :undoc-members:
   :show-inheritance:

Configuration
^^^^^^^^^^^^^

.. automodule:: nagparser.Model.NagConfig
   :members:
   :undoc-members:
   :show-inheritance:

Services and Utilities
^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: nagparser.Services.nagfactory
   :members:
   :undoc-members:

.. automodule:: nagparser.Services.nicetime
   :members:
   :undoc-members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


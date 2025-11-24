"""Unit tests for Host, Service, and ServiceGroup classes."""
import pytest
from nagparser.Model import Host, Service, ServiceGroup


class TestHost:
    """Test cases for Host class."""

    def test_host_has_services(self, test_nag):
        """Test that hosts have associated services."""
        if test_nag.hosts:
            host = test_nag.hosts.first
            assert hasattr(host, 'services')
            # Services should be a list-like object
            assert hasattr(host.services, '__iter__')

    def test_host_has_name(self, test_nag):
        """Test that hosts have a name property."""
        if test_nag.hosts:
            host = test_nag.hosts.first
            assert hasattr(host, 'name')
            assert host.name == host.host_name

    def test_host_has_status(self, test_nag):
        """Test that hosts have a status property."""
        if test_nag.hosts:
            host = test_nag.hosts.first
            assert hasattr(host, 'status')

    def test_can_create_host_object(self, test_nag):
        """Test that we can create a Host object."""
        host = Host(test_nag)
        assert isinstance(host, Host)
        assert host.host_name == ''


class TestService:
    """Test cases for Service class."""

    def test_service_has_host(self, test_nag):
        """Test that services have an associated host."""
        if test_nag.services:
            service = test_nag.services.first
            assert hasattr(service, 'host')
            if service.host:
                assert isinstance(service.host, Host)

    def test_service_has_name(self, test_nag):
        """Test that services have a name property."""
        if test_nag.services:
            service = test_nag.services.first
            assert hasattr(service, 'name')
            assert service.name == service.service_description

    def test_service_has_status(self, test_nag):
        """Test that services have a status property."""
        if test_nag.services:
            service = test_nag.services.first
            assert hasattr(service, 'status')
            status, isdowntime = service.status
            assert status in ['ok', 'warning', 'critical', 'unknown', 'stale']
            assert isinstance(isdowntime, bool)

    def test_service_has_servicegroups(self, test_nag):
        """Test that services have a servicegroups property."""
        if test_nag.services:
            service = test_nag.services.first
            assert hasattr(service, 'servicegroups')

    def test_can_create_service_object(self, test_nag):
        """Test that we can create a Service object."""
        service = Service(test_nag)
        assert isinstance(service, Service)
        assert service.host_name is None
        assert service.service_description is None


class TestServiceGroup:
    """Test cases for ServiceGroup class."""

    def test_servicegroup_has_services(self, test_nag):
        """Test that service groups have associated services."""
        servicegroups = test_nag.getservicegroups()
        if servicegroups:
            sg = servicegroups.first
            assert hasattr(sg, 'services')

    def test_servicegroup_has_name(self, test_nag):
        """Test that service groups have a name."""
        servicegroups = test_nag.getservicegroups()
        if servicegroups:
            sg = servicegroups.first
            assert hasattr(sg, 'servicegroup_name')

    def test_nag_has_servicegroups(self, test_nag):
        """Test that Nag object has service groups."""
        assert hasattr(test_nag, 'servicegroups')
        servicegroups = test_nag.servicegroups
        assert servicegroups is not None

    def test_can_create_servicegroup_object(self, test_nag):
        """Test that we can create a ServiceGroup object."""
        sg = ServiceGroup(test_nag)
        assert isinstance(sg, ServiceGroup)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

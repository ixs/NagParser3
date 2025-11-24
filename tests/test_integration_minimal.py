"""Integration tests using test data."""
import os
import pytest
from nagparser import parse, NagConfig
from nagparser.Model import Nag


class TestIntegration:
    """Integration tests using test data."""

    def test_parse_test_data(self, test_nag):
        """Test that test data can be parsed."""
        assert isinstance(test_nag, Nag)
        assert test_nag.hosts is not None
        assert test_nag.services is not None

    def test_has_hosts(self, test_nag):
        """Test that test data has hosts."""
        assert len(test_nag.hosts) > 0

    def test_has_services(self, test_nag):
        """Test that test data has services."""
        assert len(test_nag.services) > 0

    def test_host_has_name(self, test_nag):
        """Test the host has a name."""
        host = test_nag.hosts.first
        assert host.host_name is not None
        assert host.host_name != ''

    def test_host_has_services(self, test_nag):
        """Test that the host has services."""
        host = test_nag.hosts.first
        assert len(host.services) > 0

    def test_service_states(self, test_nag):
        """Test that services have valid states."""
        for service in test_nag.services:
            status, isdowntime = service.status
            assert status in ['ok', 'warning', 'critical', 'unknown', 'stale']
            assert isinstance(isdowntime, bool)

    def test_service_has_host_reference(self, test_nag):
        """Test that services have correct host reference."""
        service = test_nag.services.first
        assert service.host is not None
        assert service.host.host_name is not None

    def test_servicegroup_parsing(self, test_nag):
        """Test that service groups are parsed correctly."""
        servicegroups = test_nag.getservicegroups()
        assert servicegroups is not None
        # Should have 'noservicegroup' and 'allservices' at minimum
        assert len(servicegroups) >= 2

    def test_host_status_calculation(self, test_nag):
        """Test that host status is calculated from services."""
        host = test_nag.hosts.first
        status = host.status
        assert status is not None

    def test_nag_status_calculation(self, test_nag):
        """Test that overall Nag status is calculated."""
        status = test_nag.status
        assert status is not None

    def test_service_by_name_access(self, test_nag):
        """Test accessing services by name through NagList."""
        services = test_nag.services
        # Should have names property
        names = services.names
        assert len(names) > 0
        # Each name should be a string
        for name in names:
            assert isinstance(name, str)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

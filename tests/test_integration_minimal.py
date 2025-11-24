"""Integration tests using minimal synthetic test data."""
import os
import pytest
from nagparser import parse, NagConfig
from nagparser.Model import Nag


class TestIntegrationMinimal:
    """Integration tests using minimal synthetic test data."""

    def test_parse_minimal_data(self, minimal_nag):
        """Test that minimal data can be parsed."""
        assert isinstance(minimal_nag, Nag)
        assert minimal_nag.hosts is not None
        assert minimal_nag.services is not None

    def test_minimal_has_expected_host_count(self, minimal_nag):
        """Test that minimal data has 1 host."""
        assert len(minimal_nag.hosts) == 1

    def test_minimal_has_expected_service_count(self, minimal_nag):
        """Test that minimal data has 3 services."""
        assert len(minimal_nag.services) == 3

    def test_minimal_host_name(self, minimal_nag):
        """Test the host name from minimal data."""
        host = minimal_nag.hosts.first
        assert host.host_name == 'testhost1'

    def test_minimal_host_has_services(self, minimal_nag):
        """Test that the host has 3 services."""
        host = minimal_nag.hosts.first
        assert len(host.services) == 3

    def test_service_states_ok(self, minimal_nag):
        """Test that OK service has correct state."""
        service = minimal_nag.services.first
        if service.service_description == 'Test Service OK':
            status, _ = service.status
            assert status == 'ok'

    def test_service_states_warning(self, minimal_nag):
        """Test that WARNING service has correct state."""
        for service in minimal_nag.services:
            if service.service_description == 'Test Service WARNING':
                status, _ = service.status
                assert status == 'warning'
                break

    def test_service_states_critical(self, minimal_nag):
        """Test that CRITICAL service has correct state."""
        for service in minimal_nag.services:
            if service.service_description == 'Test Service CRITICAL':
                status, _ = service.status
                assert status == 'critical'
                break

    def test_service_has_host_reference(self, minimal_nag):
        """Test that services have correct host reference."""
        service = minimal_nag.services.first
        assert service.host is not None
        assert service.host.host_name == 'testhost1'

    def test_servicegroup_parsing(self, minimal_nag):
        """Test that service groups are parsed correctly."""
        servicegroups = minimal_nag.getservicegroups()
        assert servicegroups is not None
        # Should have the defined servicegroup plus 'noservicegroup' and 'allservices'
        assert len(servicegroups) >= 1

    def test_host_status_calculation(self, minimal_nag):
        """Test that host status is calculated from services."""
        host = minimal_nag.hosts.first
        status = host.status
        assert status is not None

    def test_nag_status_calculation(self, minimal_nag):
        """Test that overall Nag status is calculated."""
        status = minimal_nag.status
        assert status is not None

    def test_service_by_name_access(self, minimal_nag):
        """Test accessing services by name through NagList."""
        services = minimal_nag.services
        # Should have names property
        names = services.names
        assert 'Test Service OK' in names
        assert 'Test Service WARNING' in names
        assert 'Test Service CRITICAL' in names


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

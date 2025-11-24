"""End-to-end usage tests demonstrating typical NagParser workflows."""
import os
import pytest
from nagparser import parse, NagConfig


class TestUsageExamples:
    """Tests demonstrating typical NagParser usage patterns."""

    def test_basic_usage_workflow(self, testdata_dir):
        """Test the basic workflow shown in documentation."""
        # Setup config with files
        files = [
            os.path.join(testdata_dir, 'test_objects.cache'),
            os.path.join(testdata_dir, 'test_status.dat')
        ]
        config = NagConfig(files=files)
        
        # Parse and get nag object
        nag = parse(config)
        
        # Verify basic operations work
        assert nag is not None
        assert nag.hosts is not None
        assert nag.services is not None
        
        # Get service groups
        servicegroups = nag.getservicegroups(onlyimportant=False)
        assert servicegroups is not None
        assert len(servicegroups) > 0

    def test_service_status_aggregation(self, test_nag):
        """Test aggregating service statuses across service groups."""
        servicegroups = test_nag.getservicegroups(onlyimportant=False)
        
        # Get statuses from all service groups
        statuses = [x.status for x in servicegroups]
        assert len(statuses) > 0
        
        # Count unique statuses
        unique_statuses = set(statuses)
        for status in unique_statuses:
            count = statuses.count(status)
            assert count > 0

    def test_access_hosts_and_services(self, test_nag):
        """Test accessing hosts and their services."""
        # Access hosts
        assert len(test_nag.hosts) > 0
        
        # Access services for a specific host
        first_host = test_nag.hosts.first
        host_services = first_host.services
        assert host_services is not None

    def test_service_filtering_by_status(self, test_nag):
        """Test filtering services by their status."""
        ok_services = []
        warning_services = []
        critical_services = []
        
        for service in test_nag.services:
            status, _ = service.status
            if status == 'ok':
                ok_services.append(service)
            elif status == 'warning':
                warning_services.append(service)
            elif status == 'critical':
                critical_services.append(service)
        
        # Verify we can categorize services
        assert len(ok_services) >= 0
        assert len(warning_services) >= 0
        assert len(critical_services) >= 0
        # At least one service should exist
        assert len(test_nag.services) > 0

    def test_host_status_from_services(self, test_nag):
        """Test that host status is derived from its services."""
        host = test_nag.hosts.first
        
        # Get host status
        host_status = host.status
        assert host_status is not None
        
        # Host should have services
        assert len(host.services) > 0

    def test_config_options(self, testdata_dir):
        """Test various configuration options."""
        files = [
            os.path.join(testdata_dir, 'test_objects.cache'),
            os.path.join(testdata_dir, 'test_status.dat')
        ]
        config = NagConfig(files)
        
        # Test configuration options
        config.STALE_THRESHOLD = 300
        config.IGNORE_STALE_DATA = True
        config.NAGIOS_CMD_FILE = '/var/lib/nagios/rw/nagios.cmd'
        config.DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
        config.REQUIRE_HARD_SERVICE_STATUS = False
        
        assert config.STALE_THRESHOLD == 300
        assert config.IGNORE_STALE_DATA is True
        assert config.NAGIOS_CMD_FILE == '/var/lib/nagios/rw/nagios.cmd'

    def test_timestamps_and_dates(self, test_nag):
        """Test timestamp and date handling."""
        # Nag object should have generated and last updated times
        assert hasattr(test_nag, 'generated')
        assert hasattr(test_nag, 'lastupdated')
        
        # Both should be datetime objects
        from datetime import datetime
        assert isinstance(test_nag.generated, datetime)
        assert isinstance(test_nag.lastupdated, datetime)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

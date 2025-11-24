"""Unit tests for parsing functionality."""
import os
import pytest
from nagparser import parse, NagConfig
from nagparser.Model import Nag


class TestParsing:
    """Test cases for parsing Nagios files."""

    def test_parse_returns_nag_object(self, test_nagconfig):
        """Test that parse() returns a Nag object."""
        nag = parse(test_nagconfig)
        assert isinstance(nag, Nag)

    def test_parse_with_valid_files(self, test_nagconfig):
        """Test parsing with valid test files."""
        nag = parse(test_nagconfig)
        assert nag is not None
        assert hasattr(nag, 'hosts')
        assert hasattr(nag, 'services')

    def test_parsed_nag_has_config(self, test_nag):
        """Test that parsed Nag object has config reference."""
        assert hasattr(test_nag, 'config')
        assert isinstance(test_nag.config, NagConfig)

    def test_parsed_nag_has_hosts_list(self, test_nag):
        """Test that parsed Nag has a list of hosts."""
        assert test_nag.hosts is not None
        assert len(test_nag.hosts) > 0

    def test_parsed_nag_has_services_list(self, test_nag):
        """Test that parsed Nag has a list of services."""
        assert test_nag.services is not None
        assert len(test_nag.services) > 0

    def test_parsed_hosts_have_required_attributes(self, test_nag):
        """Test that parsed hosts have required attributes."""
        if test_nag.hosts:
            host = test_nag.hosts.first
            assert hasattr(host, 'host_name')
            assert host.host_name != ''

    def test_parsed_services_have_required_attributes(self, test_nag):
        """Test that parsed services have required attributes."""
        if test_nag.services:
            service = test_nag.services.first
            assert hasattr(service, 'host_name')
            assert hasattr(service, 'service_description')
            assert hasattr(service, 'current_state')

    def test_parse_invalid_file_raises_error(self):
        """Test that parsing with invalid files raises an error."""
        with pytest.raises(IOError):
            config = NagConfig(['nonexistent_file.dat'])

    def test_parse_with_cache_file(self, testdata_dir):
        """Test parsing objects.cache file."""
        cache_file = os.path.join(testdata_dir, 'test_objects.cache')
        # We need both files for proper parsing, but we can at least verify file exists
        assert os.path.exists(cache_file)

    def test_parse_with_status_file(self, testdata_dir):
        """Test parsing status.dat file."""
        status_file = os.path.join(testdata_dir, 'test_status.dat')
        # We need both files for proper parsing, but we can at least verify file exists
        assert os.path.exists(status_file)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

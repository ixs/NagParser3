"""Tests for nagfactory parse function."""
import pytest
from nagparser.Model import Nag


class TestNagFactory:
    """Test cases for the nagfactory parse function."""

    def test_build_nag_instance_from_test_config(self, test_nag):
        """Test that parse returns a Nag instance."""
        assert isinstance(test_nag, Nag)

    def test_nag_has_hosts(self, test_nag):
        """Test that the parsed Nag object has hosts."""
        assert test_nag.hosts is not None
        assert len(test_nag.hosts) > 0

    def test_nag_has_services(self, test_nag):
        """Test that the parsed Nag object has services."""
        assert test_nag.services is not None
        assert len(test_nag.services) > 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

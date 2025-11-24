"""Tests for NagConfig class."""
import os
import pytest
from nagparser.Model.NagConfig import NagConfig


def fakegetpermissions():
    """Fake permissions function for testing."""
    return ['fakepermission']


class TestNagConfig:
    """Test cases for NagConfig."""

    def test_nagconfig_is_Config_instance(self, test_nagconfig):
        """Test that nagconfig is an instance of NagConfig."""
        assert isinstance(test_nagconfig, NagConfig)

    def test_fake_files_raise_exception(self):
        """Test that non-existent files raise IOError."""
        files = ['fakefile.cache', 'fakefile.dat']
        with pytest.raises(IOError):
            NagConfig(files)

    def test_can_set_and_get_basic_apikeys(self, test_nagconfig):
        """Test setting and getting API keys."""
        # Test that passing list works
        assert test_nagconfig.APIKEYS == ['abc123', '123abc']

        # Test that passing str will result in APIKEYS returning the str as single item list
        test_nagconfig.APIKEYS = 'abc123'
        assert test_nagconfig.APIKEYS == ['abc123']

    def test_can_use_default_getpermissions(self, test_nagconfig):
        """Test the default getpermissions method."""
        assert test_nagconfig.getpermissions('abc123') == ['access granted']
        assert test_nagconfig.getpermissions('fakekey') == []


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

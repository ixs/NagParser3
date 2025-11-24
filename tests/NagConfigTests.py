"""Tests for NagConfig class."""
import os
import pytest
from nagparser.Model.NagConfig import NagConfig


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


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

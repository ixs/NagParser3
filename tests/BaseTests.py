"""Base tests for Nag object."""
import os
import pickle
import pytest

from nagparser.Model.NagCommands import NagCommands


class TestNagBase:
    """Test cases for base Nag object functionality."""

    def test_commands_property_is_NagCommands_instance(self, test_nag):
        """Test that nag.commands is a NagCommands instance."""
        assert isinstance(test_nag.commands, NagCommands)

    def test_attributes_property_is_correct(self, test_nag, expectedresults_dir):
        """Test that nag.attributes matches expected results."""
        expected_file = os.path.join(expectedresults_dir, 'nag_attributes.pickle')
        with open(expected_file, 'rb') as f:
            expected = pickle.load(f)
            assert test_nag.attributes == expected

    def test_nag_has_generated_time(self, test_nag):
        """Test that nag has a generated timestamp."""
        assert hasattr(test_nag, 'generated')
        assert test_nag.generated is not None

    def test_nag_has_last_updated_time(self, test_nag):
        """Test that nag has a last updated timestamp."""
        assert hasattr(test_nag, 'lastupdated')
        assert test_nag.lastupdated is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

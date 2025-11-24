"""Unit tests for NagList class."""
import pytest
from nagparser.Model.NagList import NagList


class MockNagObject:
    """Mock object for testing NagList."""
    def __init__(self, name):
        self.name = name


class TestNagList:
    """Test cases for NagList."""

    def test_naglist_is_list_subclass(self):
        """Test that NagList is a subclass of list."""
        naglist = NagList()
        assert isinstance(naglist, list)

    def test_naglist_first_property_returns_first_item(self):
        """Test that .first returns the first item."""
        obj1 = MockNagObject("obj1")
        obj2 = MockNagObject("obj2")
        naglist = NagList([obj1, obj2])
        assert naglist.first == obj1

    def test_naglist_first_property_returns_none_when_empty(self):
        """Test that .first returns None when list is empty."""
        naglist = NagList()
        assert naglist.first is None

    def test_naglist_names_property(self):
        """Test that .names returns list of names."""
        obj1 = MockNagObject("obj1")
        obj2 = MockNagObject("obj2")
        naglist = NagList([obj1, obj2])
        assert naglist.names == ["obj1", "obj2"]

    def test_naglist_access_by_name(self):
        """Test that we can access items by name."""
        obj1 = MockNagObject("obj1")
        obj2 = MockNagObject("obj2")
        naglist = NagList([obj1, obj2])
        assert naglist.obj1 == obj1
        assert naglist.obj2 == obj2

    def test_naglist_raises_error_for_multiple_same_names(self):
        """Test that accessing multiple items with same name raises error."""
        obj1 = MockNagObject("same")
        obj2 = MockNagObject("same")
        naglist = NagList([obj1, obj2])
        with pytest.raises(AttributeError, match="Multiple instances found"):
            _ = naglist.same

    def test_naglist_raises_error_for_unknown_name(self):
        """Test that accessing unknown name raises error."""
        obj1 = MockNagObject("obj1")
        naglist = NagList([obj1])
        with pytest.raises(AttributeError):
            _ = naglist.unknown

    def test_naglist_standard_list_operations(self):
        """Test that standard list operations work."""
        obj1 = MockNagObject("obj1")
        obj2 = MockNagObject("obj2")
        naglist = NagList([obj1])
        
        # Test append
        naglist.append(obj2)
        assert len(naglist) == 2
        
        # Test iteration
        names = [obj.name for obj in naglist]
        assert names == ["obj1", "obj2"]
        
        # Test indexing
        assert naglist[0] == obj1
        assert naglist[1] == obj2


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

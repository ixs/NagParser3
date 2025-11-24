"""Pytest configuration and shared fixtures for NagParser tests."""
import os
import pytest
from nagparser import parse, NagConfig


@pytest.fixture
def testdata_dir():
    """Return the path to the test data directory."""
    return os.path.join(os.path.dirname(__file__), 'testdata')


@pytest.fixture
def test_nagconfig(testdata_dir):
    """Create a NagConfig instance with test data files."""
    files = [
        os.path.join(testdata_dir, 'test_objects.cache'),
        os.path.join(testdata_dir, 'test_status.dat')
    ]
    nagconfig = NagConfig(files)
    nagconfig.APIKEYS = ['abc123', '123abc']
    return nagconfig


@pytest.fixture
def test_nag(test_nagconfig):
    """Create a fully hydrated Nag object from test data."""
    return parse(test_nagconfig)


@pytest.fixture
def expectedresults_dir():
    """Return the path to the expected results directory."""
    return os.path.join(os.path.dirname(__file__), 'ExpectedResults')


@pytest.fixture
def minimal_testdata_dir():
    """Return the path to the minimal test data directory."""
    return os.path.join(os.path.dirname(__file__), 'testdata')


@pytest.fixture
def minimal_nagconfig(minimal_testdata_dir):
    """Create a NagConfig with minimal test data files."""
    files = [
        os.path.join(minimal_testdata_dir, 'minimal_objects.cache'),
        os.path.join(minimal_testdata_dir, 'minimal_status.dat')
    ]
    config = NagConfig(files)
    # Ignore stale data since we're using old timestamps in test data
    config.IGNORE_STALE_DATA = True
    return config


@pytest.fixture
def minimal_nag(minimal_nagconfig):
    """Create a Nag object from minimal test data."""
    return parse(minimal_nagconfig)

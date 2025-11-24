# NagParser Test Suite

This directory contains the comprehensive pytest test suite for NagParser.

## Python Version Support

NagParser supports Python 3.6+ with tests running on:
- Python 3.6
- Python 3.7
- Python 3.8
- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

Tests are automatically run via GitHub Actions on every commit and pull request.

## Running Tests

### Using pytest directly

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_models.py

# Run specific test class
pytest tests/test_models.py::TestHost

# Run specific test
pytest tests/test_models.py::TestHost::test_host_has_services
```

### Using tox

```bash
# Run tests through tox (recommended for CI/CD)
tox

# Run tests for specific Python version
tox -e py36  # Python 3.6
tox -e py312 # Python 3.12
```

## Test Organization

### Unit Tests
- **test_naglist.py**: Tests for the NagList class (8 tests)
- **test_models.py**: Tests for Host, Service, and ServiceGroup models (14 tests)
- **test_parsing.py**: Tests for parsing functionality (10 tests)
- **test_nicetime.py**: Tests for nicetime utility functions (10 tests)
- **NagConfigTests.py**: Tests for NagConfig class (4 tests)
- **nagfactoryTests.py**: Tests for factory functions (3 tests)
- **BaseTests.py**: Base tests for Nag object (4 tests)

### Integration Tests
- **test_integration_minimal.py**: Integration tests using test data (13 tests)
- **test_usage_examples.py**: End-to-end usage examples (8 tests)

### Test Data

#### Test Data Files
- **testdata/test_status.dat**: Full Nagios status file for comprehensive testing
- **testdata/test_objects.cache**: Full Nagios objects cache for comprehensive testing

#### Expected Results
- **ExpectedResults/nag_attributes.pickle**: Pickled expected results for validation

## Test Coverage

The test suite includes 71 tests covering:
- Configuration management
- File parsing (status.dat and objects.cache)
- Object model (Nag, Host, Service, ServiceGroup)
- Data structures (NagList)
- Utility functions (nicetime)
- Status calculations
- Service state detection (OK, WARNING, CRITICAL, UNKNOWN, STALE)
- Integration scenarios

## Fixtures

The test suite uses pytest fixtures defined in `conftest.py`:
- `testdata_dir`: Path to test data directory
- `test_nagconfig`: Pre-configured NagConfig instance
- `test_nag`: Fully hydrated Nag object from test data
- `expectedresults_dir`: Path to expected results directory
- `minimal_nagconfig`: NagConfig with minimal test data
- `minimal_nag`: Nag object from minimal test data

## Writing New Tests

When adding new tests:
1. Follow pytest naming conventions (test_*.py, test_*, Test*)
2. Use fixtures from conftest.py for common setup
3. Add docstrings to explain what each test verifies
4. Group related tests in classes
5. Add synthetic test data files if testing new scenarios

## Continuous Integration

The test suite is designed to run in CI/CD pipelines using tox or pytest directly.
All tests should pass before merging changes to the main branch.

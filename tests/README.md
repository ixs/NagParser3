# NagParser Test Suite

This directory contains the comprehensive pytest test suite for NagParser.

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
- **test_integration_minimal.py**: Integration tests using minimal synthetic test data (13 tests)

### Test Data

#### Original Test Data
- **testdata/test_status.dat**: Full Nagios status file for comprehensive testing
- **testdata/test_objects.cache**: Full Nagios objects cache for comprehensive testing

#### Synthetic Test Data
- **testdata/minimal_status.dat**: Minimal status file with OK, WARNING, and CRITICAL services
- **testdata/minimal_objects.cache**: Minimal objects cache with test host and service definitions

#### Expected Results
- **ExpectedResults/nag_attributes.pickle**: Pickled expected results for validation

## Test Coverage

The test suite includes 65 tests covering:
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

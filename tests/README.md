# Test Suite Documentation

This directory contains the comprehensive test suite for the Todo API project, organized using pytest and following best practices for testing Django applications.

## Test Structure

```
tests/
├── conftest.py                          # Pytest configuration and fixtures
├── factories.py                         # Factory Boy factories for test data
├── unit/                               # Unit tests
│   ├── repositories/                   # Repository layer unit tests
│   │   ├── test_user_repository.py
│   │   └── test_task_repository.py
│   └── services/                       # Service layer unit tests
│       ├── test_user_service.py
│       └── test_task_service.py
├── integration/                        # Integration tests
│   ├── services/                       # Service layer integration tests
│   │   ├── test_user_service_integration.py
│   │   └── test_task_service_integration.py
│   └── api/                           # API endpoint integration tests
│       ├── test_auth_endpoints.py
│       └── test_task_endpoints.py
└── README.md                          # This file
```

## Test Categories

### Unit Tests (`tests/unit/`)
- **Purpose**: Test individual components in isolation
- **Scope**: Repositories and Services
- **Mocking**: Heavy use of mocks to isolate components
- **Speed**: Fast execution
- **Markers**: `@pytest.mark.unit`

### Integration Tests (`tests/integration/`)
- **Purpose**: Test component interactions and real database operations
- **Scope**: Services with real database and API endpoints
- **Mocking**: Minimal mocking, real database operations
- **Speed**: Slower than unit tests
- **Markers**: `@pytest.mark.integration`

## Test Configuration

### Pytest Configuration (`pytest.ini`)
- Uses `src.todo_api.test_settings` for test-specific Django settings
- Configured for SQLite in-memory database for faster execution
- Includes markers for test categorization
- Disabled migrations for faster test execution

### Test Settings (`src/todo_api/test_settings.py`)
- SQLite in-memory database
- Disabled migrations
- MD5 password hashing for speed
- Disabled logging
- Shorter JWT token lifetime for tests

## Running Tests

### Basic Commands

```bash
# Run all tests
python -m pytest

# Run with verbose output
python -m pytest -v

# Run only unit tests
python -m pytest -m unit

# Run only integration tests
python -m pytest -m integration

# Run tests with coverage
python -m pytest --cov=src --cov-report=html

# Run specific test file
python -m pytest tests/unit/repositories/test_user_repository.py

# Run specific test method
python -m pytest tests/unit/repositories/test_user_repository.py::TestUserRepository::test_get_by_email
```

### Using the Test Runner Script

```bash
# Run all tests
python scripts/run_tests.py

# Run only unit tests
python scripts/run_tests.py --unit

# Run only integration tests
python scripts/run_tests.py --integration

# Run with coverage
python scripts/run_tests.py --coverage

# Run with verbose output
python scripts/run_tests.py --verbose

# Run specific pattern
python scripts/run_tests.py --pattern "test_user"

# Run in parallel
python scripts/run_tests.py --parallel 4
```

## Test Data Management

### Factory Boy
The project uses Factory Boy for generating test data:

```python
# User factory
user = UserFactory(email='test@example.com')

# Task factory
task = TaskFactory(user=user, detail='Test task')

# Custom attributes
user = UserFactory(email='custom@example.com', first_name='Custom')
```

### Fixtures (`conftest.py`)
Common fixtures available for all tests:

- `client`: Django test client
- `user`: User instance
- `authenticated_client`: Client with JWT authentication
- `other_user`: Different user for permission testing

## Test Coverage

The test suite aims for comprehensive coverage of:

### Repository Layer
- CRUD operations
- Query methods
- Error handling
- Edge cases

### Service Layer
- Business logic validation
- Error handling
- Response formatting
- Integration with repositories

### API Layer
- HTTP status codes
- Request/response validation
- Authentication/authorization
- Error responses

## Best Practices

### Unit Tests
- Mock external dependencies
- Test one thing at a time
- Use descriptive test names
- Keep tests fast and isolated

### Integration Tests
- Use real database operations
- Test complete workflows
- Verify data persistence
- Test authentication flows

### General
- Follow AAA pattern (Arrange, Act, Assert)
- Use meaningful assertions
- Clean up test data
- Keep tests independent

## Continuous Integration

The test suite is designed to run in CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Tests
  run: |
    pip install -r requirements.txt
    python -m pytest --cov=src --cov-report=xml

- name: Upload Coverage
  uses: codecov/codecov-action@v1
  with:
    file: ./coverage.xml
```

## Debugging Tests

### Common Issues
1. **Database not found**: Ensure test settings are used
2. **Import errors**: Check Python path and virtual environment
3. **Authentication failures**: Verify JWT token generation
4. **Data not persisting**: Check test database configuration

### Debug Commands
```bash
# Run with debug output
python -m pytest -v -s

# Run single test with debug
python -m pytest -v -s tests/unit/repositories/test_user_repository.py::TestUserRepository::test_get_by_email

# Check test discovery
python -m pytest --collect-only
```

## Performance Considerations

- Unit tests should run in < 1 second each
- Integration tests may take 1-5 seconds each
- Use `--parallel` for faster execution
- Consider test data size for performance
- Use `--reuse-db` to avoid database recreation

## Maintenance

- Update tests when adding new features
- Refactor tests when refactoring code
- Keep test data factories up to date
- Review and update test coverage regularly
- Remove obsolete tests

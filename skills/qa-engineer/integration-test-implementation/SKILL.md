---
name: integration-test-implementation
description: |
  Create integration tests that verify API endpoints, database interactions, service communication,
  and inter-component behavior using Pytest or Jest. Use when implementing integration tests,
  API endpoint tests, database integration tests, contract tests, authentication flow tests,
  or when testing components working together with real or near-real dependencies.
---

# Integration Test Implementation

## Overview

This skill enables building robust integration test suites that verify component interactions, API contracts, and data flow across system boundaries. Integration tests validate that multiple units work together correctly with real or near-real dependencies (databases, APIs, services).

## Core Capabilities

**1. API Testing**
- REST/GraphQL endpoint validation
- Request/response schema verification
- Authentication/authorization checks
- Error handling validation

**2. Database Testing**
- CRUD operations with real database
- Transaction handling and rollbacks
- Constraint violations
- Cascading operations

**3. Contract Testing**
- Consumer-driven contract tests (Pact)
- Service boundary validation
- API contract enforcement

**4. Test Environment Setup**
- Test database configuration
- Test data seeding
- Mock external services
- Setup/teardown utilities

## Workflow

Follow this process when implementing integration tests:

### 1. Identify Integration Points

Analyze the codebase to identify:
- API endpoints (REST, GraphQL)
- Database operations (queries, transactions)
- Service-to-service calls
- Authentication flows
- External API integrations

### 2. Set Up Test Environment

**For Python/Pytest:**
```python
# conftest.py
import pytest
from app import create_app, db

@pytest.fixture(scope="session")
def app():
    """Create test application"""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture(scope="function")
def test_db(app):
    """Clean database for each test"""
    db.session.begin_nested()
    yield db
    db.session.rollback()

@pytest.fixture
def client(app):
    """Test client"""
    return app.test_client()

@pytest.fixture
def auth_headers(client):
    """Authenticated request headers"""
    response = client.post('/api/auth/login',
                          json={'username': 'test', 'password': 'test123'})
    token = response.json['token']
    return {'Authorization': f'Bearer {token}'}
```

**For TypeScript/Jest:**
```typescript
// setup.ts
import { setupTestDatabase, teardownTestDatabase } from './test-utils';

beforeAll(async () => {
  await setupTestDatabase();
});

afterAll(async () => {
  await teardownTestDatabase();
});

beforeEach(async () => {
  await clearTestData();
});
```

### 3. Implement API Endpoint Tests

**Test Structure:**
- Valid requests with expected responses
- Invalid requests with error handling
- Authentication/authorization
- Schema validation

**Example (Pytest):**
```python
# tests/integration/test_user_api.py
import pytest

class TestUserAPI:
    def test_create_user_success(self, client, auth_headers):
        """Test successful user creation"""
        response = client.post(
            '/api/users',
            json={'name': 'New User', 'email': 'new@example.com'},
            headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json
        assert data['name'] == 'New User'
        assert 'id' in data

    def test_create_user_duplicate_email(self, client, auth_headers):
        """Test duplicate email handling"""
        # Create first user
        client.post('/api/users',
                   json={'name': 'User1', 'email': 'test@example.com'},
                   headers=auth_headers)

        # Attempt duplicate
        response = client.post('/api/users',
                              json={'name': 'User2', 'email': 'test@example.com'},
                              headers=auth_headers)
        assert response.status_code == 409
        assert 'already exists' in response.json['error']

    def test_get_user_unauthorized(self, client):
        """Test endpoint requires authentication"""
        response = client.get('/api/users/1')
        assert response.status_code == 401
```

**Example (Jest/Supertest):**
```typescript
// tests/integration/user-api.test.ts
import request from 'supertest';
import { app } from '../../src/app';

describe('User API', () => {
  let authToken: string;

  beforeEach(async () => {
    const response = await request(app)
      .post('/api/auth/login')
      .send({ username: 'test', password: 'test123' });
    authToken = response.body.token;
  });

  test('creates user successfully', async () => {
    const response = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ name: 'New User', email: 'new@example.com' });

    expect(response.status).toBe(201);
    expect(response.body.name).toBe('New User');
    expect(response.body).toHaveProperty('id');
  });

  test('rejects duplicate email', async () => {
    await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ name: 'User1', email: 'test@example.com' });

    const response = await request(app)
      .post('/api/users')
      .set('Authorization', `Bearer ${authToken}`)
      .send({ name: 'User2', email: 'test@example.com' });

    expect(response.status).toBe(409);
    expect(response.body.error).toContain('already exists');
  });
});
```

### 4. Add Database Integration Tests

Test database operations directly:

```python
# tests/integration/test_database.py
class TestUserRepository:
    def test_create_and_retrieve_user(self, test_db):
        """Test user persistence"""
        user = User(name='Test User', email='test@example.com')
        test_db.session.add(user)
        test_db.session.commit()

        retrieved = User.query.filter_by(email='test@example.com').first()
        assert retrieved is not None
        assert retrieved.name == 'Test User'

    def test_cascade_delete(self, test_db):
        """Test cascading deletes"""
        user = User(name='Test User')
        post = Post(title='Test Post', user=user)
        test_db.session.add_all([user, post])
        test_db.session.commit()

        test_db.session.delete(user)
        test_db.session.commit()

        # Post should be deleted due to cascade
        assert Post.query.filter_by(title='Test Post').first() is None
```

### 5. Implement Contract Tests

For service boundaries, use contract testing:

```python
# tests/integration/test_payment_contract.py
from pact import Consumer, Provider

pact = Consumer('OrderService').has_pact_with(Provider('PaymentService'))

def test_process_payment_contract():
    """Verify payment service contract"""
    (pact
     .given('payment account exists')
     .upon_receiving('a payment request')
     .with_request('post', '/payments', body={'amount': 100.00, 'currency': 'USD'})
     .will_respond_with(200, body={'payment_id': '12345', 'status': 'completed'}))

    with pact:
        response = payment_client.process_payment(100.00, 'USD')
        assert response['status'] == 'completed'
```

### 6. Test Authentication Flows

```python
# tests/integration/test_auth.py
class TestAuthentication:
    def test_login_flow(self, client):
        """Test complete login flow"""
        response = client.post('/api/auth/login',
                              json={'username': 'test', 'password': 'test123'})
        assert response.status_code == 200
        assert 'token' in response.json

    def test_protected_endpoint_with_valid_token(self, client, auth_headers):
        """Test accessing protected resource"""
        response = client.get('/api/protected', headers=auth_headers)
        assert response.status_code == 200

    def test_token_expiration(self, client):
        """Test expired token handling"""
        expired_token = generate_expired_token()
        response = client.get('/api/protected',
                            headers={'Authorization': f'Bearer {expired_token}'})
        assert response.status_code == 401
```

### 7. Organize Test Suites

Structure tests by feature/domain:

```
tests/
├── integration/
│   ├── conftest.py              # Shared fixtures
│   ├── test_user_api.py         # User endpoints
│   ├── test_auth_api.py         # Authentication
│   ├── test_order_api.py        # Order endpoints
│   ├── test_database.py         # Database operations
│   └── test_contracts.py        # Service contracts
```

## Best Practices

**1. Test Independence**
- Each test should be independent and idempotent
- Use fixtures for setup/teardown
- Clean data between tests

**2. Test Database**
- Use separate test database
- Seed with minimal required data
- Clean up after tests

**3. Realistic Testing**
- Use real database (not mocks)
- Mock only external services
- Test with realistic data volumes

**4. Error Scenarios**
- Test validation errors
- Test constraint violations
- Test authentication failures
- Test network errors (for external services)

**5. Async Operations**
- Use proper async/await patterns
- Test race conditions
- Test timeout scenarios

**6. CI/CD Integration**
- Run in CI pipeline
- Use containerized test environment
- Parallel test execution

## Output Organization

When creating integration tests, organize output in:
`~/Documents/claude-code-skills-data/integration-test-implementation/`

Create subdirectories as needed:
- `test-reports/` - Test execution reports
- `coverage/` - Coverage reports
- `fixtures/` - Test data fixtures

## Quality Checklist

Before considering integration tests complete, verify:

- [ ] All API endpoints have integration tests
- [ ] CRUD operations tested with real database
- [ ] Authentication/authorization flows verified
- [ ] Error scenarios tested (400, 401, 403, 404, 409, 500)
- [ ] Test environment setup documented
- [ ] Tests clean up their data (no pollution)
- [ ] Tests run successfully in CI/CD
- [ ] Contract tests for service boundaries
- [ ] Transaction handling tested
- [ ] Fixtures properly scoped (session/module/function)

## Common Integration Test Patterns

### Pattern 1: API Request/Response Validation
```python
def test_api_endpoint(client, auth_headers):
    response = client.post('/api/resource', json=data, headers=auth_headers)
    assert response.status_code == 201
    assert response.json['field'] == expected_value
```

### Pattern 2: Database State Verification
```python
def test_database_state(test_db):
    # Perform operation
    service.create_user('test@example.com')

    # Verify database state
    user = User.query.filter_by(email='test@example.com').first()
    assert user is not None
```

### Pattern 3: Multi-Step Workflow
```python
def test_order_workflow(client, auth_headers):
    # Create order
    order_response = client.post('/api/orders', json=order_data, headers=auth_headers)
    order_id = order_response.json['id']

    # Add items
    client.post(f'/api/orders/{order_id}/items', json=item_data, headers=auth_headers)

    # Complete order
    response = client.post(f'/api/orders/{order_id}/complete', headers=auth_headers)
    assert response.status_code == 200
```

### Pattern 4: Error Handling
```python
def test_error_handling(client, auth_headers):
    response = client.post('/api/resource', json=invalid_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'error' in response.json
    assert 'field_name' in response.json['error']
```

## References

For more detailed patterns and examples, see:
- [Database Testing Patterns](references/database-testing.md) - Comprehensive database test patterns
- [API Testing Guide](references/api-testing.md) - REST/GraphQL testing strategies
- [Contract Testing](references/contract-testing.md) - Consumer-driven contract tests

## Tools and Frameworks

**Python:**
- Pytest - Test framework
- pytest-flask - Flask testing utilities
- pytest-django - Django testing utilities
- Requests - HTTP client for API testing
- Pact Python - Contract testing

**TypeScript/JavaScript:**
- Jest - Test framework
- Supertest - HTTP assertion library
- ts-jest - TypeScript support for Jest
- Pact JS - Contract testing

**Database:**
- pytest-postgresql - PostgreSQL fixtures
- pytest-mongodb - MongoDB fixtures
- Testcontainers - Containerized test dependencies

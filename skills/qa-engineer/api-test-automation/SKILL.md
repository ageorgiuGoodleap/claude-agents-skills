---
name: api-test-automation
description: |
  Automates comprehensive API testing with request/response validation, authentication testing,
  schema validation, and contract verification for REST and GraphQL APIs. Use when testing APIs,
  creating Postman collections, writing pytest API tests, validating endpoints, testing authentication
  flows, verifying response schemas, or implementing API test automation in CI/CD pipelines.
---

# API Test Automation

Build automated API test suites that verify endpoints, validate data contracts, and ensure API reliability.

## Core Capabilities

- **HTTP Testing**: Send requests (GET, POST, PUT, DELETE, PATCH) and validate responses
- **Schema Validation**: Verify response structure against JSON schemas or GraphQL schemas
- **Authentication Testing**: Test JWT, OAuth, API keys, session-based auth
- **Error Handling**: Verify error responses, status codes, error messages
- **Postman/Newman**: Create and run Postman collections for API testing
- **REST Testing**: Write Python/Java-based API tests with assertions
- **GraphQL Testing**: Query and mutation testing with proper validation

## Workflow

### 1. Collect API Documentation

Gather all available API documentation:
- OpenAPI/Swagger specification
- Endpoint list with methods and parameters
- Authentication requirements
- Example requests and responses
- Error response formats

### 2. Identify Test Coverage

List all endpoints to test:
- CRUD operations (Create, Read, Update, Delete)
- Special actions (search, filter, bulk operations)
- Authentication endpoints (login, refresh, logout)
- Public vs protected endpoints

### 3. Choose Testing Approach

**For quick prototyping and manual testing:**
- Use Postman collections with Newman for CI/CD
- Best for teams already using Postman

**For programmatic testing:**
- Use pytest with requests library (Python)
- Use REST Assured (Java)
- Best for integration with existing test frameworks

### 4. Implement Test Cases

For each endpoint, create tests for:

**Happy Path (2XX responses):**
```python
def test_create_user_success(api_client, auth_token):
    response = api_client.post(
        "/api/users",
        json={"name": "Test User", "email": "test@example.com"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert "id" in data
```

**Invalid Input (4XX errors):**
```python
def test_create_user_invalid_email(api_client, auth_token):
    response = api_client.post(
        "/api/users",
        json={"name": "Test", "email": "invalid-email"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 400
    assert "email" in response.json()["errors"]
```

**Unauthorized Access (401):**
```python
def test_create_user_unauthorized(api_client):
    response = api_client.post(
        "/api/users",
        json={"name": "Test", "email": "test@example.com"}
    )
    assert response.status_code == 401
```

**Forbidden (403):**
```python
def test_delete_user_forbidden(api_client, regular_user_token):
    # Regular users can't delete other users
    response = api_client.delete(
        "/api/users/admin-user-id",
        headers={"Authorization": f"Bearer {regular_user_token}"}
    )
    assert response.status_code == 403
```

**Not Found (404):**
```python
def test_get_nonexistent_user(api_client, auth_token):
    response = api_client.get(
        "/api/users/nonexistent-id",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 404
```

### 5. Test Authentication Flows

**JWT Token Flow:**
```python
class TestAuthFlow:
    def test_login_returns_tokens(self, api_client):
        response = api_client.post("/api/auth/login", json={
            "username": "testuser",
            "password": "testpass123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data

    def test_refresh_token(self, api_client, refresh_token):
        response = api_client.post("/api/auth/refresh", json={
            "refresh_token": refresh_token
        })
        assert response.status_code == 200
        assert "access_token" in response.json()

    def test_expired_token_rejected(self, api_client, expired_token):
        response = api_client.get(
            "/api/users",
            headers={"Authorization": f"Bearer {expired_token}"}
        )
        assert response.status_code == 401
```

### 6. Validate Response Schemas

**Using JSON Schema:**
```python
from jsonschema import validate, ValidationError

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "created_at"],
    "properties": {
        "id": {"type": "string"},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "created_at": {"type": "string", "format": "date-time"}
    }
}

def test_user_response_schema(api_client):
    response = api_client.get("/api/users/123")
    assert response.status_code == 200

    try:
        validate(instance=response.json(), schema=USER_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Schema validation failed: {e.message}")
```

### 7. Test Pagination

**Offset-based:**
```python
def test_pagination_offset(api_client):
    response = api_client.get("/api/users?limit=10&offset=0")
    assert response.status_code == 200
    data = response.json()

    assert len(data["items"]) <= 10
    assert data["total"] >= len(data["items"])
    assert data["offset"] == 0
    assert data["limit"] == 10
```

**Cursor-based:**
```python
def test_pagination_cursor(api_client):
    response = api_client.get("/api/users?limit=10")
    assert response.status_code == 200
    data = response.json()

    assert len(data["items"]) <= 10
    if data.get("next_cursor"):
        next_response = api_client.get(
            f"/api/users?limit=10&cursor={data['next_cursor']}"
        )
        assert next_response.status_code == 200
```

### 8. Test Filtering and Sorting

```python
def test_filter_users_by_role(api_client):
    response = api_client.get("/api/users?role=admin")
    assert response.status_code == 200
    users = response.json()["items"]

    for user in users:
        assert user["role"] == "admin"

def test_sort_users_by_name(api_client):
    response = api_client.get("/api/users?sort=name&order=asc")
    assert response.status_code == 200
    users = response.json()["items"]

    names = [user["name"] for user in users]
    assert names == sorted(names)
```

### 9. Test Rate Limiting

```python
def test_rate_limiting(api_client):
    # Make requests until rate limited
    for i in range(150):
        response = api_client.get("/api/users")
        if response.status_code == 429:
            assert "Retry-After" in response.headers
            assert "rate limit" in response.json()["message"].lower()
            return

    pytest.fail("Rate limit was not enforced")
```

### 10. Generate Test Reports

**Using Newman (Postman CLI):**
```bash
newman run collection.json \
  --environment environment.json \
  --reporters cli,html \
  --reporter-html-export reports/api-tests.html
```

**Or use the bundled script:**
```bash
python scripts/run_newman_tests.py collection.json environment.json
```

### 11. Integrate with CI/CD

**GitHub Actions example:**
```yaml
name: API Tests

on: [push, pull_request]

jobs:
  api-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          pip install pytest requests jsonschema
      - name: Run API tests
        run: pytest tests/api/ -v --html=report.html
      - name: Upload test report
        uses: actions/upload-artifact@v3
        if: always()
        with:
          name: api-test-report
          path: report.html
```

## Postman Collection Pattern

**Creating a Postman collection:**

1. Organize by resource (Users, Products, Orders)
2. Use folders for related endpoints
3. Add pre-request scripts for authentication
4. Add tests in the "Tests" tab

**Example Postman test:**
```javascript
// Test: Status code is 201
pm.test("Status code is 201", function () {
    pm.response.to.have.status(201);
});

// Test: Response has required fields
pm.test("Response has user ID", function () {
    var jsonData = pm.response.json();
    pm.expect(jsonData).to.have.property('id');
    pm.expect(jsonData.id).to.be.a('string');
});

// Test: Response matches schema
pm.test("Response matches schema", function () {
    var schema = {
        type: 'object',
        required: ['id', 'name', 'email'],
        properties: {
            id: { type: 'string' },
            name: { type: 'string' },
            email: { type: 'string', format: 'email' }
        }
    };
    pm.response.to.have.jsonSchema(schema);
});

// Save token for subsequent requests
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access_token);
}
```

## GraphQL Testing

**Query Testing:**
```python
def test_graphql_user_query(graphql_client):
    query = """
    query GetUser($id: ID!) {
        user(id: $id) {
            id
            name
            email
            posts {
                id
                title
            }
        }
    }
    """

    response = graphql_client.execute(query, variables={"id": "123"})

    assert "errors" not in response
    assert response["data"]["user"]["id"] == "123"
    assert isinstance(response["data"]["user"]["posts"], list)
```

**Mutation Testing:**
```python
def test_graphql_create_user(graphql_client):
    mutation = """
    mutation CreateUser($input: CreateUserInput!) {
        createUser(input: $input) {
            id
            name
            email
        }
    }
    """

    variables = {
        "input": {
            "name": "Test User",
            "email": "test@example.com"
        }
    }

    response = graphql_client.execute(mutation, variables=variables)

    assert "errors" not in response
    assert response["data"]["createUser"]["name"] == "Test User"
    assert response["data"]["createUser"]["id"]
```

## Test Organization

**Recommended structure:**
```
tests/
├── api/
│   ├── conftest.py           # Fixtures (api_client, auth_token)
│   ├── test_users.py         # User endpoint tests
│   ├── test_products.py      # Product endpoint tests
│   ├── test_auth.py          # Authentication flow tests
│   └── schemas/              # JSON schemas for validation
│       ├── user_schema.json
│       └── product_schema.json
└── postman/
    ├── collection.json
    └── environment.json
```

**conftest.py example:**
```python
import pytest
import requests

@pytest.fixture
def api_client():
    """Base API client."""
    class APIClient:
        def __init__(self, base_url):
            self.base_url = base_url
            self.session = requests.Session()

        def get(self, path, **kwargs):
            return self.session.get(f"{self.base_url}{path}", **kwargs)

        def post(self, path, **kwargs):
            return self.session.post(f"{self.base_url}{path}", **kwargs)

        def put(self, path, **kwargs):
            return self.session.put(f"{self.base_url}{path}", **kwargs)

        def delete(self, path, **kwargs):
            return self.session.delete(f"{self.base_url}{path}", **kwargs)

    return APIClient("http://localhost:8000")

@pytest.fixture
def auth_token(api_client):
    """Get authentication token."""
    response = api_client.post("/api/auth/login", json={
        "username": "testuser",
        "password": "testpass123"
    })
    return response.json()["access_token"]
```

## Quality Standards

Before completing API test implementation:
- [ ] All endpoints have test coverage (happy path + error cases)
- [ ] Authentication flows are tested (login, refresh, logout)
- [ ] Response schemas are validated
- [ ] Status codes are verified for all scenarios
- [ ] Pagination is tested (if applicable)
- [ ] Filtering and sorting are tested (if applicable)
- [ ] Rate limiting is tested (if applicable)
- [ ] Tests run in under 2 minutes
- [ ] Test reports are generated (HTML or JSON)
- [ ] CI/CD integration is configured

## Advanced Patterns

For more complex scenarios (contract testing, performance testing, data-driven tests), see [advanced_patterns.md](references/advanced_patterns.md).

## Common Issues

**Issue: Tests fail intermittently**
- Use proper wait strategies (polling, exponential backoff)
- Ensure test data isolation (create/cleanup for each test)
- Check for race conditions in parallel test execution

**Issue: Authentication tokens expire during test run**
- Implement token refresh logic in fixtures
- Use shorter token expiry in test environments
- Cache tokens and refresh only when needed

**Issue: Rate limiting blocks tests**
- Use test-specific API keys with higher limits
- Implement backoff and retry logic
- Run tests sequentially if parallel execution triggers limits

**Issue: Schema validation fails**
- Keep schemas in sync with API changes
- Use schema versioning
- Test schema compatibility separately

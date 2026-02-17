# Advanced API Testing Patterns

## Dynamic Test Data

### Using Faker for Test Data
```python
from faker import Faker
import pytest

fake = Faker()

@pytest.fixture
def random_user():
    return {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number()
    }

def test_create_user_with_faker(api_client, random_user):
    response = api_client.post("/users", json=random_user)
    assert response.status_code == 201
```

### Data-Driven Testing with Parametrize
```python
@pytest.mark.parametrize("invalid_email", [
    "notanemail",
    "@example.com",
    "user@",
    "user@.com",
    ""
])
def test_invalid_email_formats(api_client, invalid_email):
    response = api_client.post("/users", json={
        "name": "Test User",
        "email": invalid_email
    })
    assert response.status_code == 400
    assert "email" in response.json()["errors"]
```

## Authentication Flow Testing

### JWT Token Management
```python
import pytest
import requests
from datetime import datetime, timedelta

class TestAuthFlow:
    def test_login_get_token(self, api_client):
        response = api_client.post("/auth/login", json={
            "username": "testuser",
            "password": "testpass123"
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        return data["access_token"]

    def test_protected_endpoint_with_token(self, api_client, auth_token):
        response = api_client.get("/protected/resource",
            headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200

    def test_protected_endpoint_without_token(self, api_client):
        response = api_client.get("/protected/resource")
        assert response.status_code == 401

    def test_expired_token_rejected(self, api_client, expired_token):
        response = api_client.get("/protected/resource",
            headers={"Authorization": f"Bearer {expired_token}"})
        assert response.status_code == 401
        assert "expired" in response.json()["message"].lower()
```

## Schema Validation

### JSON Schema Validation
```python
from jsonschema import validate, ValidationError

USER_SCHEMA = {
    "type": "object",
    "required": ["id", "name", "email", "created_at"],
    "properties": {
        "id": {"type": "string", "format": "uuid"},
        "name": {"type": "string", "minLength": 1},
        "email": {"type": "string", "format": "email"},
        "created_at": {"type": "string", "format": "date-time"}
    },
    "additionalProperties": False
}

def test_user_response_schema(api_client):
    response = api_client.get("/users/123")
    assert response.status_code == 200

    data = response.json()
    try:
        validate(instance=data, schema=USER_SCHEMA)
    except ValidationError as e:
        pytest.fail(f"Response does not match schema: {e.message}")
```

### Pydantic Schema Validation
```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserResponse(BaseModel):
    id: str = Field(..., regex=r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    created_at: datetime

def test_user_response_with_pydantic(api_client):
    response = api_client.get("/users/123")
    assert response.status_code == 200

    # Will raise ValidationError if schema doesn't match
    user = UserResponse(**response.json())
    assert user.email  # Access validated fields
```

## GraphQL Testing

### Query Testing
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

    assert response["data"]["user"]["id"] == "123"
    assert "name" in response["data"]["user"]
    assert isinstance(response["data"]["user"]["posts"], list)
```

### Mutation Testing
```python
def test_graphql_create_user_mutation(graphql_client):
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

## Performance Testing

### Response Time Assertions
```python
import time

def test_response_time_acceptable(api_client):
    start = time.time()
    response = api_client.get("/users")
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 1.0, f"Response took {duration}s (max 1.0s)"
```

### Load Testing with Locust
```python
from locust import HttpUser, task, between

class APIUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        # Login and get token
        response = self.client.post("/auth/login", json={
            "username": "test",
            "password": "test123"
        })
        self.token = response.json()["access_token"]

    @task(3)
    def list_users(self):
        self.client.get("/users",
            headers={"Authorization": f"Bearer {self.token}"})

    @task(1)
    def create_user(self):
        self.client.post("/users",
            json={"name": "Test", "email": "test@example.com"},
            headers={"Authorization": f"Bearer {self.token}"})
```

## Contract Testing

### Pact Contract Testing
```python
from pact import Consumer, Provider
import pytest

@pytest.fixture
def pact():
    pact = Consumer('UserService').has_pact_with(Provider('APIBackend'))
    pact.start_service()
    yield pact
    pact.stop_service()

def test_get_user_contract(pact):
    expected = {
        'id': '123',
        'name': 'Test User',
        'email': 'test@example.com'
    }

    (pact
     .given('user 123 exists')
     .upon_receiving('a request for user 123')
     .with_request('get', '/users/123')
     .will_respond_with(200, body=expected))

    with pact:
        response = requests.get(pact.uri + '/users/123')
        assert response.json() == expected
```

## Error Handling Patterns

### Comprehensive Error Testing
```python
class TestErrorHandling:
    def test_404_not_found(self, api_client):
        response = api_client.get("/users/nonexistent")
        assert response.status_code == 404
        assert response.json()["error"] == "User not found"

    def test_400_validation_error(self, api_client):
        response = api_client.post("/users", json={"name": ""})
        assert response.status_code == 400
        errors = response.json()["errors"]
        assert "name" in errors
        assert "email" in errors  # Required field missing

    def test_429_rate_limit(self, api_client):
        # Make requests until rate limited
        for _ in range(100):
            response = api_client.get("/users")
            if response.status_code == 429:
                assert "Retry-After" in response.headers
                break
        else:
            pytest.fail("Rate limit not enforced")

    def test_500_server_error_handling(self, api_client):
        # Trigger server error condition
        response = api_client.post("/users", json={"trigger_error": True})
        assert response.status_code == 500
        assert "error" in response.json()
```

## Pagination Testing

### Cursor-Based Pagination
```python
def test_cursor_pagination(api_client):
    # Get first page
    response = api_client.get("/users?limit=10")
    assert response.status_code == 200
    data = response.json()

    assert len(data["items"]) <= 10
    assert "next_cursor" in data

    # Get next page
    if data["next_cursor"]:
        response = api_client.get(f"/users?limit=10&cursor={data['next_cursor']}")
        assert response.status_code == 200
        next_data = response.json()

        # Ensure no duplicate items
        first_ids = [item["id"] for item in data["items"]]
        next_ids = [item["id"] for item in next_data["items"]]
        assert not set(first_ids).intersection(set(next_ids))
```

### Offset-Based Pagination
```python
def test_offset_pagination(api_client):
    # Get total count
    response = api_client.get("/users?limit=10&offset=0")
    total = response.json()["total"]

    # Verify all pages
    collected_ids = set()
    for offset in range(0, total, 10):
        response = api_client.get(f"/users?limit=10&offset={offset}")
        items = response.json()["items"]

        for item in items:
            assert item["id"] not in collected_ids, "Duplicate item found"
            collected_ids.add(item["id"])

    assert len(collected_ids) == total
```

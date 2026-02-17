# API Testing Guide

## Overview

API integration tests verify that HTTP endpoints work correctly, handle errors gracefully, and enforce security policies. These tests use real HTTP clients to make requests and validate responses.

## REST API Testing

### Basic GET Request

```python
def test_get_users(client, auth_headers):
    """Test GET /api/users endpoint"""
    response = client.get('/api/users', headers=auth_headers)

    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0
    assert 'id' in response.json[0]
    assert 'username' in response.json[0]
```

### POST Request with Validation

```python
def test_create_user_success(client, auth_headers):
    """Test successful user creation"""
    payload = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'secure_password123'
    }

    response = client.post('/api/users', json=payload, headers=auth_headers)

    assert response.status_code == 201
    data = response.json
    assert data['username'] == 'newuser'
    assert data['email'] == 'newuser@example.com'
    assert 'password' not in data  # Should not return password
    assert 'id' in data
    assert 'created_at' in data

def test_create_user_invalid_email(client, auth_headers):
    """Test validation error handling"""
    payload = {
        'username': 'newuser',
        'email': 'invalid-email',
        'password': 'secure_password123'
    }

    response = client.post('/api/users', json=payload, headers=auth_headers)

    assert response.status_code == 400
    assert 'error' in response.json
    assert 'email' in response.json['error']
```

### PUT/PATCH Request

```python
def test_update_user(client, auth_headers):
    """Test user update"""
    # Create user first
    create_response = client.post('/api/users',
                                  json={'username': 'testuser', 'email': 'test@example.com'},
                                  headers=auth_headers)
    user_id = create_response.json['id']

    # Update user
    update_payload = {'username': 'updated_user'}
    response = client.patch(f'/api/users/{user_id}',
                           json=update_payload,
                           headers=auth_headers)

    assert response.status_code == 200
    assert response.json['username'] == 'updated_user'
    assert response.json['email'] == 'test@example.com'  # Unchanged
```

### DELETE Request

```python
def test_delete_user(client, auth_headers):
    """Test user deletion"""
    # Create user
    create_response = client.post('/api/users',
                                  json={'username': 'testuser', 'email': 'test@example.com'},
                                  headers=auth_headers)
    user_id = create_response.json['id']

    # Delete user
    response = client.delete(f'/api/users/{user_id}', headers=auth_headers)

    assert response.status_code == 204

    # Verify deletion
    get_response = client.get(f'/api/users/{user_id}', headers=auth_headers)
    assert get_response.status_code == 404
```

## Authentication Testing

### Login Flow

```python
def test_login_success(client):
    """Test successful login"""
    response = client.post('/api/auth/login',
                          json={'username': 'testuser', 'password': 'password123'})

    assert response.status_code == 200
    assert 'token' in response.json
    assert 'expires_at' in response.json

def test_login_invalid_credentials(client):
    """Test login with invalid credentials"""
    response = client.post('/api/auth/login',
                          json={'username': 'testuser', 'password': 'wrongpassword'})

    assert response.status_code == 401
    assert 'error' in response.json
    assert response.json['error'] == 'Invalid credentials'
```

### Token Authentication

```python
def test_access_protected_endpoint_with_token(client, auth_headers):
    """Test accessing protected resource with valid token"""
    response = client.get('/api/protected', headers=auth_headers)

    assert response.status_code == 200

def test_access_protected_endpoint_without_token(client):
    """Test accessing protected resource without token"""
    response = client.get('/api/protected')

    assert response.status_code == 401

def test_access_protected_endpoint_with_expired_token(client):
    """Test accessing protected resource with expired token"""
    expired_token = generate_expired_token()
    headers = {'Authorization': f'Bearer {expired_token}'}

    response = client.get('/api/protected', headers=headers)

    assert response.status_code == 401
    assert 'expired' in response.json['error'].lower()
```

### OAuth Flow

```python
def test_oauth_authorization_code_flow(client):
    """Test OAuth authorization code flow"""
    # Step 1: Get authorization URL
    response = client.get('/api/oauth/authorize',
                         query_string={'client_id': 'test_client', 'redirect_uri': 'http://localhost/callback'})

    assert response.status_code == 302
    assert 'code=' in response.headers['Location']

    # Step 2: Exchange code for token
    code = extract_code_from_url(response.headers['Location'])
    token_response = client.post('/api/oauth/token',
                                 json={'code': code, 'client_id': 'test_client', 'client_secret': 'secret'})

    assert token_response.status_code == 200
    assert 'access_token' in token_response.json
    assert 'refresh_token' in token_response.json
```

## Authorization Testing

### Role-Based Access Control

```python
def test_admin_can_access_admin_endpoint(client, admin_headers):
    """Test admin role can access admin endpoints"""
    response = client.get('/api/admin/users', headers=admin_headers)

    assert response.status_code == 200

def test_regular_user_cannot_access_admin_endpoint(client, user_headers):
    """Test regular user cannot access admin endpoints"""
    response = client.get('/api/admin/users', headers=user_headers)

    assert response.status_code == 403
    assert response.json['error'] == 'Insufficient permissions'
```

### Resource Ownership

```python
def test_user_can_update_own_profile(client, user_headers):
    """Test user can update their own profile"""
    response = client.patch('/api/users/me',
                           json={'bio': 'Updated bio'},
                           headers=user_headers)

    assert response.status_code == 200

def test_user_cannot_update_other_user_profile(client, user_headers):
    """Test user cannot update another user's profile"""
    response = client.patch('/api/users/999',
                           json={'bio': 'Hacked bio'},
                           headers=user_headers)

    assert response.status_code == 403
```

## Error Handling

### HTTP Status Codes

```python
def test_404_not_found(client, auth_headers):
    """Test 404 for non-existent resource"""
    response = client.get('/api/users/99999', headers=auth_headers)

    assert response.status_code == 404
    assert 'error' in response.json
    assert 'not found' in response.json['error'].lower()

def test_400_bad_request(client, auth_headers):
    """Test 400 for invalid request"""
    response = client.post('/api/users',
                          json={'invalid': 'data'},
                          headers=auth_headers)

    assert response.status_code == 400
    assert 'error' in response.json

def test_409_conflict(client, auth_headers):
    """Test 409 for duplicate resource"""
    payload = {'username': 'testuser', 'email': 'test@example.com'}

    # Create first time
    client.post('/api/users', json=payload, headers=auth_headers)

    # Attempt duplicate
    response = client.post('/api/users', json=payload, headers=auth_headers)

    assert response.status_code == 409
    assert 'already exists' in response.json['error']

def test_500_internal_server_error(client, auth_headers, monkeypatch):
    """Test 500 error handling"""
    def mock_error(*args, **kwargs):
        raise Exception('Database error')

    monkeypatch.setattr('app.services.user_service.create_user', mock_error)

    response = client.post('/api/users',
                          json={'username': 'test', 'email': 'test@example.com'},
                          headers=auth_headers)

    assert response.status_code == 500
    assert 'error' in response.json
```

## Request Validation

### Schema Validation

```python
def test_request_schema_validation(client, auth_headers):
    """Test request body schema validation"""
    # Missing required field
    response = client.post('/api/users',
                          json={'username': 'test'},  # Missing email
                          headers=auth_headers)

    assert response.status_code == 400
    assert 'email' in response.json['error']

def test_request_type_validation(client, auth_headers):
    """Test request field type validation"""
    response = client.post('/api/users',
                          json={'username': 123, 'email': 'test@example.com'},
                          headers=auth_headers)

    assert response.status_code == 400
    assert 'username' in response.json['error']
```

### Query Parameter Validation

```python
def test_query_param_validation(client, auth_headers):
    """Test query parameter validation"""
    # Invalid pagination parameters
    response = client.get('/api/users?page=-1&limit=1000', headers=auth_headers)

    assert response.status_code == 400
    assert 'page' in response.json['error'] or 'limit' in response.json['error']
```

## Response Validation

### Schema Validation

```python
def test_response_schema(client, auth_headers):
    """Test response matches expected schema"""
    response = client.get('/api/users/1', headers=auth_headers)

    assert response.status_code == 200
    data = response.json

    # Validate schema
    assert isinstance(data, dict)
    assert 'id' in data
    assert 'username' in data
    assert 'email' in data
    assert 'created_at' in data
    assert isinstance(data['id'], int)
    assert isinstance(data['username'], str)
```

### Pagination

```python
def test_pagination(client, auth_headers):
    """Test paginated response"""
    response = client.get('/api/users?page=1&limit=10', headers=auth_headers)

    assert response.status_code == 200
    data = response.json

    assert 'items' in data
    assert 'total' in data
    assert 'page' in data
    assert 'limit' in data
    assert len(data['items']) <= 10
```

## GraphQL Testing

### Query Testing

```python
def test_graphql_query(client, auth_headers):
    """Test GraphQL query"""
    query = """
    query {
        users {
            id
            username
            email
        }
    }
    """

    response = client.post('/graphql',
                          json={'query': query},
                          headers=auth_headers)

    assert response.status_code == 200
    assert 'data' in response.json
    assert 'users' in response.json['data']
    assert isinstance(response.json['data']['users'], list)
```

### Mutation Testing

```python
def test_graphql_mutation(client, auth_headers):
    """Test GraphQL mutation"""
    mutation = """
    mutation {
        createUser(input: {
            username: "newuser"
            email: "newuser@example.com"
        }) {
            id
            username
            email
        }
    }
    """

    response = client.post('/graphql',
                          json={'query': mutation},
                          headers=auth_headers)

    assert response.status_code == 200
    assert 'data' in response.json
    assert 'createUser' in response.json['data']
    assert response.json['data']['createUser']['username'] == 'newuser'
```

## Performance Testing

### Response Time

```python
import time

def test_response_time(client, auth_headers):
    """Test endpoint response time"""
    start = time.time()
    response = client.get('/api/users', headers=auth_headers)
    duration = time.time() - start

    assert response.status_code == 200
    assert duration < 0.5  # Should respond within 500ms
```

### Rate Limiting

```python
def test_rate_limiting(client, auth_headers):
    """Test rate limiting enforcement"""
    # Make requests up to rate limit
    for _ in range(100):
        response = client.get('/api/users', headers=auth_headers)
        if response.status_code == 429:
            break

    assert response.status_code == 429
    assert 'retry-after' in response.headers
```

## Testing Best Practices

1. **Use Real HTTP Clients**
   - Test through the full HTTP stack
   - Verify serialization/deserialization

2. **Test Authentication & Authorization**
   - Verify protected endpoints require auth
   - Test role-based access control
   - Validate token expiration

3. **Validate Request & Response Schemas**
   - Ensure API contracts are enforced
   - Test validation error messages

4. **Test Error Scenarios**
   - Invalid input
   - Missing resources
   - Server errors
   - Authentication failures

5. **Clean Up Test Data**
   - Delete created resources after tests
   - Use transactions when possible
   - Reset database state between tests

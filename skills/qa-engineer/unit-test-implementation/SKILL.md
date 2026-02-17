---
name: unit-test-implementation
description: |
  Implement comprehensive unit tests with high coverage (80%+) using Pytest (Python) or Jest (JavaScript/TypeScript). Create test fixtures, mock dependencies, write parameterized tests, and generate coverage reports. Use when writing unit tests, testing functions/classes, creating fixtures, mocking external dependencies, or when user mentions "unit test", "test coverage", "pytest", "jest", "mock", "fixture", "test functions", "test methods", or "coverage report".
---

# Unit Test Implementation

Implement production-grade unit tests with high coverage, proper isolation, clear structure, and maintainability. This skill focuses on testing individual functions, classes, and modules in isolation using modern testing frameworks.

## Output Location

Save all test files and coverage reports to:
```
~/Documents/claude-code-skills-data/unit-test-implementation/
```

Organize by project or module name.

## When to Use This Skill

Use this skill when:
- Writing unit tests for new code
- Improving test coverage for existing code
- Creating test fixtures for reusable test data
- Mocking external dependencies (APIs, databases, file I/O)
- Writing parameterized tests for multiple scenarios
- Generating and analyzing coverage reports
- Implementing test-driven development (TDD)

## Core Capabilities

### 1. Test Framework Mastery

Expert use of modern testing frameworks:

**Python: Pytest**
- Fixtures for test data and setup
- Parametrize decorator for data-driven tests
- Marking tests (skip, xfail, slow)
- Powerful assert introspection
- Plugin ecosystem (pytest-cov, pytest-mock, pytest-asyncio)

**JavaScript/TypeScript: Jest**
- Test suites with describe/it
- Setup/teardown with before/after hooks
- Snapshot testing for UI components
- Built-in code coverage
- Mock functions and modules
- Timer and async testing

### 2. Test Structure: Arrange-Act-Assert

Always follow the AAA pattern for clarity:

```python
def test_create_user_success():
    # Arrange: Set up test data and conditions
    user_data = {"name": "John", "email": "john@example.com"}
    service = UserService()

    # Act: Execute the code under test
    result = service.create_user(user_data)

    # Assert: Verify the expected outcome
    assert result.id is not None
    assert result.name == "John"
    assert result.email == "john@example.com"
```

### 3. Fixture Creation

Design reusable test fixtures:

**Pytest Fixtures:**
```python
import pytest

@pytest.fixture
def sample_user():
    """Reusable user data for tests"""
    return {"id": 1, "name": "Test User", "email": "test@example.com"}

@pytest.fixture
def user_service():
    """User service instance"""
    return UserService()

def test_update_user(user_service, sample_user):
    # Fixtures automatically injected
    result = user_service.update(sample_user["id"], {"name": "Updated"})
    assert result.name == "Updated"
```

**Jest Setup:**
```typescript
describe('UserService', () => {
  let service: UserService;
  let mockRepository: jest.Mocked<UserRepository>;

  beforeEach(() => {
    mockRepository = createMockRepository();
    service = new UserService(mockRepository);
  });

  it('should create user', () => {
    // Test implementation
  });
});
```

### 4. Mocking & Patching

Isolate units by mocking external dependencies:

**Pytest Mocking:**
```python
from unittest.mock import Mock, patch, MagicMock

def test_send_email_success():
    # Mock external email service
    with patch('services.email.EmailClient') as mock_client:
        mock_client.return_value.send.return_value = {"status": "sent"}

        service = NotificationService()
        result = service.send_welcome_email("user@example.com")

        assert result["status"] == "sent"
        mock_client.return_value.send.assert_called_once()
```

**Jest Mocking:**
```typescript
import { EmailService } from './email';

jest.mock('./email');

it('should send notification', async () => {
  const mockSend = jest.fn().mockResolvedValue({ status: 'sent' });
  (EmailService as jest.Mock).mockImplementation(() => ({
    send: mockSend
  }));

  const service = new NotificationService();
  const result = await service.sendWelcome('user@example.com');

  expect(result.status).toBe('sent');
  expect(mockSend).toHaveBeenCalledWith(
    'user@example.com',
    expect.any(String)
  );
});
```

### 5. Parameterized Tests

Test multiple scenarios efficiently:

**Pytest Parametrize:**
```python
import pytest

@pytest.mark.parametrize("input_value,expected", [
    (0, False),
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (18, False),
])
def test_is_prime(input_value, expected):
    result = is_prime(input_value)
    assert result == expected

@pytest.mark.parametrize("invalid_input", [
    None,
    "",
    {},
    {"name": ""},
    {"email": "invalid"},
])
def test_validate_user_invalid_inputs(invalid_input):
    with pytest.raises(ValueError):
        validate_user(invalid_input)
```

**Jest Each:**
```typescript
describe.each([
  [0, false],
  [1, false],
  [2, true],
  [3, true],
  [4, false],
])('isPrime(%i)', (input, expected) => {
  it(`returns ${expected}`, () => {
    expect(isPrime(input)).toBe(expected);
  });
});
```

### 6. Coverage Analysis

Generate and interpret coverage reports:

**Pytest Coverage:**
```bash
# Run tests with coverage
pytest --cov=src --cov-report=html --cov-report=term

# View HTML report
open htmlcov/index.html
```

**Jest Coverage:**
```bash
# Run tests with coverage
jest --coverage

# View HTML report
open coverage/lcov-report/index.html
```

**Coverage Metrics:**
- **Line coverage:** % of code lines executed
- **Branch coverage:** % of decision branches tested
- **Function coverage:** % of functions called
- **Statement coverage:** % of statements executed

**Target:** Aim for >80% coverage overall, >90% for critical modules

## Workflow: Writing Unit Tests

Follow this systematic approach:

### Step 1: Identify Units to Test

1. **List functions/classes** requiring tests
2. **Analyze function contracts:**
   - Inputs (parameters, types)
   - Outputs (return values, types)
   - Side effects (database writes, API calls)
   - Error conditions

### Step 2: Create Test File Structure

**Python Convention:**
```
src/
  module.py
tests/
  unit/
    test_module.py
```

**JavaScript Convention:**
```
src/
  module.ts
__tests__/
  unit/
    module.test.ts
```

### Step 3: Write Happy Path Tests

Start with standard successful execution:

```python
def test_calculate_total_with_valid_items():
    """Test standard total calculation"""
    items = [
        {"price": 10.00, "quantity": 2},
        {"price": 5.00, "quantity": 3},
    ]
    result = calculate_total(items)
    assert result == 35.00
```

### Step 4: Add Edge Case Tests

Test boundary values and special cases:

```python
def test_calculate_total_empty_list():
    """Test with empty input"""
    result = calculate_total([])
    assert result == 0.00

def test_calculate_total_single_item():
    """Test with single item"""
    result = calculate_total([{"price": 10.00, "quantity": 1}])
    assert result == 10.00

def test_calculate_total_zero_quantity():
    """Test with zero quantity"""
    result = calculate_total([{"price": 10.00, "quantity": 0}])
    assert result == 0.00
```

### Step 5: Add Error Handling Tests

Test exceptional conditions:

```python
def test_calculate_total_invalid_price():
    """Test with invalid price type"""
    with pytest.raises(TypeError):
        calculate_total([{"price": "invalid", "quantity": 1}])

def test_calculate_total_negative_price():
    """Test with negative price"""
    with pytest.raises(ValueError):
        calculate_total([{"price": -10.00, "quantity": 1}])

def test_calculate_total_none_input():
    """Test with None input"""
    with pytest.raises(TypeError):
        calculate_total(None)
```

### Step 6: Mock External Dependencies

Isolate the unit:

```python
@patch('services.payment.PaymentGateway')
def test_process_payment_success(mock_gateway):
    """Test payment processing with mocked gateway"""
    mock_gateway.return_value.charge.return_value = {"status": "success"}

    service = OrderService()
    result = service.process_payment(order_id=123, amount=50.00)

    assert result["status"] == "success"
    mock_gateway.return_value.charge.assert_called_once_with(50.00)
```

### Step 7: Use Parameterized Tests

Cover multiple scenarios efficiently:

```python
@pytest.mark.parametrize("discount,expected", [
    (0.0, 100.00),
    (0.1, 90.00),
    (0.25, 75.00),
    (0.5, 50.00),
    (1.0, 0.00),
])
def test_apply_discount(discount, expected):
    result = apply_discount(100.00, discount)
    assert result == expected
```

### Step 8: Run Coverage Analysis

```bash
# Pytest
pytest --cov=src --cov-report=term-missing

# Jest
jest --coverage --collectCoverageFrom='src/**/*.ts'
```

### Step 9: Identify Coverage Gaps

Review coverage report:
- **Red lines:** Not executed
- **Yellow branches:** Partially covered
- **Green:** Fully covered

Add tests for uncovered code.

### Step 10: Refactor for Maintainability

- Extract common setup to fixtures
- Use descriptive test names
- Add docstrings explaining complex tests
- Organize tests into classes or describe blocks
- Remove duplicate test logic

## Test Categories

### Happy Path Tests

Test standard successful execution:

```python
def test_user_login_with_valid_credentials():
    """Test successful login"""
    result = authenticate("user@example.com", "password123")
    assert result.authenticated is True
    assert result.user_id is not None
```

### Edge Case Tests

Test boundary values:

```python
def test_calculate_age_boundary_values():
    """Test age calculation at year boundary"""
    # Born on Jan 1
    age = calculate_age(date(2000, 1, 1), date(2025, 1, 1))
    assert age == 25

    # Born on Dec 31
    age = calculate_age(date(2000, 12, 31), date(2025, 12, 31))
    assert age == 25

def test_string_length_empty():
    """Test with empty string"""
    result = process_string("")
    assert result == ""

def test_list_operations_single_element():
    """Test with single element list"""
    result = process_list([1])
    assert result == [1]
```

### Error Handling Tests

Test exceptional conditions:

```python
def test_divide_by_zero():
    """Test division by zero raises error"""
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_invalid_email_format():
    """Test invalid email raises ValueError"""
    with pytest.raises(ValueError, match="Invalid email"):
        validate_email("not-an-email")

def test_file_not_found():
    """Test missing file raises FileNotFoundError"""
    with pytest.raises(FileNotFoundError):
        read_file("/nonexistent/path")
```

### State Change Tests

Test that state changes correctly:

```python
def test_shopping_cart_add_item():
    """Test adding item updates cart state"""
    cart = ShoppingCart()
    assert len(cart.items) == 0

    cart.add_item({"id": 1, "name": "Product", "price": 10.00})

    assert len(cart.items) == 1
    assert cart.total == 10.00

def test_user_status_after_activation():
    """Test user status changes after activation"""
    user = User(status="inactive")
    assert user.is_active is False

    user.activate()

    assert user.status == "active"
    assert user.is_active is True
```

### Async Tests

Test asynchronous functions:

**Pytest Async:**
```python
import pytest

@pytest.mark.asyncio
async def test_async_fetch_user():
    """Test async user fetch"""
    service = UserService()
    user = await service.fetch_user(user_id=1)
    assert user is not None
    assert user.id == 1
```

**Jest Async:**
```typescript
it('should fetch user asynchronously', async () => {
  const service = new UserService();
  const user = await service.fetchUser(1);
  expect(user).toBeDefined();
  expect(user.id).toBe(1);
});
```

## Test Naming Conventions

Use clear, descriptive names following this pattern:

**Format:** `test_<function>_<condition>_<expectedResult>`

**Examples:**
```python
def test_create_user_with_valid_data_returns_user():
    """Clear what is being tested"""
    pass

def test_create_user_with_duplicate_email_raises_error():
    """Indicates error case"""
    pass

def test_calculate_total_with_empty_list_returns_zero():
    """Specifies edge case"""
    pass

def test_authenticate_with_invalid_password_returns_false():
    """Describes failure scenario"""
    pass
```

**Jest/TypeScript:**
```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should return user when given valid data', () => {});
    it('should throw error when email is duplicate', () => {});
    it('should hash password before saving', () => {});
  });
});
```

## Best Practices

### 1. Test Independence

Each test should run independently:

```python
# Good: Each test creates own data
def test_create_user():
    user = UserFactory()  # Fresh data
    result = service.create(user)
    assert result.id is not None

def test_update_user():
    user = UserFactory()  # Fresh data
    result = service.update(user.id, {"name": "Updated"})
    assert result.name == "Updated"

# Bad: Tests depend on shared state
shared_user = None

def test_create_user():
    global shared_user
    shared_user = service.create(UserFactory())  # Creates shared state

def test_update_user():
    # Depends on previous test running first!
    result = service.update(shared_user.id, {"name": "Updated"})
```

### 2. Use Descriptive Assertions

Make failures informative:

```python
# Good: Descriptive assertion message
assert result.status == "active", f"Expected 'active', got '{result.status}'"

# Good: Multiple specific assertions
assert result is not None
assert result.id == expected_id
assert result.name == expected_name

# Bad: Generic assertion
assert result
```

### 3. Test One Thing Per Test

Keep tests focused:

```python
# Good: Focused test
def test_user_creation_generates_id():
    user = service.create_user({"name": "John"})
    assert user.id is not None

def test_user_creation_sets_name():
    user = service.create_user({"name": "John"})
    assert user.name == "John"

# Bad: Testing multiple things
def test_user_creation():
    user = service.create_user({"name": "John"})
    assert user.id is not None  # Test 1
    assert user.name == "John"  # Test 2
    assert user.email is None   # Test 3
    assert user.created_at is not None  # Test 4
```

### 4. Avoid Test Logic

Tests should be simple and straightforward:

```python
# Good: Simple and clear
def test_calculate_discount():
    result = calculate_discount(100, 0.1)
    assert result == 90.0

# Bad: Logic in test
def test_calculate_discount():
    prices = [100, 200, 300]
    discount = 0.1
    for price in prices:
        result = calculate_discount(price, discount)
        expected = price * (1 - discount)  # Calculation in test!
        assert result == expected
```

### 5. Fast Execution

Keep unit tests fast (<1s each):

```python
# Good: Fast unit test
def test_validate_email():
    result = validate_email("test@example.com")
    assert result is True

# Bad: Slow (database, network, file I/O)
def test_validate_email():
    db = connect_to_database()  # Slow!
    user = db.find_user("test@example.com")
    result = user is not None
    assert result is True
```

Use mocks to avoid slow operations:

```python
# Good: Mocked database
@patch('services.database.Database')
def test_find_user(mock_db):
    mock_db.return_value.find.return_value = {"id": 1}
    result = service.find_user(1)
    assert result["id"] == 1
```

## Common Patterns

### Pattern 1: Test Classes for Organization

Group related tests:

```python
class TestUserService:
    """Tests for UserService"""

    @pytest.fixture
    def service(self):
        return UserService()

    def test_create_user(self, service):
        result = service.create({"name": "John"})
        assert result.id is not None

    def test_update_user(self, service):
        result = service.update(1, {"name": "Updated"})
        assert result.name == "Updated"

    def test_delete_user(self, service):
        result = service.delete(1)
        assert result is True
```

### Pattern 2: Setup/Teardown

Use fixtures or hooks for setup/teardown:

**Pytest:**
```python
@pytest.fixture
def temp_file():
    """Create temp file, clean up after test"""
    file = create_temp_file()
    yield file
    os.remove(file.path)  # Cleanup

def test_read_file(temp_file):
    content = read_file(temp_file.path)
    assert content is not None
```

**Jest:**
```typescript
describe('FileService', () => {
  let tempFile: string;

  beforeEach(() => {
    tempFile = createTempFile();
  });

  afterEach(() => {
    fs.unlinkSync(tempFile);
  });

  it('should read file', () => {
    const content = readFile(tempFile);
    expect(content).toBeDefined();
  });
});
```

### Pattern 3: Test Doubles

Use appropriate test doubles:

**Stub:** Returns predetermined values
```python
def test_with_stub():
    stub_service = Mock()
    stub_service.get_price.return_value = 10.00
```

**Mock:** Verifies interactions
```python
def test_with_mock():
    mock_service = Mock()
    process_order(mock_service, order_id=1)
    mock_service.send_email.assert_called_once()
```

**Fake:** Working implementation
```python
class FakeDatabase:
    def __init__(self):
        self.data = {}

    def save(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)
```

## Coverage Reports

### Interpreting Coverage

**Good Coverage (>80%):**
- Most code is tested
- Critical paths have 100% coverage
- Edge cases are covered

**Coverage Gaps:**
- Red/uncovered lines need tests
- Yellow/partial branches need edge case tests
- Complex functions with low coverage are risky

**Coverage Is Not Quality:**
- 90% coverage with bad tests < 70% with good tests
- Focus on testing behavior, not just lines

### Improving Coverage

1. **Identify untested code** from coverage report
2. **Prioritize critical code** (payments, auth, data operations)
3. **Write tests for uncovered lines**
4. **Add edge case tests** for partial branches
5. **Refactor untestable code** (make it more testable)

**Example Workflow:**
```bash
# Generate coverage report
pytest --cov=src --cov-report=html

# Open report
open htmlcov/index.html

# Identify gaps (look for red lines)
# Write tests for uncovered code
# Re-run coverage
pytest --cov=src --cov-report=term

# Verify improvement
```

## Quality Checklist

Before considering unit tests complete:

- [ ] All public functions/methods have tests
- [ ] Happy path tested for each function
- [ ] Edge cases tested (empty, null, boundary values)
- [ ] Error conditions tested (exceptions, invalid inputs)
- [ ] External dependencies are mocked
- [ ] Tests use arrange-act-assert structure
- [ ] Test names are descriptive
- [ ] Tests are independent (can run in any order)
- [ ] Tests are fast (<1s each)
- [ ] Coverage is >80% (>90% for critical modules)
- [ ] Coverage report reviewed for gaps
- [ ] No flaky tests (100% pass rate)

## Reference Material

For detailed patterns and examples, see:
- [Test Patterns](references/test_patterns.md)
- [Mocking Guide](references/mocking_guide.md)
- [Coverage Best Practices](references/coverage_best_practices.md)

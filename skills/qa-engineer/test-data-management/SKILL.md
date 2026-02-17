---
name: test-data-management
description: |
  Creates and manages test data infrastructure including factory classes, database seeding,
  mock data generation, and test fixtures. Implements patterns for consistent, isolated,
  realistic test data across all testing layers using factory_boy, Faker, and builder patterns.
  Use when working with test data, fixtures, seeding test databases, creating data factories,
  mock data generation, pytest fixtures, test setup/teardown, or when the user mentions
  test data management, factory patterns, database seeding, or test data isolation.
---

# Test Data Management

## Overview

This skill enables building robust test data systems that provide consistent, isolated, and realistic test data across all testing layers (unit, integration, E2E). It covers factory patterns, database seeding, mock data generation, and data isolation strategies.

## Output Location

**Default Output Location**: Unless specified by the user, save all output files (factory classes, seeding scripts, fixtures) to `~/Documents/claude-code-skills-data/test-data-management/` directory. Create the directory if it doesn't exist.

## Workflow

Follow this sequential process for implementing test data management:

### 1. Analyze Data Models and Needs

Start by understanding what data the tests require:

1. **Identify entities**: List all models/entities that need test data (User, Post, Order, etc.)
2. **Map relationships**: Document foreign keys, one-to-many, many-to-many relationships
3. **Identify test scenarios**: List different test cases and their data requirements
4. **Determine data volume**: Understand if tests need 1, 10, or 1000+ records

### 2. Choose Tools and Setup

Select appropriate tools based on the technology stack:

**Python:**
- `factory_boy` - Primary tool for factory classes
- `Faker` - Generate realistic mock data (names, emails, addresses, dates)
- `pytest-factoryboy` - Integration with pytest fixtures

**JavaScript/TypeScript:**
- `@faker-js/faker` - Mock data generation
- Custom factory functions or libraries like `fishery`
- `jest` or `vitest` fixtures

**Installation (Python example):**
```bash
pip install factory-boy faker pytest-factoryboy
```

### 3. Create Factory Classes

Build factory classes for each entity with realistic defaults and relationship support.

#### Basic Factory Pattern (Python)

```python
# tests/factories/user_factory.py
import factory
from factory import Faker
from app.models import User

class UserFactory(factory.Factory):
    class Meta:
        model = User

    # Auto-increment ID
    id = factory.Sequence(lambda n: n)

    # Realistic generated data using Faker
    username = Faker('user_name')
    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')

    # Sensible defaults
    is_active = True
    is_staff = False

    # Generated date in the past year
    created_at = Faker('date_time_this_year')
```

#### Factory with Relationships

```python
# tests/factories/post_factory.py
import factory
from factory import Faker, LazyFunction
from app.models import Post
from .user_factory import UserFactory

class PostFactory(factory.Factory):
    class Meta:
        model = Post

    title = Faker('sentence', nb_words=6)
    content = Faker('paragraph', nb_sentences=5)

    # Related object - creates a new User automatically
    author = factory.SubFactory(UserFactory)

    # Generated list
    tags = LazyFunction(lambda: [Faker('word').generate() for _ in range(3)])

    published_at = Faker('date_time_this_month')
    view_count = Faker('random_int', min=0, max=1000)
```

#### Factory Usage in Tests

```python
# Usage patterns
def test_user_creation():
    # Generate with defaults
    user = UserFactory()
    assert user.email is not None

    # Override specific fields
    admin = UserFactory(username='admin', is_staff=True, is_superuser=True)
    assert admin.username == 'admin'

    # Create multiple instances
    users = UserFactory.create_batch(10)
    assert len(users) == 10

def test_post_with_author():
    # Create post with auto-generated author
    post = PostFactory()
    assert post.author.email is not None

    # Create multiple posts by same author
    author = UserFactory()
    posts = PostFactory.create_batch(5, author=author)
    assert all(p.author == author for p in posts)
```

### 4. Implement Database Seeding

Create scripts to populate test databases with baseline data.

#### Seeding Script Pattern

```python
# tests/seeds/seed_test_db.py
from tests.factories import UserFactory, PostFactory, CategoryFactory

def seed_database():
    """Seed test database with baseline data for all tests"""

    # Create admin user with known credentials
    admin = UserFactory(
        username='admin',
        email='admin@test.com',
        is_staff=True,
        is_superuser=True
    )

    # Create test users with different roles
    regular_users = UserFactory.create_batch(10, is_staff=False)
    staff_users = UserFactory.create_batch(3, is_staff=True)

    # Create reference data (categories, tags)
    categories = CategoryFactory.create_batch(5)

    # Create posts distributed across users
    for user in regular_users[:5]:
        PostFactory.create_batch(5, author=user)

    print(f"✅ Seeded database:")
    print(f"   - {len(regular_users) + len(staff_users) + 1} users")
    print(f"   - {len(categories)} categories")
    print(f"   - {5 * 5} posts")

if __name__ == '__main__':
    seed_database()
```

#### Database Reset Script

```python
# tests/seeds/reset_test_db.py
from app.database import db
from app.models import User, Post, Category

def reset_database():
    """Clean and reseed test database"""

    # Clear all tables
    db.session.query(Post).delete()
    db.session.query(User).delete()
    db.session.query(Category).delete()
    db.session.commit()

    print("🧹 Database cleared")

    # Re-seed
    from .seed_test_db import seed_database
    seed_database()

if __name__ == '__main__':
    reset_database()
```

### 5. Create Test Fixtures with Setup/Teardown

Implement pytest fixtures that create data before tests and clean up after.

#### Basic Fixture Pattern

```python
# tests/conftest.py
import pytest
from tests.factories import UserFactory, PostFactory

@pytest.fixture
def test_user(db_session):
    """Create a test user, clean up after test"""
    user = UserFactory()
    db_session.add(user)
    db_session.commit()

    yield user  # Test runs here

    # Cleanup
    db_session.delete(user)
    db_session.commit()

@pytest.fixture
def admin_user(db_session):
    """Create an admin user"""
    admin = UserFactory(is_staff=True, is_superuser=True)
    db_session.add(admin)
    db_session.commit()

    yield admin

    db_session.delete(admin)
    db_session.commit()
```

#### Populated Database Fixture

```python
@pytest.fixture
def populated_database(db_session):
    """Seed database with comprehensive test data"""
    users = UserFactory.create_batch(5)
    posts = []

    for user in users:
        user_posts = PostFactory.create_batch(4, author=user)
        posts.extend(user_posts)

    db_session.add_all(users + posts)
    db_session.commit()

    yield {"users": users, "posts": posts}

    # Cleanup
    db_session.query(Post).delete()
    db_session.query(User).delete()
    db_session.commit()

# Usage in tests
def test_with_populated_db(populated_database):
    users = populated_database["users"]
    posts = populated_database["posts"]

    assert len(users) == 5
    assert len(posts) == 20
```

### 6. Implement Data Builders (Optional)

For complex objects requiring multi-step construction, use the builder pattern.

```python
# tests/builders/order_builder.py
from tests.factories import OrderFactory, OrderItemFactory, UserFactory

class OrderBuilder:
    """Builder for complex Order objects with multiple items"""

    def __init__(self):
        self.user = None
        self.items = []
        self.status = 'pending'
        self.discount = 0

    def for_user(self, user):
        self.user = user
        return self

    def with_item(self, product, quantity=1, price=None):
        self.items.append({
            'product': product,
            'quantity': quantity,
            'price': price
        })
        return self

    def with_status(self, status):
        self.status = status
        return self

    def with_discount(self, discount):
        self.discount = discount
        return self

    def build(self):
        if not self.user:
            self.user = UserFactory()

        order = OrderFactory(
            user=self.user,
            status=self.status,
            discount=self.discount
        )

        for item_data in self.items:
            OrderItemFactory(
                order=order,
                product=item_data['product'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )

        return order

# Usage
def test_complex_order():
    product1 = ProductFactory(name='Widget', price=10.00)
    product2 = ProductFactory(name='Gadget', price=25.00)

    order = (OrderBuilder()
        .for_user(UserFactory(email='customer@test.com'))
        .with_item(product1, quantity=2)
        .with_item(product2, quantity=1)
        .with_discount(5.00)
        .with_status('completed')
        .build())

    assert order.total == 40.00  # (10*2 + 25*1) - 5
```

### 7. Ensure Data Isolation

Implement strategies to prevent tests from affecting each other.

#### Strategy 1: Database Transactions (Recommended)

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope='function')
def db_session(db_engine):
    """Create a new database session with rollback for each test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    # Roll back all changes after test
    session.close()
    transaction.rollback()
    connection.close()
```

#### Strategy 2: Unique Identifiers

```python
# Use unique values to avoid collisions
import uuid

class UserFactory(factory.Factory):
    class Meta:
        model = User

    # Guarantee unique email even in parallel tests
    email = factory.LazyFunction(lambda: f"{uuid.uuid4()}@test.com")
    username = factory.LazyFunction(lambda: f"user_{uuid.uuid4().hex[:8]}")
```

#### Strategy 3: Separate Test Database

```python
# tests/conftest.py
@pytest.fixture(scope='session')
def test_database():
    """Use separate database for tests"""
    test_db_url = "postgresql://localhost/myapp_test"

    # Create test database
    engine = create_engine(test_db_url)
    Base.metadata.create_all(engine)

    yield engine

    # Drop test database
    Base.metadata.drop_all(engine)
```

### 8. Mock External Dependencies

Use Faker and factory patterns for external service data.

```python
# Mock external API responses
class ExternalAPIResponseFactory(factory.DictFactory):
    user_id = factory.Sequence(lambda n: n)
    status = "success"
    data = factory.LazyFunction(lambda: {
        "name": Faker('name').generate(),
        "location": Faker('city').generate(),
        "timestamp": Faker('iso8601').generate()
    })

# Usage in tests
def test_external_api_integration(mock_api):
    response = ExternalAPIResponseFactory()
    mock_api.return_value = response

    result = service.fetch_user_data(user_id=1)
    assert result['status'] == 'success'
```

## Common Patterns

### Pattern: Minimal vs. Complete Data

**Minimal factories** - Only required fields:
```python
class MinimalUserFactory(factory.Factory):
    class Meta:
        model = User

    email = Faker('email')
    # Only required fields
```

**Complete factories** - All fields with realistic data:
```python
class CompleteUserFactory(factory.Factory):
    class Meta:
        model = User

    email = Faker('email')
    first_name = Faker('first_name')
    last_name = Faker('last_name')
    phone = Faker('phone_number')
    address = Faker('address')
    bio = Faker('paragraph')
    # All fields populated
```

Use minimal factories by default, complete factories when testing specific features.

### Pattern: State-Based Factories

Create variants for different states:

```python
class UserFactory(factory.Factory):
    class Meta:
        model = User

    @classmethod
    def active(cls):
        return cls(is_active=True, verified=True)

    @classmethod
    def inactive(cls):
        return cls(is_active=False)

    @classmethod
    def admin(cls):
        return cls(is_staff=True, is_superuser=True)

# Usage
active_user = UserFactory.active()
admin_user = UserFactory.admin()
```

### Pattern: Trait-Based Factories

```python
class PostFactory(factory.Factory):
    class Meta:
        model = Post

    class Params:
        # Traits
        published = factory.Trait(
            status='published',
            published_at=Faker('date_time_this_month')
        )
        draft = factory.Trait(
            status='draft',
            published_at=None
        )
        featured = factory.Trait(
            is_featured=True,
            featured_at=Faker('date_time_this_week')
        )

# Usage
draft_post = PostFactory(draft=True)
featured_post = PostFactory(published=True, featured=True)
```

## Quality Standards

Ensure test data management meets these criteria:

**Factory Coverage:**
- [ ] Factory class exists for every major entity
- [ ] All relationships are properly modeled (SubFactory)
- [ ] Factories use realistic data (Faker)
- [ ] Factories support easy overrides

**Data Isolation:**
- [ ] Tests don't share data (use transactions or unique IDs)
- [ ] Database is cleaned between tests
- [ ] Parallel tests don't interfere with each other

**Performance:**
- [ ] Factory generation is fast (<100ms per object)
- [ ] Database seeding completes quickly (<5s)
- [ ] Minimal data created (don't over-seed)

**Maintainability:**
- [ ] Factory usage is documented
- [ ] Seeding scripts are automated
- [ ] Fixtures are reusable across tests
- [ ] Clear setup/teardown patterns

**Realism:**
- [ ] Generated data looks realistic (proper names, emails, dates)
- [ ] Data relationships make sense
- [ ] Edge cases are covered (empty strings, nulls, special chars)

## Troubleshooting

### Issue: Tests are slow due to data creation

**Solution:** Use database transactions to avoid committing data:
```python
@pytest.fixture
def db_session():
    transaction = db.begin_nested()
    yield db
    transaction.rollback()
```

### Issue: Tests fail intermittently due to unique constraint violations

**Solution:** Use UUIDs or Sequences for unique fields:
```python
email = factory.LazyFunction(lambda: f"{uuid.uuid4()}@test.com")
```

### Issue: Factories create too much related data

**Solution:** Use `build()` instead of `create()` or lazy evaluation:
```python
# Doesn't save to database
user = UserFactory.build()

# Only creates User, not related objects
post = PostFactory(author=user)
```

## File Organization

Organize test data files following this structure:

```
tests/
├── factories/
│   ├── __init__.py          # Export all factories
│   ├── user_factory.py
│   ├── post_factory.py
│   └── order_factory.py
├── fixtures/
│   └── conftest.py          # Pytest fixtures
├── seeds/
│   ├── seed_test_db.py      # Database seeding
│   └── reset_test_db.py     # Database reset
├── builders/                 # Optional: Complex builders
│   └── order_builder.py
└── utils/
    └── data_helpers.py       # Shared utilities
```

## References

**Key Libraries:**
- **factory_boy**: https://factoryboy.readthedocs.io/
- **Faker**: https://faker.readthedocs.io/
- **pytest-factoryboy**: https://pytest-factoryboy.readthedocs.io/

**Faker Providers** (commonly used):
- `Faker('name')` - Full name
- `Faker('email')` - Email address
- `Faker('user_name')` - Username
- `Faker('paragraph')` - Lorem ipsum text
- `Faker('date_time_this_year')` - Random datetime
- `Faker('random_int', min=0, max=100)` - Random integer
- `Faker('url')` - Random URL
- `Faker('phone_number')` - Phone number
- `Faker('address')` - Street address
- `Faker('company')` - Company name

See full list: https://faker.readthedocs.io/en/master/providers.html

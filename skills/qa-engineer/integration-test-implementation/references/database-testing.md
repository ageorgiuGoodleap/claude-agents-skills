# Database Testing Patterns

## Overview

Database integration tests verify that data persistence, retrieval, and manipulation work correctly with a real database. These tests ensure data integrity, constraint enforcement, and proper transaction handling.

## Test Database Setup

### PostgreSQL with Pytest

```python
# conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base

@pytest.fixture(scope="session")
def db_engine():
    """Create test database engine"""
    engine = create_engine('postgresql://test:test@localhost/testdb')
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Provide clean database session per test"""
    connection = db_engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    yield session

    session.close()
    transaction.rollback()
    connection.close()
```

### MongoDB with Pytest

```python
@pytest.fixture(scope="session")
def mongo_client():
    """Create test MongoDB client"""
    client = MongoClient('mongodb://localhost:27017/')
    db = client['test_database']
    yield db
    client.drop_database('test_database')
    client.close()

@pytest.fixture
def clean_collections(mongo_client):
    """Clean all collections before each test"""
    for collection in mongo_client.list_collection_names():
        mongo_client[collection].delete_many({})
```

## CRUD Testing Patterns

### Create Operations

```python
def test_create_user(db_session):
    """Test user creation"""
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password'
    )
    db_session.add(user)
    db_session.commit()

    # Verify creation
    assert user.id is not None
    assert user.created_at is not None

    # Verify retrieval
    retrieved = db_session.query(User).filter_by(email='test@example.com').first()
    assert retrieved.username == 'testuser'
```

### Read Operations

```python
def test_query_users_by_criteria(db_session):
    """Test complex query with filters"""
    # Setup: Create test data
    users = [
        User(username='user1', email='user1@example.com', is_active=True),
        User(username='user2', email='user2@example.com', is_active=False),
        User(username='user3', email='user3@example.com', is_active=True),
    ]
    db_session.add_all(users)
    db_session.commit()

    # Test query
    active_users = db_session.query(User).filter_by(is_active=True).all()
    assert len(active_users) == 2
    assert all(user.is_active for user in active_users)
```

### Update Operations

```python
def test_update_user(db_session):
    """Test user update"""
    user = User(username='testuser', email='test@example.com')
    db_session.add(user)
    db_session.commit()

    user_id = user.id

    # Update
    user.username = 'updated_user'
    db_session.commit()

    # Verify update
    updated = db_session.query(User).get(user_id)
    assert updated.username == 'updated_user'
    assert updated.email == 'test@example.com'  # Unchanged
```

### Delete Operations

```python
def test_delete_user(db_session):
    """Test user deletion"""
    user = User(username='testuser', email='test@example.com')
    db_session.add(user)
    db_session.commit()

    user_id = user.id

    # Delete
    db_session.delete(user)
    db_session.commit()

    # Verify deletion
    deleted = db_session.query(User).get(user_id)
    assert deleted is None
```

## Relationship Testing

### One-to-Many Relationships

```python
def test_one_to_many_relationship(db_session):
    """Test user-posts relationship"""
    user = User(username='testuser', email='test@example.com')
    post1 = Post(title='Post 1', content='Content 1', author=user)
    post2 = Post(title='Post 2', content='Content 2', author=user)

    db_session.add_all([user, post1, post2])
    db_session.commit()

    # Verify relationship
    retrieved_user = db_session.query(User).filter_by(username='testuser').first()
    assert len(retrieved_user.posts) == 2
    assert post1 in retrieved_user.posts
    assert post2 in retrieved_user.posts
```

### Many-to-Many Relationships

```python
def test_many_to_many_relationship(db_session):
    """Test user-roles relationship"""
    user1 = User(username='user1')
    user2 = User(username='user2')
    role1 = Role(name='admin')
    role2 = Role(name='editor')

    user1.roles.extend([role1, role2])
    user2.roles.append(role1)

    db_session.add_all([user1, user2, role1, role2])
    db_session.commit()

    # Verify relationships
    admin_role = db_session.query(Role).filter_by(name='admin').first()
    assert len(admin_role.users) == 2
    assert user1 in admin_role.users
    assert user2 in admin_role.users
```

### Cascade Deletes

```python
def test_cascade_delete(db_session):
    """Test cascading deletion"""
    user = User(username='testuser')
    post = Post(title='Post', author=user)
    comment = Comment(content='Comment', post=post)

    db_session.add_all([user, post, comment])
    db_session.commit()

    # Delete user (should cascade to posts and comments)
    db_session.delete(user)
    db_session.commit()

    # Verify cascade
    assert db_session.query(Post).count() == 0
    assert db_session.query(Comment).count() == 0
```

## Transaction Testing

### Commit and Rollback

```python
def test_transaction_commit(db_session):
    """Test transaction commit"""
    user = User(username='testuser', email='test@example.com')
    db_session.add(user)
    db_session.commit()

    # Verify persistence after commit
    assert db_session.query(User).filter_by(username='testuser').first() is not None

def test_transaction_rollback(db_session):
    """Test transaction rollback"""
    user = User(username='testuser', email='test@example.com')
    db_session.add(user)
    db_session.rollback()

    # Verify no persistence after rollback
    assert db_session.query(User).filter_by(username='testuser').first() is None
```

### Nested Transactions

```python
def test_nested_transactions(db_session):
    """Test savepoint functionality"""
    user1 = User(username='user1')
    db_session.add(user1)
    db_session.commit()

    # Start nested transaction
    nested = db_session.begin_nested()

    user2 = User(username='user2')
    db_session.add(user2)
    nested.rollback()

    # user1 persists, user2 does not
    assert db_session.query(User).filter_by(username='user1').first() is not None
    assert db_session.query(User).filter_by(username='user2').first() is None
```

## Constraint Testing

### Unique Constraints

```python
def test_unique_constraint(db_session):
    """Test unique email constraint"""
    from sqlalchemy.exc import IntegrityError

    user1 = User(username='user1', email='test@example.com')
    db_session.add(user1)
    db_session.commit()

    user2 = User(username='user2', email='test@example.com')
    db_session.add(user2)

    with pytest.raises(IntegrityError):
        db_session.commit()
```

### Foreign Key Constraints

```python
def test_foreign_key_constraint(db_session):
    """Test foreign key enforcement"""
    from sqlalchemy.exc import IntegrityError

    # Create post without user (should fail)
    post = Post(title='Post', author_id=999)
    db_session.add(post)

    with pytest.raises(IntegrityError):
        db_session.commit()
```

### Not Null Constraints

```python
def test_not_null_constraint(db_session):
    """Test not null constraint"""
    from sqlalchemy.exc import IntegrityError

    user = User(username='testuser')  # Missing required email
    db_session.add(user)

    with pytest.raises(IntegrityError):
        db_session.commit()
```

### Check Constraints

```python
def test_check_constraint(db_session):
    """Test check constraint (e.g., age >= 0)"""
    from sqlalchemy.exc import IntegrityError

    user = User(username='testuser', email='test@example.com', age=-5)
    db_session.add(user)

    with pytest.raises(IntegrityError):
        db_session.commit()
```

## Query Performance Testing

### N+1 Query Problem

```python
def test_eager_loading_prevents_n_plus_1(db_session):
    """Test that eager loading is used"""
    from sqlalchemy.orm import joinedload

    # Setup: Create users with posts
    for i in range(5):
        user = User(username=f'user{i}')
        for j in range(3):
            post = Post(title=f'Post {j}', author=user)
            db_session.add(post)
        db_session.add(user)
    db_session.commit()

    # Query with eager loading
    users = db_session.query(User).options(joinedload(User.posts)).all()

    # Access posts (should not trigger additional queries)
    for user in users:
        _ = user.posts
```

### Bulk Operations

```python
def test_bulk_insert(db_session):
    """Test bulk insert performance"""
    users = [
        User(username=f'user{i}', email=f'user{i}@example.com')
        for i in range(1000)
    ]

    db_session.bulk_save_objects(users)
    db_session.commit()

    assert db_session.query(User).count() == 1000
```

## Data Integrity Testing

### Concurrent Modifications

```python
def test_optimistic_locking(db_session):
    """Test version-based optimistic locking"""
    user = User(username='testuser', email='test@example.com', version=1)
    db_session.add(user)
    db_session.commit()

    # Simulate concurrent modification
    user.username = 'updated'
    user.version = 2

    # Meanwhile, another transaction updated the user
    db_session.execute(
        "UPDATE users SET username='conflict', version=2 WHERE id=:id",
        {'id': user.id}
    )

    with pytest.raises(Exception):  # Optimistic lock exception
        db_session.commit()
```

### Data Validation

```python
def test_email_format_validation(db_session):
    """Test email format validation at database level"""
    user = User(username='testuser', email='invalid-email')
    db_session.add(user)

    with pytest.raises(Exception):  # Validation error
        db_session.commit()
```

## Testing Best Practices

1. **Use Transactions for Isolation**
   - Each test should run in its own transaction
   - Rollback after each test to ensure clean state

2. **Seed Minimal Data**
   - Only create data needed for the specific test
   - Avoid large fixture files that slow down tests

3. **Test Constraints**
   - Verify unique constraints
   - Test foreign key relationships
   - Validate check constraints

4. **Test Edge Cases**
   - Null values
   - Empty strings
   - Maximum lengths
   - Boundary values

5. **Performance Considerations**
   - Use in-memory databases for unit tests
   - Run integration tests against real database
   - Test query performance for critical paths

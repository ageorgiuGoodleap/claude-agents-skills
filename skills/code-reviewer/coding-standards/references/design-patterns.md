# Design and Architecture Patterns to Enforce Simplicity

Use these patterns as decision rules, not excuses to over-engineer. Add structure only when needed.

## 1. When to Add Structure

Add architectural patterns and abstractions ONLY when one of these is true:

### You Need Testability and Isolation of Side Effects
* Core logic mixed with I/O, HTTP, database calls is hard to test
* Pure functions are easier to test and reason about
* Separate "what to do" (domain logic) from "how to do it" (infrastructure)

### You Expect Multiple Implementations of a Dependency
* Database could be PostgreSQL, MySQL, or in-memory for tests
* Email service could be SendGrid, AWS SES, or mock for development
* Payment processor could be Stripe, PayPal, or test implementation

### You Need a Stable Boundary Between Domain Logic and Infrastructure
* Domain logic should not depend on framework specifics
* Business rules should not change when you swap databases or web frameworks
* Ports and adapters pattern creates stable interfaces

### You Are NOT Adding Structure If:
* You have a single implementation and no plans for more
* The code is already testable and simple
* You are "future-proofing" against hypothetical requirements
* You are following a pattern because it feels professional

## 2. Practical Patterns That Stay Simple

### 2.1 Dependency Injection (DI)

**What**: Pass dependencies explicitly rather than importing globals or singletons.

**Why**: Makes dependencies visible, testable, and swappable.

**Python Example**:
```python
# Bad - hidden global dependency
import database

def create_order(user_id: int, items: list[Item]) -> Order:
    order = Order(user_id=user_id, items=items)
    database.save(order)  # Hidden dependency
    return order

# Good - explicit dependency injection
def create_order(user_id: int, items: list[Item], db: Database) -> Order:
    order = Order(user_id=user_id, items=items)
    db.save(order)  # Dependency passed in
    return order

# Usage
db = PostgresDatabase()
order = create_order(user_id=123, items=[...], db=db)

# Testing
mock_db = MockDatabase()
order = create_order(user_id=123, items=[...], db=mock_db)
```

**TypeScript Example**:
```typescript
// Bad - hidden global dependency
import { database } from './database';

function createOrder(userId: number, items: Item[]): Order {
  const order = new Order(userId, items);
  database.save(order);  // Hidden dependency
  return order;
}

// Good - explicit dependency injection
interface Database {
  save(order: Order): Promise<void>;
}

function createOrder(userId: number, items: Item[], db: Database): Order {
  const order = new Order(userId, items);
  db.save(order);  // Dependency passed in
  return order;
}

// Usage
const db = new PostgresDatabase();
const order = createOrder(123, [...], db);

// Testing
const mockDb = new MockDatabase();
const order = createOrder(123, [...], mockDb);
```

### 2.2 Ports and Adapters (Hexagonal Architecture)

**What**: Domain defines interfaces (ports), infrastructure implements them (adapters).

**Why**: Domain logic stays pure and framework-agnostic. Infrastructure is swappable.

**Structure**:
* **Domain**: Business logic, entities, interfaces (ports)
* **Application**: Use cases, orchestration
* **Infrastructure**: Adapters for database, HTTP, email, etc.

**Python Example**:
```python
# Domain layer - defines interface (port)
from abc import ABC, abstractmethod

class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None:
        pass

    @abstractmethod
    def find_by_id(self, order_id: int) -> Order | None:
        pass

# Domain service - uses interface
class OrderService:
    def __init__(self, repository: OrderRepository):
        self.repository = repository

    def create_order(self, user_id: int, items: list[Item]) -> Order:
        order = Order(user_id=user_id, items=items)
        self.repository.save(order)
        return order

# Infrastructure layer - implements interface (adapter)
class PostgresOrderRepository(OrderRepository):
    def __init__(self, connection):
        self.connection = connection

    def save(self, order: Order) -> None:
        self.connection.execute("INSERT INTO orders ...")

    def find_by_id(self, order_id: int) -> Order | None:
        result = self.connection.execute("SELECT * FROM orders WHERE id = ?", [order_id])
        return Order.from_dict(result) if result else None

# Usage
repository = PostgresOrderRepository(db_connection)
service = OrderService(repository)
order = service.create_order(user_id=123, items=[...])
```

**TypeScript Example**:
```typescript
// Domain layer - defines interface (port)
interface OrderRepository {
  save(order: Order): Promise<void>;
  findById(orderId: number): Promise<Order | null>;
}

// Domain service - uses interface
class OrderService {
  constructor(private repository: OrderRepository) {}

  async createOrder(userId: number, items: Item[]): Promise<Order> {
    const order = new Order(userId, items);
    await this.repository.save(order);
    return order;
  }
}

// Infrastructure layer - implements interface (adapter)
class PostgresOrderRepository implements OrderRepository {
  constructor(private db: Database) {}

  async save(order: Order): Promise<void> {
    await this.db.query('INSERT INTO orders ...');
  }

  async findById(orderId: number): Promise<Order | null> {
    const result = await this.db.query('SELECT * FROM orders WHERE id = $1', [orderId]);
    return result ? Order.fromDict(result) : null;
  }
}

// Usage
const repository = new PostgresOrderRepository(dbConnection);
const service = new OrderService(repository);
const order = await service.createOrder(123, [...]);
```

### 2.3 Strategy Pattern

**What**: Select behavior by injected function or object rather than conditionals scattered everywhere.

**Why**: Eliminates complex if/else chains. Makes behavior swappable and testable.

**Python Example**:
```python
# Bad - scattered conditionals
def calculate_shipping(order: Order, country: str) -> float:
    if country == 'US':
        return order.total * 0.05
    elif country == 'EU':
        return order.total * 0.10
    elif country == 'ASIA':
        return order.total * 0.15
    else:
        return order.total * 0.20

# Good - strategy pattern
from abc import ABC, abstractmethod

class ShippingStrategy(ABC):
    @abstractmethod
    def calculate(self, order: Order) -> float:
        pass

class USShipping(ShippingStrategy):
    def calculate(self, order: Order) -> float:
        return order.total * 0.05

class EUShipping(ShippingStrategy):
    def calculate(self, order: Order) -> float:
        return order.total * 0.10

# Usage
strategy = USShipping()
shipping_cost = strategy.calculate(order)
```

**TypeScript Example**:
```typescript
// Strategy interface
interface ShippingStrategy {
  calculate(order: Order): number;
}

class USShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.total * 0.05;
  }
}

class EUShipping implements ShippingStrategy {
  calculate(order: Order): number {
    return order.total * 0.10;
  }
}

// Context
class OrderProcessor {
  constructor(private shippingStrategy: ShippingStrategy) {}

  processOrder(order: Order): number {
    const shipping = this.shippingStrategy.calculate(order);
    return order.total + shipping;
  }
}

// Usage
const processor = new OrderProcessor(new USShipping());
const total = processor.processOrder(order);
```

### 2.4 State Modeling with Explicit State Machines

**What**: Model state transitions explicitly with exhaustive handling.

**Why**: Makes legal states representable and illegal states impossible. Compiler enforces completeness.

**Python Example**:
```python
from enum import Enum, auto
from dataclasses import dataclass

class OrderStatus(Enum):
    PENDING = auto()
    PAID = auto()
    SHIPPED = auto()
    DELIVERED = auto()
    CANCELLED = auto()

@dataclass
class Order:
    id: int
    status: OrderStatus

    def pay(self) -> 'Order':
        if self.status != OrderStatus.PENDING:
            raise ValueError(f"Cannot pay order in status {self.status}")
        return Order(id=self.id, status=OrderStatus.PAID)

    def ship(self) -> 'Order':
        if self.status != OrderStatus.PAID:
            raise ValueError(f"Cannot ship order in status {self.status}")
        return Order(id=self.id, status=OrderStatus.SHIPPED)

    def deliver(self) -> 'Order':
        if self.status != OrderStatus.SHIPPED:
            raise ValueError(f"Cannot deliver order in status {self.status}")
        return Order(id=self.id, status=OrderStatus.DELIVERED)

    def cancel(self) -> 'Order':
        if self.status in [OrderStatus.DELIVERED, OrderStatus.CANCELLED]:
            raise ValueError(f"Cannot cancel order in status {self.status}")
        return Order(id=self.id, status=OrderStatus.CANCELLED)
```

**TypeScript Example** (using discriminated unions):
```typescript
type OrderState =
  | { status: 'pending'; id: number }
  | { status: 'paid'; id: number; paymentId: string }
  | { status: 'shipped'; id: number; paymentId: string; trackingNumber: string }
  | { status: 'delivered'; id: number; paymentId: string; trackingNumber: string }
  | { status: 'cancelled'; id: number; reason: string };

function payOrder(order: OrderState, paymentId: string): OrderState {
  if (order.status !== 'pending') {
    throw new Error(`Cannot pay order in status ${order.status}`);
  }
  return { status: 'paid', id: order.id, paymentId };
}

function shipOrder(order: OrderState, trackingNumber: string): OrderState {
  if (order.status !== 'paid') {
    throw new Error(`Cannot ship order in status ${order.status}`);
  }
  return { status: 'shipped', id: order.id, paymentId: order.paymentId, trackingNumber };
}

// TypeScript enforces exhaustiveness
function getOrderSummary(order: OrderState): string {
  switch (order.status) {
    case 'pending':
      return `Order ${order.id} is pending`;
    case 'paid':
      return `Order ${order.id} is paid (${order.paymentId})`;
    case 'shipped':
      return `Order ${order.id} is shipped (${order.trackingNumber})`;
    case 'delivered':
      return `Order ${order.id} is delivered`;
    case 'cancelled':
      return `Order ${order.id} is cancelled: ${order.reason}`;
    // If you add a new status, TypeScript will error here until you handle it
  }
}
```

## 3. Architectural Defaults

### 3.1 Layered Architecture

**Structure**: Organize code into layers with clear responsibilities.

**Layers**:
1. **Domain**: Business entities, rules, interfaces (no framework dependencies)
2. **Application**: Use cases, orchestration, application services
3. **Infrastructure**: Adapters for database, HTTP, email, external services
4. **Presentation**: Controllers, API endpoints, UI (web framework specific)

**Dependency Rule**: Outer layers depend on inner layers, never the reverse.
* Presentation → Application → Domain
* Infrastructure → Domain (implements domain interfaces)

**Python Project Structure**:
```
src/
├── domain/
│   ├── entities/
│   ├── repositories/  # Interfaces only
│   └── services/
├── application/
│   └── use_cases/
├── infrastructure/
│   ├── database/
│   ├── email/
│   └── repositories/  # Implementations
└── presentation/
    └── api/
```

**TypeScript Project Structure**:
```
src/
├── domain/
│   ├── entities/
│   ├── repositories/  # Interfaces only
│   └── services/
├── application/
│   └── use-cases/
├── infrastructure/
│   ├── database/
│   ├── email/
│   └── repositories/  # Implementations
└── presentation/
    └── api/
```

### 3.2 Keep Domain Logic Free of Frameworks

* Domain entities and services should not import web frameworks, ORMs, or external libraries
* Domain defines interfaces, infrastructure implements them
* Allows you to swap frameworks without rewriting business logic

**Example**: Domain entity should not know about Django, Flask, FastAPI, Express, etc.

```python
# Bad - domain depends on framework
from django.db import models

class Order(models.Model):  # Coupled to Django ORM
    user_id = models.IntegerField()
    total = models.DecimalField()

# Good - domain is framework-agnostic
from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Order:
    id: int
    user_id: int
    total: Decimal
```

### 3.3 Twelve-Factor App Principles (for services)

Apply twelve-factor methodology when building services or applications:

1. **Codebase**: One codebase tracked in version control, many deploys
2. **Dependencies**: Explicitly declare and isolate dependencies
3. **Config**: Store config in environment variables, not code
4. **Backing services**: Treat databases, queues, caches as attached resources
5. **Build, release, run**: Strictly separate build and run stages
6. **Processes**: Execute app as stateless processes
7. **Port binding**: Export services via port binding
8. **Concurrency**: Scale out via the process model
9. **Disposability**: Fast startup and graceful shutdown
10. **Dev/prod parity**: Keep development, staging, production as similar as possible
11. **Logs**: Treat logs as event streams
12. **Admin processes**: Run admin tasks as one-off processes

Reference: https://12factor.net/

## 4. Decision Tree: Do I Need a Pattern?

Use this decision tree before adding architectural complexity:

```
Is the code hard to test?
├─ YES → Consider dependency injection or ports/adapters
└─ NO → Keep it simple

Do I have complex conditional logic that is duplicated?
├─ YES → Consider strategy pattern or state machine
└─ NO → Keep it simple

Do I need to swap implementations (database, email, payment, etc.)?
├─ YES → Use dependency injection + interfaces (ports/adapters)
└─ NO → Keep it simple

Is my domain logic coupled to framework code?
├─ YES → Separate domain from infrastructure (layered architecture)
└─ NO → Keep it simple

Am I adding this pattern "just in case" or for future requirements?
├─ YES → DO NOT add it. Wait until you need it.
└─ NO → Proceed carefully
```

## 5. Anti-Patterns to Avoid

### Over-Engineering
* Adding abstractions before you need them
* Creating interfaces with a single implementation and no plans for more
* Using design patterns to look professional, not to solve a problem

### Premature Abstraction
* "I might need to support MongoDB later" (but you don't right now)
* Creating generic solutions for specific problems
* YAGNI: You Aren't Gonna Need It

### Anemic Domain Model
* Domain objects with no behavior, only getters/setters
* All logic in service layer, domain is just data containers
* Solution: Put behavior in domain entities where it belongs

### God Object
* One class/module that does everything
* Violates single responsibility principle
* Solution: Break into focused, cohesive units

### Shotgun Surgery
* One change requires modifying many unrelated files
* Sign of poor cohesion
* Solution: Group related functionality together

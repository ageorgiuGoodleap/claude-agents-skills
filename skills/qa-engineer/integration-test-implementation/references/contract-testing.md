# Contract Testing

## Overview

Contract testing ensures that services communicate correctly by verifying that consumers and providers agree on API contracts. This prevents integration failures when services evolve independently.

## What is Contract Testing?

**Traditional Integration Testing:**
- Test full integration between services
- Requires all services to be running
- Slow and brittle
- Catches issues late

**Contract Testing:**
- Test service boundaries independently
- Consumers define expected contracts
- Providers verify they meet contracts
- Fast and reliable
- Catches issues early

## Consumer-Driven Contract Testing (Pact)

### Consumer Side

The consumer defines what it expects from the provider.

```python
# consumer_tests/test_payment_service.py
from pact import Consumer, Provider
import pytest

pact = Consumer('OrderService').has_pact_with(Provider('PaymentService'))

@pytest.fixture(scope='module')
def payment_service():
    """Start Pact mock service"""
    pact.start_service()
    yield pact
    pact.stop_service()

def test_process_payment(payment_service):
    """Consumer expects payment processing endpoint"""
    expected = {
        'payment_id': '12345',
        'status': 'completed',
        'amount': 100.00
    }

    (pact
     .given('user account has sufficient funds')
     .upon_receiving('a payment request')
     .with_request(method='POST', path='/payments', body={
         'amount': 100.00,
         'currency': 'USD',
         'user_id': '123'
     })
     .will_respond_with(status=200, body=expected))

    with pact:
        # Make actual request to mock service
        response = payment_client.process_payment(100.00, 'USD', '123')

        assert response['status'] == 'completed'
        assert response['payment_id'] == '12345'

def test_process_payment_insufficient_funds(payment_service):
    """Consumer expects error when insufficient funds"""
    (pact
     .given('user account has insufficient funds')
     .upon_receiving('a payment request')
     .with_request(method='POST', path='/payments', body={
         'amount': 100.00,
         'currency': 'USD',
         'user_id': '123'
     })
     .will_respond_with(status=402, body={
         'error': 'Insufficient funds',
         'code': 'INSUFFICIENT_FUNDS'
     }))

    with pact:
        with pytest.raises(InsufficientFundsError):
            payment_client.process_payment(100.00, 'USD', '123')
```

### Provider Side

The provider verifies it meets all consumer contracts.

```python
# provider_tests/test_payment_provider.py
from pact import Verifier

def test_payment_service_provider():
    """Verify provider meets all consumer contracts"""
    verifier = Verifier(
        provider='PaymentService',
        provider_base_url='http://localhost:8000'
    )

    # Setup provider state
    def provider_states():
        return {
            'user account has sufficient funds': setup_sufficient_funds,
            'user account has insufficient funds': setup_insufficient_funds
        }

    def setup_sufficient_funds():
        """Setup: Create user with sufficient funds"""
        db.create_user(id='123', balance=1000.00)

    def setup_insufficient_funds():
        """Setup: Create user with insufficient funds"""
        db.create_user(id='123', balance=0.00)

    # Verify against published pacts
    success, logs = verifier.verify_pacts(
        './pacts/orderservice-paymentservice.json',
        provider_states_setup_url='http://localhost:8000/setup-states',
        enable_pending=False,
        verbose=True
    )

    assert success
```

## TypeScript/JavaScript Contract Testing

### Consumer (Jest + Pact)

```typescript
// consumer.spec.ts
import { pactWith } from 'jest-pact';
import { PaymentClient } from '../payment-client';

pactWith({ consumer: 'OrderService', provider: 'PaymentService' }, (provider) => {
  let client: PaymentClient;

  beforeEach(() => {
    client = new PaymentClient(provider.mockService.baseUrl);
  });

  describe('process payment', () => {
    beforeEach(() => {
      const interaction = {
        state: 'user account has sufficient funds',
        uponReceiving: 'a payment request',
        withRequest: {
          method: 'POST',
          path: '/payments',
          headers: { 'Content-Type': 'application/json' },
          body: {
            amount: 100.00,
            currency: 'USD',
            userId: '123'
          }
        },
        willRespondWith: {
          status: 200,
          headers: { 'Content-Type': 'application/json' },
          body: {
            paymentId: '12345',
            status: 'completed',
            amount: 100.00
          }
        }
      };

      return provider.addInteraction(interaction);
    });

    it('processes payment successfully', async () => {
      const result = await client.processPayment(100.00, 'USD', '123');

      expect(result.status).toBe('completed');
      expect(result.paymentId).toBe('12345');
    });
  });
});
```

### Provider (Pact Verifier)

```typescript
// provider.spec.ts
import { Verifier } from '@pact-foundation/pact';
import { server } from '../server';

describe('Payment Service Provider', () => {
  let app;

  beforeAll(() => {
    app = server.listen(8000);
  });

  afterAll(() => {
    app.close();
  });

  it('validates the expectations of OrderService', () => {
    const opts = {
      provider: 'PaymentService',
      providerBaseUrl: 'http://localhost:8000',
      pactUrls: ['./pacts/orderservice-paymentservice.json'],
      stateHandlers: {
        'user account has sufficient funds': () => {
          // Setup database state
          return db.createUser({ id: '123', balance: 1000.00 });
        },
        'user account has insufficient funds': () => {
          return db.createUser({ id: '123', balance: 0.00 });
        }
      }
    };

    return new Verifier(opts).verifyProvider();
  });
});
```

## Contract Testing Workflow

### 1. Consumer Writes Test

Consumer defines expected API contract:
```python
def test_get_user_by_id(pact):
    (pact
     .given('user 123 exists')
     .upon_receiving('a request for user 123')
     .with_request(method='GET', path='/users/123')
     .will_respond_with(status=200, body={'id': '123', 'name': 'John'}))
```

### 2. Generate Pact File

Running the test generates a pact file:
```json
{
  "consumer": { "name": "OrderService" },
  "provider": { "name": "UserService" },
  "interactions": [
    {
      "description": "a request for user 123",
      "providerState": "user 123 exists",
      "request": {
        "method": "GET",
        "path": "/users/123"
      },
      "response": {
        "status": 200,
        "body": {
          "id": "123",
          "name": "John"
        }
      }
    }
  ]
}
```

### 3. Share Pact File

Options:
- Commit to repository
- Publish to Pact Broker
- Share via artifact storage

### 4. Provider Verifies Contract

Provider runs verification:
```python
verifier.verify_pacts('./pacts/orderservice-userservice.json')
```

If verification fails, provider must:
- Fix the implementation
- Or negotiate contract change with consumer

## Advanced Contract Testing

### Matching Rules

Use matchers for flexible contracts:

```python
from pact import Like, EachLike, Term

(pact
 .upon_receiving('a list of users')
 .with_request(method='GET', path='/users')
 .will_respond_with(status=200, body=EachLike({
     'id': Like('123'),              # Type match (string)
     'email': Term(r'.+@.+\..+', 'test@example.com'),  # Regex match
     'created_at': Term(r'\d{4}-\d{2}-\d{2}', '2024-01-01')
 })))
```

### Provider States

Setup different scenarios:

```python
# Consumer defines state
(pact
 .given('user 123 exists and has orders')
 .upon_receiving('a request for user orders')
 .with_request(method='GET', path='/users/123/orders')
 .will_respond_with(status=200, body=[]))

# Provider handles state
def setup_user_with_orders():
    user = db.create_user(id='123')
    db.create_order(user_id='123', amount=100)
    db.create_order(user_id='123', amount=200)
```

### Request Matching

Match request parameters:

```python
(pact
 .upon_receiving('a search request')
 .with_request(
     method='GET',
     path='/users',
     query={'name': 'John', 'age': Like(30)}
 )
 .will_respond_with(status=200, body=[]))
```

### Headers Matching

Verify headers:

```python
(pact
 .upon_receiving('an authenticated request')
 .with_request(
     method='GET',
     path='/protected',
     headers={'Authorization': Like('Bearer token123')}
 )
 .will_respond_with(status=200))
```

## Pact Broker

### Publishing Pacts

```bash
# Publish consumer pact
pact-broker publish ./pacts \
  --consumer-app-version=1.0.0 \
  --broker-base-url=https://pact-broker.example.com \
  --broker-token=$PACT_BROKER_TOKEN
```

### Retrieving Pacts

```python
# Provider retrieves pacts from broker
verifier.verify_pacts(
    broker_url='https://pact-broker.example.com',
    broker_token=os.getenv('PACT_BROKER_TOKEN'),
    provider_version='2.0.0',
    publish_verification_results=True
)
```

### Can-I-Deploy

Check if safe to deploy:

```bash
# Check if consumer can deploy
pact-broker can-i-deploy \
  --pacticipant=OrderService \
  --version=1.0.0 \
  --to=production
```

## Best Practices

1. **Start Simple**
   - Begin with happy path contracts
   - Add error scenarios gradually
   - Focus on service boundaries

2. **Consumer-Driven**
   - Consumers define contracts they need
   - Don't test provider's full API
   - Only test what you use

3. **Provider States**
   - Keep states minimal
   - Use idempotent setup
   - Clean up after verification

4. **Versioning**
   - Tag pacts with versions
   - Use Pact Broker for management
   - Check compatibility before deployment

5. **CI/CD Integration**
   - Run consumer tests on every commit
   - Publish pacts automatically
   - Verify provider against latest pacts
   - Use can-i-deploy before production

6. **Maintenance**
   - Remove obsolete pacts
   - Keep contracts up to date
   - Version breaking changes carefully

## Common Pitfalls

1. **Over-Specification**
   - Don't match exact values unless necessary
   - Use type matching (Like) for flexible contracts

2. **Testing Too Much**
   - Contract tests verify API contracts, not business logic
   - Keep provider state setup simple

3. **Ignoring Failures**
   - Contract failures indicate breaking changes
   - Address them before deploying

4. **Not Using Pact Broker**
   - Manual pact sharing is error-prone
   - Use Pact Broker for proper versioning

## Tools and Resources

**Python:**
- pact-python - Pact implementation for Python

**JavaScript/TypeScript:**
- @pact-foundation/pact - Pact JS implementation
- jest-pact - Jest integration

**Pact Broker:**
- pactflow.io - Hosted Pact Broker
- pact-broker - Self-hosted option

**Documentation:**
- docs.pact.io - Official Pact documentation

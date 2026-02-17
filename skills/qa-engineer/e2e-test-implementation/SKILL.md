---
name: e2e-test-implementation
description: |
  Build end-to-end test scenarios using Playwright that test complete user workflows through
  the browser with Page Object Model pattern. Use when implementing E2E tests, Playwright tests,
  Cypress tests, browser automation, user flow testing, UI testing, or when testing critical
  paths from the user's perspective with realistic interactions.
---

# E2E Test Implementation

## Overview

This skill enables creating robust, maintainable end-to-end tests using modern browser automation with Playwright. E2E tests verify complete user workflows from the browser perspective, ensuring critical paths work correctly across the full application stack.

## Core Capabilities

**1. Playwright Mastery**
- Browser automation (Chromium, Firefox, WebKit)
- Element interaction (clicks, typing, selections)
- Async handling and waiting strategies
- Screenshot and video capture

**2. Page Object Model**
- Maintainable page abstractions
- Reusable component objects
- Clear separation of test logic and selectors

**3. User Flow Testing**
- Multi-step workflow validation
- Authentication flows
- Form submissions
- Navigation testing

**4. Test Reliability**
- Proper wait strategies
- Error handling
- Flaky test prevention
- Failure debugging with traces

## Workflow

Follow this process when implementing E2E tests:

### 1. Identify Critical User Flows

Prioritize the most important user journeys:
- Authentication (signup, login, logout)
- Core user actions (create, edit, delete)
- Purchase/checkout flows
- Profile management
- Search and filtering

**Example Critical Flows:**
- User signup → email verification → onboarding → first action
- Login → navigate to dashboard → create item → verify item appears
- Add to cart → checkout → payment → order confirmation

### 2. Set Up Playwright Project

**Installation:**
```bash
npm init playwright@latest
```

**Configuration (playwright.config.ts):**
```typescript
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  timeout: 30000,
  expect: {
    timeout: 5000
  },
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['html'],
    ['json', { outputFile: 'test-results/results.json' }]
  ],
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'firefox',
      use: { ...devices['Desktop Firefox'] },
    },
    {
      name: 'webkit',
      use: { ...devices['Desktop Safari'] },
    },
  ],
});
```

### 3. Create Page Object Model

**Structure:**
```
tests/
├── e2e/
│   ├── auth.spec.ts
│   ├── dashboard.spec.ts
│   └── checkout.spec.ts
├── pages/
│   ├── LoginPage.ts
│   ├── DashboardPage.ts
│   └── CheckoutPage.ts
└── fixtures/
    └── test-data.ts
```

**Example Page Object:**
```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.locator('[data-testid="username"]');
    this.passwordInput = page.locator('[data-testid="password"]');
    this.loginButton = page.locator('[data-testid="login-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
  }

  async goto() {
    await this.page.goto('/login');
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
    await this.page.waitForURL('/dashboard');
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }
}
```

**Example Component Object:**
```typescript
// pages/components/NavBar.ts
import { Page, Locator } from '@playwright/test';

export class NavBar {
  readonly page: Page;
  readonly userMenu: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.userMenu = page.locator('[data-testid="user-menu"]');
    this.logoutButton = page.locator('[data-testid="logout-button"]');
  }

  async logout() {
    await this.userMenu.click();
    await this.logoutButton.click();
  }
}
```

### 4. Write E2E Test Scenarios

**Authentication Tests:**
```typescript
// tests/e2e/auth.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

test.describe('User Authentication', () => {
  test('successful login redirects to dashboard', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('testuser', 'password123');

    // Verify redirect
    await expect(page).toHaveURL('/dashboard');
    await expect(page.locator('[data-testid="user-menu"]')).toBeVisible();
  });

  test('invalid credentials show error message', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('testuser', 'wrongpassword');

    // Verify error
    const error = await loginPage.getErrorMessage();
    expect(error).toContain('Invalid credentials');
  });

  test('logout redirects to home page', async ({ page }) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('testuser', 'password123');

    // Logout
    const navBar = new NavBar(page);
    await navBar.logout();

    // Verify redirect to login
    await expect(page).toHaveURL('/');
  });
});
```

**User Flow Tests:**
```typescript
// tests/e2e/dashboard.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';

test.describe('Dashboard Operations', () => {
  test.beforeEach(async ({ page }) => {
    // Setup: Login before each test
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('testuser', 'password123');
  });

  test('create new item', async ({ page }) => {
    const dashboard = new DashboardPage(page);

    // Create item
    await dashboard.clickCreateButton();
    await dashboard.fillItemForm({
      title: 'New Item',
      description: 'Test Description'
    });
    await dashboard.submitForm();

    // Verify item appears
    await expect(page.locator('[data-testid="item-list"]')).toContainText('New Item');
  });

  test('edit existing item', async ({ page }) => {
    const dashboard = new DashboardPage(page);

    // Find and edit item
    await dashboard.clickItemByTitle('Existing Item');
    await dashboard.clickEditButton();
    await dashboard.fillItemForm({ title: 'Updated Item' });
    await dashboard.submitForm();

    // Verify update
    await expect(page.locator('[data-testid="item-list"]')).toContainText('Updated Item');
  });

  test('delete item', async ({ page }) => {
    const dashboard = new DashboardPage(page);

    // Delete item
    await dashboard.clickItemByTitle('Item to Delete');
    await dashboard.clickDeleteButton();
    await dashboard.confirmDeletion();

    // Verify deletion
    await expect(page.locator('[data-testid="item-list"]')).not.toContainText('Item to Delete');
  });
});
```

**Form Validation Tests:**
```typescript
// tests/e2e/forms.spec.ts
test.describe('Form Validation', () => {
  test('shows validation errors for invalid input', async ({ page }) => {
    await page.goto('/create-item');

    // Submit without required fields
    await page.click('[data-testid="submit-button"]');

    // Verify validation errors
    await expect(page.locator('[data-testid="title-error"]')).toBeVisible();
    await expect(page.locator('[data-testid="title-error"]')).toContainText('Title is required');
  });

  test('validates email format', async ({ page }) => {
    await page.goto('/profile');

    // Enter invalid email
    await page.fill('[data-testid="email"]', 'invalid-email');
    await page.click('[data-testid="submit-button"]');

    // Verify error
    await expect(page.locator('[data-testid="email-error"]')).toContainText('Invalid email format');
  });
});
```

### 5. Implement Proper Waiting Strategies

**Wait for Elements:**
```typescript
// Wait for element to be visible
await page.locator('[data-testid="button"]').waitFor({ state: 'visible' });

// Wait for element to be hidden
await page.locator('[data-testid="loading"]').waitFor({ state: 'hidden' });

// Wait for element to be enabled
await page.locator('[data-testid="submit"]').waitFor({ state: 'enabled' });
```

**Wait for Navigation:**
```typescript
// Wait for URL change
await page.waitForURL('/dashboard');

// Wait for navigation after click
await Promise.all([
  page.waitForNavigation(),
  page.click('[data-testid="link"]')
]);
```

**Wait for Network Requests:**
```typescript
// Wait for API response
await Promise.all([
  page.waitForResponse(response =>
    response.url().includes('/api/users') && response.status() === 200
  ),
  page.click('[data-testid="load-users"]')
]);

// Wait for specific request
await page.waitForRequest(request =>
  request.url().includes('/api/save') && request.method() === 'POST'
);
```

**Wait for Custom Conditions:**
```typescript
// Wait until condition is true
await page.waitForFunction(() => {
  return document.querySelectorAll('.item').length === 5;
});
```

### 6. Handle Dynamic Content

**Waiting for Dynamic Elements:**
```typescript
// Wait for element to appear after API call
await page.click('[data-testid="load-more"]');
await page.waitForSelector('[data-testid="new-item"]');
```

**Handling Animations:**
```typescript
// Wait for animation to complete
await page.click('[data-testid="menu"]');
await page.locator('[data-testid="dropdown"]').waitFor({ state: 'visible' });
await page.waitForTimeout(300); // Wait for CSS animation
```

**Auto-Waiting:**
Playwright auto-waits for elements before actions:
```typescript
// These automatically wait for element to be actionable
await page.click('[data-testid="button"]');      // Waits for visible + enabled
await page.fill('[data-testid="input"]', 'text'); // Waits for visible + enabled
await page.selectOption('select', 'option1');      // Waits for visible + enabled
```

### 7. Create Test Fixtures

**Shared Test Data:**
```typescript
// tests/fixtures/test-data.ts
export const testUsers = {
  admin: { username: 'admin', password: 'admin123' },
  user: { username: 'testuser', password: 'password123' }
};

export const testItems = [
  { title: 'Item 1', description: 'Description 1' },
  { title: 'Item 2', description: 'Description 2' }
];
```

**Custom Fixtures:**
```typescript
// tests/fixtures/auth.ts
import { test as base } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';

export const test = base.extend({
  authenticatedPage: async ({ page }, use) => {
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    await loginPage.login('testuser', 'password123');
    await use(page);
  }
});

// Usage
test('authenticated user can create item', async ({ authenticatedPage }) => {
  // User is already logged in
  await authenticatedPage.goto('/create');
  // ...
});
```

### 8. Debugging Failed Tests

**Generate Traces:**
```typescript
// Traces are automatically captured on failure (if configured)
// View with: npx playwright show-trace trace.zip
```

**Screenshots:**
```typescript
// Manual screenshot
await page.screenshot({ path: 'screenshot.png' });

// Screenshot of specific element
await page.locator('[data-testid="card"]').screenshot({ path: 'card.png' });
```

**Videos:**
```typescript
// Videos are automatically recorded (if configured)
// View in test-results/ folder
```

**Step-by-Step Debugging:**
```typescript
// Run in headed mode with slow motion
// npx playwright test --headed --slow-mo=1000

// Add debugger
await page.pause();
```

### 9. Test Organization

```
tests/
├── e2e/
│   ├── auth/
│   │   ├── login.spec.ts
│   │   ├── signup.spec.ts
│   │   └── password-reset.spec.ts
│   ├── dashboard/
│   │   ├── create-item.spec.ts
│   │   ├── edit-item.spec.ts
│   │   └── delete-item.spec.ts
│   └── checkout/
│       ├── cart.spec.ts
│       ├── payment.spec.ts
│       └── confirmation.spec.ts
├── pages/
│   ├── LoginPage.ts
│   ├── DashboardPage.ts
│   └── CheckoutPage.ts
├── components/
│   ├── NavBar.ts
│   └── Modal.ts
└── fixtures/
    ├── auth.ts
    └── test-data.ts
```

## Locator Strategies

### Priority Order (Best to Worst)

**1. data-testid (Recommended):**
```typescript
await page.locator('[data-testid="submit-button"]').click();
```

**2. Role-based:**
```typescript
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('test@example.com');
```

**3. Text content:**
```typescript
await page.getByText('Welcome').click();
await page.getByText(/welcome/i).click(); // Case insensitive
```

**4. Label:**
```typescript
await page.getByLabel('Email').fill('test@example.com');
```

**5. CSS selectors (avoid if possible):**
```typescript
await page.locator('.submit-btn').click();
await page.locator('#email-input').fill('test@example.com');
```

## Best Practices

**1. Use Page Object Model**
- Keep test logic separate from selectors
- Reuse page objects across tests
- Make tests readable

**2. Prefer data-testid Attributes**
- Stable across UI changes
- Clear semantic meaning
- Easy to maintain

**3. Independent Tests**
- Each test should be runnable in isolation
- Don't depend on test execution order
- Clean up test data

**4. Proper Waits**
- Use auto-waiting when possible
- Avoid arbitrary timeouts (page.waitForTimeout)
- Wait for specific conditions

**5. Handle Flaky Tests**
- Use proper wait strategies
- Avoid race conditions
- Add retries for known-flaky tests

**6. Screenshots and Videos**
- Capture on failure for debugging
- Use traces for detailed debugging
- Keep artifacts for CI failures

## Output Organization

When creating E2E tests, organize output in:
`~/Documents/claude-code-skills-data/e2e-test-implementation/`

Create subdirectories as needed:
- `test-results/` - Test execution results
- `screenshots/` - Failure screenshots
- `videos/` - Test execution videos
- `traces/` - Playwright traces

## Quality Checklist

Before considering E2E tests complete, verify:

- [ ] All critical user paths covered (top 5-10 workflows)
- [ ] Page Object Model implemented (no direct selectors in tests)
- [ ] Proper async waits (no arbitrary sleeps)
- [ ] Tests are independent (can run in any order)
- [ ] Authentication flows tested
- [ ] Form validation tested
- [ ] Error scenarios tested
- [ ] Videos/screenshots configured for failures
- [ ] Tests run in CI/CD
- [ ] Execution time <5min for full suite

## Common E2E Test Patterns

### Pattern 1: Login Before Test
```typescript
test.beforeEach(async ({ page }) => {
  await page.goto('/login');
  await page.fill('[data-testid="username"]', 'testuser');
  await page.fill('[data-testid="password"]', 'password123');
  await page.click('[data-testid="login-button"]');
  await page.waitForURL('/dashboard');
});
```

### Pattern 2: Multi-Step Workflow
```typescript
test('complete checkout flow', async ({ page }) => {
  // Step 1: Add to cart
  await page.goto('/products/123');
  await page.click('[data-testid="add-to-cart"]');

  // Step 2: View cart
  await page.click('[data-testid="cart-icon"]');
  await expect(page.locator('[data-testid="cart-item"]')).toBeVisible();

  // Step 3: Checkout
  await page.click('[data-testid="checkout-button"]');
  await page.fill('[data-testid="address"]', '123 Main St');

  // Step 4: Payment
  await page.fill('[data-testid="card-number"]', '4242424242424242');
  await page.click('[data-testid="pay-button"]');

  // Step 5: Confirmation
  await expect(page.locator('[data-testid="order-confirmation"]')).toBeVisible();
});
```

### Pattern 3: Error Handling
```typescript
test('handles network errors gracefully', async ({ page }) => {
  // Simulate network failure
  await page.route('**/api/users', route => route.abort());

  await page.goto('/users');

  // Verify error message
  await expect(page.locator('[data-testid="error-message"]')).toContainText('Failed to load');
});
```

## References

For more detailed patterns and examples, see:
- [Page Object Model Guide](references/page-object-model.md) - Comprehensive POM patterns
- [Playwright Best Practices](references/playwright-best-practices.md) - Advanced Playwright techniques
- [Locator Strategies](references/locator-strategies.md) - Selector best practices

## Tools and Frameworks

**Playwright:**
- @playwright/test - Test runner and assertion library
- playwright - Browser automation

**Alternative Tools:**
- Cypress - Alternative E2E framework
- Selenium - Traditional browser automation
- Puppeteer - Headless Chrome automation

**CI/CD Integration:**
- GitHub Actions - playwright-action
- GitLab CI - Playwright Docker images
- Jenkins - Playwright plugins

# Page Object Model Guide

## Overview

The Page Object Model (POM) is a design pattern that creates an abstraction layer between tests and the UI. Each page or component gets its own class, containing locators and methods that represent user interactions.

## Benefits of POM

1. **Maintainability**: When UI changes, update only page objects, not tests
2. **Reusability**: Page objects can be used across multiple tests
3. **Readability**: Tests read like user stories, not technical implementations
4. **Reduced Duplication**: Common operations defined once, used everywhere

## Basic Page Object Structure

```typescript
// pages/LoginPage.ts
import { Page, Locator } from '@playwright/test';

export class LoginPage {
  // Page reference
  readonly page: Page;

  // Locators (elements on the page)
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

  // Navigation method
  async goto() {
    await this.page.goto('/login');
  }

  // User action methods
  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
  }

  // Assertion helper methods
  async getErrorMessage(): Promise<string | null> {
    return await this.errorMessage.textContent();
  }

  async isLoggedIn(): Promise<boolean> {
    return this.page.url().includes('/dashboard');
  }
}
```

## Component Objects

For reusable UI components (navigation bars, modals, forms), create component objects:

```typescript
// pages/components/NavBar.ts
import { Page, Locator } from '@playwright/test';

export class NavBar {
  readonly page: Page;
  readonly homeLink: Locator;
  readonly profileLink: Locator;
  readonly settingsLink: Locator;
  readonly userMenu: Locator;
  readonly logoutButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.homeLink = page.locator('[data-testid="nav-home"]');
    this.profileLink = page.locator('[data-testid="nav-profile"]');
    this.settingsLink = page.locator('[data-testid="nav-settings"]');
    this.userMenu = page.locator('[data-testid="user-menu"]');
    this.logoutButton = page.locator('[data-testid="logout-button"]');
  }

  async navigateToHome() {
    await this.homeLink.click();
  }

  async navigateToProfile() {
    await this.profileLink.click();
  }

  async logout() {
    await this.userMenu.click();
    await this.logoutButton.click();
  }
}
```

## Advanced Page Object Patterns

### Composing Page Objects

Pages can include component objects:

```typescript
// pages/DashboardPage.ts
import { Page, Locator } from '@playwright/test';
import { NavBar } from './components/NavBar';
import { Sidebar } from './components/Sidebar';

export class DashboardPage {
  readonly page: Page;
  readonly nav: NavBar;
  readonly sidebar: Sidebar;
  readonly createButton: Locator;
  readonly itemList: Locator;

  constructor(page: Page) {
    this.page = page;
    this.nav = new NavBar(page);
    this.sidebar = new Sidebar(page);
    this.createButton = page.locator('[data-testid="create-button"]');
    this.itemList = page.locator('[data-testid="item-list"]');
  }

  async goto() {
    await this.page.goto('/dashboard');
  }

  async createItem(title: string, description: string) {
    await this.createButton.click();
    // Form filling logic...
  }

  async getItemCount(): Promise<number> {
    return await this.itemList.locator('.item').count();
  }
}
```

### Page Object with Form Handling

```typescript
// pages/CreateItemPage.ts
import { Page, Locator } from '@playwright/test';

export class CreateItemPage {
  readonly page: Page;
  readonly titleInput: Locator;
  readonly descriptionInput: Locator;
  readonly categorySelect: Locator;
  readonly tagsInput: Locator;
  readonly submitButton: Locator;
  readonly cancelButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.titleInput = page.locator('[data-testid="title"]');
    this.descriptionInput = page.locator('[data-testid="description"]');
    this.categorySelect = page.locator('[data-testid="category"]');
    this.tagsInput = page.locator('[data-testid="tags"]');
    this.submitButton = page.locator('[data-testid="submit"]');
    this.cancelButton = page.locator('[data-testid="cancel"]');
  }

  async goto() {
    await this.page.goto('/items/create');
  }

  async fillForm(data: {
    title?: string;
    description?: string;
    category?: string;
    tags?: string[];
  }) {
    if (data.title) {
      await this.titleInput.fill(data.title);
    }
    if (data.description) {
      await this.descriptionInput.fill(data.description);
    }
    if (data.category) {
      await this.categorySelect.selectOption(data.category);
    }
    if (data.tags) {
      for (const tag of data.tags) {
        await this.tagsInput.fill(tag);
        await this.page.keyboard.press('Enter');
      }
    }
  }

  async submit() {
    await this.submitButton.click();
    await this.page.waitForURL('/items/*');
  }

  async cancel() {
    await this.cancelButton.click();
  }

  async getValidationError(field: string): Promise<string | null> {
    const errorLocator = this.page.locator(`[data-testid="${field}-error"]`);
    return await errorLocator.textContent();
  }
}
```

### Page Object with Dynamic Content

```typescript
// pages/SearchResultsPage.ts
import { Page, Locator } from '@playwright/test';

export class SearchResultsPage {
  readonly page: Page;
  readonly searchInput: Locator;
  readonly searchButton: Locator;
  readonly resultsContainer: Locator;
  readonly noResultsMessage: Locator;

  constructor(page: Page) {
    this.page = page;
    this.searchInput = page.locator('[data-testid="search-input"]');
    this.searchButton = page.locator('[data-testid="search-button"]');
    this.resultsContainer = page.locator('[data-testid="results"]');
    this.noResultsMessage = page.locator('[data-testid="no-results"]');
  }

  async search(query: string) {
    await this.searchInput.fill(query);
    await this.searchButton.click();
    // Wait for results to load
    await this.page.waitForResponse(resp =>
      resp.url().includes('/api/search') && resp.status() === 200
    );
  }

  async getResultCount(): Promise<number> {
    return await this.resultsContainer.locator('.result-item').count();
  }

  async getResultTitles(): Promise<string[]> {
    const titles = await this.resultsContainer
      .locator('.result-title')
      .allTextContents();
    return titles;
  }

  async clickResult(index: number) {
    await this.resultsContainer
      .locator('.result-item')
      .nth(index)
      .click();
  }

  async hasNoResults(): Promise<boolean> {
    return await this.noResultsMessage.isVisible();
  }
}
```

### Page Object with Modal Handling

```typescript
// pages/components/ConfirmationModal.ts
import { Page, Locator } from '@playwright/test';

export class ConfirmationModal {
  readonly page: Page;
  readonly modal: Locator;
  readonly title: Locator;
  readonly message: Locator;
  readonly confirmButton: Locator;
  readonly cancelButton: Locator;

  constructor(page: Page) {
    this.page = page;
    this.modal = page.locator('[data-testid="confirmation-modal"]');
    this.title = this.modal.locator('[data-testid="modal-title"]');
    this.message = this.modal.locator('[data-testid="modal-message"]');
    this.confirmButton = this.modal.locator('[data-testid="confirm-button"]');
    this.cancelButton = this.modal.locator('[data-testid="cancel-button"]');
  }

  async waitForModal() {
    await this.modal.waitFor({ state: 'visible' });
  }

  async confirm() {
    await this.confirmButton.click();
    await this.modal.waitFor({ state: 'hidden' });
  }

  async cancel() {
    await this.cancelButton.click();
    await this.modal.waitFor({ state: 'hidden' });
  }

  async getTitle(): Promise<string | null> {
    return await this.title.textContent();
  }

  async getMessage(): Promise<string | null> {
    return await this.message.textContent();
  }
}
```

## Page Object Best Practices

### 1. Keep Locators in Page Objects

**Good:**
```typescript
export class LoginPage {
  readonly usernameInput = page.locator('[data-testid="username"]');

  async fillUsername(username: string) {
    await this.usernameInput.fill(username);
  }
}
```

**Bad:**
```typescript
// Test file with hardcoded locators
await page.locator('[data-testid="username"]').fill('testuser');
```

### 2. Return Page Objects for Navigation

```typescript
export class LoginPage {
  async login(username: string, password: string): Promise<DashboardPage> {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();
    await this.page.waitForURL('/dashboard');
    return new DashboardPage(this.page);
  }
}

// Usage in test
const loginPage = new LoginPage(page);
const dashboardPage = await loginPage.login('user', 'pass');
await dashboardPage.createItem('New Item');
```

### 3. Use Method Chaining for Fluent API

```typescript
export class SearchPage {
  async search(query: string) {
    await this.searchInput.fill(query);
    await this.searchButton.click();
    return this; // Enable chaining
  }

  async filterByCategory(category: string) {
    await this.categoryFilter.selectOption(category);
    return this;
  }

  async sortBy(sortOption: string) {
    await this.sortDropdown.selectOption(sortOption);
    return this;
  }
}

// Usage with chaining
await searchPage
  .search('laptop')
  .filterByCategory('electronics')
  .sortBy('price-asc');
```

### 4. Separate Actions from Assertions

**Page Object** (actions only):
```typescript
export class UserProfilePage {
  async updateEmail(newEmail: string) {
    await this.emailInput.fill(newEmail);
    await this.saveButton.click();
  }

  async getDisplayedEmail(): Promise<string | null> {
    return await this.emailDisplay.textContent();
  }
}
```

**Test** (assertions):
```typescript
test('update email', async ({ page }) => {
  const profilePage = new UserProfilePage(page);
  await profilePage.updateEmail('newemail@example.com');

  // Assertions in test, not page object
  const displayedEmail = await profilePage.getDisplayedEmail();
  expect(displayedEmail).toBe('newemail@example.com');
});
```

### 5. Handle Waits in Page Objects

```typescript
export class ProductPage {
  async addToCart() {
    await this.addToCartButton.click();

    // Handle wait in page object
    await this.page.waitForResponse(resp =>
      resp.url().includes('/api/cart') && resp.status() === 200
    );

    // Wait for success message
    await this.successMessage.waitFor({ state: 'visible' });
  }
}
```

### 6. Use TypeScript for Type Safety

```typescript
interface ItemFormData {
  title: string;
  description?: string;
  category?: string;
  price?: number;
}

export class CreateItemPage {
  async fillForm(data: ItemFormData) {
    await this.titleInput.fill(data.title);

    if (data.description) {
      await this.descriptionInput.fill(data.description);
    }

    if (data.category) {
      await this.categorySelect.selectOption(data.category);
    }

    if (data.price) {
      await this.priceInput.fill(data.price.toString());
    }
  }
}
```

## Page Object Organization

```
tests/
├── pages/
│   ├── LoginPage.ts
│   ├── DashboardPage.ts
│   ├── CreateItemPage.ts
│   ├── SearchPage.ts
│   ├── UserProfilePage.ts
│   └── components/
│       ├── NavBar.ts
│       ├── Sidebar.ts
│       ├── Modal.ts
│       └── ItemCard.ts
├── e2e/
│   ├── auth.spec.ts
│   ├── items.spec.ts
│   └── search.spec.ts
└── fixtures/
    └── test-data.ts
```

## Testing with Page Objects

```typescript
// tests/e2e/items.spec.ts
import { test, expect } from '@playwright/test';
import { LoginPage } from '../pages/LoginPage';
import { DashboardPage } from '../pages/DashboardPage';
import { CreateItemPage } from '../pages/CreateItemPage';

test.describe('Item Management', () => {
  let dashboardPage: DashboardPage;

  test.beforeEach(async ({ page }) => {
    // Login using page object
    const loginPage = new LoginPage(page);
    await loginPage.goto();
    dashboardPage = await loginPage.login('testuser', 'password123');
  });

  test('create new item', async ({ page }) => {
    // Navigate to create page
    const createPage = await dashboardPage.navigateToCreateItem();

    // Fill form using page object
    await createPage.fillForm({
      title: 'New Item',
      description: 'Test Description',
      category: 'electronics',
      price: 99.99
    });

    // Submit form
    const itemPage = await createPage.submit();

    // Verify using page object methods
    const title = await itemPage.getTitle();
    expect(title).toBe('New Item');
  });
});
```

## Common Patterns

### Loading States

```typescript
export class DashboardPage {
  readonly loadingSpinner = this.page.locator('[data-testid="loading"]');

  async waitForPageLoad() {
    await this.loadingSpinner.waitFor({ state: 'hidden' });
  }
}
```

### Error Handling

```typescript
export class FormPage {
  async getFieldError(fieldName: string): Promise<string | null> {
    const errorLocator = this.page.locator(`[data-testid="${fieldName}-error"]`);
    if (await errorLocator.isVisible()) {
      return await errorLocator.textContent();
    }
    return null;
  }

  async hasValidationErrors(): Promise<boolean> {
    return await this.page.locator('.field-error').count() > 0;
  }
}
```

### Pagination

```typescript
export class ListPage {
  readonly nextButton = this.page.locator('[data-testid="next-page"]');
  readonly prevButton = this.page.locator('[data-testid="prev-page"]');
  readonly pageInfo = this.page.locator('[data-testid="page-info"]');

  async goToNextPage() {
    await this.nextButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async goToPreviousPage() {
    await this.prevButton.click();
    await this.page.waitForLoadState('networkidle');
  }

  async getCurrentPage(): Promise<number> {
    const text = await this.pageInfo.textContent();
    const match = text?.match(/Page (\d+)/);
    return match ? parseInt(match[1]) : 1;
  }
}
```

## Summary

- **Page Objects** represent pages with locators and methods
- **Component Objects** represent reusable UI components
- **Keep tests readable** by abstracting implementation details
- **Maintain easily** by updating page objects instead of tests
- **Reuse code** across multiple test files
- **Separate concerns** between actions (page objects) and assertions (tests)

# TypeScript Best Practices Stack

## 1. Compiler Strictness

### Enable Strict Mode
* Enable `strict` in `tsconfig.json` for strongest correctness guarantees
* Strict mode enables: `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, `strictBindCallApply`, `strictPropertyInitialization`, `noImplicitThis`, `alwaysStrict`
* Example `tsconfig.json`:
  ```json
  {
    "compilerOptions": {
      "strict": true,
      "target": "ES2022",
      "module": "ESNext",
      "moduleResolution": "bundler",
      "esModuleInterop": true,
      "skipLibCheck": true,
      "forceConsistentCasingInFileNames": true,
      "resolveJsonModule": true,
      "isolatedModules": true,
      "noUnusedLocals": true,
      "noUnusedParameters": true,
      "noFallthroughCasesInSwitch": true
    }
  }
  ```
* Reference: https://www.typescriptlang.org/tsconfig/strict.html

### Additional Strictness Options
* `noUncheckedIndexedAccess`: Treat array/object access as potentially undefined
* `exactOptionalPropertyTypes`: Distinguish between `undefined` and missing properties
* `noImplicitReturns`: Ensure all code paths return a value
* `noPropertyAccessFromIndexSignature`: Force bracket notation for index signatures

## 2. Linting and Formatting

### ESLint
* Use ESLint to detect problematic patterns and enforce code quality
* Install: `npm install -D eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin`
* Example `.eslintrc.json`:
  ```json
  {
    "parser": "@typescript-eslint/parser",
    "parserOptions": {
      "ecmaVersion": 2022,
      "sourceType": "module",
      "project": "./tsconfig.json"
    },
    "extends": [
      "eslint:recommended",
      "plugin:@typescript-eslint/recommended",
      "plugin:@typescript-eslint/recommended-requiring-type-checking"
    ],
    "rules": {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/explicit-function-return-type": "warn",
      "@typescript-eslint/no-unused-vars": ["error", { "argsIgnorePattern": "^_" }]
    }
  }
  ```
* Run: `eslint . --ext .ts,.tsx`
* Reference: https://eslint.org/

### TypeScript ESLint
* Use typescript-eslint for TypeScript-specific linting rules
* Recommended rule sets: `recommended`, `recommended-requiring-type-checking`, `strict`
* Key rules:
  - `@typescript-eslint/no-explicit-any`: Ban `any` type
  - `@typescript-eslint/no-floating-promises`: Ensure promises are handled
  - `@typescript-eslint/no-misused-promises`: Prevent incorrect async usage
  - `@typescript-eslint/await-thenable`: Only await Promises
* Reference: https://typescript-eslint.io/

### Prettier
* Use Prettier for consistent formatting
* Install: `npm install -D prettier`
* Example `.prettierrc.json`:
  ```json
  {
    "semi": true,
    "trailingComma": "es5",
    "singleQuote": true,
    "printWidth": 100,
    "tabWidth": 2,
    "arrowParens": "always"
  }
  ```
* Integrate with ESLint: `npm install -D eslint-config-prettier`
* Run: `prettier --write .`
* Reference: https://prettier.io/

## 3. Types That Reduce Complexity

### Type Boundaries Hard
* Validate untrusted inputs at boundaries (API, user input, external data)
* Convert to typed domain objects early
* Use type guards for runtime validation:
  ```typescript
  interface User {
    id: number;
    email: string;
    name: string;
  }

  function isUser(value: unknown): value is User {
    return (
      typeof value === 'object' &&
      value !== null &&
      'id' in value &&
      typeof value.id === 'number' &&
      'email' in value &&
      typeof value.email === 'string' &&
      'name' in value &&
      typeof value.name === 'string'
    );
  }

  function createUser(data: unknown): User {
    if (!isUser(data)) {
      throw new Error('Invalid user data');
    }
    return data;
  }
  ```

### Prefer Union Types Over Inheritance
* Use union types and type narrowing instead of complex class hierarchies
* Easier to understand, test, and maintain
  ```typescript
  // Good - union types
  type Shape = Circle | Rectangle | Triangle;

  interface Circle {
    kind: 'circle';
    radius: number;
  }

  interface Rectangle {
    kind: 'rectangle';
    width: number;
    height: number;
  }

  interface Triangle {
    kind: 'triangle';
    base: number;
    height: number;
  }

  function area(shape: Shape): number {
    switch (shape.kind) {
      case 'circle':
        return Math.PI * shape.radius ** 2;
      case 'rectangle':
        return shape.width * shape.height;
      case 'triangle':
        return (shape.base * shape.height) / 2;
    }
  }
  ```

### Discriminated Unions for State Modeling
* Use discriminated unions to make illegal states unrepresentable
* TypeScript enforces exhaustiveness checking
  ```typescript
  type RequestState<T> =
    | { status: 'idle' }
    | { status: 'loading' }
    | { status: 'success'; data: T }
    | { status: 'error'; error: Error };

  function handleRequest<T>(state: RequestState<T>): string {
    switch (state.status) {
      case 'idle':
        return 'Not started';
      case 'loading':
        return 'Loading...';
      case 'success':
        return `Data: ${state.data}`;
      case 'error':
        return `Error: ${state.error.message}`;
    }
  }
  ```

### Avoid `any`, Prefer `unknown`
* Never use `any` - it disables type checking
* Use `unknown` for truly unknown types, then narrow
* Use type guards to narrow `unknown` to specific types:
  ```typescript
  // Bad
  function process(data: any) {
    return data.value.toUpperCase();  // No type safety
  }

  // Good
  function process(data: unknown): string {
    if (
      typeof data === 'object' &&
      data !== null &&
      'value' in data &&
      typeof data.value === 'string'
    ) {
      return data.value.toUpperCase();
    }
    throw new Error('Invalid data');
  }
  ```

## 4. Testing

### Vitest
* Modern testing framework for TypeScript/JavaScript projects
* Fast, ESM-native, TypeScript support out of the box
* Install: `npm install -D vitest`
* Example `vitest.config.ts`:
  ```typescript
  import { defineConfig } from 'vitest/config';

  export default defineConfig({
    test: {
      globals: true,
      environment: 'node',
      coverage: {
        provider: 'v8',
        reporter: ['text', 'json', 'html'],
      },
    },
  });
  ```
* Run: `vitest` or `vitest run` (CI mode)
* Reference: https://vitest.dev/

### Jest with TypeScript
* If using Jest, configure for TypeScript
* Install: `npm install -D jest @types/jest ts-jest`
* Example `jest.config.js`:
  ```javascript
  module.exports = {
    preset: 'ts-jest',
    testEnvironment: 'node',
    roots: ['<rootDir>/src'],
    testMatch: ['**/__tests__/**/*.ts', '**/?(*.)+(spec|test).ts'],
    collectCoverageFrom: ['src/**/*.ts', '!src/**/*.d.ts'],
  };
  ```
* Run: `jest` or `jest --coverage`
* Note: Babel-based transpilation does not type check - run `tsc --noEmit` separately
* Reference: https://jestjs.io/

## 5. Concrete TypeScript Rules That Keep Code Clean

### Export Only Public API
* Do not export internal types/functions that are not part of the API contract
* Keep implementation details private
* Use type-only exports when exporting only for types:
  ```typescript
  // Good
  export type { User };  // Type-only export
  export { createUser, updateUser };  // Value exports

  // Internal - not exported
  interface UserDTO { ... }
  function validateUser(user: User): boolean { ... }
  ```

### Make Illegal States Unrepresentable
* Use the type system to prevent invalid states
* Example: loading state cannot have data, error state must have error
  ```typescript
  // Bad - can have loading=true AND data AND error simultaneously
  interface BadState {
    loading: boolean;
    data?: string;
    error?: Error;
  }

  // Good - mutually exclusive states
  type GoodState =
    | { status: 'loading' }
    | { status: 'success'; data: string }
    | { status: 'error'; error: Error };
  ```

### Keep Side Effects Localized
* Separate pure logic from integration code
* Pure functions are easier to test and reason about
  ```typescript
  // Pure function - no side effects
  function calculateTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
  }

  // Side effect function - clearly separated
  async function saveOrder(order: Order, db: Database): Promise<void> {
    await db.orders.insert(order);
  }
  ```

### Prefer Small Modules Over Barrel Files
* Barrel files (`index.ts` re-exporting everything) hide dependency structure
* Make imports explicit to understand dependencies
  ```typescript
  // Bad - barrel file hides structure
  // index.ts
  export * from './user';
  export * from './order';
  export * from './product';

  // Good - explicit imports show dependencies
  import { User } from './user';
  import { Order } from './order';
  ```

### Use `readonly` for Immutability
* Mark properties `readonly` to prevent accidental mutation
* Use `ReadonlyArray<T>` or `readonly T[]` for immutable arrays
  ```typescript
  interface User {
    readonly id: number;
    readonly email: string;
    name: string;  // Can be updated
  }

  function processUsers(users: readonly User[]): void {
    // users.push(...) // Error: readonly array
  }
  ```

### Explicit Function Return Types
* Always specify return types for public functions
* Prevents accidental API changes
* Makes intent clear
  ```typescript
  // Good
  function getUser(id: number): Promise<User | null> {
    return db.users.findById(id);
  }

  // Bad - return type inferred, could change accidentally
  function getUser(id: number) {
    return db.users.findById(id);
  }
  ```

### Use Const Assertions
* Use `as const` for literal types and immutable objects
  ```typescript
  // String literal type
  const colors = ['red', 'green', 'blue'] as const;
  type Color = typeof colors[number];  // 'red' | 'green' | 'blue'

  // Immutable object
  const config = {
    apiUrl: 'https://api.example.com',
    timeout: 5000,
  } as const;
  ```

### Utility Types
* Use built-in utility types for common transformations:
  - `Partial<T>`: All properties optional
  - `Required<T>`: All properties required
  - `Readonly<T>`: All properties readonly
  - `Pick<T, K>`: Select subset of properties
  - `Omit<T, K>`: Exclude subset of properties
  - `Record<K, V>`: Object with keys K and values V
  - `NonNullable<T>`: Exclude null/undefined

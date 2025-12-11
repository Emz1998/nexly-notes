---
paths: src/**/*.{ts,tsx,js,jsx}
---

# Coding Rules & Style Guide

## 1. Core Principles

- **Write for clarity first.**  
  Code should be instantly understandable without mental decoding. Avoid clever one-liners or obscure language features unless necessary for performance or readability.

- **Always handle errors explicitly.**  
  Never allow silent failures. Use `try/catch` or guards where runtime failures are possible, and validate all inputs and edge cases.

- **Validate assumptions.**  
  Always check for `null`, `undefined`, array bounds, and object property existence. Treat all external inputs as potentially malformed.

- **Type safety (TypeScript).**  
  Use explicit types. Avoid `any` or implicit inference unless it’s absolutely necessary (e.g., third-party libraries).

- **Atomic components.**  
  Break complex components into smaller, testable, reusable units. Each should have a clear, single responsibility.

---

## 2. Coding Style

- **Variables and functions:** use `camelCase`  
  Example: `getUserData()`

- **Classes and components:** use `PascalCase`  
  Example: `UserProfile`

- **Constants:** use `UPPER_SNAKE_CASE`  
  Example: `MAX_RETRIES`

- **Filenames and directories:** use `kebab-case`  
  Example: `user-profile.ts`

- **Booleans:** use clear prefixes for intent  
  Example: `isValid`, `hasAccess`, `canSubmit`

- **Types Over Interface:** prefer types over interface  
  Example: `type exampleString= string`

---

## 3. Function and Module Design

- **Keep functions concise (around 20–30 lines).**  
  Each function should do one thing and do it well. The 20-line limit is a guideline — prioritize clarity and cohesion over strict length limits.

- **Modularize aggressively.**  
  Split logic into focused files or modules by responsibility (e.g., `utils/`, `services/`, `types/`, `hooks/`). Avoid files that handle multiple unrelated tasks.

- **Refactor for readability.**  
  Prefer descriptive naming and clear logic over clever shortcuts. Extract helpers for repetitive or conceptually distinct logic.

---

## 4. Error Handling and Validation

- Always wrap potentially unsafe operations in `try/catch` blocks.
- Provide meaningful error messages and clear recovery options.
- Validate:
  - **Function inputs:** type, range, and format.
  - **API responses:** required properties and expected data shape.
  - **User input:** sanitize and normalize before processing.

---

## 5. Maintainability

- Write code that is **easy to test, debug, and extend.**
- Favor **composition over inheritance** for flexibility.
- Keep side effects isolated and predictable.
- Use concise comments to explain _why_ the code exists, not _what_ it does.

---

## 6. Dependency Management

- Design for **low coupling and high cohesion.**
- Each module should expose a clear, minimal interface.
- Avoid reaching into another module’s internal logic — depend only on its public API.
- Use dependency injection or factory patterns when sharing resources between modules.
- Never make changes in one module that require ripple changes in multiple others.
- When two modules must interact, define explicit types or interfaces to enforce boundaries and prevent hidden dependencies.

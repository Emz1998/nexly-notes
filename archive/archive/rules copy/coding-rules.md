# Coding Rules

## Core rules

- **Prioritize readability over cleverness** - Write code that's immediately understandable. Avoid complex one-liners or obscure language features unless specifically requested.
- **Always handle errors** - Never write code that could fail silently. Include try-catch blocks, error checking, and validation for all inputs and edge cases.
- **Include type hints/annotations** - For TypeScript use explicit types, for JavaScript add JSDoc comments. Never use any or leave types implicit unless requested.
- **Write defensive code** - Check for null/undefined, validate array bounds, verify object properties exist. Assume inputs could be malformed.
- **Atomic Components** - Break down complex components into smaller, more manageable components.

## Coding Styles

- `CamelCase` for variables and functions (getUserData).
- `PascalCase` for classes (UserProfile).
- `UPPER_SNAKE_CASE`   for constants (MAX_RETRIES).
- `kebab-case` for filenames and directories (user-profile.js).
- Consistent prefixes (e.g., is, has, can for booleans).


## Code Structure Rules

-  **Keep functions under 20 lines** - If a function is longer, break it into smaller, focused functions. Each function does exactly one thing.
- **Use guard clauses** - Return early for edge cases and errors. Don't nest the happy path in deep if-statements.
- **No magic numbers or strings** - Define constants at the top of files with descriptive names. Configuration should be centralized and obvious.
- **Implement proper separation of concerns** -  Separate data logic, business logic, and presentation. Don't mix database queries with UI rendering.
- Apply **DRY principle (Don’t Repeat Yourself)** 
- Apply **KISS principle (Keep It Simple, Stupid)**
- **Modularization** - split code into files and packages logically.

## Code Documentation Rules

- **Add comprehensive docstrings** - Every function needs a docstring explaining purpose, parameters, return values, and potential exceptions.
- **Include inline comments for complex logic** - If code requires thought to understand, add a comment explaining the "why" not the "what".
- **Provide usage examples** - For reusable functions or classes, include code examples showing how to use them correctly.

## Safety Rules

- **Never hardcode secrets** - Always use environment variables or config files for API keys, passwords, and sensitive data. Include placeholder examples.
- **Sanitize all inputs** - Prevent SQL injection, XSS, command injection. Use parameterized queries, escape HTML, validate file paths.
- **Set security headers** - For web applications, include CORS, CSP, and other security headers. Default to restrictive permissions.
- **Use cryptographically secure methods** - For random tokens, passwords, or security-critical operations, use appropriate cryptographic libraries, never Math.random().

## Testing Rules

- **Write testable code** - Use dependency injection, avoid global state, return values instead of using side effects where possible.
- **Include basic tests** - When asked for code, include at least basic unit tests unless explicitly told not to.
- **Test edge cases** - Include tests for empty inputs, null values, boundary conditions, and error scenarios.

## Performance Rules

- **Use efficient algorithms** - Default to O(n log n) or better for sorting/searching. Use appropriate data structures (Set for uniqueness, Map for lookups).
- **Implement pagination** - Never return unlimited results from databases or APIs. Always include limit/offset or cursor-based pagination.
- **Add caching strategically** - Cache expensive computations and external API calls, but always include cache invalidation logic.

## Code Completeness Rules

- **Provide complete, runnable code** - Include all necessary imports, dependencies, and setup code. Code should work when copied and pasted.
- **Include error recovery** - Don't just catch errors, implement retry logic, fallbacks, and graceful degradation where appropriate.
- **Add logging strategically** - Include debug logs for important operations but avoid log spam. Use appropriate log levels.

## API and Interface Rules
- **Design consistent APIs** - Use RESTful conventions, consistent naming, predictable request/response formats.
- **Version APIs** - Include versioning strategy for APIs to allow backwards compatibility.
- **Validate schemas** - Use schema validation libraries (Joi, Zod, Pydantic) for API inputs and outputs.


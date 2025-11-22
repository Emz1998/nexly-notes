# Coding Rules

## Core Rules

### Type Safety

- Never use `any` type in TypeScript - always define explicit types or use `unknown`.
- Always use explicit return types for all functions (except simple callbacks).
- Never ignore TypeScript errors - fix them or properly type the code.
- Avoid using `!` (non-null assertion) - properly handle null cases instead.

### Error Handling

- Always include error handling with try-catch blocks, never assume operations succeed.
- Check for null/undefined before accessing properties (use optional chaining `?.`).
- Always handle async errors - don't use async functions without try-catch or .catch().
- Don't mix async/await with .then() - choose one pattern consistently.

### Data Validation & Security

- Validate all external inputs with Zod schemas before processing.
- Never store sensitive data (tokens, passwords) in localStorage - use secure cookies.
- Never mutate state directly - always create new objects/arrays.

### React Best Practices

- Always clean up side effects (event listeners, timers, subscriptions) in useEffect cleanup.
- Never use index as key in React lists unless array is truly static.
- Destructure props at function signature, not inside component body.

### Code Quality

- Never commit TODO comments - create tickets instead.
- Avoid nested ternaries - use if-else or extract to functions.
- Don't use `console.log` in production code - use proper logging utilities.
- Don't use `var` - always use `const` or `let`.
- Extract magic numbers/strings to named constants.

## Coding Styles

### Naming Conventions

- Prefix boolean variables/functions with `is`, `has`, `can`, `should` (isLoading, hasPermission).
- Prefix event handlers with `handle` (handleClick, handleSubmit, handleModeChange).
- Prefix custom hooks with `use` (useAutoComplete, useNoteSync).
- Use `PascalCase` for React components and TypeScript interfaces/types.
- Use `camelCase` for variables, functions, and object properties.
- Use `UPPER_SNAKE_CASE` for true constants (MAX_RETRIES, API_BASE_URL).
- Use `kebab-case` for file names (note-editor.tsx, inline-diff.ts).

### Code Organization

- Group imports: React first, then third-party, then local, then types.
- Order React hooks: useState, useRef, useEffect, custom hooks.
- Always add trailing commas in multi-line arrays/objects for cleaner git diffs.

### Formatting

- Use template literals instead of string concatenation.

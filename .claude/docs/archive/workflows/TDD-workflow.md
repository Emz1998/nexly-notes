# TDD Workflow

## Core Cycle: Red → Green → Refactor

### 1. Red Phase - Write a Failing Test
- Write the smallest test that captures one behavior
- Run test and ensure it fails
- If it passes without implementation, the test is wrong

### 2. Green Phase - Make It Pass
- Write minimum code to make test pass
- Take shortcuts, hardcode values if needed
- Goal: reach green FAST (under 5 minutes)

### 3. Refactor Phase - Make It Right
- Improve code while keeping tests green
- Extract methods, remove duplication, rename variables
- Run tests after each change

## Complete Workflow Steps

### Step 1: Define the Feature
Write a one-sentence description of what you're building before any code.

### Step 2: Create a Test List
Break feature into tiny, testable behaviors:
- [ ] Success case with valid input
- [ ] Failure case with invalid input
- [ ] Edge case with empty input
- [ ] Boundary conditions
- [ ] Error handling

### Step 3: Pick the Simplest Test
Start with the happiest path, simplest case. Don't tackle edge cases first.

### Step 4: Write One Failing Test
- Name test clearly: `test_user_can_login_with_valid_credentials()`
- Arrange: Set up test data
- Act: Call the method
- Assert: Check the result
- Run test, see it fail

### Step 5: Write Minimum Code
- Make the test pass with simplest implementation
- Don't worry about elegance or efficiency
- Hardcode returns if that's fastest
- Confirm test passes

### Step 6: Refactor
- Remove duplication
- Improve naming
- Extract functions
- Apply design patterns
- Run tests after each change

### Step 7: Repeat
- Mark test complete in your list
- Pick next simplest test
- Repeat cycle until feature is complete

## Best Practices

**Timing**
- Each cycle: 5-10 minutes max
- If longer, test is too big - break it down

**Test Quality**
- Test behavior, not implementation
- One assertion per test (when possible)
- Use descriptive test names
- Test public API only

**When to Write Tests**
- Before implementation (always)
- When fixing bugs (write failing test first)
- Before refactoring (ensure coverage)

**Test Organization**
- Group related tests in classes/modules
- Use setup/teardown for common code
- Keep tests independent - no shared state



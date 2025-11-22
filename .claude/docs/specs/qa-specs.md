# Quality Assurance Specifications - NEXLY RN MVP

## Testing Philosophy: Test-Driven Development (TDD)

**Red-Green-Refactor Cycle:**
1. **Red** - Write a failing test for the smallest piece of functionality
2. **Green** - Write minimal code to make the test pass
3. **Refactor** - Clean up code while keeping tests passing
4. **Repeat** - Move to next small piece of functionality

**Coverage Targets:**
- 60% for critical user paths (auth, create note, edit note)
- 40% overall codebase coverage
- Write tests BEFORE implementation

**Test Pyramid:**
- 60% Unit Tests (write first for utilities, hooks, components)
- 30% Manual Testing (integration, E2E workflows)
- 10% Automated E2E (3 core workflows)

---

## 1. Testing Stack

### Unit Testing
- **Vitest 3.2.4** - Test runner with native ESM support
- **React Testing Library 16.3.0** - Component testing
- **jsdom 25.x** - DOM simulation
- **vi.mock** - Built-in mocking

### End-to-End Testing
- **Playwright 1.55.0** - Chromium only

### Manual Testing
- **15-minute smoke test** before each release

---

## 2. TDD Workflow Example

### Example: Building `useAuth` Hook

**Step 1: Write Failing Test (Red)**
```typescript
// src/hooks/useAuth.test.ts
import { renderHook, act } from '@testing-library/react';
import { useAuth } from './useAuth';

test('login sets user state and auth cookie', async () => {
  const { result } = renderHook(() => useAuth());

  await act(async () => {
    await result.current.login('test@example.com', 'password123');
  });

  expect(result.current.user).toEqual({ email: 'test@example.com' });
  expect(document.cookie).toContain('auth-token');
});
```

**Step 2: Run Test (Should Fail)**
```bash
npm test src/hooks/useAuth.test.ts
# Expected: FAIL - useAuth not implemented yet
```

**Step 3: Write Minimal Implementation (Green)**
```typescript
// src/hooks/useAuth.ts
export function useAuth() {
  const [user, setUser] = useState(null);

  const login = async (email: string, password: string) => {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    const data = await response.json();
    setUser({ email });
    document.cookie = `auth-token=${data.token}`;
  };

  return { user, login };
}
```

**Step 4: Run Test Again (Should Pass)**
```bash
npm test src/hooks/useAuth.test.ts
# Expected: PASS
```

**Step 5: Refactor** (improve code quality, tests still pass)

**Step 6: Repeat** for logout, token refresh, etc.

---

## 3. Unit Tests to Write First (25-30 Tests)

### Critical Components (10 tests)

**TiptapEditor (3 tests)** - Write tests first, then implement component
1. Renders in Create mode with placeholder text
2. Content updates trigger debounced onChange callback
3. Read-only in Study mode (contenteditable="false")

**ModeSelector (2 tests)**
1. Clicking mode buttons fires onModeChange with correct mode
2. Visual indicators show active mode (CSS classes)

**AutocompletePopup (3 tests)**
1. Displays max 5 suggestions
2. Arrow keys navigate suggestions
3. Enter key selects highlighted suggestion

**Auth Components (2 tests)**
1. LoginForm validates email format before submission
2. ProtectedRoute redirects to /login when not authenticated

### Critical Hooks (8 tests)

**useAuth (3 tests)** - Write all tests first, implement to make them pass
1. Login sets user state and auth cookie
2. Logout clears user state and redirects to /login
3. Token refresh triggers before expiration

**useAutocomplete (2 tests)**
1. Debounces input by 150ms before requesting suggestions
2. Falls back to local dictionary when quota exceeded

**useNoteSync (3 tests)**
1. Saves note to IndexedDB immediately
2. Queues Firestore sync when online
3. Retries failed sync with exponential backoff

### Critical Utilities (7 tests)

**Validators (3 tests)** - Pure functions, perfect for TDD
1. noteSchema validates title length (max 200 chars)
2. autocompleteRequestSchema rejects invalid cursor positions
3. Environment variables schema throws on missing required vars

**Formatters (2 tests)**
1. formatDate returns "Today" for current date
2. sanitizeContent strips script tags from HTML

**Diff Calculator (2 tests)**
1. Calculates word-level diff for changed content
2. Returns additions and deletions arrays

---

## 4. API Route Tests to Write First (8 Tests)

### TDD Approach for API Routes
1. Write test for API route behavior
2. Run test (it fails - route doesn't exist)
3. Create route with minimal implementation
4. Run test (it passes)
5. Refactor route handler

### Authentication Routes (3 tests)
1. `POST /api/auth/login` - Returns 200 with valid credentials, 401 with invalid
2. `POST /api/auth/signup` - Creates user and returns auth token
3. `POST /api/auth/logout` - Clears auth cookie and returns 200

### AI Feature Routes (3 tests)
1. `POST /api/ai/autocomplete` - Returns suggestions array with valid context
2. `POST /api/ai/autocomplete` - Returns fallback suggestions when quota exceeded
3. `POST /api/ai/spot-terms` - Returns terms array with importance levels

### User Management Routes (2 tests)
1. `GET /api/users/profile` - Returns user data for authenticated user
2. `PATCH /api/users/profile` - Updates user profile with valid data

**Test Requirements:**
- All protected routes verify auth token
- All inputs validated with Zod schemas
- Error responses use correct HTTP status codes

---

## 5. E2E Tests (3 Tests - Write After Unit Tests Pass)

**When to Write E2E Tests:** After implementing features with TDD at unit level

### Test 1: Signup & Create Note
```
1. Navigate to /signup → Fill form → Submit
2. Verify redirect to /notes
3. Click "New Note" → Type content → Wait for auto-save
4. Verify note appears in library
```

### Test 2: Edit Note with Diff
```
1. Login → Navigate to /notes → Open note
2. Select "Edit" → Modify content
3. Click "View Changes" → Verify diff highlights
4. Save → Verify success
```

### Test 3: Auth Protection
```
1. Navigate to /notes (logged out) → Verify redirect to /login
2. Login → Verify redirect to /notes
3. Logout → Verify redirect to landing
```

---

## 6. Manual Testing Checklist (15 minutes)

**Run before each release after all automated tests pass**

### Pre-Release Smoke Test

**Authentication**
- [ ] Signup → Login → Logout flow works

**Create/Edit/Study Modes**
- [ ] Create mode (blue accent) - autocomplete works, auto-save persists
- [ ] Edit mode (purple accent) - inline diff shows changes
- [ ] Study mode (green accent) - read-only, key terms spotted

**Offline Functionality**
- [ ] Disconnect network → Create note → Reconnect → Syncs to Firestore

**DevTools Checks**
- [ ] No console errors
- [ ] IndexedDB has notes data
- [ ] Auth cookie has HttpOnly + Secure flags

---

## 7. Performance & Security (Manual)

### Performance Targets
- **Autocomplete**: <300ms
- **Mode transition**: <100ms
- **Lighthouse**: Performance >70, Accessibility >80

**Manual Check:** Run Lighthouse before release

### Security Tests (5 Manual Tests)

1. **Privilege Escalation** - User A cannot access User B's notes
2. **XSS Prevention** - `<script>alert('XSS')</script>` is sanitized
3. **API Auth** - Unauthenticated requests return 401
4. **Env Validation** - Missing env vars cause startup error
5. **Rate Limiting** - 100 rapid requests trigger 429

---

## 8. Accessibility (Manual)

**15-minute Manual A11y Check:**
- [ ] Tab through all elements - logical order, visible focus
- [ ] Enter activates buttons, Escape closes modals
- [ ] All inputs have labels
- [ ] Lighthouse accessibility score >80

---

## 9. Browser Compatibility

**Testing Strategy:**
- Automated tests: Chromium only
- Manual spot-check: Firefox, Safari before launch

---

## 10. Code Quality

### Pre-Commit (Automated)
```bash
npm run lint        # ESLint + TypeScript
npm run format      # Prettier
npm test            # All unit tests must pass before commit
```

**Standards:**
- Max function: 50 lines
- Max file: 400 lines
- No `console.log` in production
- No `any` types (warn only)

---

## 11. CI/CD Pipeline

**On Every Push/PR:**
1. Lint (ESLint + TypeScript)
2. Unit Tests (Vitest)

**On Release Branch:**
3. Security Audit (`npm audit`)
4. E2E Tests (Playwright)

**Pre-Deploy (Manual):**
5. 15-min smoke test
6. Lighthouse audit

### Sample GitHub Actions
```yaml
name: CI
on: [push, pull_request]

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm run lint

  unit-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm ci
      - run: npm test
```

---

## 12. Integration Testing (Manual)

### Firebase Security Rules
1. Login as User A → Create note → Copy URL
2. Login as User B → Paste URL → Verify cannot access

### IndexedDB (Dexie)
1. Open DevTools > Application > IndexedDB
2. Create note → Verify in `notes` table
3. Edit offline → Verify in `syncQueue` table

### Offline Sync
1. Disconnect network → Create note → Reconnect
2. Verify note syncs to Firestore within 10s

---

## 13. Release Criteria

**Must Pass Before Beta Launch:**

**Testing** ✓
- [ ] All 25-30 unit tests pass
- [ ] All 8 API route tests pass
- [ ] All 3 E2E tests pass
- [ ] 15-min smoke test complete (no critical bugs)
- [ ] 5 security tests pass

**Code Quality** ✓
- [ ] ESLint passes (zero errors)
- [ ] TypeScript type-check passes
- [ ] Prettier formatted
- [ ] No `console.log` in production

**Performance** ✓
- [ ] Lighthouse: Performance >70, Accessibility >80
- [ ] Autocomplete <300ms
- [ ] No long tasks >50ms

**Security** ✓
- [ ] npm audit clean (no high/critical)
- [ ] No hardcoded API keys
- [ ] User data isolation verified

---

## 14. Test Environment Setup

### Local Development
```bash
npm install          # Install dependencies
npm test             # Run tests (with watch mode by default)
npm test -- --run    # Run tests once (CI mode)
npx playwright test  # Run E2E tests
```

### Environment Variables
Create `.env.local`:
```bash
# Firebase Client
NEXT_PUBLIC_FIREBASE_API_KEY=your-dev-key
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=your-dev-project.firebaseapp.com
NEXT_PUBLIC_FIREBASE_PROJECT_ID=your-dev-project

# Firebase Admin (server-only)
FIREBASE_ADMIN_PROJECT_ID=your-dev-project
FIREBASE_ADMIN_CLIENT_EMAIL=firebase-adminsdk@...
FIREBASE_ADMIN_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n..."

# OpenAI
OPENAI_API_KEY=sk-test-...
```

### Firebase Dev Project
1. Create separate Firebase project for development
2. Enable Authentication (Email/Password)
3. Create Firestore database with security rules
4. Generate Admin SDK credentials

---

## 15. TDD Best Practices

### Do's ✓
- Write test first, implementation second
- Test one thing per test (single assertion when possible)
- Use descriptive test names (what it should do)
- Keep tests fast (<100ms per unit test)
- Mock external dependencies (Firebase, OpenAI API)
- Run tests frequently during development

### Don'ts ✗
- Don't write implementation before test
- Don't test implementation details (test behavior)
- Don't write tests after code is complete (defeats TDD)
- Don't skip refactor step
- Don't commit failing tests

### Red-Green-Refactor Rhythm
```
Write test (2 min) → Watch it fail (10 sec) →
Write code (5 min) → Watch it pass (10 sec) →
Refactor (3 min) → Tests still pass (10 sec) →
Commit → Repeat
```

---

## Summary

**TDD Approach for MVP:**
- ✓ Write tests BEFORE implementation
- ✓ 25-30 unit tests (components, hooks, utilities)
- ✓ 8 API route tests
- ✓ 3 E2E tests
- ✓ 15-min manual smoke test
- ✓ Red-Green-Refactor cycle

**Quality Targets:**
- 60% critical path coverage, 40% overall
- ~40 total automated tests
- Manual-first for integration/E2E
- Fast feedback loop (<10 min to run all unit tests)

**CI/CD:**
- Lint + unit tests on every push (must pass)
- Security + E2E on release branch
- Manual smoke test + Lighthouse pre-deploy

**Development Flow:**
1. Pick small feature (e.g., login button validation)
2. Write failing test
3. Run test (watch it fail - RED)
4. Write minimal code to pass
5. Run test (watch it pass - GREEN)
6. Refactor code (tests still pass)
7. Commit and repeat

**TDD Benefits:**
- Fewer bugs (tests written before code)
- Better design (testable code is well-designed)
- Faster debugging (failing test pinpoints issue)
- Confidence to refactor (tests catch regressions)
- Living documentation (tests show how code works)

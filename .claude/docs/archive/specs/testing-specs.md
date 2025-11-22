# Testing Specifications (4-Week MVP)

## 1. Testing Strategy

### Philosophy

- **Test-Driven Development (TDD)**: Write tests before implementation
- **Testing Pyramid**: 70% unit, 20% integration, 10% end-to-end
- **Continuous Testing**: Automated tests on every commit
- **Coverage Target**: 90%+ for MVP critical paths, 60%+ overall

### Frameworks and Tools

**Unit Testing**
- Vitest 3.2.4 for test runner
- React Testing Library 16.3.0 for component tests
- Happy DOM 18.0.1 for DOM simulation
- fake-indexeddb for Dexie mocking

**Integration Testing**
- Firebase Emulator Suite for backend testing
- Playwright 1.55.0 for API integration tests

**End-to-End Testing**
- Playwright 1.55.0 for browser automation
- Cross-browser testing: Chromium, Firefox, WebKit

## 2. Unit Testing (MVP Features)

### Component Tests

**Note Editor Component**
- Renders Tiptap editor correctly
- Switches between Create/Edit/Study modes
- Displays mode-specific UI elements (Blue/Purple/Green accents)
- Handles content updates with debouncing
- Shows autocomplete suggestions in Create and Edit modes
- Disables editing in Study Mode

**Mode Toggle Component**
- Toggles between Create/Edit/Study modes
- Updates visual indicators (accent colors)
- Preserves scroll position during transitions
- Fires mode change events
- Transition animation completes within 300ms

**Inline Diff Component (Edit Mode Only)**
- Displays diff between current content and last saved snapshot
- Highlights additions (green), deletions (red), unchanged (gray)
- Updates in real-time with 500ms debounce
- Shows toolbar button only in Edit Mode
- Calculates diff within 200ms

**Autocomplete Popup**
- Appears after 150ms typing pause
- Displays max 5 suggestions
- Keyboard navigation (Arrow Up/Down, Enter/Tab, Escape)
- Highlights matched prefix in suggestions
- Dismisses on selection or Escape key
- Falls back to local dictionary when quota exceeded

**Key Terms Sidebar (Study Mode Only)**
- Displays spotted terms with context
- Click term to jump to location in note
- Shows importance level (high/medium/low)
- Export key terms list button
- Only visible in Study Mode

### State Management Tests

**Zustand Store**
- Updates editor mode (Create/Edit/Study)
- Tracks mode transition state
- Manages user preferences
- Stores note metadata
- Manages AI request quota tracking (autocomplete + key term spotting)
- Handles quota usage updates

### Custom Tiptap Extension Tests

**Autocomplete Extension**
- Triggers suggestions after typing pause (150ms)
- Filters suggestions based on context
- Inserts selected suggestion at cursor
- Tracks quota usage
- Falls back to dictionary when quota exceeded

**Inline Diff Extension (Edit Mode)**
- Calculates diff between current and saved content
- Highlights changes inline
- Updates on content change (debounced 500ms)

### Business Logic Tests

**Diff Calculation Utilities**
- Calculates word-level diff accurately
- Generates additions, deletions, unchanged sections
- Computes change summary (added/removed words)
- Performs diff calculation within 200ms target
- Handles large documents (3000+ words)

**Sync Queue Manager**
- Adds operations to queue (create, update, delete)
- Processes queue in order (FIFO)
- Retries failed operations with exponential backoff
- Removes operations after 5 failed retries
- Tracks retry count and last error

**Quota Tracker (MVP: 2 quotas)**
- Increments autocomplete request count
- Increments key term spotting use count
- Resets quota on monthly cycle
- Enforces Free tier limits (100 autocomplete, 10 key term spotting)
- Allows unlimited for Pro tier

**Version Snapshot Manager (Backend Only)**
- Creates snapshots on auto-save interval (30s)
- Creates snapshots on manual save
- Creates snapshots on mode switch
- Calculates change summary accurately
- Enforces retention policy (Free: 5 snapshots, Pro: unlimited)
- **No UI tests needed** (backend infrastructure only)

## 3. Integration Testing (MVP)

### Firebase Integration

**Authentication**
- Signs up new user with email/password
- Signs in existing user
- Signs out user
- Sends password reset email
- Validates auth token on API requests

**Firestore Operations**
- Creates user document on signup
- Creates note document with correct schema
- Updates note content and metadata
- Deletes note and cascades to snapshots
- Queries notes with filters (course, tags, date)
- Enforces security rules (user isolation)

**Version Snapshot Operations (Backend Only)**
- Creates snapshot in subcollection
- Retrieves last saved snapshot for inline diff
- Deletes excess snapshots (Free tier cleanup)
- **No UI integration tests** (backend infrastructure only)

**Cloud Functions (MVP Only)**
- Initializes user document on signup
- Processes AI autocomplete request (GPT-4.1 nano)
- Processes key term spotting request (GPT-4o-mini)
- Tracks quota usage accurately
- Returns 429 when quota exceeded

### Dexie Integration

**Local Storage Operations**
- Stores notes in IndexedDB
- Retrieves notes with queries
- Updates note content locally
- Deletes notes and related snapshots
- Performs full-text search

**Sync Queue Operations**
- Adds operations to queue
- Processes queue when online
- Marks operations as synced on success
- Retries failed operations
- Cleans up completed operations

**Conflict Resolution**
- Resolves conflicts using last-write-wins
- Compares version numbers
- Compares timestamps when versions match
- Merges remote changes with local data

### Mode Transition Integration

**Create to Edit Transition**
- Creates mode_switch snapshot before transition
- Updates mode indicator (Blue to Purple)
- Shows inline diff button in Edit mode
- Preserves note content and cursor position

**Edit to Study Transition**
- Creates mode_switch snapshot before transition
- Updates mode indicator (Purple to Green)
- Disables editing in Study Mode
- Shows key terms sidebar

**Study to Edit Transition**
- Updates mode indicator (Green to Purple)
- Re-enables editing
- Shows inline diff button
- Hides key terms sidebar

## 4. End-to-End Testing (MVP)

### Critical User Workflows

**New User Onboarding**
- Sign up with email/password
- Complete 2-screen onboarding
  - Screen 1: Learn about three modes
  - Screen 2: Interactive demo
- Create first note

**Create Note Workflow**
- Create new note in Create mode
- Type with AI autocomplete assistance (GPT-4.1 nano)
- Auto-save creates snapshots every 30s
- Manual save creates snapshot
- Note appears in Note Library

**Edit Note Workflow**
- Open existing note from library
- Edit or Study Dialog appears
- Select "Edit this note"
- Make changes with autocomplete
- Click inline diff button to view changes
- Save changes manually

**Study Note Workflow**
- Open existing note from library
- Edit or Study Dialog appears
- Select "Study this note"
- AI spots key terms (GPT-4o-mini)
- View key terms in sidebar
- Click term to jump to location
- Export key terms list

**Edit or Study Dialog**
- Dialog appears when opening existing note
- Shows note metadata (created, last edited, word count)
- Two buttons: "Edit this note" | "Study this note"
- Clicking Edit opens in Edit Mode
- Clicking Study opens in Study Mode

### Performance Testing (MVP)

**Autocomplete Latency**
- Trigger autocomplete after typing pause
- Measure latency from keystroke to suggestion display
- Verify <100ms performance target (GPT-4.1 nano)
- Test with 200-character context

**Mode Transition Speed**
- Measure UI response time for mode switch
- Verify <50ms transition target
- Test smooth animation (300ms color fade)

**Inline Diff Calculation**
- Measure diff calculation time in Edit mode
- Verify <200ms target for 3000-word note
- Test real-time updates with 500ms debounce

**AI Feature Performance**
- Key term spotting: <5s for 3000-word note (GPT-4o-mini)

## 5. Security Testing (MVP)

**Authentication Security**
- Validates Firebase Auth tokens on all requests
- Rejects requests with missing or invalid tokens
- Enforces session timeout (1-hour refresh)

**Firestore Security Rules**
- Users can only read/write their own data
- Snapshots inherit parent note permissions
- Notes isolated by userId

**Input Validation**
- Validates all API inputs with Zod schemas
- Sanitizes user input to prevent XSS
- Validates file uploads (size, type)

## 6. Accessibility Testing (MVP)

**Keyboard Navigation**
- Tab order follows visual hierarchy
- All actions accessible via keyboard shortcuts
- Autocomplete navigable with Arrow keys
- Focus indicators visible (2px outline)

**Screen Reader Support**
- ARIA labels on all interactive elements
- Role attributes for custom components
- Live regions for autocomplete and notifications

**Color Contrast**
- WCAG AA compliance (4.5:1 minimum)
- Mode indicators use both color and icon
- Dark mode maintains contrast ratios

## 7. Offline and Sync Testing (MVP)

**Offline Functionality**
- Create notes offline (stored in Dexie)
- Edit notes offline with auto-save
- Queue sync operations when offline
- Display sync status indicator

**Sync Queue Processing**
- Process queue when back online
- Retry failed operations with backoff
- Update sync status on success
- Log errors after 5 failures

**Conflict Resolution**
- Detect conflicts using version numbers
- Apply last-write-wins strategy
- Merge remote changes correctly
- Update local cache after sync

## 8. AI Feature Testing (MVP Only)

**Autocomplete Accuracy (GPT-4.1 nano)**
- Suggests nursing-specific terminology
- Suggests common abbreviations
- Falls back to dictionary when quota exceeded
- Acceptance rate target: >40%

**Key Term Spotting Accuracy (GPT-4o-mini)**
- Identifies exam-relevant terms
- Detects professor emphasis cues ("important", "remember", "test will cover")
- Highlights critical concepts
- Provides context snippets
- Precision target: >80%

## 9. Tier and Quota Testing (MVP)

**Free Tier Limits**
- Enforces 100 autocomplete requests/month
- Enforces 10 key term spotting uses/month
- Shows quota warning at 80% usage
- Displays upgrade modal at 100% usage
- Falls back to dictionary autocomplete
- Retains last 5 snapshots per note (backend only)

**Pro Tier Unlimited**
- Allows unlimited autocomplete requests
- Allows unlimited key term spotting
- Retains unlimited snapshots (backend only)

**Quota Tracking**
- Increments quota accurately
- Resets quota monthly
- Tracks across devices (Firestore sync)
- Displays remaining quota in UI

## 10. Test Environment Setup

**Firebase Emulator**
- Firestore emulator on localhost:8080
- Auth emulator on localhost:9099
- Functions emulator on localhost:5001

**Test Data Fixtures**
- Sample user accounts (Free, Pro, Team tiers)
- Sample notes with various content types
- Sample version snapshots (backend only)

**Mock Services**
- Mock OpenAI API responses (GPT-4.1 nano, GPT-4o-mini)
- Mock network failures for offline testing
- Mock quota limits for tier testing

## 11. CI/CD Integration

**Automated Testing Pipeline**
- Run unit tests on every commit
- Run integration tests on PR
- Run E2E tests on staging deployment
- Generate coverage reports
- Block merge if coverage drops below threshold (90% for critical paths)

**Pre-commit Hooks**
- Run ESLint and TypeScript checks
- Run unit tests for changed files
- Format code with Prettier

## 12. Test Coverage Requirements (MVP)

**Critical Paths (90%+ coverage required)**
- Three-mode workflow (Create/Edit/Study)
- Mode transitions and visual indicators
- AI autocomplete with quota (GPT-4.1 nano)
- Inline diff calculation (Edit Mode)
- Key term spotting (Study Mode, GPT-4o-mini)
- Auto-save with version snapshots (backend)
- Sync functionality
- Security rules enforcement

**Important Paths (80%+ coverage required)**
- Edit or Study Dialog
- 2-screen onboarding
- Note library with search
- Offline functionality
- Error handling and recovery

**Supporting Features (60%+ coverage required)**
- UI components
- Utility functions
- Analytics and logging

## 13. Deferred Testing (Fast-Follow: Week 5-8)

**Week 5-6**
- Templates testing
- Slash commands testing
- Shorthand expansion testing
- Definition lookup testing

**Week 7-8**
- Cloze deletion generator testing
- Full version history UI testing
- Side-by-side diff viewer testing

## 14. MVP Testing Checklist

Before beta launch (Week 5), all critical paths must have:
- ✓ Unit tests written and passing (90%+ coverage)
- ✓ Integration tests passing
- ✓ E2E tests for complete workflows passing
- ✓ Performance tests meeting targets (<100ms autocomplete, <5s key terms, <200ms inline diff)
- ✓ Security tests passing
- ✓ Accessibility tests passing (WCAG AA)
- ✓ Cross-browser tests passing (Chromium, Firefox, WebKit)
- ✓ Offline functionality tests passing
- ✓ Quota enforcement tests passing

**No Exceptions**: MVP launches with 90%+ test coverage on critical paths.

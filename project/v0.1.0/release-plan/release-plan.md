# Release Plan: NEXLY RN - Nursing Note-Taking Application

## Overview

**Project Title:** NEXLY RN - AI-Powered Nursing Note-Taking PWA

**Version:** `v0.1.0`

**Target Release Date:** 6-Week Build Timeline

**Last Updated:** 2025-12-02

**Related Documentation:**

- PRD: `project/v0.1.0/specs/prd.md`
- Tech Specs: `project/v0.1.0/specs/tech-specs.md`
- UI/UX: `project/v0.1.0/specs/ux.md`

**Development Approach:** Contract-First, Mock-Driven Development

1. Define interfaces, types, and Zod schemas as single source of truth
2. Build frontend/UI with mocked data including error states and edge cases
3. Validate and iterate on UX quickly while backend is fake
4. Implement real backend incrementally, one endpoint at a time
5. Replace mocks with real integrations using feature flags
6. Enforce end-to-end type safety with shared schemas
7. Keep mocks for testing and local development

## Roadmap

**Task ID Convention:** Sequential numbering (T001, T002, T003...)

**Notation Guide:**

- [P] for Parallel Tasks - task has NO dependencies on other tasks in same milestone
- [SA] for Subagent Tasks - isolated tasks that can be delegated to subagents without context
- Tasks without [P] have dependencies on previous tasks
- MS-[NNN]: Milestone Number (e.g. MS-001)
- T[NNN]: Task Number (e.g. T001)

---

### Phase 1: Foundation & Contracts

**CRITICAL: This phase establishes the development environment, type system, and mock infrastructure. All subsequent phases depend on successful completion.**

#### **MS-001:** Environment Setup (Week 1)

**Goal:** Next.js 15 + React 19 development environment fully configured with TypeScript strict mode, testing infrastructure, and PWA support

**Tasks:**

- [ ] T001 [P]: Initialize Next.js 15.1 project with App Router, React 19.1, and TypeScript 5.9
- [ ] T002 [P]: Configure Tailwind CSS 4.1 with Shadcn UI theme tokens (see UX Section 2)
- [ ] T003 [P]: Set up ESLint, Prettier, and TypeScript strict mode configuration
- [ ] T004: Install core dependencies (Zod, Zustand, Immer, next-pwa)
- [ ] T005: Install dev dependencies (Vitest 3.2.4, Playwright 1.55.0, React Testing Library, MSW)
- [ ] T006: Configure Vitest for unit testing with React support
- [ ] T007: Configure Playwright for E2E testing (Chrome, Firefox, WebKit)
- [ ] T008: Set up environment variables structure (.env.local, .env.example) per Tech Specs Section 12
- [ ] T009: Configure next-pwa 5.6.0 with service worker and manifest.json (FR-035, FR-036, FR-037)
- [ ] T010: Create project folder structure per Tech Specs Section 11
- [ ] T010A [P]: Configure global React error boundary component for unhandled errors
- [ ] T010B [P]: Set up structured logging with log levels (debug, info, warn, error)

**Acceptance Criteria:**

- [ ] `npm run dev` starts development server without errors
- [ ] `npm run build` completes successfully
- [ ] TypeScript compilation passes with strict mode
- [ ] PWA manifest loads correctly with app icons
- [ ] Service worker registers in browser
- [ ] Vitest runs with `npm test`

**Verification:**

- Run `npm run build && npm run start` and verify production build works
- Install PWA on desktop and verify it launches standalone
- Run `npx vitest run` to verify test infrastructure

---

#### **MS-002:** Core Type Definitions & Zod Schemas (Week 1)

**Goal:** Define TypeScript interfaces and Zod validation schemas as single source of truth for all data models

**Tasks:**

- [ ] T011 [P] [SA]: Define UserProfile type with tier, usage, settings, and Stripe fields (Tech Specs Section 3)
- [ ] T012 [P] [SA]: Define Note type with content (JSONContent), category, metadata, syncStatus
- [ ] T013 [P] [SA]: Define Snapshot type for sync conflict recovery
- [ ] T014 [P] [SA]: Define category enum: pharmacology, med-surg, pediatrics, ob, mental-health, clinical-rotation, other
- [ ] T015: Create Zod schemas for Note validation (noteSchema, noteContentSchema) with runtime validation
- [ ] T016: Create Zod schemas for User validation (userSchema, userPreferencesSchema)
- [ ] T017: Define API request/response types with Zod schemas (autocompleteRequestSchema, autocompleteResponseSchema)
- [ ] T018 [SA]: Define AI types (AutocompleteRequest, AutocompleteResponse, suggestion source)
- [ ] T019 [SA]: Define Stripe types (checkout session, webhook events, subscription status)
- [ ] T020 [SA]: Create shared utility types (Result<T,E>, AsyncState<T>, APIResponse<T>)
- [ ] T021 [SA]: Define error types (AppError, ValidationError, NetworkError, SyncError)
- [ ] T022: Create type-safe API client interface with inferred types from Zod schemas
- [ ] T023: Create barrel exports in src/types/index.ts

**Acceptance Criteria:**

- [ ] All core types defined with proper TypeScript interfaces
- [ ] Zod schemas implemented for all critical data structures
- [ ] API types inferred from Zod schemas (no duplication)
- [ ] Type exports organized in barrel files
- [ ] No TypeScript compilation errors

**Verification:**

- Run `npx tsc --noEmit` and confirm zero errors
- Verify all types are exported from src/types/index.ts
- Test Zod schema validation with sample data

---

#### **MS-003:** Mock Infrastructure & API Layer (Week 1)

**Goal:** Create comprehensive mock system for all APIs with realistic delays, error states, and edge cases

**Tasks:**

- [ ] T024 [P]: Set up MSW (Mock Service Worker) for API mocking in browser and tests
- [ ] T025 [P]: Create mock data generators using Zod schemas (faker integration)
- [ ] T026 [P]: Create mock user data with different tiers (free, pro) and quota states
- [ ] T027 [P]: Create mock notes collection (10-20 notes across all categories)
- [ ] T028: Create mock AI autocomplete handler with realistic 150-200ms delays
- [ ] T029: Create mock dictionary fallback with 5,000+ nursing terms sample
- [ ] T030: Create mock Stripe checkout/webhook handlers
- [ ] T031: Create mock auth handlers (login, signup, logout, password reset)
- [ ] T032: Implement error simulation (network errors, quota exceeded, validation failures)
- [ ] T033: Create feature flag system for toggling mock vs real APIs
- [ ] T034: Create mock sync status simulation (online, offline, syncing, conflict)
- [ ] T035: Document mock API contracts in src/mocks/README.md
- [ ] T035A [P]: Create migration versioning strategy for PostgreSQL schema changes

**Acceptance Criteria:**

- [ ] MSW intercepts all API calls in development mode
- [ ] Mock responses match Zod schema definitions exactly
- [ ] Error states can be triggered programmatically
- [ ] Feature flags toggle between mock and real APIs
- [ ] Realistic delays simulate production latency

**Verification:**

- Start dev server and verify network tab shows mocked responses
- Trigger error states and verify UI handles them correctly
- Toggle feature flags and verify API switching works

---

### Phase 2: UI Development with Mocks

**Build complete frontend experience using mocked backends. Validate UX before implementing real integrations.**

#### **MS-004:** Authentication UI (Week 1-2)

**Goal:** Complete authentication flow with form validation, error handling, and session management (all using mocks)

**Tasks:**

- [ ] T036 [P]: Build Login page UI with form validation (8+ chars, 1 upper, 1 lower, 1 number, 1 special)
- [ ] T037 [P]: Build Sign Up page UI with password requirements checklist (UX Section 4.1)
- [ ] T038 [P]: Build Password Reset page and email flow UI
- [ ] T039: Create useAuth hook with mock authentication state
- [ ] T040: Create auth middleware for protected routes (middleware.ts) using mock session
- [ ] T041: Implement session state management with Zustand
- [ ] T042: Add session expiry handling UI (prompt re-authentication, preserve local data)
- [ ] T043: Create AuthProvider context with mock user data
- [ ] T044: Add loading states and error handling for all auth flows
- [ ] T045: Write unit tests for auth forms and validation

**Acceptance Criteria:**

- [ ] User can sign up with mock email/password meeting requirements (FR-022)
- [ ] User can log in and maintain mock session across browser sessions (FR-023)
- [ ] User can reset password via mock email flow (FR-024)
- [ ] Protected routes redirect unauthenticated users to login
- [ ] All form validations work with proper error messages

**Verification:**

- Test signup flow with valid/invalid inputs
- Test login with mock credentials
- Verify protected route redirection
- Test password reset flow

---

#### **MS-005:** Tiptap Editor Integration (Week 2)

**Goal:** Rich text editor with auto-save, formatting toolbar, and distraction-free UI (local storage only)

**Tasks:**

- [ ] T046: Install Tiptap 3.4 dependencies (@tiptap/react, @tiptap/starter-kit, extensions)
- [ ] T047: Create base TiptapEditor component with dynamic import (SSR disabled)
- [ ] T048: Implement editor placeholder: "Start typing your notes... Type / for commands"
- [ ] T049: Build editor toolbar with formatting buttons (Bold, Italic, Heading, List, Link) per UX Section 4.4
- [ ] T050: Create inline title editing in toolbar
- [ ] T051: Implement category dropdown in toolbar (7 predefined categories)
- [ ] T052: Add AI quota badge component showing remaining requests or "Dictionary" mode (mock data)
- [ ] T053: Add sync status indicator (Synced/Offline/Syncing...) with color states (mock states)
- [ ] T054: Add save status indicator ("Saved just now" → "Saved 1m ago" → "Saved 5m ago")
- [ ] T055: Implement editor max-width 900px centered layout with responsive padding
- [ ] T056: Create EditorSkeleton loading component for dynamic import
- [ ] T057: Write unit tests for editor toolbar and status indicators
- [ ] T057A [P]: Implement XSS sanitization layer for Tiptap content using DOMPurify
- [ ] T057B [P]: Handle large paste operations (>10KB) with progress indicator

**Acceptance Criteria:**

- [ ] Editor loads without SSR errors
- [ ] All formatting options work (bold, italic, headings, lists, links)
- [ ] Toolbar displays all status indicators correctly
- [ ] Editor handles up to 50,000 characters without performance degradation (NFR)

**Verification:**

- Paste 50,000 character document and verify no lag
- Test all formatting options and verify they apply correctly
- Verify toolbar is responsive on mobile (overflow menu)

---

#### **MS-006:** Auto-Save & Local Storage (Week 2)

**Goal:** Implement 30-second auto-save to localStorage/IndexedDB with visual feedback (mock sync layer)

**Tasks:**

- [ ] T058: Create local storage abstraction layer (PowerSync SQLite interface)
- [ ] T059: Implement note CRUD operations on local storage
- [ ] T060: Create useAutoSave hook with 30-second debounced save
- [ ] T061: Implement save indicator state machine (idle → saving → saved)
- [ ] T062: Create useLocalNotes hook for CRUD operations
- [ ] T063: Implement note version tracking (version number increments on each save)
- [ ] T064: Add error handling for failed local saves with retry
- [ ] T065: Create mock sync queue that simulates PowerSync behavior
- [ ] T066: Write unit tests for auto-save and local storage hooks

**Acceptance Criteria:**

- [ ] Notes auto-save every 30 seconds without blocking editor (FR-016)
- [ ] Save indicator shows "Saved" with timestamp after successful save
- [ ] Local saves complete within 500ms (NFR)
- [ ] App preserves changes if closed without manual save

**Verification:**

- Edit note, wait 30 seconds, close browser, reopen and verify changes preserved
- Time save operation and confirm <500ms
- Test save while "offline" (must complete within 500ms locally)

---

#### **MS-007:** Slash Command System (Week 2)

**Goal:** Implement /template and /formula slash commands with floating menu

**Tasks:**

- [ ] T067: Create Tiptap slash command extension with "/" trigger
- [ ] T068: Build SlashCommandMenu floating component (320px width, 400px max-height)
- [ ] T069: Implement menu keyboard navigation (arrow keys, Enter, Escape)
- [ ] T070 [SA]: Create template content definitions (Care Plan, Medication Card, SOAP Note, Head-to-Toe, Pathophysiology)
- [ ] T071 [SA]: Create formula content definitions with normal ranges (MAP, BMI, IV Drip, Dosage, GCS, Fluid Deficit)
- [ ] T072: Implement template insertion with cursor positioning in first field
- [ ] T073: Implement formula insertion with formatted structure
- [ ] T074: Add search/filter as user types after "/"
- [ ] T075: Style menu items per UX Section 4.5 (44px height, hover states)
- [ ] T076: Add mobile adaptation (full-width bottom sheet, 52px touch targets)
- [ ] T077: Write unit tests for slash command parsing and insertion

**Acceptance Criteria:**

- [ ] Typing "/" opens command menu (FR-003)
- [ ] /template offers 5 template options (FR-004)
- [ ] /formula offers 6 formula options with normal ranges (FR-005)
- [ ] Selected template inserts with cursor in first field
- [ ] Menu closes on Escape or clicking outside

**Verification:**

- Type "/template" and verify all 5 options appear
- Insert Care Plan and verify cursor is in Nursing Diagnosis section
- Insert MAP formula and verify normal range "70-100 mmHg" is included

---

#### **MS-008:** AI Autocomplete UI (Week 2)

**Goal:** Implement autocomplete UI with mock AI responses and dictionary fallback

**Tasks:**

- [ ] T078: Create AutocompletePopup component (300px width, 5 suggestions max)
- [ ] T079: Create useAutocomplete hook with mock AI/dictionary source detection
- [ ] T080: Load sample nursing dictionary (500 terms for development)
- [ ] T081: Implement dictionary prefix matching for offline/over-quota fallback
- [ ] T082: Add suggestion source badges ("AI" blue / "Dictionary" gray)
- [ ] T083: Implement Tab/Enter to accept suggestion
- [ ] T084: Add debouncing (150ms) for autocomplete requests
- [ ] T085: Handle mock API timeout with dictionary fallback
- [ ] T086: Create quota tracking UI with mock data
- [ ] T087: Write unit tests for autocomplete hook and popup

**Acceptance Criteria:**

- [ ] Mock AI suggestions appear within 200ms of typing (FR-001)
- [ ] Dictionary fallback works when simulating offline (FR-002)
- [ ] Dictionary fallback works when simulating quota exceeded (FR-002)
- [ ] Quota badge updates after each mock AI request (FR-027)

**Verification:**

- Type "met" and verify mock suggestions appear
- Simulate quota exceeded and verify seamless switch to dictionary mode
- Simulate offline and verify dictionary autocomplete still works

---

#### **MS-009:** Note CRUD UI (Week 2)

**Goal:** Complete note library with create, read, update, delete functionality (mock data)

**Tasks:**

- [ ] T088: Create Notes Library page layout with header, filter bar, note cards
- [ ] T089: Build NoteCard component with title, preview, category badge, date, sync status
- [ ] T090: Implement "New Note" button opening blank editor (FR-006)
- [ ] T091: Implement note list with grid/list view toggle (FR-007)
- [ ] T092: Implement click-to-open note in editor (FR-008)
- [ ] T093: Add inline note title renaming (FR-010)
- [ ] T094: Implement note duplication (FR-011)
- [ ] T095: Add context menu (right-click/long-press) with Rename, Duplicate, Export, Delete
- [ ] T096: Implement soft delete (isDeleted flag, deletedAt timestamp) (FR-009)
- [ ] T097 [SA]: Create empty state with illustration and "Create Note" CTA (UX Section 4.3)
- [ ] T098: Write unit tests for note card and library components
- [ ] T098A [P]: Add analytics tracking for slash command usage (measure PRD Goal #3)

**Acceptance Criteria:**

- [ ] User can create new notes with cursor ready for input (FR-006)
- [ ] User can view notes in library with previews (FR-007)
- [ ] User can edit existing notes by clicking them (FR-008)
- [ ] User can rename, duplicate, and delete notes
- [ ] Empty state displays when no notes exist

**Verification:**

- Create 10 notes with different categories
- Rename a note and verify title updates in library
- Delete a note and verify it disappears from main library

---

#### **MS-010:** Note Organization UI (Week 2-3)

**Goal:** Implement category filtering, search, and sorting with mock data

**Tasks:**

- [ ] T099: Implement category filter dropdown/chips (7 categories) (FR-012)
- [ ] T100: Implement sort options (date created, last modified, alphabetical) (FR-013)
- [ ] T101: Create useNoteSearch hook with real-time search on title and content (FR-014)
- [ ] T102: Build search input with debounced query (300ms)
- [ ] T103: Add "No results" empty state for search (UX Section 10)
- [ ] T104: Add "No notes in [category]" empty state for category filter
- [ ] T105: Persist filter/sort preferences in localStorage
- [ ] T106: Write unit tests for search and filter logic

**Acceptance Criteria:**

- [ ] Category filter shows only notes in selected category
- [ ] Search returns results within 300ms for up to 1,000 notes (NFR)
- [ ] Sort options work correctly for all three modes
- [ ] Preferences persist across sessions

**Verification:**

- Create notes in multiple categories, filter by each
- Search for partial term in note content, verify results appear
- Time search with 100 mock notes, confirm <300ms

---

#### **MS-011:** Trash System UI (Week 3)

**Goal:** Implement trash folder with 30-day recovery and permanent deletion UI

**Tasks:**

- [ ] T107: Create Trash page with header showing 30-day warning (UX Section 4.7)
- [ ] T108: Build TrashNoteCard with "Deleted X days ago" label
- [ ] T109: Implement "Restore" action to un-delete note (FR-015)
- [ ] T110: Implement "Delete Forever" action with confirmation dialog
- [ ] T111: Add "Empty Trash" button with bulk permanent delete (FR-015)
- [ ] T112 [SA]: Create trash empty state with empty bin illustration
- [ ] T113: Update notes library to exclude deleted notes from view
- [ ] T114: Write unit tests for trash operations

**Acceptance Criteria:**

- [ ] Deleted notes appear in trash folder
- [ ] User can restore notes within 30 days (FR-009)
- [ ] User can permanently delete from trash (FR-015)
- [ ] Restored notes appear back in main library

**Verification:**

- Delete a note, navigate to trash, verify it appears
- Restore a note, verify it returns to library with content intact
- Permanently delete a note, verify it no longer exists

---

#### **MS-012:** Settings & Subscription UI (Week 3)

**Goal:** Complete settings page with mock subscription and tier management

**Tasks:**

- [ ] T115: Create Settings page layout with sidebar navigation (desktop) and tabs (mobile)
- [ ] T116: Build Account section (email, display name, change password link)
- [ ] T117: Build Subscription section (tier badge, quota bar, upgrade/manage buttons) with mock data
- [ ] T118: Build Preferences section (theme toggle: Light/Dark/System, auto-save toggle)
- [ ] T119: Build Data section (export all, delete account with confirmation)
- [ ] T120: Implement theme switching with system preference detection
- [ ] T121: Persist theme preference to localStorage
- [ ] T122: Build Upgrade Modal component with feature comparison table (UX Section 4.9)
- [ ] T123: Mock Stripe checkout flow (redirect simulation)
- [ ] T124: Write unit tests for settings components

**Acceptance Criteria:**

- [ ] All settings sections display correctly
- [ ] Theme changes apply immediately across app
- [ ] Quota usage bar shows mock data accurately
- [ ] Upgrade modal displays correctly

**Verification:**

- Toggle theme and verify all pages update
- Check quota bar reflects mock usage
- Test upgrade modal display

---

#### **MS-013:** Onboarding Flow UI (Week 3)

**Goal:** Implement 2-screen onboarding introducing AI autocomplete and slash commands

**Tasks:**

- [ ] T125: Create onboarding route (/onboarding)
- [ ] T126: Build Screen 1: Welcome with feature cards (AI Autocomplete, Slash Commands) (UX Section 4.2)
- [ ] T127: Build Screen 2: Interactive demo with mini-editor for /template
- [ ] T128: Implement demo celebration animation on successful template insertion
- [ ] T129: Track onboarding completion in localStorage (mock user document)
- [ ] T130: Add in-editor tooltip showing "/" trigger until user uses 5+ times
- [ ] T131: Implement keyboard shortcut cheatsheet (accessible via "?" key)
- [ ] T132: Create persistent UI hint near editor for available commands
- [ ] T133: Write unit tests for onboarding flow

**Acceptance Criteria:**

- [ ] New users see onboarding after signup (User Story 1)
- [ ] Interactive demo lets user try /template before proceeding
- [ ] Onboarding only shows once per user
- [ ] Slash command hints persist until adoption threshold reached

**Verification:**

- Create new account, verify onboarding appears
- Complete demo interaction, verify "Start creating" button enables
- Log in again, verify onboarding does not reappear

---

#### **MS-014:** Export Functionality (Week 3)

**Goal:** Implement note export to Markdown, Plain Text, and bulk ZIP

**Tasks:**

- [ ] T134 [SA]: Implement Tiptap content to Markdown converter
- [ ] T135 [SA]: Implement Tiptap content to Plain Text converter
- [ ] T136: Add export menu options (Markdown, Plain Text) in note context menu (FR-033)
- [ ] T137: Create download trigger for single note export
- [ ] T138: Implement bulk export to ZIP with notes organized by category (FR-034)
- [ ] T139: Add "Export all notes" button in Settings (UX Section 4.8)
- [ ] T140: Write unit tests for export converters

**Acceptance Criteria:**

- [ ] User can export individual notes to .md and .txt (FR-033)
- [ ] User can bulk export all notes as ZIP (FR-034)
- [ ] Exported Markdown preserves formatting
- [ ] ZIP organized by category folders

**Verification:**

- Export note with headings, lists, bold text to Markdown
- Open in Markdown editor and verify formatting preserved
- Bulk export 5 notes in different categories, verify ZIP structure

---

#### **MS-015:** Responsive Design & Dark Mode (Week 3)

**Goal:** Ensure responsive design across all breakpoints and complete dark mode support

**Tasks:**

- [ ] T141 [P]: Implement responsive breakpoints (Mobile <640px, Tablet 640-1023px, Desktop 1024px+)
- [ ] T142 [P] [SA]: Implement dark mode color palette (UX Section 2)
- [ ] T143: Adapt navbar for mobile (hamburger menu, condensed logo)
- [ ] T144: Adapt editor toolbar for mobile (formatting in overflow menu)
- [ ] T145: Adapt notes library for mobile (search expands on tap, filters in bottom sheet)
- [ ] T146: Adapt slash command menu for mobile (full-width bottom sheet, 52px items)
- [ ] T147: Adapt settings for mobile (tab navigation instead of sidebar)
- [ ] T148: Test and fix all pages at 320px, 640px, 1024px, 2560px widths
- [ ] T149: Implement prefers-reduced-motion support (UX Section 9)
- [ ] T150: Write visual regression tests for responsive layouts

**Acceptance Criteria:**

- [ ] App usable on screens from 320px to 2560px (NFR)
- [ ] Dark mode complete with all components styled
- [ ] Mobile touch targets minimum 44x44px
- [ ] Reduced motion respected when enabled

**Verification:**

- Test on iPhone SE (320px) and 4K monitor (2560px)
- Toggle dark mode and verify all components styled correctly
- Enable reduced motion in OS, verify animations disabled

---

#### **MS-016:** Accessibility (Week 3)

**Goal:** Achieve WCAG AA compliance with keyboard navigation and screen reader support

**Tasks:**

- [ ] T151 [P]: Add ARIA labels to all interactive elements
- [ ] T152 [P]: Implement logical tab order across all pages
- [ ] T153: Add visible focus indicators to all focusable elements
- [ ] T154: Ensure 4.5:1 minimum contrast ratio for all text
- [ ] T155: Add screen reader announcements for status changes (aria-live)
- [ ] T156: Make slash command menu accessible (ARIA announcements, keyboard nav)
- [ ] T157: Test with VoiceOver (macOS/iOS) and NVDA (Windows)
- [ ] T158: Add alt text to all images and icons
- [ ] T159: Test at 200% browser zoom and fix any layout issues
- [ ] T160: Run Lighthouse accessibility audit

**Acceptance Criteria:**

- [ ] All interactive elements keyboard accessible
- [ ] Screen readers announce all content correctly
- [ ] Contrast ratios meet WCAG AA (4.5:1)
- [ ] 200% zoom works without layout breaking (NFR)

**Verification:**

- Navigate entire app using only keyboard
- Complete user flow with VoiceOver enabled
- Run Lighthouse accessibility audit (target 90+)

---

### Phase 3: Real Backend Integration

**Incrementally replace mocks with real integrations. Use feature flags to toggle during transition.**

#### **MS-017:** Supabase Setup (Week 3)

**Goal:** Configure Supabase project with Auth, PostgreSQL, and Row Level Security

**Tasks:**

- [ ] T161 [P]: Create Supabase project and configure environment variables
- [ ] T162: Configure Supabase Client SDK (client-side initialization)
- [ ] T163: Configure Supabase Admin SDK (server-side for API routes)
- [ ] T164: Create PostgreSQL tables (users, notes, snapshots) per Tech Specs Section 3
- [ ] T165: Implement Row Level Security policies per Tech Specs Section 4
- [ ] T166: Create database indexes for performance
- [ ] T167: Test RLS policies prevent cross-user data access
- [ ] T168: Create feature flag to toggle mock vs real Supabase auth

**Acceptance Criteria:**

- [ ] Supabase project fully configured
- [ ] All tables created with proper schemas
- [ ] RLS policies enforce user isolation
- [ ] Feature flag switches between mock and real auth

**Verification:**

- Attempt to access another user's data via direct query (should fail)
- Toggle feature flag and verify auth switching works

---

#### **MS-018:** Real Authentication Integration (Week 3)

**Goal:** Replace mock auth with real Supabase Auth

**Tasks:**

- [ ] T169: Implement real Supabase signup with email/password
- [ ] T170: Implement real Supabase login with session management
- [ ] T171: Implement real password reset email flow
- [ ] T172: Create POST /api/auth/initialize endpoint for user document creation
- [ ] T173: Implement session management with secure cookies (24-hour expiry)
- [ ] T174: Update auth middleware to use real Supabase session
- [ ] T175: Update AuthProvider to use real Supabase client
- [ ] T176: Add session expiry handling (prompt re-authentication, preserve local data)
- [ ] T177: Write integration tests for auth flows
- [ ] T177A [P]: Handle concurrent session detection (new device login invalidates old sessions)

**Acceptance Criteria:**

- [ ] Real signup creates user in Supabase Auth and users table
- [ ] Real login creates session that persists across browser refresh
- [ ] Password reset sends real email via Supabase
- [ ] Protected routes work with real session

**Verification:**

- Create real test account, log in, refresh browser, verify session persists
- Test password reset flow with real email
- Verify session expiry prompts re-authentication

---

#### **MS-019:** PowerSync Offline Sync (Week 3-4)

**Goal:** Implement PowerSync for offline-first sync between SQLite and Supabase

**Tasks:**

- [ ] T178: Install and configure PowerSync (@powersync/web)
- [ ] T179: Create PowerSync schema matching PostgreSQL tables
- [ ] T180: Configure PowerSync bucket definitions for user data isolation
- [ ] T181: Replace local storage layer with PowerSync SQLite
- [ ] T182: Implement useOnlineStatus hook to detect connectivity changes
- [ ] T183: Create sync status indicator connected to PowerSync state
- [ ] T184: Implement auto-sync when network restored
- [ ] T185: Create feature flag to toggle mock vs real sync
- [ ] T186: Write integration tests for offline/online sync scenarios
- [ ] T186A [P]: Handle partial sync failures with retry queue and user notification

**Acceptance Criteria:**

- [ ] Notes save to local SQLite instantly
- [ ] Notes sync to Supabase within 5 seconds of connectivity restoration (P95)
- [ ] Offline editing works with all features (FR-018)
- [ ] Sync status indicator reflects real state

**Verification:**

- Edit note offline, restore network, verify sync completes
- Check Supabase database for synced notes

---

#### **MS-020:** Sync Conflict Resolution (Week 4)

**Goal:** Implement last-write-wins conflict resolution with version history

**Tasks:**

- [ ] T187: Implement conflict detection (compare version and updatedAt)
- [ ] T188: Implement last-write-wins algorithm per Tech Specs Section 7
- [ ] T189: Create Snapshot when conflict detected (snapshotType: "sync_conflict")
- [ ] T190: Display toast notification on conflict resolution ("Version from [device] kept")
- [ ] T191: Implement exponential backoff retry (5s, 15s, 30s, 60s, 120s) for failed syncs
- [ ] T192: Update sync status indicator based on conflict state
- [ ] T193: Write integration tests for conflict scenarios

**Acceptance Criteria:**

- [ ] Conflicts resolved with last-write-wins algorithm (FR-019)
- [ ] Overwritten versions preserved as snapshots (FR-020)
- [ ] Toast notification shows conflict resolution result
- [ ] 99%+ sync reliability (NFR)
- [ ] Exponential backoff retry completes within 5 minutes or fails with user notification

**Verification:**

- Edit same note on two devices offline, bring online, verify conflict resolution
- Check snapshots table for conflict record

---

#### **MS-021:** Real AI Integration (Week 4)

**Goal:** Replace mock AI with real OpenAI GPT-4.1 nano autocomplete

**Tasks:**

- [ ] T194: Create POST /api/ai/autocomplete endpoint with token validation
- [ ] T195: Implement OpenAI GPT-4.1 nano integration with <200ms target
- [ ] T196: Add request throttling (max 1 request per 3 seconds per user)
- [ ] T197: Implement quota tracking in Supabase users table
- [ ] T198: Create GET /api/users/quota endpoint for quota checking
- [ ] T199: Load full 5,000+ nursing dictionary (nursing-terms.json) into memory
- [ ] T200: Implement dictionary prefix matching for production fallback
- [ ] T201: Update useAutocomplete hook to use real API with feature flag
- [ ] T202: Handle API timeout (>500ms) with dictionary fallback
- [ ] T203: Write integration tests for AI autocomplete

**Acceptance Criteria:**

- [ ] Real AI suggestions appear within 200ms (P95) measured from last keystroke (FR-001)
- [ ] Dictionary fallback works offline (FR-002)
- [ ] Dictionary fallback works when quota exceeded (FR-002)
- [ ] Quota updates in database after each AI request (FR-027)
- [ ] Request throttling enforced (1 per 3 seconds)

**Verification:**

- Type "met" with real API and verify suggestions appear
- Exceed quota and verify seamless switch to dictionary mode
- Time AI response and confirm <200ms typical latency

---

#### **MS-022:** Stripe Integration (Week 4)

**Goal:** Implement Pro tier subscription with Stripe checkout, webhooks, and customer portal

**Tasks:**

- [ ] T204: Create Stripe account and configure products (Pro Monthly $8.99, Pro Annual $79)
- [ ] T205: Create POST /api/stripe/checkout endpoint for checkout session
- [ ] T206: Create POST /api/stripe/webhook endpoint with signature validation
- [ ] T207: Handle checkout.session.completed webhook (update tier to Pro)
- [ ] T208: Handle customer.subscription.updated webhook (plan changes)
- [ ] T209: Handle customer.subscription.deleted webhook (downgrade to Free)
- [ ] T210: Handle invoice.payment_failed webhook (payment failure handling)
- [ ] T211: Create POST /api/stripe/portal endpoint for customer portal session
- [ ] T212: Update Settings subscription section with real Stripe data
- [ ] T213: Implement tier enforcement in AI autocomplete endpoint
- [ ] T214: Create feature flag to toggle mock vs real Stripe
- [ ] T215: Write integration tests for Stripe webhooks

**Acceptance Criteria:**

- [ ] Free users limited to 100 AI requests/month (FR-027)
- [ ] Pro users have unlimited AI requests (FR-028)
- [ ] User can upgrade via real Stripe checkout (FR-030)
- [ ] User can manage subscription via customer portal (FR-031)
- [ ] Subscription status displays correctly from Stripe

**Verification:**

- Test Stripe checkout flow with test card
- Verify webhook updates user tier in Supabase
- Confirm AI quota enforced correctly for free tier

---

### Phase 4: Testing & Deployment

#### **MS-023:** Testing Suite (Week 4)

**Goal:** Comprehensive test coverage for critical paths

**Tasks:**

- [ ] T216: Write unit tests for slash command parser and template insertion
- [ ] T217: Write unit tests for autocomplete hook (AI and dictionary modes)
- [ ] T218: Write unit tests for sync queue and conflict resolution logic
- [ ] T219 [SA]: Write unit tests for Zod validation schemas
- [ ] T220: Write E2E test: signup → onboarding → create note → save flow
- [ ] T221: Write E2E test: offline editing → reconnect → sync verification
- [ ] T222: Write E2E test: slash command insertion (/template, /formula)
- [ ] T223: Write E2E test: AI autocomplete flow and quota enforcement
- [ ] T224: Write E2E test: Stripe checkout and subscription upgrade
- [ ] T225: Set up GitHub Actions CI for test runs on PR
- [ ] T226: Ensure mocks remain available for test environment

**Acceptance Criteria:**

- [ ] All unit tests pass
- [ ] All E2E tests pass on Chromium, Firefox, WebKit
- [ ] CI runs tests on every PR
- [ ] Mocks work correctly in test environment
- [ ] Critical paths have test coverage

**Verification:**

- Run `npm run test` and confirm all pass
- Run `npm run test:e2e` on all browsers
- Create PR and verify CI runs

---

#### **MS-024:** Performance Optimization (Week 4)

**Goal:** Meet all Core Web Vitals and performance targets

**Tasks:**

- [ ] T227: Implement code splitting with dynamic imports for heavy components
- [ ] T228: Add lazy loading for notes library (virtual scrolling if >100 notes)
- [ ] T229: Optimize images with Next.js Image component
- [ ] T230: Configure service worker caching strategies (NetworkFirst for API, CacheFirst for assets)
- [ ] T231: Run Lighthouse audit and address any issues
- [ ] T232: Verify FCP <1.5s, LCP <2.5s, TTI <3.5s, CLS <0.1 (Tech Specs Section 10)
- [ ] T233: Profile and optimize Tiptap editor for 50,000 character documents
- [ ] T234: Verify client-side memory stays under 150MB with 20 notes loaded

**Acceptance Criteria:**

- [ ] Lighthouse Performance score 90+
- [ ] Core Web Vitals all in green
- [ ] AI autocomplete <200ms typical
- [ ] Search <300ms for 1,000 notes

**Verification:**

- Run Lighthouse on production build
- Test with 50,000 character note, no lag
- Profile memory usage in Chrome DevTools

---

#### **MS-025:** Deployment & Monitoring (Week 4)

**Goal:** Deploy to Vercel with monitoring, error tracking, and cost alerts

**Tasks:**

- [ ] T235: Configure Vercel project with environment variables
- [ ] T236: Set up custom domain and SSL certificate
- [ ] T237: Deploy production build to Vercel
- [ ] T238: Configure Sentry error tracking
- [ ] T239: Configure Vercel Analytics for user behavior
- [ ] T240: Set up monitoring alerts for error rates >5%
- [ ] T241: Set up cost alerts at $50, $75, $100 thresholds
- [ ] T242: Create monitoring dashboard for AI API costs per tier
- [ ] T243: Configure Supabase automatic backup
- [ ] T244: Document rollback procedure
- [ ] T245: Remove or disable mock feature flags for production
- [ ] T245A [P]: Implement PWA update notification with prompt to refresh when new version available
- [ ] T245B [P]: Configure analytics dashboard for tracking AI acceptance rate (PRD Goal #6)

**Acceptance Criteria:**

- [ ] Production app accessible at custom domain
- [ ] All unhandled exceptions, API errors (4xx/5xx), and sync failures reported to Sentry with user ID, session ID, and stack trace
- [ ] Analytics tracking user sessions
- [ ] Cost alerts configured
- [ ] Mocks disabled in production

**Verification:**

- Access production URL, verify app loads
- Trigger intentional error, verify Sentry captures
- Check Vercel Analytics dashboard

---

## Dependencies and Execution Order

**Phase Dependencies:**

- Phase 2 (UI Development) depends on Phase 1 (Foundation & Contracts) for types and mocks
- Phase 3 (Backend Integration) can begin once core UI is functional (MS-004 through MS-009)
- Phase 4 (Testing & Deployment) depends on Phase 3 completion

**Milestone Prerequisites:**

Each milestone's Goal and Prerequisite for dependency tracking:

### Phase 1: Foundation & Contracts

| Milestone  | Goal                                | Prerequisite                               |
| ---------- | ----------------------------------- | ------------------------------------------ |
| **MS-001** | Environment Setup                   | None (starting point)                      |
| **MS-002** | Core Type Definitions & Zod Schemas | MS-001 complete                            |
| **MS-003** | Mock Infrastructure & API Layer     | MS-002 complete (types must exist to mock) |

### Phase 2: UI Development with Mocks

| Milestone  | Goal                          | Prerequisite                                             |
| ---------- | ----------------------------- | -------------------------------------------------------- |
| **MS-004** | Authentication UI             | MS-003 complete                                          |
| **MS-005** | Tiptap Editor Integration     | MS-003 complete                                          |
| **MS-006** | Auto-Save & Local Storage     | MS-005 (T046-T057) complete (functional editor required) |
| **MS-007** | Slash Command System          | MS-005 (T046-T057) complete (functional editor required) |
| **MS-008** | AI Autocomplete UI            | MS-003 complete                                          |
| **MS-009** | Note CRUD UI                  | MS-003 complete                                          |
| **MS-010** | Note Organization UI          | MS-009 (T088-T091) complete                              |
| **MS-011** | Trash System UI               | MS-009 (T088-T091) complete                              |
| **MS-012** | Settings & Subscription UI    | MS-003 complete                                          |
| **MS-013** | Onboarding Flow UI            | MS-003 complete                                          |
| **MS-014** | Export Functionality          | MS-005 complete (needs Tiptap content)                   |
| **MS-015** | Responsive Design & Dark Mode | MS-004 through MS-014 complete                           |
| **MS-016** | Accessibility                 | MS-004 through MS-014 complete                           |

### Phase 3: Real Backend Integration

| Milestone  | Goal                            | Prerequisite                                                                  |
| ---------- | ------------------------------- | ----------------------------------------------------------------------------- |
| **MS-017** | Supabase Setup                  | MS-009 complete (core UI works)                                               |
| **MS-018** | Real Authentication Integration | MS-017 complete                                                               |
| **MS-019** | PowerSync Offline Sync          | MS-017 complete                                                               |
| **MS-020** | Sync Conflict Resolution        | MS-019 complete                                                               |
| **MS-021** | Real AI Integration             | MS-017 complete + MS-008 (T078-T079) complete (useAutocomplete hook required) |
| **MS-022** | Stripe Integration              | MS-018 complete (needs real auth)                                             |

### Phase 4: Testing & Deployment

| Milestone  | Goal                     | Prerequisite                                |
| ---------- | ------------------------ | ------------------------------------------- |
| **MS-023** | Testing Suite            | All feature milestones complete             |
| **MS-024** | Performance Optimization | MS-023 complete (optimize after tests pass) |
| **MS-025** | Deployment & Monitoring  | MS-024 complete (deploy optimized build)    |

### Prerequisite Visualization

```
MS-001 (Environment)
    │
    ▼
MS-002 (Types)
    │
    ▼
MS-003 (Mocks)
    │
    ├──────────────────────────────────────────────────┐
    ▼                                                  ▼
MS-004 (Auth UI) ‖ MS-005 (Editor) ‖ MS-008 ‖ MS-009 ‖ MS-012 ‖ MS-013
                       │                    │
                       ▼                    ▼
              MS-006 ‖ MS-007        MS-010 ‖ MS-011
                                            │
                                            ▼
                                    MS-014 (Export)
                                            │
                                            ▼
                                    MS-015 ‖ MS-016 (Polish)
                                            │
    ┌───────────────────────────────────────┘
    ▼
MS-017 (Supabase) ─────────────────┬───────────────────┐
    │                              │                   │
    ▼                              ▼                   ▼
MS-018 (Real Auth)          MS-019 (PowerSync)   MS-021 (Real AI)
    │                              │
    ▼                              ▼
MS-022 (Stripe)             MS-020 (Conflict)
    │                              │
    └──────────────┬───────────────┘
                   ▼
            MS-023 (Testing)
                   │
                   ▼
            MS-024 (Performance)
                   │
                   ▼
            MS-025 (Deployment)
```

**Critical Path:**

T001 → T004 → T005 → T011 → T024 → T036 → T046 → T088 → T161 → T178 → T194 → T235

(Setup → Dependencies → Types → Mocks → Auth UI → Editor → Notes UI → Supabase → PowerSync → AI → Deploy)

---

## Parallel Opportunities

**Parallel Execution Groups:**

The following milestones and tasks can run simultaneously (no dependencies between items in each group):

### Week 1: Foundation Parallel Groups

**Group 1A - Environment Setup (MS-001 internal):**

- T001: Initialize Next.js project
- T002: Configure Tailwind CSS
- T003: Set up ESLint/Prettier/TypeScript

**Group 1B - Type Definitions (MS-002 internal):**

- T011: UserProfile type
- T012: Note type
- T013: Snapshot type
- T014: Category enum

**Group 1C - Mock Infrastructure (MS-003 internal):**

- T024: Set up MSW
- T025: Mock data generators
- T026: Mock user data
- T027: Mock notes collection

### Week 1-2: UI Development Parallel Groups

**Group 2A - Auth + Editor (run simultaneously):**

- MS-004: Authentication UI
- MS-005: Tiptap Editor Integration

**Group 2B - Editor Extensions (after MS-005 T046-T047):**

- MS-006: Auto-Save & Local Storage
- MS-007: Slash Command System

**Group 2C - AI Autocomplete (MS-008 internal):**

- Backend tasks: T080, T081, T085
- Frontend tasks: T078, T079, T082-T084, T086-T087

### Week 2-3: Feature UI Parallel Groups

**Group 3A - Note Features (after MS-009 T088-T091):**

- MS-010: Note Organization UI
- MS-011: Trash System UI

**Group 3B - Settings + Onboarding + Export (run simultaneously):**

- MS-012: Settings & Subscription UI
- MS-013: Onboarding Flow UI
- MS-014: Export Functionality

### Week 3: Polish Parallel Groups

**Group 4A - Responsive + Accessibility (run simultaneously):**

- MS-015: Responsive Design & Dark Mode
- MS-016: Accessibility

### Week 3-4: Backend Parallel Groups

**Group 5A - Independent Backend Systems:**

- MS-017: Supabase Setup
- MS-021: Real AI Integration

### Week 4: Testing Parallel Groups

**Group 6A - Test Types (MS-023 internal):**

- Unit Tests: T216-T219
- E2E Tests: T220-T224

---

**Subagent Tasks (SA):**

The following 16 tasks are isolated and can be delegated to subagents without context:

| Milestone | SA Tasks | Task IDs             |
| --------- | -------- | -------------------- |
| MS-002    | 8        | T011-T014, T018-T021 |
| MS-007    | 2        | T070, T071           |
| MS-009    | 1        | T097                 |
| MS-011    | 1        | T112                 |
| MS-014    | 2        | T134, T135           |
| MS-015    | 1        | T142                 |
| MS-023    | 1        | T219                 |
| **Total** | **16**   |                      |

**UI vs Backend Parallelization:**

After Phase 1 completion, UI development (Phase 2) and backend preparation can overlap:

- Team A: Continue UI development (MS-004 through MS-016)
- Team B: Start Supabase setup (MS-017) once MS-009 is in progress

**Mock Preservation:**

- Mocks developed in MS-003 remain available throughout project
- Feature flags allow gradual migration from mocks to real backends
- Tests continue using mocks even after real backends deployed

---

## Implementation Strategy

1. **Week 1 Priority:** Complete MS-001 (Environment), MS-002 (Types)
2. **Week 2 Priority:** Complete MS-003 (Mocks), MS-004 (Auth UI)
3. **Week 3 Priority:** Complete MS-005 through MS-009 (Editor, Auto-save, Slash Commands, AI, CRUD)
4. **Week 4 Priority:** Complete MS-010 through MS-014 (Organization, Trash, Settings, Onboarding, Export)
5. **Week 5 Priority:** Complete MS-015 through MS-020 (Responsive, Accessibility, Supabase, Auth, PowerSync, Conflicts)
6. **Week 6 Priority:** Complete MS-021 through MS-025 (AI Integration, Stripe, Testing, Performance, Deployment)

**Contract-First Approach:**

- Zod schemas are single source of truth
- Types derived from schemas (no duplication)
- Mocks validate against schemas
- API responses validated at runtime

**Mock-Driven Development:**

- Build complete UI before touching real backends
- Mocks include realistic delays, errors, and edge cases
- Feature flags control mock vs real switching
- Mocks preserved for development and testing

**Incremental Integration:**

- Replace one mock at a time with real implementation
- Feature flags enable gradual rollout
- Rollback to mocks if issues discovered
- Integration tests verify each replacement

---

## Risks & Blockers

| Risk ID | Description                             | Affected Milestone(s) | Mitigation Plan                                                  |
| ------- | --------------------------------------- | --------------------- | ---------------------------------------------------------------- |
| R001    | OpenAI API unavailability               | MS-021                | Dictionary fallback implemented; mocks available                 |
| R002    | Stripe webhook signature validation     | MS-022                | Use Stripe CLI for local testing; mock webhooks available        |
| R003    | Tiptap performance with large documents | MS-005                | Early performance testing with 50k char docs                     |
| R004    | Sync conflicts data loss                | MS-020                | Comprehensive snapshot system; mock conflict scenarios           |
| R005    | PWA installation discoverability        | MS-001                | Clear install prompts; test on multiple platforms                |
| R006    | Supabase service outages                | MS-019                | Offline-first with PowerSync; mocks as fallback                  |
| R007    | AI hallucination (incorrect terms)      | MS-021                | Validate against dictionary; test with mock edge cases           |
| R008    | Mock/Real integration gaps              | MS-017-022            | Schema validation ensures mock/real parity                       |
| R009    | Timeline pressure with 6-week schedule  | All                   | Weekly scope reviews; prioritize P0 features; defer enhancements |
| R010    | React 19 / Next.js 15 ecosystem gaps    | MS-001                | Pin exact versions; test early; have fallback to React 18        |
| R011    | PowerSync learning curve                | MS-019                | Allocate extra time; review documentation; build POC first       |

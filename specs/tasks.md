# Tasks: NEXLY RN - Nursing Note-Taking Application

## Overview

**Project Title:** NEXLY RN - AI-Powered Nursing Note-Taking PWA

**Target Release Date:** 4-Week Build Timeline (see Tech Specs Section 16)

**Last Updated:** 2025-11-26

**Related Documentation:**

- PRD: `specs/prd.md`
- Tech Specs: `specs/tech-specs.md`
- UI/UX: `specs/ux.md`

**Task Status Legend:**

- ⏳ Not Started
- 🔄 In Progress
- ✅ Completed
- ⚠️ Blocked (include blocker ID)
- ❌ Cancelled

## Roadmap

**Task ID Convention:** Sequential numbering (T001, T002, T003...)

**Notation Guide:**

- [P] for Parallel Tasks - task has NO dependencies on other tasks in same sprint
- Tasks without [P] have dependencies on previous tasks

---

### Phase 1: Foundation

**CRITICAL: This phase establishes the development environment and core type system. All subsequent phases depend on successful completion.**

#### **SPRINT-001:** Environment Setup (Week 1)

**Goal:** Next.js 15 + React 19 development environment fully configured with Firebase, Stripe, and PWA support

**Tasks:**

- T001 [P]: Initialize Next.js 15.1 project with App Router, React 19.1, and TypeScript 5.9
- T002 [P]: Configure Tailwind CSS 4.1 with Shadcn UI theme tokens (see UX Section 2)
- T003 [P]: Set up ESLint, Prettier, and TypeScript strict mode configuration
- T004: Install core dependencies (Firebase SDK, Dexie, Zustand, Immer, OpenAI, Stripe, Zod)
- T005: Install dev dependencies (Vitest 3.2.4, Playwright 1.55.0, React Testing Library)
- T006: Configure Vitest for unit testing with React support
- T007: Configure Playwright for E2E testing (Chrome, Firefox, WebKit)
- T008: Set up environment variables structure (.env.local, .env.example) per Tech Specs Section 12
- T009: Configure next-pwa 5.6.0 with service worker and manifest.json (FR-035, FR-036, FR-037)
- T010: Create project folder structure per Tech Specs Section 11

**Acceptance Criteria:**

- [ ] `npm run dev` starts development server without errors
- [ ] `npm run build` completes successfully
- [ ] TypeScript compilation passes with strict mode
- [ ] PWA manifest loads correctly with app icons
- [ ] Service worker registers in browser

**Verification:**

- Run `npm run build && npm run start` and verify production build works
- Install PWA on desktop and verify it launches standalone
- Run `npx vitest run` to verify test infrastructure

---

#### **SPRINT-002:** Firebase & Authentication Setup (Week 1)

**Goal:** Firebase project configured with Auth and Firestore, authentication flows implemented

**Tasks:**

- T011: Configure Firebase Client SDK (Client-side initialization)
- T012: Configure Firebase Admin SDK (Server-side for API routes)
- T013: Implement Firestore security rules per Tech Specs Section 4
- T014: Create auth middleware for protected routes (middleware.ts)
- T015: Build Login page UI with form validation (8+ chars, 1 upper, 1 lower, 1 number, 1 special)
- T016: Build Sign Up page UI with password requirements checklist (UX Section 4.1)
- T017: Build Password Reset page and email flow
- T018: Implement session management with httpOnly cookies (24-hour expiry)
- T019: Create POST /api/auth/initialize endpoint for user document creation
- T020: Add session expiry handling (prompt re-authentication, preserve local data)

**Acceptance Criteria:**

- [ ] User can sign up with email/password meeting requirements (FR-022)
- [ ] User can log in and maintain session across browser sessions (FR-023)
- [ ] User can reset password via email (FR-024)
- [ ] Protected routes redirect unauthenticated users to login
- [ ] Firestore rules prevent cross-user data access

**Verification:**

- Create test account, log in, refresh browser, verify session persists
- Attempt to access another user's data via direct Firestore query (should fail)
- Test password reset flow end-to-end

---

#### **SPRINT-003:** Core Type Definitions (Week 1)

**Goal:** Define TypeScript interfaces and Zod validation schemas for all data models

**Tasks:**

- T021 [P]: Define UserProfile type with tier, usage, settings, and Stripe fields (Tech Specs Section 3)
- T022 [P]: Define Note type with content (JSONContent), category, metadata, syncStatus
- T023 [P]: Define VersionSnapshot type for sync conflict recovery
- T024 [P]: Define category enum: pharmacology, med-surg, pediatrics, ob, mental-health, clinical-rotation, other
- T025: Create Zod schemas for Note validation (noteSchema, noteContentSchema)
- T026: Create Zod schemas for API request/response validation
- T027: Define Dexie database schema (NexlyDatabase class) per Tech Specs Section 3
- T028: Define AI types (AutocompleteRequest, AutocompleteResponse, suggestion source)
- T029: Define Stripe types (checkout session, webhook events, subscription status)
- T030: Create shared utility types (Result<T,E>, AsyncState<T>, APIResponse<T>)
- T031: Define error types (AppError, ValidationError, NetworkError, SyncError)
- T032: Create barrel exports in src/types/index.ts

**Acceptance Criteria:**

- [ ] All core types defined with proper TypeScript interfaces
- [ ] Zod schemas implemented for critical data structures
- [ ] Type exports organized in barrel files
- [ ] No TypeScript compilation errors

**Verification:**

- Run `npx tsc --noEmit` and confirm zero errors
- Verify all types are exported from src/types/index.ts

---

### Phase 2: Core Editor & AI (Week 2)

#### **SPRINT-004:** Tiptap Editor Integration

**Goal:** Rich text editor with auto-save, formatting toolbar, and distraction-free UI

**Tasks:**

- T033: Install Tiptap 3.4 dependencies (@tiptap/react, @tiptap/starter-kit, extensions)
- T034: Create base TiptapEditor component with dynamic import (SSR disabled)
- T035: Implement editor placeholder: "Start typing your notes... Type / for commands"
- T036: Build editor toolbar with formatting buttons (Bold, Italic, Heading, List, Link) per UX Section 4.4
- T037: Create inline title editing in toolbar
- T038: Implement category dropdown in toolbar (7 predefined categories)
- T039: Add AI quota badge component showing remaining requests or "Dictionary" mode
- T040: Add sync status indicator (Synced/Offline/Syncing...) with color states
- T041: Add save status indicator ("Saved just now" → "Saved 1m ago" → "Saved 5m ago")
- T042: Implement editor max-width 900px centered layout with responsive padding

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

#### **SPRINT-005:** Auto-Save & Local Storage

**Goal:** Implement 30-second auto-save to IndexedDB with visual feedback

**Tasks:**

- T043: Initialize Dexie database with notes, syncQueue, versionSnapshots tables
- T044: Create useAutoSave hook with 30-second debounced save to Dexie
- T045: Implement save indicator state machine (idle → saving → saved)
- T046: Create useLocalNotes hook for CRUD operations on Dexie
- T047: Implement note version tracking (version number increments on each save)
- T048: Add error handling for failed local saves with retry
- T049: Create EditorSkeleton loading component for dynamic import

**Acceptance Criteria:**

- [ ] Notes auto-save every 30 seconds without blocking editor (FR-016)
- [ ] Save indicator shows "Saved" with timestamp after successful save
- [ ] Local saves complete within 500ms (NFR)
- [ ] App preserves changes if closed without manual save

**Verification:**

- Edit note, wait 30 seconds, close browser, reopen and verify changes preserved
- Time save operation and confirm <500ms
- Test save while offline (should work)

---

#### **SPRINT-006:** Slash Command System

**Goal:** Implement /template and /formula slash commands with floating menu

**Tasks:**

- T050: Create Tiptap slash command extension with "/" trigger
- T051: Build SlashCommandMenu floating component (320px width, 400px max-height)
- T052: Implement menu keyboard navigation (arrow keys, Enter, Escape)
- T053: Create template content definitions (Care Plan, Medication Card, SOAP Note, Head-to-Toe, Pathophysiology)
- T054: Create formula content definitions with normal ranges (MAP, BMI, IV Drip, Dosage, GCS, Fluid Deficit)
- T055: Implement template insertion with cursor positioning in first field
- T056: Implement formula insertion with formatted structure
- T057: Add search/filter as user types after "/"
- T058: Style menu items per UX Section 4.5 (44px height, hover states)
- T059: Add mobile adaptation (full-width bottom sheet, 52px touch targets)

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

#### **SPRINT-007:** AI Autocomplete Integration

**Goal:** Implement GPT-4.1 nano autocomplete with dictionary fallback

**Tasks:**

- T060: Create POST /api/ai/autocomplete endpoint with token validation
- T061: Implement OpenAI GPT-4.1 nano integration with <200ms target
- T062: Add request throttling (max 1 request per 3 seconds per user)
- T063: Implement quota tracking in Firestore user document
- T064: Create GET /api/users/quota endpoint for quota checking
- T065: Load 5,000+ nursing dictionary (nursing-terms.json) into memory
- T066: Implement dictionary prefix matching for offline/over-quota fallback
- T067: Create useAutocomplete hook with AI/dictionary source detection
- T068: Build AutocompletePopup component (300px width, 5 suggestions max)
- T069: Add suggestion source badges ("AI" blue / "Dictionary" gray)
- T070: Implement Tab/Enter to accept suggestion
- T071: Add debouncing (150ms) for autocomplete requests
- T072: Handle API timeout (>500ms) with dictionary fallback

**Acceptance Criteria:**

- [ ] AI suggestions appear within 200ms of typing (FR-001)
- [ ] Dictionary fallback works offline (FR-002)
- [ ] Dictionary fallback works when quota exceeded (FR-002)
- [ ] Quota badge updates after each AI request (FR-027)
- [ ] Request throttling enforced (1 per 3 seconds)

**Verification:**

- Type "met" and verify suggestions like "metoprolol", "metformin" appear
- Exceed quota and verify seamless switch to dictionary mode
- Disconnect network and verify dictionary autocomplete still works
- Time AI response and confirm <200ms typical latency

---

### Phase 3: Note Management & Sync (Week 3)

#### **SPRINT-008:** Note CRUD Operations

**Goal:** Complete note library with create, read, update, delete functionality

**Tasks:**

- T073: Create Notes Library page layout with header, filter bar, note cards
- T074: Build NoteCard component with title, preview, category badge, date, sync status
- T075: Implement "New Note" button opening blank editor (FR-006)
- T076: Implement note list with grid/list view toggle (FR-007)
- T077: Implement click-to-open note in editor (FR-008)
- T078: Add inline note title renaming (FR-010)
- T079: Implement note duplication (FR-011)
- T080: Add context menu (right-click/long-press) with Rename, Duplicate, Export, Delete
- T081: Implement soft delete (isDeleted flag, deletedAt timestamp) (FR-009)
- T082: Create empty state with illustration and "Create Note" CTA (UX Section 4.3)

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

#### **SPRINT-009:** Note Organization

**Goal:** Implement category filtering, search, and sorting

**Tasks:**

- T083: Implement category filter dropdown/chips (7 categories) (FR-012)
- T084: Implement sort options (date created, last modified, alphabetical) (FR-013)
- T085: Create useNoteSearch hook with real-time search on title and content (FR-014)
- T086: Build search input with debounced query (300ms)
- T087: Add "No results" empty state for search (UX Section 10)
- T088: Add "No notes in [category]" empty state for category filter
- T089: Persist filter/sort preferences in localStorage

**Acceptance Criteria:**

- [ ] Category filter shows only notes in selected category
- [ ] Search returns results within 300ms for up to 1,000 notes (NFR)
- [ ] Sort options work correctly for all three modes
- [ ] Preferences persist across sessions

**Verification:**

- Create notes in multiple categories, filter by each
- Search for partial term in note content, verify results appear
- Time search with 100 notes, confirm <300ms

---

#### **SPRINT-010:** Trash System

**Goal:** Implement trash folder with 30-day recovery and permanent deletion

**Tasks:**

- T090: Create Trash page with header showing 30-day warning (UX Section 4.7)
- T091: Build TrashNoteCard with "Deleted X days ago" label
- T092: Implement "Restore" action to un-delete note (FR-015)
- T093: Implement "Delete Forever" action with confirmation dialog
- T094: Add "Empty Trash" button with bulk permanent delete (FR-015)
- T095: Create trash empty state with empty bin illustration
- T096: Update notes library to exclude deleted notes from view

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

#### **SPRINT-011:** Offline Sync & Conflict Resolution

**Goal:** Implement Firestore sync with offline queue and last-write-wins conflict resolution

**Tasks:**

- T097: Create sync queue table in Dexie for offline operations
- T098: Implement useOnlineStatus hook to detect connectivity changes
- T099: Create useSyncQueue hook for queuing create/update/delete operations
- T100: Implement sync worker that processes queue when online
- T101: Add exponential backoff retry (5s, 15s, 30s, 60s, 120s) for failed syncs
- T102: Implement last-write-wins conflict detection (compare version and updatedAt)
- T103: Create VersionSnapshot when conflict detected (snapshotType: "sync_conflict")
- T104: Display toast notification on conflict resolution ("Version from [device] kept")
- T105: Update sync status indicator based on queue state
- T106: Implement auto-sync when network restored

**Acceptance Criteria:**

- [ ] Notes sync to Firestore automatically when online (FR-017)
- [ ] Offline editing works with all features (FR-018)
- [ ] Conflicts resolved with last-write-wins algorithm (FR-019)
- [ ] Overwritten versions preserved as snapshots (FR-020)
- [ ] 99%+ sync reliability (NFR)

**Verification:**

- Edit note offline, restore network, verify sync completes
- Edit same note on two devices offline, bring online, verify conflict resolution
- Check Firestore snapshots collection for conflict record

---

### Phase 4: Payment & Polish (Week 4)

#### **SPRINT-012:** Stripe Integration

**Goal:** Implement Pro tier subscription with Stripe checkout, webhooks, and customer portal

**Tasks:**

- T107: Create Stripe account and configure products (Pro Monthly $8.99, Pro Annual $79)
- T108: Create POST /api/stripe/checkout endpoint for checkout session
- T109: Create POST /api/stripe/webhook endpoint with signature validation
- T110: Handle checkout.session.completed webhook (update tier to Pro)
- T111: Handle customer.subscription.updated webhook (plan changes)
- T112: Handle customer.subscription.deleted webhook (downgrade to Free)
- T113: Handle invoice.payment_failed webhook (payment failure handling)
- T114: Create POST /api/stripe/portal endpoint for customer portal session
- T115: Build Upgrade Modal component with feature comparison table (UX Section 4.9)
- T116: Add "Upgrade to Pro" button in settings and quota badge
- T117: Display subscription status, billing date, payment method in settings (FR-032)
- T118: Implement tier enforcement in AI autocomplete endpoint

**Acceptance Criteria:**

- [ ] Free users limited to 100 AI requests/month (FR-027)
- [ ] Pro users have unlimited AI requests (FR-028)
- [ ] User can upgrade via Stripe checkout (FR-030)
- [ ] User can manage subscription via customer portal (FR-031)
- [ ] Subscription status displays correctly in settings

**Verification:**

- Test Stripe checkout flow with test card
- Verify webhook updates user tier in Firestore
- Confirm AI quota enforced correctly for free tier

---

#### **SPRINT-013:** Onboarding Flow

**Goal:** Implement 2-screen onboarding introducing AI autocomplete and slash commands

**Tasks:**

- T119: Create onboarding route (/onboarding)
- T120: Build Screen 1: Welcome with feature cards (AI Autocomplete, Slash Commands) (UX Section 4.2)
- T121: Build Screen 2: Interactive demo with mini-editor for /template
- T122: Implement demo celebration animation on successful template insertion
- T123: Track onboarding completion in user document
- T124: Add in-editor tooltip showing "/" trigger until user uses 5+ times
- T125: Implement keyboard shortcut cheatsheet (accessible via "?" key)
- T126: Create persistent UI hint near editor for available commands

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

#### **SPRINT-014:** Export Functionality

**Goal:** Implement note export to Markdown, Plain Text, and bulk ZIP

**Tasks:**

- T127: Implement Tiptap content to Markdown converter
- T128: Implement Tiptap content to Plain Text converter
- T129: Add export menu options (Markdown, Plain Text) in note context menu (FR-033)
- T130: Create download trigger for single note export
- T131: Implement bulk export to ZIP with notes organized by category (FR-034)
- T132: Add "Export all notes" button in Settings (UX Section 4.8)

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

#### **SPRINT-015:** Settings Page

**Goal:** Complete settings page with account, subscription, preferences, and data sections

**Tasks:**

- T133: Create Settings page layout with sidebar navigation (desktop) and tabs (mobile)
- T134: Build Account section (email, display name, change password link)
- T135: Build Subscription section (tier badge, quota bar, upgrade/manage buttons)
- T136: Build Preferences section (theme toggle: Light/Dark/System, auto-save toggle)
- T137: Build Data section (export all, delete account with confirmation)
- T138: Implement theme switching with system preference detection
- T139: Persist theme preference to localStorage and user document
- T140: Implement delete account flow with Firestore and Firebase Auth cleanup

**Acceptance Criteria:**

- [ ] All settings sections display correctly
- [ ] Theme changes apply immediately across app
- [ ] Quota usage bar accurate and updates after AI requests
- [ ] Delete account removes all user data

**Verification:**

- Toggle theme and verify all pages update
- Check quota bar reflects actual usage
- Test delete account flow (use test account)

---

#### **SPRINT-016:** Responsive Design & Dark Mode

**Goal:** Ensure responsive design across all breakpoints and complete dark mode support

**Tasks:**

- T141 [P]: Implement responsive breakpoints (Mobile <640px, Tablet 640-1023px, Desktop 1024px+)
- T142 [P]: Implement dark mode color palette (UX Section 2)
- T143: Adapt navbar for mobile (hamburger menu, condensed logo)
- T144: Adapt editor toolbar for mobile (formatting in overflow menu)
- T145: Adapt notes library for mobile (search expands on tap, filters in bottom sheet)
- T146: Adapt slash command menu for mobile (full-width bottom sheet, 52px items)
- T147: Adapt settings for mobile (tab navigation instead of sidebar)
- T148: Test and fix all pages at 320px, 640px, 1024px, 2560px widths
- T149: Implement prefers-reduced-motion support (UX Section 9)

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

#### **SPRINT-017:** Accessibility

**Goal:** Achieve WCAG AA compliance with keyboard navigation and screen reader support

**Tasks:**

- T150 [P]: Add ARIA labels to all interactive elements
- T151 [P]: Implement logical tab order across all pages
- T152: Add visible focus indicators to all focusable elements
- T153: Ensure 4.5:1 minimum contrast ratio for all text
- T154: Add screen reader announcements for status changes (aria-live)
- T155: Make slash command menu accessible (ARIA announcements, keyboard nav)
- T156: Test with VoiceOver (macOS/iOS) and NVDA (Windows)
- T157: Add alt text to all images and icons
- T158: Test at 200% browser zoom and fix any layout issues

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

### Phase 5: Testing & Deployment

#### **SPRINT-018:** Testing Suite

**Goal:** Comprehensive test coverage for critical paths

**Tasks:**

- T159: Write unit tests for slash command parser and template insertion
- T160: Write unit tests for autocomplete hook (AI and dictionary modes)
- T161: Write unit tests for sync queue and conflict resolution logic
- T162: Write unit tests for Zod validation schemas
- T163: Write E2E test: signup → onboarding → create note → save flow
- T164: Write E2E test: offline editing → reconnect → sync verification
- T165: Write E2E test: slash command insertion (/template, /formula)
- T166: Write E2E test: AI autocomplete flow and quota enforcement
- T167: Write E2E test: Stripe checkout and subscription upgrade
- T168: Set up GitHub Actions CI for test runs on PR

**Acceptance Criteria:**

- [ ] All unit tests pass
- [ ] All E2E tests pass on Chromium, Firefox, WebKit
- [ ] CI runs tests on every PR
- [ ] Critical paths have test coverage

**Verification:**

- Run `npm run test` and confirm all pass
- Run `npm run test:e2e` on all browsers
- Create PR and verify CI runs

---

#### **SPRINT-019:** Performance Optimization

**Goal:** Meet all Core Web Vitals and performance targets

**Tasks:**

- T169: Implement code splitting with dynamic imports for heavy components
- T170: Add lazy loading for notes library (virtual scrolling if >100 notes)
- T171: Optimize images with Next.js Image component
- T172: Configure service worker caching strategies (NetworkFirst for API, CacheFirst for assets)
- T173: Run Lighthouse audit and address any issues
- T174: Verify FCP <1.5s, LCP <2.5s, TTI <3.5s, CLS <0.1 (Tech Specs Section 10)
- T175: Profile and optimize Tiptap editor for 50,000 character documents
- T176: Verify client-side memory stays under 150MB with 20 notes loaded

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

#### **SPRINT-020:** Deployment & Monitoring

**Goal:** Deploy to Vercel with monitoring, error tracking, and cost alerts

**Tasks:**

- T177: Configure Vercel project with environment variables
- T178: Set up custom domain and SSL certificate
- T179: Deploy production build to Vercel
- T180: Configure Sentry error tracking
- T181: Configure Vercel Analytics for user behavior
- T182: Set up monitoring alerts for error rates >5%
- T183: Set up cost alerts at $50, $75, $100 thresholds
- T184: Create monitoring dashboard for AI API costs per tier
- T185: Configure Firebase automatic backup
- T186: Document rollback procedure

**Acceptance Criteria:**

- [ ] Production app accessible at custom domain
- [ ] Errors reported to Sentry
- [ ] Analytics tracking user sessions
- [ ] Cost alerts configured

**Verification:**

- Access production URL, verify app loads
- Trigger intentional error, verify Sentry captures
- Check Vercel Analytics dashboard

---

## Dependencies and Execution Order

**Sprint Dependencies:**

- SPRINT-002 depends on SPRINT-001 (Firebase requires initialized project)
- SPRINT-003 depends on SPRINT-001 (Types require TypeScript setup)
- SPRINT-004 depends on SPRINT-003 (Editor needs types defined)
- SPRINT-005 depends on SPRINT-003 and SPRINT-004 (Auto-save needs Dexie types and editor)
- SPRINT-006 depends on SPRINT-004 (Slash commands are Tiptap extension)
- SPRINT-007 depends on SPRINT-002 and SPRINT-006 (AI needs auth and editor)
- SPRINT-008 depends on SPRINT-005 (CRUD needs local storage)
- SPRINT-009 depends on SPRINT-008 (Organization needs note library)
- SPRINT-010 depends on SPRINT-008 (Trash needs note CRUD)
- SPRINT-011 depends on SPRINT-005 and SPRINT-008 (Sync needs local storage and CRUD)
- SPRINT-012 depends on SPRINT-002 and SPRINT-007 (Stripe needs auth and AI quota)
- SPRINT-013 depends on SPRINT-006 (Onboarding demos slash commands)
- SPRINT-014 depends on SPRINT-008 (Export needs note CRUD)
- SPRINT-015 depends on SPRINT-012 (Settings shows subscription)
- SPRINT-016 depends on SPRINT-004 through SPRINT-015 (Responsive applies to all)
- SPRINT-017 depends on SPRINT-016 (Accessibility on final components)
- SPRINT-018 depends on all feature sprints (Tests verify features)
- SPRINT-019 depends on SPRINT-018 (Optimize after tests pass)
- SPRINT-020 depends on SPRINT-019 (Deploy optimized build)

**Critical Path:**

T001 → T011 → T021 → T033 → T043 → T060 → T073 → T097 → T107 → T177

(Project setup → Firebase → Types → Editor → Auto-save → AI → Note CRUD → Sync → Stripe → Deploy)

---

## Parallel Opportunities

**Parallel Sprints:**

- SPRINT-001, SPRINT-002, SPRINT-003 can have some parallel work (different domains)
- SPRINT-008, SPRINT-009, SPRINT-010 can be parallelized (different note management features)
- SPRINT-013, SPRINT-014 can run in parallel (independent features)

**Parallel Tasks Within Sprint:**

- T001, T002, T003 (SPRINT-001 setup tasks)
- T021, T022, T023, T024 (SPRINT-003 type definitions)
- T141, T142 (SPRINT-016 responsive and dark mode base)
- T150, T151 (SPRINT-017 accessibility base)

**Resource Allocation:**

- Frontend focus: T033-T042, T073-T089, T119-T126, T133-T149
- Backend focus: T011-T020, T060-T072, T097-T118
- Full-stack: T050-T059, T159-T186

---

## Implementation Strategy

1. **Week 1 Priority:** Complete SPRINT-001 through SPRINT-003 (foundation)
2. **Week 2 Priority:** Complete SPRINT-004 through SPRINT-007 (editor and AI)
3. **Week 3 Priority:** Complete SPRINT-008 through SPRINT-011 (note management and sync)
4. **Week 4 Priority:** Complete SPRINT-012 through SPRINT-020 (payment, polish, deploy)

**TDD Approach:**
- Write types and interfaces first (SPRINT-003)
- Write unit tests for logic-heavy modules before implementation
- E2E tests written after feature implementation verified manually

**Offline-First Strategy:**
- Dexie (local) is source of truth
- Firestore is sync layer
- All features must work offline first, then add sync

---

## Risks & Blockers

| Risk ID | Description | Affected Sprint(s) | Mitigation Plan | Owner | Status |
|---------|-------------|-------------------|-----------------|-------|--------|
| R001 | OpenAI API unavailability | SPRINT-007 | Dictionary fallback implemented as primary offline mode | Dev Team | ⏳ Not Started |
| R002 | Stripe webhook signature validation | SPRINT-012 | Use Stripe CLI for local testing before production | Dev Team | ⏳ Not Started |
| R003 | Tiptap performance with large documents | SPRINT-004 | Virtualization and lazy loading for 50k+ chars | Dev Team | ⏳ Not Started |
| R004 | Sync conflicts data loss | SPRINT-011 | Comprehensive snapshot system with conflict detection | Dev Team | ⏳ Not Started |
| R005 | PWA installation discoverability | SPRINT-001 | Clear install prompts and video tutorials | Dev Team | ⏳ Not Started |
| R006 | Firebase service outages | SPRINT-011 | Offline-first architecture ensures local functionality | Dev Team | ⏳ Not Started |
| R007 | AI hallucination (incorrect terms) | SPRINT-007 | Validate AI suggestions against dictionary before display | Dev Team | ⏳ Not Started |

**Status Legend:**

- ⏳ Not Started - Risk identified, mitigation planned
- 🔄 In Progress - Actively working on mitigation
- ✅ Resolved - Risk mitigated
- ⚠️ Active - Issue occurring, mitigation underway

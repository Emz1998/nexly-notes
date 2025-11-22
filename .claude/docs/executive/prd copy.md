# NEXLY RN — Product Requirements Document (4-Week MVP - Next.js Stack)

## 1. Product Overview

- **Name:** NEXLY RN — AI-Powered Nursing Education Platform
- **Elevator Pitch:** NEXLY RN transforms study notes into active learning material through three distinct modes: Create (fast capture), Edit (revision with quick change preview), and Study (AI-powered key term spotting)—helping nursing students capture, refine, and master their material efficiently
- **Problem:** Nursing students need fast note-taking tools but also want to refine notes later and identify exam-relevant content—current tools don't separate these workflows, leading to either slow capture or unclear study priorities
- **Solution:** NEXLY RN provides AI-powered note-taking through three modes:
  1. **Create Note Mode:** Fast capture with AI autocomplete and minimal UI
  2. **Edit Mode:** Revision with inline diff view to see changes since last save
  3. **Study Mode:** AI-powered key term spotting to identify exam-relevant content

## 2. Goals & Success Criteria

### Primary Goals (4-Week MVP)

1. **Validate three-mode hypothesis**: ≥60% of users use all three modes in Week 1
2. **Prove Create Mode speed**: Users report "this is faster than [current method]"
3. **Demonstrate Edit Mode confidence**: ≥70% use inline diff button in Edit Mode
4. **Validate Study Mode value**: ≥50% use Key Term Spotting at least once
5. **Measure autocomplete effectiveness**: ≥40% acceptance rate

### Non-Goals (Out of Scope for 4-Week MVP)

- Templates and slash commands (Fast-Follow: Week 5-6)
- Shorthand expansion (Fast-Follow: Week 5-6)
- Definition-on-demand (Fast-Follow: Week 5-6)
- Cloze deletion generator (Fast-Follow: Week 7-8)
- Full version history UI with side-by-side diff (Fast-Follow: Week 7-8)
- Audio recording/transcription
- Time-based lecture tracking
- Flashcards/quizzes
- Clinical documentation for patient care
- Real-time collaboration
- Native mobile apps (PWA only for MVP)
- LMS integrations
- Spaced repetition/scheduling
- Full visual concept maps

### Success Criteria (Definition of Done - 4-Week MVP)

After 2 weeks with 50 beta users:

- ≥60% use all three modes (Create/Edit/Study) in Week 1
- Autocomplete acceptance rate ≥40%
- ≥70% of Edit Mode sessions use inline diff button
- ≥50% use Key Term Spotting at least once
- Users report "faster than [current method]" in feedback
- <5% critical bugs or crashes

## 3. Target Users

### Primary Persona

Pre-licensure Nursing Students (ADN/BSN)

### Secondary Persona

Advanced Practice Nursing Students (MSN/DNP)

### Tertiary Persona

Nursing Educators (as validators and institutional adopters - post-MVP)

### Pain Points

- Need fast note capture without UI clutter
- Want to see what changed when editing without digging through history
- Difficulty identifying exam-relevant content in notes
- Missing key concepts emphasized by professors
- Unclear what to focus on when studying

## 4. User Stories

### Primary Persona: Pre-licensure Nursing Students (ADN/BSN)

#### As a nursing student taking lecture notes, I want to...

**Create Mode Stories**
- Capture notes quickly during lecture without UI distractions, so I don't miss important professor statements
- Get AI suggestions for nursing abbreviations and terminology as I type, so I can type faster and catch proper medical terms
- Have my notes auto-save every 30 seconds, so I never lose work if my browser crashes or battery dies
- See a clear visual indicator (blue accent) that I'm in Create Mode, so I know the interface is optimized for fast capture

**Edit Mode Stories**
- See exactly what changed since I last saved my notes, so I can confidently revise without losing track of edits
- Get AI autocomplete while editing, so I can add missing details efficiently
- Click a simple "View Changes" button to see inline diffs, so I don't have to dig through version history
- See a clear visual indicator (purple accent) that I'm in Edit Mode with diff capabilities available

**Study Mode Stories**
- Have AI automatically identify exam-relevant terms in my notes, so I can focus study time on what professors emphasized
- See highlighted terms with context snippets, so I understand why each term is important
- Click a spotted term to jump to its location in my notes, so I can review the full context quickly
- Export a list of key terms for quick review before exams, so I have a study checklist
- See a clear visual indicator (green accent) that I'm in Study Mode and editing is disabled

**General Workflow Stories**
- Choose between "Edit" or "Study" when opening existing notes, so I can set clear intentions for each session
- Complete a 2-screen onboarding that explains all three modes, so I understand the workflow immediately
- Search my notes by title to find specific lectures quickly
- Access my notes offline when internet is unavailable, so I can study anywhere
- Install the app to my desktop or phone like a native app, so I can access it faster

### Secondary Persona: Advanced Practice Nursing Students (MSN/DNP)

#### As a graduate nursing student, I want to...

**Create Mode Stories**
- Capture complex pathophysiology and advanced practice concepts quickly during lectures
- Get AI suggestions for advanced medical terminology and pharmacology terms
- Keep focused on dense academic content without interface interruptions

**Edit Mode Stories**
- Review and refine comprehensive care plans and case study notes
- See what details I added during revision sessions for my own learning tracking
- Add evidence-based practice citations and research notes efficiently

**Study Mode Stories**
- Identify critical concepts for board certification exams (ANCC, AANP)
- Spot evidence-based practice keywords and advanced assessment terminology
- Export term lists for specialty certification preparation

### Tertiary Persona: Nursing Educators (Post-MVP Focus)

#### As a nursing educator, I want to...
- Validate that students are capturing key concepts from my lectures (future feature)
- See which terms students identify as important for alignment with learning objectives (future feature)
- Provide feedback on student note quality through the platform (future feature)

### Freemium User Stories

#### As a free tier user, I want to...
- Use all three modes (Create, Edit, Study) without restrictions
- Get up to 100 AI autocomplete requests per month to evaluate the product value
- Fall back to dictionary-based suggestions when I exceed my AI quota, so I can still use the app
- Use AI Key Term Spotting up to 10 times per month to test Study Mode effectiveness
- Keep my last 5 version snapshots per note in the background for peace of mind

#### As a Pro tier user, I want to...
- Get unlimited AI autocomplete so I never hit quota limits during busy exam weeks
- Use unlimited AI Key Term Spotting for all my notes without counting requests
- Keep unlimited version snapshots for comprehensive note history
- Get early access to new features like templates and shorthand expansion
- Export key terms lists for all my notes

## 5. Edge Cases

### Authentication & Session Management

**Edge Case: User loses internet during note creation**
- **Expected Behavior**: Notes continue saving to IndexedDB locally; sync to Firestore when connection restored
- **Validation**: Background sync queue retries failed saves; user sees "Syncing..." indicator

**Edge Case: User exceeds free tier AI autocomplete quota mid-session**
- **Expected Behavior**: System switches seamlessly to dictionary-based autocomplete; user sees one-time notification
- **Validation**: No autocomplete interruption; fallback suggestions continue appearing

**Edge Case: Multiple browser tabs open with same note**
- **Expected Behavior**: Last write wins; optional: show "Note updated in another tab" warning
- **Validation**: Firestore real-time listener detects external changes; prompt user to reload or keep local version

**Edge Case: User's session expires during active editing**
- **Expected Behavior**: Notes save to IndexedDB; user prompted to re-authenticate; notes sync after login
- **Validation**: No data loss; seamless re-auth flow

### AI Autocomplete (Create + Edit Modes)

**Edge Case: AI autocomplete API returns error or timeout**
- **Expected Behavior**: Fall back to dictionary-based suggestions silently; log error for monitoring
- **Validation**: User sees no error message; autocomplete continues with local dictionary

**Edge Case: User types faster than AI response time (<100ms target)**
- **Expected Behavior**: Cancel in-flight AI request; debounce next request by 150ms
- **Validation**: No suggestion flickering; only show suggestions for current cursor position

**Edge Case: AI suggests incorrect or inappropriate medical term**
- **Expected Behavior**: User can reject suggestion (press Escape or keep typing); feedback mechanism for future model improvement
- **Validation**: No forced acceptance; user maintains full control

**Edge Case: User accepts autocomplete suggestion then immediately undos (Cmd+Z)**
- **Expected Behavior**: Undo removes AI-suggested text and restores original cursor position
- **Validation**: Standard editor undo/redo behavior works with AI suggestions

**Edge Case: User reaches end of free tier quota exactly during autocomplete request**
- **Expected Behavior**: Complete in-flight AI request; switch to dictionary for next request
- **Validation**: No mid-suggestion switch; clean transition at request boundary

### Inline Diff View (Edit Mode)

**Edge Case: User clicks "View Changes" but has made no edits since last save**
- **Expected Behavior**: Show message "No changes since last save" or display empty diff view
- **Validation**: No errors; clear user feedback

**Edge Case: User makes 10,000+ character edit in single session**
- **Expected Behavior**: Diff calculation completes in <200ms using efficient algorithm; may paginate diff view if needed
- **Validation**: Performance testing with large notes (5,000+ words)

**Edge Case: User rapidly types while diff view is open**
- **Expected Behavior**: Diff view updates in real-time with 500ms debounce; no UI lag
- **Validation**: Smooth typing experience; diff view updates smoothly

**Edge Case: User switches from Edit Mode to Study Mode without saving**
- **Expected Behavior**: Prompt "Save changes before switching to Study Mode?" with Save/Discard/Cancel options
- **Validation**: No accidental data loss

### AI Key Term Spotting (Study Mode)

**Edge Case: User opens Study Mode on empty note**
- **Expected Behavior**: Show message "Add content to your note to spot key terms"
- **Validation**: No API call; clear user guidance

**Edge Case: AI Key Term Spotting takes >5 seconds due to network latency**
- **Expected Behavior**: Show loading indicator with progress message; allow user to cancel
- **Validation**: User can navigate away; request cancels cleanly

**Edge Case: AI identifies 100+ key terms in single note**
- **Expected Behavior**: Paginate or virtualize term list sidebar; show top 50 by relevance; allow "Show more"
- **Validation**: UI remains responsive; no layout breaking

**Edge Case: AI returns zero key terms for valid nursing content**
- **Expected Behavior**: Show message "No key terms detected. Try Edit Mode to add professor emphasis cues (e.g., 'important,' 'test will cover')"
- **Validation**: User understands AI limitation; gets actionable guidance

**Edge Case: User clicks spotted term but content has been deleted in Edit Mode**
- **Expected Behavior**: Scroll to nearest remaining content or show "Term no longer found in note"
- **Validation**: No console errors; graceful degradation

**Edge Case: User exceeds free tier Key Term Spotting quota (10/month)**
- **Expected Behavior**: Show upgrade prompt with Pro tier benefits; disable Key Term Spotting button until next billing cycle or upgrade
- **Validation**: Clear messaging; no broken UI

### Auto-Save & Version Snapshots

**Edge Case: Auto-save triggers while user is actively typing**
- **Expected Behavior**: Save occurs in background without interrupting typing; show subtle "Saving..." then "Saved" indicator
- **Validation**: No cursor jump; no typing lag

**Edge Case: Firestore write fails due to network error during auto-save**
- **Expected Behavior**: Retry with exponential backoff; keep note in IndexedDB; show "Offline - changes saved locally"
- **Validation**: User data safe; background sync resumes when online

**Edge Case: User has 100 notes with 5 snapshots each (free tier limit)**
- **Expected Behavior**: Oldest snapshots auto-deleted when new ones created; user sees storage usage indicator
- **Validation**: Background cleanup job; no user-facing errors

**Edge Case: User rapidly switches between notes (within 30s auto-save window)**
- **Expected Behavior**: Trigger immediate save on note close; respect 30s interval for background saves
- **Validation**: No data loss; efficient save batching

### Mode Switching & Dialog

**Edge Case: User opens note, sees "Edit or Study" dialog, then closes tab without choosing**
- **Expected Behavior**: No mode selected; note remains closed; no auto-selection
- **Validation**: Explicit user intent required

**Edge Case: User in Study Mode tries to edit note by typing**
- **Expected Behavior**: Show tooltip "Switch to Edit Mode to make changes" near cursor; keep note read-only
- **Validation**: Clear user guidance; no accidental edits

**Edge Case: User switches modes 10+ times in single session**
- **Expected Behavior**: Mode transitions remain fast (<50ms); no performance degradation
- **Validation**: State management optimized; no memory leaks

### Note Library & Search

**Edge Case: User has 1,000+ notes in library**
- **Expected Behavior**: Virtualize note list; search remains fast with IndexedDB full-text index
- **Validation**: Performance testing with large datasets; <500ms search response

**Edge Case: User searches for term with special characters (e.g., "HTN @ 120/80")**
- **Expected Behavior**: Search handles special chars correctly; returns relevant results
- **Validation**: Proper text escaping; regex safety

**Edge Case: User deletes note while it's open in another tab**
- **Expected Behavior**: Show "This note has been deleted" message; prevent further edits; offer undo within 5 seconds
- **Validation**: Real-time sync; data consistency

### PWA & Offline Support

**Edge Case: User installs PWA then clears browser cache**
- **Expected Behavior**: IndexedDB persists; notes remain available; service worker re-registers
- **Validation**: Persistent storage API; user data protected

**Edge Case: User tries to use AI features while offline**
- **Expected Behavior**: Show "AI features require internet connection" message; fall back to dictionary autocomplete
- **Validation**: Clear offline state indicators; graceful degradation

**Edge Case: Service worker update available during active editing session**
- **Expected Behavior**: Show "Update available" banner; allow user to update when convenient (not forced)
- **Validation**: No data loss during update; smooth transition

### Onboarding

**Edge Case: User dismisses onboarding after first screen**
- **Expected Behavior**: Allow dismissal; show "Complete onboarding" link in settings for later access
- **Validation**: User can skip and return later

**Edge Case: User completes onboarding but doesn't understand modes**
- **Expected Behavior**: Contextual tooltips appear on first use of each mode; "Help" link in nav bar
- **Validation**: Progressive disclosure; not overwhelming

### Payment & Tier Management

**Edge Case: User upgrades to Pro mid-month**
- **Expected Behavior**: Immediate quota increase; pro-rated billing; quotas reset at billing cycle
- **Validation**: Real-time tier validation; no service interruption

**Edge Case: User downgrades from Pro to Free with >5 snapshots per note**
- **Expected Behavior**: Keep existing snapshots; stop creating new ones beyond free tier limit
- **Validation**: Graceful degradation; no data deletion

**Edge Case: Payment fails for Pro tier renewal**
- **Expected Behavior**: Grace period (7 days); email notification; revert to Free tier if not resolved
- **Validation**: Clear communication; no abrupt service loss

### Performance & Scalability

**Edge Case: User creates note with 20,000+ words**
- **Expected Behavior**: Editor remains responsive; diff calculation may take up to 500ms (within tolerance)
- **Validation**: Load testing; consider pagination or warning for extremely large notes

**Edge Case: Concurrent users editing 100+ notes simultaneously**
- **Expected Behavior**: Firestore handles concurrent writes; no conflicts due to document-level locking
- **Validation**: Load testing; Firestore scaling

**Edge Case: API rate limit hit on OpenAI requests**
- **Expected Behavior**: Queue requests with exponential backoff; show "AI temporarily busy" message; fall back to dictionary
- **Validation**: Rate limit monitoring; graceful degradation

## 6. Functional Requirements

### FR1: User Authentication & Authorization

**FR1.1: User Registration**
- System SHALL allow users to create an account using email/password
- System SHALL support OAuth authentication (Google, Microsoft)
- System SHALL validate email format and password strength (min 8 characters, 1 uppercase, 1 number)
- System SHALL send email verification link upon registration
- System SHALL prevent duplicate account creation with same email

**FR1.2: User Login**
- System SHALL authenticate users via email/password or OAuth
- System SHALL maintain session state across browser refreshes
- System SHALL support "Remember Me" functionality (30-day session)
- System SHALL implement password reset via email link
- System SHALL lock account after 5 failed login attempts (15-minute lockout)

**FR1.3: Session Management**
- System SHALL expire inactive sessions after 24 hours
- System SHALL allow concurrent sessions across multiple devices
- System SHALL provide "Log out of all devices" functionality
- System SHALL preserve unsaved work in IndexedDB during session expiration

### FR2: Note Creation & Management

**FR2.1: Create Note (Create Mode)**
- System SHALL open new notes in Create Mode by default
- System SHALL display blue visual accent indicating Create Mode
- System SHALL provide minimal UI (editor + autocomplete only)
- System SHALL auto-save note content every 30 seconds
- System SHALL save note immediately when user clicks "Save" button
- System SHALL generate unique note ID using Firebase Firestore auto-ID
- System SHALL capture note metadata: creation timestamp, last modified timestamp, word count
- System SHALL allow users to set note title (required field)

**FR2.2: Edit Note (Edit Mode)**
- System SHALL display "Edit or Study" dialog when opening existing note
- System SHALL open note in Edit Mode when user selects "Edit this note"
- System SHALL display purple visual accent indicating Edit Mode
- System SHALL provide "View Changes Since Last Save" button in toolbar
- System SHALL calculate and display inline diff on button click
- System SHALL show additions in green, deletions in red, unchanged text in gray
- System SHALL auto-save changes every 30 seconds
- System SHALL preserve scroll position during auto-save

**FR2.3: Study Note (Study Mode)**
- System SHALL open note in Study Mode when user selects "Study this note"
- System SHALL display green visual accent indicating Study Mode
- System SHALL make note content read-only (editing disabled)
- System SHALL provide "Switch to Edit Mode" button in toolbar
- System SHALL preserve scroll position when switching modes

**FR2.4: Note Library**
- System SHALL display all user notes in list view
- System SHALL sort notes by: Last Edited (default), Created Date, Title (A-Z)
- System SHALL show note metadata: Title, last edited date, word count
- System SHALL provide search functionality (search by title)
- System SHALL support full-text search using Dexie IndexedDB indexes
- System SHALL return search results in <500ms for libraries with 1,000+ notes
- System SHALL provide "New Note" button to create notes
- System SHALL allow note deletion with confirmation prompt
- System SHALL provide undo functionality for deletion (5-second window)

**FR2.5: Note Export**
- System SHALL allow users to export individual notes
- System SHALL support export formats: Markdown (.md), Plain Text (.txt)
- System SHALL preserve note formatting in exported files
- System SHALL include note title and metadata in export

### FR3: AI Autocomplete

**FR3.1: Autocomplete Triggering (Create + Edit Modes)**
- System SHALL trigger autocomplete after 150ms typing pause
- System SHALL send cursor context (previous 200 characters) to AI API
- System SHALL display autocomplete suggestions inline at cursor position
- System SHALL show suggestions in gray, italicized text
- System SHALL NOT trigger autocomplete in Study Mode

**FR3.2: Autocomplete Interaction**
- System SHALL allow users to accept suggestions with Tab key
- System SHALL allow users to reject suggestions with Escape key or continued typing
- System SHALL allow partial acceptance using Right Arrow key (word-by-word)
- System SHALL cancel in-flight requests when user continues typing
- System SHALL log accepted/rejected suggestions for quality monitoring

**FR3.3: Autocomplete Quota Management**
- System SHALL track autocomplete request count per user per billing cycle
- System SHALL enforce 100 requests/month limit for Free tier users
- System SHALL switch to dictionary-based autocomplete when quota exceeded
- System SHALL display one-time notification when switching to fallback mode
- System SHALL reset quota on billing cycle date (monthly)
- System SHALL allow unlimited requests for Pro tier users

**FR3.4: Dictionary Fallback**
- System SHALL load 5,000+ nursing terms dictionary on app initialization
- System SHALL provide local autocomplete suggestions when AI quota exceeded
- System SHALL match terms based on prefix (case-insensitive)
- System SHALL rank suggestions by relevance and frequency
- System SHALL respond to autocomplete requests in <50ms using local dictionary

### FR4: Inline Diff View (Edit Mode)

**FR4.1: Diff Calculation**
- System SHALL compare current editor content with last saved version
- System SHALL use efficient diff algorithm (Myers' diff or similar)
- System SHALL complete diff calculation in <200ms for notes up to 10,000 words
- System SHALL debounce diff updates by 500ms while user is typing

**FR4.2: Diff Display**
- System SHALL display additions with green background
- System SHALL display deletions with red strikethrough
- System SHALL display unchanged text in gray
- System SHALL maintain original text formatting (bold, italic, lists)
- System SHALL provide "Exit Diff View" button to return to normal editing

**FR4.3: Diff Limitations**
- System SHALL NOT provide diff view in Create Mode
- System SHALL display "No changes since last save" when content is identical
- System SHALL disable diff view in Study Mode

### FR5: AI Key Term Spotting (Study Mode)

**FR5.1: Term Detection**
- System SHALL analyze note content for exam-relevant terms using GPT-4o-mini
- System SHALL detect professor emphasis cues (keywords: "important", "remember", "test will cover", "key concept", "exam")
- System SHALL use Structured Outputs schema to ensure consistent JSON response
- System SHALL complete analysis in <5 seconds for notes up to 3,000 words
- System SHALL identify 10-50 key terms per note (ranked by relevance)

**FR5.2: Term Presentation**
- System SHALL display key terms in sidebar panel (right side of screen)
- System SHALL show term name and context snippet (50 characters surrounding term)
- System SHALL highlight detected terms in note content with yellow background
- System SHALL allow users to click term in sidebar to jump to location in note
- System SHALL smooth-scroll to term location with highlight animation

**FR5.3: Term Export**
- System SHALL provide "Export Key Terms" button in Study Mode
- System SHALL generate downloadable file with all detected terms
- System SHALL include term name, context snippet, and location (line number)
- System SHALL support export formats: CSV, JSON, Plain Text

**FR5.4: Quota Management**
- System SHALL enforce 10 uses/month limit for Free tier users
- System SHALL track Key Term Spotting usage per user per billing cycle
- System SHALL display remaining quota in Study Mode UI
- System SHALL show upgrade prompt when quota exceeded
- System SHALL allow unlimited uses for Pro tier users

### FR6: Auto-Save & Version Snapshots

**FR6.1: Auto-Save Logic**
- System SHALL auto-save note content every 30 seconds in Create and Edit modes
- System SHALL save to IndexedDB first (local-first architecture)
- System SHALL sync to Firestore in background when online
- System SHALL queue failed saves for retry with exponential backoff (1s, 2s, 4s, 8s max)
- System SHALL display "Saving..." indicator during save operation
- System SHALL display "Saved" indicator on successful save (shown for 2 seconds)
- System SHALL display "Offline - Saved locally" when internet unavailable

**FR6.2: Version Snapshot Creation**
- System SHALL create version snapshot on each save operation
- System SHALL store snapshot in Firestore subcollection: `/notes/{noteId}/versions/{versionId}`
- System SHALL include full note content, timestamp, and metadata in snapshot
- System SHALL NOT display version history UI in MVP (backend only)

**FR6.3: Snapshot Retention**
- System SHALL retain last 5 snapshots per note for Free tier users
- System SHALL auto-delete oldest snapshots when limit exceeded
- System SHALL retain unlimited snapshots for Pro tier users
- System SHALL execute cleanup job on each new snapshot creation

**FR6.4: Conflict Resolution**
- System SHALL detect conflicts when note modified in multiple tabs/devices
- System SHALL implement "last write wins" strategy by default
- System SHALL optionally display "Note updated elsewhere" warning
- System SHALL allow user to choose: Keep Local Version, Use Remote Version, or View Diff

### FR7: Mode Switching & Dialog

**FR7.1: Edit or Study Dialog**
- System SHALL display dialog when user opens existing note
- System SHALL show two buttons: "Edit this note" | "Study this note"
- System SHALL display note metadata: Created date, last edited, word count
- System SHALL close dialog and open note in selected mode on button click
- System SHALL allow dialog dismissal without opening note (close/cancel)

**FR7.2: Mode Transitions**
- System SHALL complete mode transitions in <50ms
- System SHALL update visual accent color on mode change
- System SHALL preserve scroll position during mode transitions
- System SHALL prompt to save unsaved changes before switching modes
- System SHALL provide "Save", "Discard", "Cancel" options in save prompt

**FR7.3: Mode Indicators**
- System SHALL display mode indicator bar at top of editor
- System SHALL show "Create Mode" label with blue accent
- System SHALL show "Edit Mode" label with purple accent
- System SHALL show "Study Mode" label with green accent

### FR8: Onboarding

**FR8.1: First-Time User Flow**
- System SHALL display 2-screen onboarding for new users on first login
- System SHALL explain Create/Edit/Study modes with visual examples
- System SHALL provide interactive demo (create sample note, try autocomplete)
- System SHALL allow users to skip onboarding at any screen
- System SHALL mark onboarding as completed in user profile

**FR8.2: Onboarding Access**
- System SHALL provide "Restart Onboarding" option in Settings
- System SHALL allow returning to onboarding after initial dismissal

### FR9: Offline Support & PWA

**FR9.1: Offline Functionality**
- System SHALL save all notes to IndexedDB for offline access
- System SHALL allow reading notes while offline
- System SHALL allow creating/editing notes while offline (local saves only)
- System SHALL disable AI features (autocomplete, key term spotting) when offline
- System SHALL display clear "Offline" indicator in UI
- System SHALL sync all local changes to Firestore when connection restored

**FR9.2: PWA Installation**
- System SHALL provide installable Progressive Web App
- System SHALL prompt users to install after 2 visits or 5 minutes of use
- System SHALL register Service Worker for offline caching
- System SHALL cache static assets (CSS, JS, fonts, icons)
- System SHALL provide app icons for desktop and mobile (192x192, 512x512)

**FR9.3: Background Sync**
- System SHALL use Background Sync API to retry failed network requests
- System SHALL sync pending changes when network connection restored
- System SHALL notify user of sync completion

### FR10: User Settings & Preferences

**FR10.1: Account Settings**
- System SHALL allow users to update email address (with verification)
- System SHALL allow users to change password
- System SHALL allow users to delete account (with confirmation and 30-day grace period)
- System SHALL display current subscription tier (Free/Pro)

**FR10.2: Display Preferences**
- System SHALL support light and dark themes
- System SHALL auto-detect system theme preference on first visit
- System SHALL persist theme preference in user profile
- System SHALL allow manual theme override

**FR10.3: Editor Preferences**
- System SHALL allow users to set default font size (12px-20px)
- System SHALL allow users to toggle autocomplete on/off
- System SHALL allow users to adjust auto-save interval (15s-60s)

## 7. Non-Functional Requirements

### NFR1: Performance

**NFR1.1: Response Times**
- AI Autocomplete SHALL respond in <100ms (p95)
- Dictionary Autocomplete SHALL respond in <50ms (p95)
- Mode Transitions SHALL complete in <50ms (p95)
- Edit or Study Dialog SHALL display in <100ms (p95)
- Inline Diff Calculation SHALL complete in <200ms for notes up to 5,000 words (p95)
- AI Key Term Spotting SHALL complete in <5s for notes up to 3,000 words (p95)
- Note Search SHALL return results in <500ms for libraries with 1,000+ notes (p95)

**NFR1.2: Page Load Performance**
- First Contentful Paint (FCP) SHALL be <1.5s (p75)
- Largest Contentful Paint (LCP) SHALL be <2.5s (p75)
- Time to Interactive (TTI) SHALL be <3.5s (p75)
- Cumulative Layout Shift (CLS) SHALL be <0.1

**NFR1.3: Scalability**
- System SHALL support 10,000 concurrent active users
- System SHALL handle 100,000+ registered users
- System SHALL support individual note sizes up to 50,000 words
- System SHALL support user libraries with 10,000+ notes
- System SHALL handle 1,000 API requests/second to autocomplete endpoint

### NFR2: Reliability & Availability

**NFR2.1: Uptime**
- System SHALL maintain 99.5% uptime (excluding planned maintenance)
- Planned maintenance SHALL not exceed 4 hours per month
- Maintenance SHALL be scheduled during low-traffic periods (2-6 AM EST)

**NFR2.2: Data Durability**
- System SHALL ensure 99.999999999% (11 nines) data durability via Firestore
- System SHALL maintain redundant backups across multiple geographic regions
- System SHALL retain deleted notes for 30 days in soft-delete state

**NFR2.3: Error Handling**
- System SHALL log all errors to centralized monitoring service
- System SHALL display user-friendly error messages (no stack traces)
- System SHALL provide graceful degradation when services unavailable
- System SHALL retry failed operations with exponential backoff
- System SHALL maintain <0.1% error rate across all API endpoints

### NFR3: Security

**NFR3.1: Authentication & Authorization**
- System SHALL enforce strong password requirements (min 8 chars, 1 uppercase, 1 number, 1 special)
- System SHALL hash passwords using bcrypt with salt rounds ≥12
- System SHALL implement rate limiting on authentication endpoints (5 attempts per 15 minutes)
- System SHALL use JWT tokens with 24-hour expiration for session management
- System SHALL implement HTTPS-only communication (TLS 1.3)

**NFR3.2: Data Protection**
- System SHALL encrypt data in transit using TLS 1.3
- System SHALL encrypt data at rest in Firestore (AES-256)
- System SHALL implement row-level security rules in Firestore
- System SHALL ensure users can only access their own notes
- System SHALL sanitize all user input to prevent XSS attacks
- System SHALL implement CSRF protection on all state-changing operations

**NFR3.3: API Security**
- System SHALL store API keys in environment variables (not in code)
- System SHALL rotate OpenAI API keys every 90 days
- System SHALL implement rate limiting on all API endpoints
- System SHALL validate and sanitize all API inputs
- System SHALL implement request signing for sensitive operations

**NFR3.4: Privacy**
- System SHALL NOT use user notes to train AI models
- System SHALL NOT share user data with third parties (except service providers: OpenAI, Firebase)
- System SHALL allow users to export all their data (GDPR compliance)
- System SHALL allow users to delete all their data permanently
- System SHALL anonymize usage analytics (no PII)

### NFR4: Usability

**NFR4.1: User Interface**
- UI SHALL be responsive and work on screens from 320px to 4K resolution
- UI SHALL support keyboard navigation for all primary functions
- UI SHALL provide clear visual feedback for all user actions (<100ms)
- UI SHALL use consistent design patterns across all screens
- UI SHALL display loading indicators for operations taking >500ms

**NFR4.2: Accessibility**
- System SHALL meet WCAG 2.1 Level AA standards
- System SHALL support screen readers (NVDA, JAWS, VoiceOver)
- System SHALL provide keyboard shortcuts for common actions
- System SHALL maintain minimum 4.5:1 contrast ratio for text
- System SHALL provide alt text for all images and icons
- System SHALL support browser zoom up to 200% without layout breaking

**NFR4.3: Learnability**
- New users SHALL complete onboarding in <2 minutes
- Users SHALL successfully create first note within 30 seconds of onboarding completion
- UI SHALL provide contextual tooltips for all non-obvious features
- Error messages SHALL include actionable guidance (not just error codes)

### NFR5: Maintainability

**NFR5.1: Code Quality**
- Codebase SHALL maintain TypeScript strict mode compliance
- Codebase SHALL maintain >80% test coverage
- Code SHALL follow consistent style guide (enforced via ESLint)
- Code SHALL include JSDoc comments for all public functions
- Code SHALL use semantic versioning (SemVer)

**NFR5.2: Monitoring & Observability**
- System SHALL log all errors to centralized logging service (e.g., Sentry)
- System SHALL track key performance metrics (response times, error rates)
- System SHALL implement health check endpoints for all services
- System SHALL provide real-time dashboard for system status

**NFR5.3: Deployment**
- System SHALL support automated CI/CD pipeline
- Deployments SHALL include automated rollback capability
- System SHALL maintain separate environments: development, staging, production
- Breaking changes SHALL trigger major version increment

### NFR6: Compatibility

**NFR6.1: Browser Support**
- System SHALL support latest 2 versions of Chrome, Firefox, Safari, Edge
- System SHALL gracefully degrade on older browsers with warning message
- System SHALL support mobile browsers: Safari (iOS 14+), Chrome (Android 10+)

**NFR6.2: Device Support**
- System SHALL work on desktop (Windows, macOS, Linux)
- System SHALL work on tablets (iPad, Android tablets)
- System SHALL work on mobile phones (iOS 14+, Android 10+)
- PWA SHALL be installable on all supported platforms

**NFR6.3: Network Conditions**
- System SHALL function on connections as slow as 3G (1 Mbps)
- System SHALL optimize asset delivery for low-bandwidth scenarios
- System SHALL provide offline-first experience with background sync

### NFR7: Compliance & Legal

**NFR7.1: Data Regulations**
- System SHALL comply with GDPR (EU General Data Protection Regulation)
- System SHALL comply with CCPA (California Consumer Privacy Act)
- System SHALL provide data export functionality (user data portability)
- System SHALL provide data deletion functionality (right to be forgotten)

**NFR7.2: Terms of Service**
- System SHALL display Terms of Service and Privacy Policy during signup
- System SHALL require users to accept terms before creating account
- System SHALL notify users of material policy changes via email

**NFR7.3: Educational Use**
- System SHALL NOT claim to replace professional medical education
- System SHALL include disclaimer: "For educational purposes only, not medical advice"
- System SHALL NOT store Protected Health Information (PHI)

### NFR8: Cost Efficiency

**NFR8.1: Infrastructure Costs**
- System SHALL optimize Firestore reads/writes to minimize costs
- System SHALL implement caching to reduce redundant API calls
- System SHALL use IndexedDB for local storage to reduce Firestore reads
- System SHALL implement request batching where possible

**NFR8.2: AI API Costs**
- System SHALL use GPT-4.1 nano for autocomplete (most cost-effective model)
- System SHALL implement request debouncing to reduce unnecessary API calls
- System SHALL fall back to local dictionary when quota exceeded
- System SHALL monitor and alert on API cost thresholds

## 8. Features (4-Week MVP)

### MVP Core Features

#### 1. Three-Mode Architecture

_Core Concept:_ Three distinct modes optimized for different stages of the note-taking and learning workflow

**Create Note Mode** (for new notes)

- Visual indicator: Blue accent color
- AI autocomplete active (GPT-4.1 nano)
- Auto-save every 30 seconds
- UI: Minimal - just editor and autocomplete
- Optimized for speed and focus

**Edit Mode** (for existing notes via "Edit" choice)

- Visual indicator: Purple accent color
- AI autocomplete active (GPT-4.1 nano)
- **Inline Diff Button** in toolbar: "View Changes Since Last Save"
- Clicking button shows inline diff view (additions, deletions, unchanged)
- Auto-save every 30 seconds

**Study Mode** (for existing notes via "Study" choice)

- Visual indicator: Green accent color
- Editing DISABLED (read-only)
- AI Key Term Spotting active
- Can switch to Edit Mode to make changes

#### 2. AI Autocompletion (Create + Edit Modes)

_Purpose:_ Reduce typing load and catch missed terminology in real-time

- Model: GPT-4.1 nano
- Suggests nursing-specific abbreviations, terminology, and common phrases
- Non-intrusive: appears only after typing pauses (150ms)
- Performance target: <100ms
- Active in both Create Note Mode and Edit Mode only
- **Free tier**: 100 requests/month
- **Fallback**: Local dictionary (5,000+ nursing terms) when quota exceeded

#### 3. Auto-Save with Version Snapshots (Backend Only)

_Purpose:_ Never lose work, enable future features

- Auto-saves content every 30 seconds
- Creates version snapshots in background (Firestore)
- **No UI for version history in MVP** (backend infrastructure only)
- Enables future features: version restore, full history viewer
- **Free tier**: Last 5 snapshots per note (retained in backend)
- **Pro tier**: Unlimited snapshots

#### 4. Inline Diff View (Edit Mode Only)

_Purpose:_ Instant visibility into what changed since last save for confident editing

- Simple button in toolbar: "View Changes Since Last Save"
- Shows inline diff: Green (added), Red (removed), Gray (unchanged)
- Updates in real-time as user types (debounced 500ms)
- Performance target: <200ms diff calculation
- **NOT available in Create Mode** (keeps UI minimal for speed)

#### 5. AI Key Term Spotting (Study Mode - Core Differentiator)

_Purpose:_ Automatically identify exam-relevant terms and professor emphasis cues

- Model: GPT-4o-mini with Structured Outputs
- AI automatically detects exam-relevant terms in notes
- Highlights terms with emphasis signals (e.g., "important", "remember", "test will cover")
- Uses regex + AI to detect professor cues and critical concepts
- Sidebar panel shows all spotted terms with context snippets
- Click term to jump to location in note
- Export key terms list
- Performance target: <5s for 3,000-word note
- Available only in Study Mode (editing disabled)
- **Free tier**: 10 uses/month
- **Pro tier**: Unlimited

#### 6. Edit or Study Dialog

_Purpose:_ Make mode selection explicit and intentional when revisiting notes

- Appears when opening any existing note
- Two buttons: "Edit this note" | "Study this note"
- Shows note metadata: Created date, last edited, word count
- Simple, fast, clear decision point

#### 7. 2-Screen Onboarding

_Purpose:_ Ensure students understand workflow immediately

- **Screen 1**: "Welcome to NEXLY RN - Three modes for better learning"
  - Quick explanation of Create/Edit/Study
  - Visual indicators (Blue/Purple/Green)
- **Screen 2**: "Try it now"
  - Create a sample note (autocomplete demo)
  - See the Edit or Study Dialog
  - Quick tour done in <2 minutes

#### 8. Note Library

_Purpose:_ Find and open notes quickly

- Simple list view (no grid view in MVP)
- Search by title (local full-text search via Dexie)
- Sort by: Last edited, Created date, Title
- Click note → Opens Edit or Study Dialog
- "New Note" button → Opens Create Mode
- **NO filters in MVP** (defer to Fast-Follow)

## 9. Technical Stack (Next.js)

### Frontend

- **Next.js 15.1** with App Router
- **React 19.1** with concurrent features
- **TypeScript 5.9.3** with strict mode
- **Tiptap 3.4** editor (Client Component)
- **Shadcn UI** components (built on Radix UI)
- **Tailwind CSS 4.1** for styling
- **next-themes** for dark mode
- **Zustand 5.0.8** for client state management
- **Dexie 4.2.0** for offline IndexedDB storage

### Backend

- **Next.js API Routes** (serverless functions)
- **Firebase Authentication** (Client SDK + Admin SDK)
- **Firestore** (direct access from client + Admin SDK in API routes)
- **Firebase Admin SDK** for server-side operations
- **OpenAI API** (via Next.js API routes)

### AI

- **GPT-4.1 nano** for autocomplete (Create + Edit modes)
- **GPT-4o-mini with Structured Outputs** for key term spotting (Study Mode)
- Custom 5,000+ nursing terms DB for autocomplete fallback

### Deployment

- **Vercel** (recommended) or Firebase Hosting
- **PWA** (installable on desktop and mobile via next-pwa)
- **Progressive Web App** features:
  - Installable on all platforms
  - Offline support with Service Worker
  - Background sync for notes
  - No app store required

### Testing

- **Vitest 3.2.4** for unit tests
- **React Testing Library 16.3.0** for component tests
- **Playwright 1.55.0** for E2E tests
- **Firebase Emulator Suite** for backend testing

### Performance Targets

- Autocomplete: <100ms (GPT-4.1 nano)
- Mode transitions: <50ms
- Dialog display: <100ms
- Inline diff calculation: <200ms
- Key term spotting: <5s (GPT-4o-mini)
- First Contentful Paint: <1.5s
- Largest Contentful Paint: <2.5s

## 10. Monetization Strategy

**Important!** We are adopting a **freemium SaaS model** with a **request-based cap** for autocomplete to avoid heavy token-tracking complexity while still controlling costs

### Free Tier (Baseline Adoption — $0/month)

- Unlimited note-taking in all three modes
- Create Note Mode + Edit Mode + Study Mode
- **AI Autocompletion:** up to 100 requests/month (Create + Edit modes)
- After limit: fallback to dictionary-based autocomplete (5,000+ nursing terms DB, no API cost)
- **AI Key Term Spotting:** up to 10 uses/month
- Version snapshots: Last 5 per note (backend only, no UI in MVP)
- Inline diff view (Edit Mode): Available
- Local note storage + export (PDF/DOCX)

### Pro Tier (Core Value Unlock — $8.99/month or $79/year)

- Everything in Free, plus:
- **Unlimited AI Autocompletion** (Create + Edit modes)
- **Unlimited AI Key Term Spotting** (Study Mode)
- Unlimited version snapshots (backend)
- Early access to Fast-Follow features (templates, expansion, definitions, cloze)
- Advanced diff features when shipped (three-way diff, annotations)
- Export key terms list
- Advanced Note Library search
- Priority support + feature voting

### Team/Educator Tier (Institutional — $19.99/month per seat)

- Everything in Pro, plus:
- Educator Dashboard for validation workflows (future)
- Institution-level note sharing + analytics (future)
- Bulk license management
- Early access to beta features

### Rationale

- **Free Tier:** Showcases core product value while capping costs via request limits
- **Pro Tier:** Removes caps, adds study accelerators, ensures heavy users upgrade
- **Team/Educator Tier:** Supports institutional adoption and credibility-building

## 11. Success Metrics

### MVP Validation Metrics (2 weeks after beta launch)

**Core Workflow Metrics**

- **Mode Adoption Rate:** % of users using all three modes (Create/Edit/Study) in week 1
  - **Green light**: ≥60%
  - **Yellow light**: 40-59%
  - **Red light**: <40% (pivot strategy)
- **Create Mode Speed:** Avg time from note creation to first save
  - **Green light**: Users say "faster than [current method]"
  - **Yellow light**: Mixed feedback
  - **Red light**: "Too slow" or "No different"
- **Inline Diff Usage:** % of Edit Mode sessions using "View Changes" button
  - **Green light**: ≥70%
  - **Yellow light**: 50-69%
  - **Red light**: <50%
- **Study Mode Engagement:** % of users using Key Term Spotting at least once
  - **Green light**: ≥50%
  - **Yellow light**: 30-49%
  - **Red light**: <30% (users ignore Study Mode)
- **Autocomplete Acceptance:** % of suggestions accepted
  - **Green light**: ≥40%
  - **Yellow light**: 25-39%
  - **Red light**: <25% (accuracy too low)
- **Onboarding Completion:** % of users finishing the 2-screen onboarding
  - **Green light**: ≥80%
  - **Yellow light**: 60-79%
  - **Red light**: <60%

### Decision Matrix

**Green Light (Keep Building)**

- ≥60% use all three modes
- ≥70% use inline diff button
- ≥50% use Study Mode feature
- Users say "this is faster than [current method]"

**Yellow Light (Iterate)**

- Users understand modes but don't use one of them
- Autocomplete accuracy is poor
- Users confused by workflow

**Red Light (Pivot)**

- Users ignore Study Mode entirely
- "Why do I need three modes?"
- "Can I just have one mode with everything?"

### Lagging Metrics (Track but don't optimize for in MVP)

- DAU
- Retention
- Free-to-paid conversion
- Churn

## 12. Challenges & Risks

### Technical

- Autocomplete accuracy in Create and Edit modes
- Inline diff performance with very large notes
- AI accuracy for key term detection (false positives/negatives)
- Latency at scale
- PWA offline support reliability

### User Behavior

- Users confused by three modes instead of one
- Students failing to adopt Edit or Study modes
- Users bypassing Study Mode features
- Resistance to changing workflows
- Over-reliance on AI leading to passive note-taking

### Business

- Competition from generalist AI note apps
- Dependence on OpenAI API pricing
- User expectations for features not in MVP

### Mitigations

- Interactive 2-screen onboarding explaining when to use each mode
- Edit or Study Dialog makes mode choice explicit
- Efficient diff algorithm with debouncing
- User feedback loop for key term quality
- Snapshot retention limits on Free tier
- Version restore infrastructure ready for Fast-Follow
- Data privacy: notes not used to train AI
- Clear roadmap communication: "Coming in Week 5-6"

## 13. Timeline

### 4-Week Build Plan (Next.js)

**Week 1: Foundation**

- Set up Next.js 15.1 project with App Router
- Firebase integration (Client SDK + Admin SDK)
- Shadcn UI components setup
- Basic authentication flow (Firebase Auth)
- Mode switching logic + visual indicators (Blue/Purple/Green)
- Edit or Study Dialog

**Week 2: AI Autocomplete**

- Tiptap editor integration (Client Component)
- AI autocomplete (GPT-4.1 nano via Next.js API route)
- Auto-save logic with version snapshots (backend)
- Freemium request tracking in Firestore
- Local dictionary fallback

**Week 3: Diff & Key Terms**

- Inline diff button + diff view (Edit Mode)
- AI Key Term Spotting (GPT-4o-mini via Next.js API route)
- Key terms sidebar UI (Study Mode)
- Export key terms list

**Week 4: Polish & Launch Prep**

- Note library + search (Dexie full-text)
- 2-screen onboarding
- PWA configuration (next-pwa)
- Performance optimization
- E2E testing (Playwright)
- Deployment to Vercel

**Week 5: Beta Launch**

- Deploy to 20-50 nursing students
- Gather feedback for 2 weeks
- Measure success criteria
- Decide what to build next based on data

### Fast-Follow Schedule

**Week 5-6** (if green light from beta):

- Templates + slash commands
- Shorthand expansion
- Definition-on-demand

**Week 7-8** (based on user feedback):

- Cloze deletion generator
- Full version history UI
- Side-by-side diff viewer

**Month 2+**: Everything else based on validated learning

## 14. What We'll Learn From This MVP

After 2 weeks of users testing:

✓ **Do users understand the three modes?**

- Metric: % who use all three modes in Week 1

✓ **Is Create Mode actually faster than their current method?**

- Metric: Avg time from note creation to save
- Metric: Autocomplete acceptance rate
- Metric: User feedback

✓ **Do they use the Inline Diff button in Edit Mode?**

- Metric: % of Edit sessions clicking "View Changes"

✓ **Do they actually open Study Mode?**

- Metric: Study Mode adoption rate
- Metric: Key Term Spotting uses per note

✓ **What do users ask for?**

- If they request templates → build templates
- If they request more AI features → build more AI features
- If they ignore Study Mode → pivot strategy
- If they request version history UI → prioritize Fast-Follow

## 15. Why This 4-Week MVP Works

### Fast Time to Market

- 4 weeks to build vs 12 weeks for original scope
- Test with real users 2 months earlier
- Faster feedback loop = faster product-market fit

### Clear Learning

- You'll know if the three-mode concept resonates
- You'll know which Study Mode features users want most (expansion vs definitions vs cloze)
- You'll know if inline diff is sufficient or if full version history UI is needed

### Reduced Risk

- If users don't want Study Mode, you didn't waste 6 weeks building 4 features
- If they don't need Edit Mode's diff view, you didn't build a complex version history system
- You can pivot based on real usage data

### Better Focus

- One Study Mode feature done really well > four features done poorly
- Minimal UI in Create Mode truly minimal, not cluttered
- Each mode has a clear, distinct purpose

### PWA Benefits (vs Tauri)

- **No platform-specific builds** - one codebase for all platforms
- **Instant updates** - no app store approval process
- **Easier distribution** - just share a URL
- **Lower maintenance** - no native code to debug
- **Mobile support** - works on iOS/Android without native apps
- **Still installable** - users can install to desktop/home screen
- **Offline support** - service worker enables offline functionality

This validates your core hypothesis without the scope creep. You'll have a working product in a month instead of three months, and you'll learn what actually matters to nursing students.

## 16. Deployment Architecture

### Hosting

- **Primary**: Vercel (recommended for Next.js)
  - Automatic deployments from Git
  - Edge functions for API routes
  - CDN for static assets
  - Built-in analytics
- **Alternative**: Firebase Hosting
  - Integrated with Firebase services
  - CDN for global distribution
  - Custom domain support

### PWA Distribution

- **Web**: Simply share URL (https://nexly-rn.vercel.app)
- **Desktop Install**: Browser prompt to "Install app"
- **Mobile Install**: "Add to Home Screen" on iOS/Android
- **No app stores required** - instant access for all users

### Scalability

- **Next.js API Routes**: Serverless functions scale automatically
- **Firestore**: Auto-scaling NoSQL database
- **Vercel Edge Network**: Global CDN for low latency
- **Service Worker**: Offline support + background sync

This completes the revised PRD for the Next.js/PWA stack.

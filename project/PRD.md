# NEXLY RN Product Requirements Document

**Document Version:** 1.0
**Product Version:** v0.1.0 (MVP)
**Last Updated:** 2025-12-08

---

## Overview

- **Name:** NEXLY RN - Nursing Note-Taking Application
- **Current Version:** v0.1.0 (MVP)

- **Elevator Pitch:** NEXLY RN empowers nursing students to capture knowledge faster with AI-powered medical autocomplete, nursing-specific templates, and bulletproof offline sync—so they can focus on becoming exceptional nurses instead of fighting their note-taking tools.

- **Problem:** Nursing students face critical productivity barriers during lectures, clinicals, and study sessions:

  - Generic note-taking tools don't understand medical terminology, forcing manual typing of complex drug names and pathophysiology terms
  - Creating structured nursing documents (care plans, medication cards, SOAP notes) from scratch wastes 5-10 minutes per note
  - Students struggle to recall critical clinical formulas (MAP, dosage calculations, drip rates) during exams and rotations
  - Unreliable sync causes data loss anxiety during clinical rotations when internet connectivity is unstable
  - Current solutions either lack nursing-specific features or are too complex for fast note-taking

- **Solution:**

  - AI-powered medical autocomplete with real-time terminology suggestions during typing (one AI request = one suggestion batch per keystroke sequence)
  - 5,000+ term nursing dictionary (sourced from OpenMD Nursing Terminology Database under CC BY-SA 4.0 license) as seamless fallback when offline or over AI quota
  - Slash command system for instant template insertion (/template for care plans, SOAP notes, med cards)
  - Clinical formula library with normal ranges (/formula for MAP, BMI, drip rates, dosage calculations)
  - Bulletproof offline-first architecture with auto-save every 30 seconds, cloud sync, and last-write-wins conflict resolution with full version history
  - Clean, distraction-free editor focused exclusively on speed and reliability
  - Free tier with 100 AI requests/month and Pro tier with unlimited AI for $8.99/month via Stripe payment processing

- **Goals:**

  1. Reduce note-taking time by 50% compared to generic tools through AI autocomplete and templates, measured via self-reported user surveys comparing time-to-completion for creating standard nursing documents (care plan, med card) in NEXLY vs. Google Docs [Priority: P0]
  2. Achieve 99%+ sync reliability with zero data loss during offline clinical rotations, measured by successful sync operations / total sync attempts [Priority: P0]
  3. Reach 60%+ slash command adoption rate within first week of user onboarding, measured as percentage of users who execute at least one slash command in first 7 days [Priority: P0]
  4. Convert 5% of free users to Pro tier within 3 months of launch [Priority: P1]
  5. Maintain infrastructure costs under $85/month while supporting 1,000+ active users (breakdown: Vercel $20, Supabase $25, OpenAI API $25, PowerSync $10, monitoring $5) [Priority: P1]
  6. Achieve 40%+ AI autocomplete acceptance rate, calculated as (accepted suggestions / total suggestions shown) per user session [Priority: P1]
  7. Launch fully functional PWA with cross-platform support (desktop, tablet, mobile) [Priority: P0]
  8. Build foundation for future NCLEX prep integration and community features [Priority: P2]

- **Non-Goals (Out of Scope for v0.1.0 MVP):**
  - Three-Mode Architecture (Create/Edit/Study) → v0.2.0
  - Inline diff view → v0.3.0
  - AI Key Term Spotting → v0.4.0
  - Shorthand expansion, Definition-on-demand → v0.5.0
  - Version history UI, Cloze deletion generator → v0.6.0
  - Custom template builder, Spaced repetition → v0.7.0
  - Audio recording, Flashcards/quizzes → v0.8.0
  - Visual concept maps, Native mobile apps → v0.9.0
  - LMS integrations, Educator dashboard → v1.0.0
  - Real-time collaboration, Clinical documentation → Post-v1.0

---

## Version Roadmap

### v0.1.0 - MVP (Current Release)

**Theme:** Foundation & Core Note-Taking
**Target:** Initial launch

**Features included in this release:**

- AI-powered medical autocomplete (GPT-4.1 nano, <200ms response)
- Local 5,000+ nursing term dictionary fallback
- Slash commands (/template, /formula)
- Auto-save every 30 seconds with visual indicator
- Note CRUD operations (create, read, update, delete)
- Note organization (7 categories: Pharmacology, Med-Surg, Pediatrics, OB, Mental Health, Clinical Rotation, Other)
- Search by title and content
- Trash with 30-day recovery
- Offline-first architecture with PowerSync
- Email/password authentication via Supabase
- Free tier (100 AI requests/month) / Pro tier ($8.99/month, $79/year)
- PWA support (desktop, tablet, mobile)
- Export to Markdown and Plain Text
- Version snapshots (backend storage only, no UI)

---

### v0.2.0 - Mode Architecture

**Theme:** Three-Mode System & Intelligent Workflows

**New features:**

- **Three-Mode Architecture** (core differentiator)
  - Create Note Mode: Blue accent, AI autocomplete active, minimal UI optimized for speed
  - Edit Mode: Purple accent, AI autocomplete active, full editing capabilities
  - Study Mode: Green accent, read-only (editing DISABLED), optimized for review
- **Edit or Study Dialog**: Appears when opening existing notes with two clear choices
  - Shows note metadata: created date, last edited, word count
  - Explicit mode selection for intentional workflows
- **Mode visual indicators**: Color-coded accents throughout UI
- **2-Screen Onboarding**: Welcome flow completing in <2 minutes
  - Screen 1: "Welcome to NEXLY RN - Three modes for better learning"
  - Screen 2: "Try it now" with autocomplete demo and dialog preview
- **Tighter autocomplete latency**: <100ms (improved from MVP's <200ms)

**Performance targets:**

- Mode transitions: <50ms
- Dialog display: <100ms
- Autocomplete: <100ms

---

### v0.3.0 - Edit Intelligence

**Theme:** Smart Editing & Change Tracking

**New features:**

- **Inline Diff View** (Edit Mode only)
  - "View Changes Since Last Save" button in toolbar
  - Color-coded changes: Green (added), Red (removed), Gray (unchanged)
  - Real-time updates (debounced 500ms)
  - diff-match-patch library integration

**Performance targets:**

- Diff calculation: <200ms

---

### v0.4.0 - Study Mode Intelligence

**Theme:** AI-Powered Learning (Core Differentiator)

**New features:**

- **AI Key Term Spotting** (Study Mode only)
  - Model: GPT-4o-mini with Structured Outputs
  - Automatically detects exam-relevant terms in notes
  - Highlights professor emphasis cues ("important", "remember", "test will cover")
  - Regex + AI detection for critical concepts
  - Sidebar panel with all spotted terms and context snippets
  - Click-to-jump navigation from term list to note location
  - Export key terms list functionality
- **Tier limits for Key Term Spotting:**
  - Free tier: 10 uses/month
  - Pro tier: Unlimited

**Performance targets:**

- Key term spotting: <5s for 3,000-word note

---

### v0.5.0 - Productivity Enhancements

**Theme:** AI-Powered Writing Assistance

**New features:**

- **SBAR Template**: New template added to existing /template command
  - Situation → Background → Assessment → Recommendation structure
- **Shorthand Expansion**: AI converts nursing abbreviations to full text
  - Example: "pt c/o SOB" → "patient complains of shortness of breath"
- **Definition-on-Demand**: Highlight text → AI defines medical term
  - Tooltip with term definition, category, and related terms

_Note: `/template` and `/formula` slash commands exist since v0.1.0. This version EXTENDS them._

---

### v0.6.0 - Study Tools

**Theme:** Active Learning Features

**New features:**

- **Cloze Deletion Generator**: AI suggests fill-in-the-blank questions from notes
  - Automatic identification of key facts suitable for cloze format
  - One-click conversion of highlighted text to cloze card
- **Version History UI**: Timeline view of note snapshots
  - Visual timeline showing save points
  - Preview any previous version
  - Restore with one click
- **Side-by-Side Diff Viewer**: Compare any two versions
  - Select two snapshots from timeline
  - Synchronized scrolling between versions

_Note: Version snapshots are stored in backend since v0.1.0. This version adds the USER INTERFACE._

---

### v0.7.0 - Customization

**Theme:** Personalization & Advanced Features

**New features:**

- **Custom Template Designer**: Create personalized templates
  - Drag-and-drop section builder
  - Save and reuse custom templates
  - Share templates (Pro feature)
- **Advanced Diff Features**:
  - Three-way diff for merge conflicts
  - Annotations on diff view
- **Spaced Repetition**: For cloze cards created in v0.6.0
  - SM-2 algorithm implementation
  - Review scheduling and reminders

---

### v0.8.0 - Audio & Visual

**Theme:** Multimedia Learning

**New features:**

- **Audio Sync**: Record lectures with note timestamps
  - Audio recording during note-taking
  - Clickable timestamps in notes to jump to audio position
  - Audio playback with synchronized note highlighting
- **Flashcards from Key Terms**: Convert spotted terms to flashcards
  - Automatic flashcard generation from v0.4.0 key terms
  - Flashcard review interface
- **Quiz Generation**: Create quizzes from notes
  - AI-generated multiple choice questions
  - True/false questions from note content
  - Quiz results and progress tracking

---

### v0.9.0 - Visual Learning

**Theme:** Concept Mapping

**New features:**

- **Visual Concept Mapping**: Create mind maps from notes
  - AI-suggested connections between concepts
  - Drag-and-drop concept arrangement
  - Link concepts to note sections
- **Mobile Companion App**: React Native application
  - Native iOS and Android apps
  - Offline-first with sync to main app
  - Optimized mobile note-taking experience

---

### v1.0.0 - Enterprise & Integration

**Theme:** Full Platform Release

**New features:**

- **LMS Integration**: Connect with learning management systems
  - Canvas integration
  - Blackboard integration
  - Assignment submission support
- **Advanced Analytics**: Study patterns and progress tracking
  - Time spent per note/category
  - Study streak tracking
  - Learning progress dashboards
- **Educator Dashboard**: Production-ready instructor tools
  - Class management
  - Template distribution
  - Student progress overview

---

### Post-v1.0 Roadmap (2026+)

- SimPatient builder
- AR/VR integration
- NCLEX readiness features
- Personalized study guidance
- Real-time collaboration
- Clinical documentation for patient care

## User Stories

### User Story 1: Fast Medical Terminology Entry

As a nursing student taking notes during a fast-paced pharmacology lecture, I want AI to autocomplete complex medical terms as I type, so that I can keep up with the professor without missing critical information.

**Acceptance Scenarios:**

- **Given I'm typing a medication name, when I type "met", then I see suggestions like "metoprolol", "metformin", "methotrexate" in real-time**
- **Given I'm offline during clinical rotation, when I type medical terms, then the local 5,000+ term dictionary provides autocomplete suggestions**
- **Given I've exceeded my monthly AI quota, when I continue typing, then the system seamlessly falls back to dictionary autocomplete without interruption**
- **Given I accept an AI suggestion, when I press Tab or Enter, then the complete term is inserted and I can continue typing immediately**

### User Story 2: Instant Nursing Template Insertion

As a nursing student creating a care plan for a patient case study, I want to instantly insert a structured care plan template, so that I can focus on clinical reasoning instead of formatting.

**Acceptance Scenarios:**

- **Given I type "/template" in the editor, when the slash command menu appears, then I see options for Care Plan, Medication Card, SOAP Note, Head-to-Toe Assessment, and Pathophysiology Outline**
- **Given I select "Care Plan" from the menu, when it inserts, then I see pre-formatted sections for Nursing Diagnosis → Goals → Interventions → Evaluation with cursor positioned in the first field**
- **Given I select "Medication Card", when it inserts, then I see structured fields for Drug → Classification → Action → Dose → Side Effects → Nursing Considerations**
- **Given I'm creating a clinical note, when I use "/template" and select "SOAP Note", then I get Subjective → Objective → Assessment → Plan sections ready to fill**

### User Story 3: Quick Clinical Formula Access

As a nursing student during a medication calculation exam, I want to quickly insert clinical formulas with normal ranges, so that I can accurately calculate dosages and vital signs without memorizing formulas.

**Acceptance Scenarios:**

- **Given I type "/formula" in the editor, when the command menu appears, then I see formulas for MAP, BMI, IV Drip Rates, Dosage Calculations, Glasgow Coma Scale, and Fluid Deficit**
- **Given I select "MAP (Mean Arterial Pressure)", when it inserts, then I see the formula with normal range: "Normal 70-100 mmHg"**
- **Given I select "BMI", when it inserts, then I see the calculation formula and "Normal 18.5-24.9" range**
- **Given I need to calculate IV drip rates, when I select the drip rate formula, then I receive the complete calculation structure with unit conversions**

### User Story 4: Reliable Offline Note-Taking with Conflict Resolution

As a nursing student in a clinical rotation with spotty WiFi, I want my notes to auto-save locally and sync automatically when I'm back online with clear conflict resolution, so that I never lose critical patient case notes.

**Acceptance Scenarios:**

- **Given I'm editing a note offline, when 30 seconds pass, then the note auto-saves to local SQLite storage (via PowerSync)**
- **Given I close my laptop during clinical without saving manually, when I reopen the app, then my latest changes are preserved**
- **Given I regain internet connectivity after being offline, when the app detects connection, then all local changes sync to Supabase automatically**
- **Given I edit the same note on my phone and laptop while offline, when both devices come online, then the system applies last-write-wins resolution (most recent timestamp wins) and preserves the overwritten version in version history**
- **Given a sync conflict occurs, when the conflict is resolved, then I see a notification indicating which device's version was kept and can access the alternate version via version history**

### User Story 5: Tier-Based AI Access Management

As a free-tier nursing student, I want to use AI autocomplete for my most important notes, and fall back to dictionary autocomplete when I exceed my quota, so that I can evaluate the Pro tier before committing to a subscription.

**Acceptance Scenarios:**

- **Given I'm on the free tier with 100 AI requests/month, when I use AI autocomplete, then I see my remaining quota in the UI**
- **Given I reach my monthly AI limit, when I continue typing, then the app seamlessly switches to the 5,000+ term local dictionary without errors**
- **Given I upgrade to Pro tier ($8.99/month), when I start typing, then I have unlimited AI autocomplete requests**
- **Given I'm considering Pro, when I view the pricing page, then I see clear comparison: Free (100 AI/month) vs Pro (unlimited AI)**

### User Story 6: Account and Authentication

As a nursing student, I want to create an account with my email and password, so that my notes sync across my devices and remain secure.

**Acceptance Scenarios:**

- **Given I'm a new user, when I sign up with email and password, then my account is created and I'm logged in immediately**
- **Given I'm a returning user, when I log in with my credentials, then I see my synced notes from all devices**
- **Given I forget my password, when I use password reset, then I receive an email with reset instructions**
- **Given I'm logged in, when my session expires, then I'm prompted to re-authenticate without losing local note data**

### User Story 7: Cross-Platform PWA Access

As a nursing student using multiple devices, I want to access NEXLY RN on my laptop, tablet, and phone through a PWA, so that I can take notes wherever I study.

**Acceptance Scenarios:**

- **Given I access NEXLY RN in my browser, when I install the PWA, then it appears as a standalone app icon on my device**
- **Given I'm using the PWA on desktop, when I take notes, then the experience is identical to a native application**
- **Given I'm on my phone during clinical, when I open the PWA, then I have full editor functionality with touch-optimized controls**
- **Given I switch from tablet to laptop, when I open the app, then my notes are synced and accessible immediately**

### User Story 8: Note Organization and Management

As a nursing student with multiple courses and clinical rotations, I want to organize my notes by category and quickly search for specific topics, so that I can find information when I need it.

**Acceptance Scenarios:**

- **Given I create a new note, when I save it, then I can assign it to a category (e.g., Pharmacology, Med-Surg, Pediatrics, Clinical Rotation)**
- **Given I have multiple notes, when I view my notes library, then I can filter by category and sort by date created or last modified**
- **Given I need to find specific information, when I use the search function, then I see results matching note titles and content**
- **Given I no longer need a note, when I delete it, then it moves to a trash folder where I can recover it within 30 days before permanent deletion**
- **Given I accidentally delete a note, when I access the trash folder, then I can restore the note with all content intact**

### User Story 9: Note CRUD Operations

As a nursing student, I want to create, view, edit, and delete notes seamlessly, so that I can manage my study materials efficiently.

**Acceptance Scenarios:**

- **Given I'm on the notes dashboard, when I click "New Note", then a new blank note opens in the editor with cursor ready for input**
- **Given I have existing notes, when I click on a note title, then the note opens in the editor with full content displayed**
- **Given I'm editing a note, when I make changes, then the changes auto-save every 30 seconds and I see a "Saved" indicator**
- **Given I want to start fresh, when I create a new note, then I have the option to use a blank canvas or select a template via slash commands**
- **Given I'm viewing my notes list, when I right-click or long-press a note, then I see options to rename, duplicate, export, or delete the note**

## Requirements

### Functional Requirements

#### Core Editor Features

- **FR-001:** The editor must provide real-time AI-powered autocomplete suggestions for medical terminology as users type, with suggestions appearing within 200ms of keystroke input.
- **FR-002:** The system must include a local 5,000+ term nursing dictionary (sourced from OpenMD Nursing Terminology Database under CC BY-SA 4.0 license) that activates automatically when AI quota is exceeded or offline mode is detected.
- **FR-003:** Users must be able to trigger slash commands by typing "/" followed by command keywords (e.g., "/template", "/formula") to insert structured content.
- **FR-004:** The "/template" command must provide pre-formatted options for: Care Plans, Medication Cards, SOAP Notes, Head-to-Toe Assessments, and Pathophysiology Outlines.
- **FR-005:** The "/formula" command must insert clinical formulas with normal ranges including: MAP (70-100 mmHg), BMI (18.5-24.9), IV Drip Rates (gtt/min and mL/hr conversions), Dosage Calculations (mg/kg), Glasgow Coma Scale (3-15), and Fluid Deficit.

#### Note Management (CRUD)

- **FR-006:** Users must be able to create new notes via "New Note" button, opening a blank editor with cursor positioned for immediate input.
- **FR-007:** Users must be able to view all their notes in a notes library with list/grid view options showing note title, preview, category, and last modified date.
- **FR-008:** Users must be able to edit existing notes by clicking on them from the notes library, opening the note in the editor with full content loaded.
- **FR-009:** Users must be able to delete notes, which moves them to a trash folder where they can be recovered within 30 days before permanent deletion.
- **FR-010:** Users must be able to rename notes via inline editing in the notes library or within the editor header.
- **FR-011:** Users must be able to duplicate existing notes to create copies for reuse (e.g., duplicating a template-based care plan).

#### Note Organization

- **FR-012:** Users must be able to assign categories to notes (Pharmacology, Med-Surg, Pediatrics, OB, Mental Health, Clinical Rotation, Other).
- **FR-013:** Users must be able to filter notes by category and sort by date created, last modified, or alphabetically by title.
- **FR-014:** Users must be able to search notes by title and content with real-time search results.
- **FR-015:** Users must be able to access a trash folder to view deleted notes and restore or permanently delete them.

#### Auto-Save and Sync

- **FR-016:** Notes must auto-save to local SQLite storage (via PowerSync) every 30 seconds without requiring manual user action, with visual "Saved" indicator.
- **FR-017:** The system must sync local notes to Supabase PostgreSQL automatically when internet connectivity is available.
- **FR-018:** Offline editing must be fully functional with all core features (editor, slash commands, dictionary autocomplete, note CRUD) available without internet.
- **FR-019:** The system must detect sync conflicts when the same note is edited on multiple devices while offline and resolve using last-write-wins algorithm (most recent timestamp wins).
- **FR-020:** When sync conflicts occur, the system must preserve the overwritten version in version history and display a notification to the user indicating which version was kept.
- **FR-021:** The system must maintain version history for each note, storing snapshots at each sync event to enable conflict recovery and historical review.

#### Authentication and Account Management

- **FR-022:** Users must be able to create accounts using email/password authentication via Supabase Auth with minimum password requirements (8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character).
- **FR-023:** Users must be able to log in with email/password credentials, with session persistence across browser sessions.
- **FR-024:** Users must be able to reset forgotten passwords via email reset link sent through Supabase Auth.
- **FR-025:** The system must enforce session timeout after 24 hours of inactivity, requiring re-authentication while preserving local note data.
- **FR-026:** The system must support concurrent sessions (same user logged in on multiple devices) with proper sync conflict resolution.

#### Tier Management and Payment

- **FR-027:** Free tier users must receive 100 AI autocomplete requests per month (one request = one suggestion batch per keystroke sequence) with visual quota tracking showing remaining requests.
- **FR-028:** Pro tier users ($8.99/month or $79/year) must receive unlimited AI autocomplete requests.
- **FR-029:** The system must track user tier status and enforce quota limits on AI requests based on subscription level, falling back to dictionary autocomplete when quota exceeded.
- **FR-030:** The system must integrate with Stripe for payment processing, supporting both monthly ($8.99) and annual ($79) subscription billing.
- **FR-031:** Users must be able to upgrade from Free to Pro tier via in-app payment flow and downgrade from Pro to Free tier with changes taking effect at next billing cycle.
- **FR-032:** The system must display current subscription status, billing date, and payment method in user account settings.

#### Export and Data Portability

- **FR-033:** Users must be able to export individual notes to Markdown (.md) and Plain Text (.txt) formats via export menu.
- **FR-034:** Users must be able to bulk export all notes as a ZIP archive containing Markdown files organized by category.

#### Progressive Web App (PWA)

- **FR-035:** The application must function as a PWA installable on desktop, tablet, and mobile devices with proper manifest configuration.
- **FR-036:** The PWA must include service workers enabling offline functionality and cache management.
- **FR-037:** The PWA must display custom app icon, splash screen, and app name when installed on user devices.

---

### Version-Specific Functional Requirements

#### v0.2.0 - Mode Architecture Requirements

- **FR-038:** The system must support three distinct editing modes: Create Note Mode, Edit Mode, and Study Mode, with clear visual differentiation.
- **FR-039:** Create Note Mode must display a blue accent color and provide a minimal UI optimized for speed with AI autocomplete active.
- **FR-040:** Edit Mode must display a purple accent color with full editing capabilities and AI autocomplete active.
- **FR-041:** Study Mode must display a green accent color, disable all editing functionality, and display content as read-only.
- **FR-042:** When opening an existing note, the system must display an "Edit or Study" dialog presenting two clear choices with note metadata (created date, last edited, word count).
- **FR-043:** The system must provide a 2-screen onboarding flow completing in under 2 minutes, introducing the three-mode architecture and demonstrating autocomplete functionality.
- **FR-044:** Mode transitions must complete within 50ms with no visible UI lag.

#### v0.3.0 - Edit Intelligence Requirements

- **FR-045:** In Edit Mode, the toolbar must include a "View Changes Since Last Save" button that displays an inline diff view.
- **FR-046:** The inline diff view must color-code changes: green for additions, red for deletions, and gray for unchanged content.
- **FR-047:** The diff view must update in real-time as the user types, with updates debounced at 500ms intervals.
- **FR-048:** Diff calculations must complete within 200ms for notes up to 50,000 characters.

#### v0.4.0 - Study Mode Intelligence Requirements

- **FR-049:** In Study Mode, the system must provide AI Key Term Spotting functionality using GPT-4o-mini with Structured Outputs.
- **FR-050:** AI Key Term Spotting must automatically identify exam-relevant terms and professor emphasis cues (e.g., "important", "remember", "test will cover").
- **FR-051:** A sidebar panel must display all spotted key terms with context snippets and click-to-jump navigation.
- **FR-052:** Users must be able to export the key terms list in text format.
- **FR-053:** Key Term Spotting must complete within 5 seconds for notes up to 3,000 words.
- **FR-054:** Free tier users must receive 10 Key Term Spotting uses per month; Pro tier users receive unlimited uses.

#### v0.5.0 - Productivity Enhancement Requirements

- **FR-055:** The "/template" command must include an SBAR template option (Situation → Background → Assessment → Recommendation).
- **FR-056:** The system must provide Shorthand Expansion functionality that converts nursing abbreviations to full text (e.g., "pt c/o SOB" → "patient complains of shortness of breath").
- **FR-057:** Users must be able to highlight text and trigger Definition-on-Demand to receive AI-generated medical term definitions in a tooltip.

#### v0.6.0 - Study Tools Requirements

- **FR-058:** The system must provide a Cloze Deletion Generator that suggests fill-in-the-blank questions from note content.
- **FR-059:** The system must provide a Version History UI displaying a timeline of note snapshots with preview and one-click restore functionality.
- **FR-060:** The system must provide a Side-by-Side Diff Viewer allowing comparison of any two version snapshots with synchronized scrolling.

#### v0.7.0 - Customization Requirements

- **FR-061:** Users must be able to create custom templates using a drag-and-drop section builder.
- **FR-062:** Pro tier users must be able to share custom templates with other users.
- **FR-063:** The system must implement spaced repetition scheduling for cloze cards using the SM-2 algorithm.

#### v0.8.0 - Audio & Visual Requirements

- **FR-064:** Users must be able to record audio during note-taking with automatic timestamp markers.
- **FR-065:** Users must be able to click timestamps in notes to jump to corresponding audio positions.
- **FR-066:** Users must be able to convert Key Terms (from v0.4.0) into flashcards with a single click.
- **FR-067:** The system must generate multiple-choice and true/false quiz questions from note content.

#### v0.9.0 - Visual Learning Requirements

- **FR-068:** Users must be able to create visual concept maps from notes with AI-suggested connections.
- **FR-069:** A native mobile companion app (iOS and Android) must provide offline-first note-taking synchronized with the main application.

#### v1.0.0 - Enterprise Requirements

- **FR-070:** The system must integrate with Canvas and Blackboard LMS platforms for assignment submission.
- **FR-071:** Users must have access to an analytics dashboard showing study patterns, time spent per note/category, and learning progress.
- **FR-072:** Educators must have access to a dashboard for class management, template distribution, and student progress overview.

---

### Non-Functional Requirements

- **Performance Requirements:**

  - AI autocomplete suggestions must appear within 200ms of keystroke input
  - Auto-save operations must complete within 500ms without blocking the editor
  - Initial page load must complete within 2 seconds on 3G connection with LCP (Largest Contentful Paint) < 2.5s
  - Editor must handle notes up to 50,000 characters without performance degradation (note: typical note length is 1,000-5,000 characters; 50,000 is edge case)
  - Client-side memory usage must remain under 150MB for typical usage (10-20 notes loaded in memory)
  - Search operations must return results within 300ms for libraries up to 1,000 notes

- **Scalability Requirements:**

  - Support 1,000+ concurrent active users on MVP infrastructure
  - Handle 10,000+ AI autocomplete requests per day
  - Scale to 10,000+ total users within 6 months post-launch
  - Supabase PostgreSQL must accommodate 100,000+ note records efficiently
  - API endpoints must support rate limiting of 60 requests per minute per user (excluding AI requests which have quota limits)

- **Security Requirements:**

  - All user authentication must use Supabase Auth with encrypted password storage
  - Passwords must meet minimum requirements: 8 characters, 1 uppercase, 1 lowercase, 1 number, 1 special character
  - API endpoints must validate user tier and quota before processing AI requests
  - User notes must be stored with proper PostgreSQL Row Level Security policies (users can only access their own notes)
  - HTTPS must be enforced for all client-server communication
  - Environment variables containing API keys must never be exposed to client-side code
  - Stripe webhook signatures must be validated to prevent payment fraud
  - Session tokens must be securely stored in httpOnly cookies with 24-hour expiration

- **Accessibility Requirements:**

  - Editor must be keyboard-navigable with logical tab order
  - ARIA labels must be present on all interactive elements
  - Minimum contrast ratio of 4.5:1 for text elements (WCAG AA compliance)
  - Slash command menu must be accessible via screen readers with proper ARIA announcements
  - Support for browser zoom up to 200% without layout breaking
  - Focus indicators must be visible on all interactive elements

- **Compatibility Requirements:**

  - Support latest versions of Chrome, Firefox, Safari, and Edge browsers (last 2 major versions)
  - PWA must install and function on Windows, macOS, Linux, iOS, and Android
  - Responsive design supporting screen sizes from 320px (mobile) to 2560px (desktop)
  - Offline functionality must work across all supported browsers with service worker support

- **Reliability Requirements:**

  - 99%+ sync success rate for online operations
  - Zero data loss during offline-to-online transitions
  - Auto-save must have 99.9%+ success rate
  - System uptime of 99.5% (excluding planned maintenance windows of max 2 hours/month)

- **Monitoring and Observability Requirements:**
  - System must log all authentication events (login, logout, password reset) for security auditing
  - System must track AI API costs per user tier to monitor budget adherence
  - System must monitor sync conflict frequency and resolution success rate
  - System must track error rates for critical operations (save, sync, payment processing)
  - System must provide real-time alerts when error rates exceed 5% or infrastructure costs exceed $75/month

## Technical Stack

### v0.1.0 Core Stack

- **Frontend Framework:** Next.js 14+ (App Router) with React 19
- **Language:** TypeScript
- **Editor:** Tiptap (ProseMirror-based rich text editor)
- **Styling:** Tailwind CSS v4 with Shadcn UI components
- **Authentication:** Supabase Auth (email/password)
- **Backend/Database:** Supabase PostgreSQL (cloud sync)
- **Local Storage:** PowerSync (SQLite-based offline-first sync)
- **AI Integration:** OpenAI GPT-4.1 nano API (medical autocomplete)
- **Payment Processing:** Stripe (subscription billing and checkout)
- **Deployment:** Vercel (Next.js hosting with serverless API routes)
- **PWA:** Next.js PWA plugin with service workers
- **Analytics:** Vercel Analytics (user behavior tracking)
- **Error Tracking:** Sentry (error monitoring and reporting)
- **Monitoring:** Vercel Monitoring + custom dashboard for cost tracking
- **Testing:** Vitest 3.2.4 (unit/integration tests) + Playwright 1.55.0 (E2E tests)

### Version-Specific Dependencies

| Version | New Dependencies             | Purpose                                      |
| ------- | ---------------------------- | -------------------------------------------- |
| v0.3.0  | diff-match-patch             | Inline diff view calculations                |
| v0.4.0  | GPT-4o-mini (OpenAI)         | AI Key Term Spotting with Structured Outputs |
| v0.7.0  | SM-2 algorithm library       | Spaced repetition scheduling                 |
| v0.8.0  | Web Audio API, MediaRecorder | Audio recording and playback                 |
| v0.9.0  | React Native, Expo           | Native mobile companion app                  |
| v1.0.0  | Canvas/Blackboard SDKs       | LMS integration APIs                         |

## Dependencies and Assumptions

**Dependencies:**

- Supabase project configured with PostgreSQL and Authentication enabled
- OpenAI API access with GPT-3.5-turbo for autocomplete functionality
- Stripe account for payment processing with webhook endpoints configured
- Vercel account for deployment and serverless function hosting
- Domain name and SSL certificate for production deployment
- 5,000+ term nursing dictionary dataset (JSON format) sourced from OpenMD Nursing Terminology Database under CC BY-SA 4.0 license for offline autocomplete
- Email service for password reset functionality (Supabase Auth handles this)
- Sentry account for error tracking and monitoring
- Vercel Analytics enabled for user behavior tracking

**Assumptions:**

- Target users have modern browsers (released within last 2 years) with service worker support
- Students have intermittent internet access but not constant connectivity
- Average note length is 1,000-5,000 characters (edge cases up to 50,000 characters supported)
- Users will primarily access the app on laptops/tablets during study sessions
- Free tier users will average 50 AI requests/month (under 100 quota)
- 5% conversion rate from free to Pro tier is achievable with clear value demonstration
- Infrastructure costs will remain under $85/month for 1,000 active users (breakdown: Vercel $20, Supabase $25, OpenAI $25, PowerSync $10, monitoring $5)
- Nursing terminology remains relatively stable (dictionary updates quarterly)
- Students prefer speed and simplicity over complex formatting features
- Users will primarily edit notes individually (no real-time collaborative editing required for MVP)
- OpenMD Nursing Terminology Database will remain available under CC BY-SA 4.0 license for commercial use

## Risks and Mitigation

### Risk 1: Low Slash Command Adoption

**Overview:** Students may not discover or use slash commands (/template, /formula) due to lack of awareness or discoverability, resulting in the app not delivering its core value proposition of speed.

**Mitigation Strategy:**

- Implement onboarding tour highlighting slash commands with interactive demo on first login
- Display in-editor tooltips showing "/" trigger when user pauses typing
- Track slash command usage metrics from day 1 to identify adoption gaps
- Add persistent UI hint near editor showing available commands until user has used them 5+ times
- Include keyboard shortcut cheatsheet accessible via "?" key

### Risk 2: AI API Costs Exceed Revenue

**Overview:** If AI autocomplete usage significantly exceeds projections (especially if free tier users abuse the 100 request quota), OpenAI API costs could exceed Pro tier revenue, making the business model unsustainable.

**Mitigation Strategy:**

- Implement strict request-based quota enforcement at API route level
- Monitor AI API costs weekly and set alerts at $50, $75, $100 thresholds
- Use GPT-3.5-turbo instead of GPT-4 to reduce per-request costs by 90%
- Implement request throttling (max 1 AI request per 3 seconds per user)
- Fall back to local dictionary automatically when quota exceeded to control costs
- Consider reducing free tier quota from 100 to 50 requests/month if costs remain high

### Risk 3: Generic Note Apps Add Nursing Features

**Overview:** Competitors like Notion or Google Docs could add medical terminology autocomplete or template libraries, reducing NEXLY RN's differentiation and market position.

**Mitigation Strategy:**

- Move fast and ship MVP within 4-6 weeks to establish market presence early
- Build strong nursing student community through Reddit, nursing school partnerships, and social media
- Focus on nursing-specific depth (specialty templates, NCLEX integration) that generalist tools won't prioritize
- Develop unique IP in clinical formula library and nursing-optimized UX
- Gather direct user feedback weekly to iterate faster than large competitors

### Risk 4: Sync Conflicts Cause Data Loss

**Overview:** When users edit the same note on multiple devices while offline, the conflict resolution algorithm could fail and cause permanent data loss, destroying user trust in reliability.

**Mitigation Strategy:**

- Implement last-write-wins conflict resolution with full version history preservation
- Store conflicting versions in PostgreSQL snapshots table for manual user review
- Display clear conflict notification UI when sync conflicts are detected
- Auto-backup all notes to Supabase every 5 minutes when online (not just on manual save)
- Implement comprehensive sync testing with automated offline/online scenario tests
- Add manual sync trigger button for users to control sync timing

### Risk 5: Student Churn During Summer/Graduation

**Overview:** Nursing students graduate or take summer breaks, causing high seasonal churn and revenue volatility, especially for monthly subscribers.

**Mitigation Strategy:**

- Offer annual pricing ($79/year vs $107.88 monthly) with 27% discount to lock in year-long commitment
- Build NCLEX prep features (practice questions, spaced repetition) to retain graduating students preparing for licensure exam
- Launch "Summer Study Mode" with discounted rates to retain users during break periods
- Create alumni discount tier for graduated nurses to maintain long-term relationship
- Develop referral program incentivizing current students to recruit incoming cohorts

### Risk 6: PWA Installation and Discoverability

**Overview:** Users may not understand how to install the PWA or may prefer waiting for native mobile apps, reducing cross-platform adoption and mobile usage.

**Mitigation Strategy:**

- Display clear PWA installation prompts with screenshots showing the "Add to Home Screen" process
- Create video tutorials for PWA installation on iOS, Android, Windows, and macOS
- Ensure PWA manifest is properly configured with app icons, splash screens, and offline support
- Track PWA installation rate and optimize prompts if below 30% installation rate
- Communicate "works like a native app" messaging clearly in marketing

### Risk 7: OpenAI API Unavailability or Rate Limiting

**Overview:** If OpenAI experiences service outages or implements stricter rate limiting, AI autocomplete could become unavailable, degrading the core user experience and value proposition.

**Mitigation Strategy:**

- Implement automatic fallback to local 5,000+ term nursing dictionary when AI API fails or times out
- Cache recent AI autocomplete responses locally (per session) to reduce API dependency
- Display clear user messaging when AI is unavailable: "Using offline dictionary mode"
- Monitor OpenAI API status page and set up alerts for service degradation
- Consider backup AI provider (Anthropic Claude, Google Gemini) for future redundancy
- Design UX so dictionary fallback feels seamless, not like a degraded experience

### Risk 8: Supabase Service Outages Affecting Core Functionality

**Overview:** Supabase PostgreSQL or Authentication outages could prevent users from logging in, syncing notes, or accessing their data, causing frustration and potential data loss anxiety.

**Mitigation Strategy:**

- Ensure full offline-first architecture where all core editing features work without Supabase connection
- Display clear status messaging when Supabase is unreachable: "Working offline - will sync when connection restored"
- Implement exponential backoff retry logic for failed sync operations (retry after 5s, 15s, 30s, 60s)
- Monitor Supabase status dashboard and communicate proactively to users during known outages
- Maintain local SQLite (via PowerSync) as source of truth, with Supabase as sync layer (not primary storage)
- Test app behavior during simulated Supabase outages in QA

### Risk 9: Medical Terminology Accuracy (AI Hallucinations)

**Overview:** OpenAI's GPT models could hallucinate incorrect medical terminology or suggest inappropriate terms, potentially leading students to document incorrect information in their notes.

**Mitigation Strategy:**

- Validate all AI suggestions against the 5,000+ term nursing dictionary before displaying to users (only show suggestions that match known valid terms)
- Display clear disclaimer in onboarding: "AI suggestions are tools for speed, not medical advice - always verify terminology"
- Implement user feedback mechanism to report incorrect suggestions (thumbs up/down on autocomplete)
- Monitor flagged suggestions weekly and add to blocklist if patterns of incorrect terms emerge
- Prioritize local dictionary over AI when confidence scores are low
- Consider hybrid approach: AI generates candidates, dictionary validates before showing to user

## Success Criteria

### v0.1.0 MVP Success Criteria

**MVP Validation (2 weeks, 50 beta users)**

- **SC-001:** 60%+ of beta users actively use slash commands (/template or /formula) within their first week, measured as (users who executed ≥1 slash command in first 7 days / total users who completed onboarding)
- **SC-002:** 40%+ AI autocomplete acceptance rate, calculated as (total accepted AI suggestions / total AI suggestions shown) across all user sessions during beta period
- **SC-003:** 99%+ sync reliability with zero reported data loss incidents during beta period, measured as (successful sync operations / total sync attempts)
- **SC-004:** Average user feedback score of 4+/5 on "faster than current note-taking method" metric from exit survey
- **SC-005:** 80%+ of users report successful offline editing without issues in exit survey

**Launch Success (3 months post-launch)**

- **SC-006:** 1,000+ active users, defined as users creating or editing at least one note per week, tracked via analytics
- **SC-007:** 5% conversion rate from free to Pro tier (50+ paying subscribers), calculated as (Pro subscribers / total registered users)
- **SC-008:** Infrastructure costs remain under $85/month while supporting user base, tracked via monthly spend dashboard
- **SC-009:** Net revenue of $364.50+/month, calculated as (50 Pro users × $8.99 = $449.50 revenue) - $85 infrastructure costs = $364.50 net
- **SC-010:** 70%+ user retention rate after first month, measured as (users active in month 2 / users who signed up in month 1)

**Product-Market Fit Validation**

- **SC-011:** 50%+ of users report they would be "very disappointed" if NEXLY RN no longer existed (Sean Ellis test), measured via quarterly PMF survey
- **SC-012:** Average session length of 15+ minutes (indicating deep engagement with editor), measured via analytics session duration
- **SC-013:** 30%+ of users create 10+ notes within first month (power user indicator), tracked via database query
- **SC-014:** Organic growth rate of 15%+ month-over-month through word-of-mouth referrals, measured as (new users month N / new users month N-1) - 1
- **SC-015:** NPS (Net Promoter Score) of 40+ indicating strong user satisfaction and recommendation likelihood, measured via quarterly NPS survey

---

### Version-Specific Success Criteria

#### v0.2.0 - Mode Architecture Success

- **SC-016:** 80%+ of users complete the 2-screen onboarding flow within 2 minutes
- **SC-017:** Mode transitions consistently complete within 50ms (99th percentile)
- **SC-018:** 70%+ of users who open existing notes use the Edit or Study dialog appropriately
- **SC-019:** Users report 4+/5 satisfaction with mode differentiation in post-release survey

#### v0.3.0 - Edit Intelligence Success

- **SC-020:** 50%+ of Edit Mode users utilize the "View Changes Since Last Save" feature at least once per week
- **SC-021:** Diff calculations consistently complete within 200ms for notes up to 50,000 characters
- **SC-022:** User feedback score of 4+/5 on "confident editing with change visibility" metric

#### v0.4.0 - Study Mode Intelligence Success

- **SC-023:** 60%+ of Study Mode users engage with AI Key Term Spotting feature
- **SC-024:** Key Term Spotting completes within 5 seconds for 95% of notes up to 3,000 words
- **SC-025:** 40%+ of users export key terms lists for external study use
- **SC-026:** Pro tier conversion increases by 2% attributable to Key Term Spotting feature

#### v0.5.0 - Productivity Enhancements Success

- **SC-027:** SBAR template becomes one of top 3 most-used templates within 30 days of release
- **SC-028:** 30%+ of users try Shorthand Expansion feature at least once
- **SC-029:** Definition-on-Demand usage averages 5+ lookups per active user per week

#### v0.6.0 - Study Tools Success

- **SC-030:** 40%+ of users create at least one cloze card from their notes
- **SC-031:** 50%+ of users access Version History UI at least once per month
- **SC-032:** Side-by-Side Diff Viewer used by 25%+ of users who access Version History

#### v0.7.0 - Customization Success

- **SC-033:** 20%+ of Pro users create at least one custom template
- **SC-034:** Custom templates are shared 100+ times within first 60 days
- **SC-035:** 30%+ of cloze card creators engage with spaced repetition scheduling

#### v0.8.0 - Audio & Visual Success

- **SC-036:** 25%+ of users record at least one audio note within first month
- **SC-037:** 40%+ of Key Term users convert terms to flashcards
- **SC-038:** Quiz completion rate of 70%+ for generated quizzes

#### v0.9.0 - Visual Learning Success

- **SC-039:** 20%+ of users create at least one concept map
- **SC-040:** Mobile companion app achieves 4+ star rating on App Store and Google Play
- **SC-041:** 30%+ of desktop users also install and use mobile app

#### v1.0.0 - Enterprise Success

- **SC-042:** Successful LMS integration with at least one educational institution
- **SC-043:** 50%+ of users engage with analytics dashboard monthly
- **SC-044:** 10+ educators actively using the Educator Dashboard
- **SC-045:** Overall user base reaches 10,000+ active users
- **SC-046:** Pro tier conversion rate reaches 8%+ (up from initial 5% target)

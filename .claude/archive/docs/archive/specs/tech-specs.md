# Technical Specifications (4-Week MVP)

## 1. System Overview

**Architecture**: Desktop-first application using Tauri with web fallback
**Primary Stack**: React 19.1 + TypeScript 5.9 + Tailwind 4.1 + Tiptap 3.4
**Deployment**: Tauri desktop app, Progressive Web App (PWA)
**Core Concept**: Three-mode workflow (Create, Edit, Study) separating fast capture, confident revision, and AI-powered key term identification

## 2. Frontend Architecture

### Core Framework

- **React**: 19.1.1 with concurrent features
- **TypeScript**: 5.9.3 with strict mode enabled
- **Build Tool**: Vite 7.1.7 with HMR and code splitting
- **Desktop Runtime**: Tauri 2.8.4 (Rust-based, replaces Electron)

### UI Layer

**Component Library**
- Radix UI primitives for accessible, unstyled components
- Shadcn UI patterns built on Radix
- Custom components in `/src/components`

**Styling**
- Tailwind CSS 4.1.13 with Vite plugin
- Class utilities: `clsx`, `tailwind-merge`, `class-variance-authority`
- Responsive design with mobile-first approach
- Dark mode support via CSS variables

**Icons**
- Primary: Lucide React (544+ icons)
- Secondary: Tabler Icons (3.35.0)

### Rich Text Editor

**Tiptap 3.4.2**
- Core editor framework
- Starter Kit: basic formatting, headings, lists, code blocks
- Placeholder extension for empty state hints
- Custom extensions for:
  - Nursing terminology autocomplete (GPT-4.1 nano)
  - Inline diff highlighting (Edit Mode)

### State Management

**Zustand 5.0.8**
- Lightweight store for:
  - Editor mode (Create, Edit, Study)
  - Mode transition state
  - User preferences
  - Note metadata
  - AI request quota tracking
- Immer 10.1.3 for immutable state updates

### Local Database

**Dexie 4.2.0** (IndexedDB wrapper)
- Offline-first note storage
- Schema versioning and migrations
- Full-text search indexing
- Sync queue for Firebase replication

## 3. Backend Architecture

### Firebase Services

**Authentication**
- Email/password signup
- Google OAuth (future)
- Session persistence

**Firestore Database**
- Collections: `users`, `notes`, `versionSnapshots` (backend only)
- Security rules for user isolation
- Real-time sync for cross-device access
- Offline support with local cache

**Cloud Functions** (Node.js 20)
- AI request orchestration (autocomplete + key term spotting)
- Usage quota tracking (Free tier: 100 autocomplete requests/month, 10 key term spotting)
- Export generation (PDF/DOCX - future)

**Storage**
- Note attachments (images, PDFs - future)
- Exported note files (future)

### API Integration

**OpenAI API** (5.23.1)
- **GPT-4.1 nano** for autocompletion (<100ms target)
- **GPT-4o-mini with Structured Outputs** for key term spotting (<5s target)
- Fallback: Local nursing terms dictionary (5,000+ terms) when quota exceeded

## 4. Data Architecture

### Schema Design

**Notes Table** (Firestore/Dexie)
```
{
  id: string (UUID)
  userId: string
  title: string
  content: JSON (Tiptap document)
  mode: 'create' | 'edit' | 'study'
  createdAt: timestamp
  updatedAt: timestamp
  tags: string[]
  metadata: {
    courseCode: string
  }
}
```

**Version Snapshots Collection** (Firestore/Dexie - Backend Only, No UI in MVP)
```
{
  id: string (UUID)
  noteId: string
  userId: string
  content: JSON (Tiptap document)
  mode: 'create' | 'edit' | 'study'
  timestamp: timestamp
  changesSummary: {
    addedWords: number
    removedWords: number
    wordCountChange: number
  }
  snapshotType: 'auto' | 'manual' | 'mode_switch'
}
```

**User Preferences** (Firestore)
```
{
  userId: string
  tier: 'free' | 'pro' | 'team'
  usage: {
    autocompleteRequests: number
    keyTermSpottingUses: number
    resetDate: timestamp
  }
  settings: {
    theme: 'light' | 'dark'
    autoSave: boolean
  }
}
```

### Validation Layer

**Zod 3.25.67**
- Runtime schema validation for all API inputs
- Type-safe form validation
- Environment variable validation

## 5. Testing Strategy

### Unit Testing

**Vitest 3.2.4**
- Component tests with React Testing Library 16.3.0
- Business logic tests (utils, hooks)
- Coverage target: 90%+ for MVP critical paths
- Mocking: `fake-indexeddb` for Dexie tests

### Integration Testing

**Playwright 1.55.0**
- End-to-end user workflows
- Cross-browser testing (Chromium, Firefox, WebKit)
- Critical paths:
  - Signup → 2-Screen Onboarding → Create Mode
  - Mode transitions (Create ↔ Edit ↔ Study)
  - Autocompletion flow (Create & Edit modes)
  - Inline diff view (Edit mode)
  - Key term spotting (Study mode)

### Test Environment

- Happy DOM 18.0.1 for lightweight DOM simulation
- Coverage reporting with V8 provider

## 6. Performance Requirements

### Target Metrics

- **Autocompletion latency**: <100ms from keystroke to suggestion
- **Mode transitions**: <50ms UI response
- **Dialog display**: <100ms (Edit or Study Dialog)
- **Inline diff calculation** (Edit Mode): <200ms
- **Key term spotting**: <5s for 3,000-word note
- **Cold start**: <2s on desktop, <3s on web
- **Bundle size**: <500KB initial JS (code-split routes)

### Optimization Strategies

- Lazy load non-critical routes
- Debounce autocomplete requests (150ms)
- Debounce inline diff calculation (500ms)
- IndexedDB for offline caching
- Tauri native performance for desktop

## 7. Build & Deployment

### Development

```bash
npm start              # Web dev server (Vite)
npm run tauri:dev      # Desktop dev server
npm test               # Vitest unit tests
npm run test:e2e       # Playwright E2E tests
```

### Production Build

**Desktop** (Tauri)
- Platform-specific installers (Windows .msi, macOS .dmg, Linux .AppImage)
- Auto-update via Tauri updater
- Native OS integration (notifications, file system)

**Web** (PWA)
- Service Worker for offline support
- Lighthouse score target: 90+ performance
- CDN deployment (Vercel/Netlify)

### CI/CD Pipeline

- ESLint 9.36.0 + TypeScript ESLint for linting
- Prettier with XML plugin for formatting
- Pre-commit hooks for type checking
- Automated test runs on PR
- Staging preview deployments

## 8. Security

### Data Protection

- All Firebase communication over HTTPS
- Firestore security rules enforce user isolation
- No AI training on user notes (OpenAI data usage policy)
- Environment variables for secrets (`.env` files)

### Input Sanitization

- Zod validation on all user inputs
- XSS prevention via React's default escaping
- SQL injection N/A (using Firestore)

### Authentication

- Firebase Auth session tokens (1-hour refresh)
- Secure cookie storage
- CORS restrictions on API endpoints

## 9. Feature-to-Tech Mapping (4-Week MVP)

### Three-Mode Architecture

**State Management**
- State: Zustand store for current mode (Create/Edit/Study)
- UI: Mode-specific accent colors (Blue/Purple/Green) via CSS variables
- Persistence: Dexie + Firestore sync
- Transitions: <50ms with smooth color fade animations
- Visual indicators: Radix UI components + custom styling

**Edit or Study Dialog**
- Trigger: Opening any existing note
- UI: Radix Alert Dialog
- State: Zustand for user preference storage
- Actions: Route to Edit Mode or Study Mode
- Metadata display: Created date, last edited, word count

### AI Autocompletion (Create + Edit Modes Only)

**Tech Stack**
- Editor: Tiptap custom extension
- API: OpenAI GPT-4.1 nano via Firebase Function
- Fallback: Local dictionary (5,000 terms in JSON)
- Quota: Tracked in Firestore `users` collection
- Active in: Create Mode and Edit Mode only (disabled in Study Mode)

**Performance**
- Latency target: <100ms
- Debounce: 150ms typing pause
- Request size: ~100 tokens (last 50 words context)
- Response size: ~20 tokens (suggestions)

**Quota Management**
- Free tier: 100 requests/month
- Pro tier: Unlimited
- Fallback: Automatic switch to local dictionary when exceeded

### Auto-Save with Version Snapshots (Backend Only)

**Implementation**
- Storage: Firestore `versionSnapshots` collection + Dexie local cache
- Triggers: Auto-save interval (30s), manual save, mode switch
- Snapshot retention: Last 5 versions (Free tier), unlimited (Pro tier)
- **No UI in MVP** - backend infrastructure only for future features

**Conflict Resolution**
- Strategy: Last-write-wins with timestamp comparison
- Version tracking for optimistic concurrency control

### Inline Diff View (Edit Mode Only)

**Tech Stack**
- Diff library: diff-match-patch
- UI: Inline highlighting within editor
- Comparison: Current unsaved content vs last saved snapshot
- Update frequency: Debounced 500ms as user types
- Performance: <200ms diff calculation target

**Implementation**
- Button in toolbar triggers diff view
- Highlighting: Additions (green), deletions (red), unchanged (gray)
- **NOT available in Create Mode** (minimal UI for speed)

### AI Key Term Spotting (Study Mode Only)

**Tech Stack**
- Processing: OpenAI GPT-4o-mini with Structured Outputs via Firebase Function
- Performance: <5s for 3,000-word note
- UI: Sidebar panel with spotted terms + context snippets
- Features: Click term to jump to location, export key terms list
- Emphasis signals: "important", "remember", "test will cover"

**Implementation**
- Detection: Regex + AI to identify exam-relevant terms and professor cues
- Available only in Study Mode (editing disabled)
- Quota: 10 uses/month (Free), unlimited (Pro)

### 2-Screen Onboarding

**Tech Stack**
- Framework: Custom Tauri window or Radix Dialog
- Demo data: Pre-seeded Tiptap document
- Progress tracking: Zustand store

**Workflow**
- Screen 1: Explain three modes with visual indicators
- Screen 2: Interactive demo (create note → open → see dialog → modes)

### Note Library

**Tech Stack**
- UI: Simple list view with Radix Scroll Area
- Search: Local Dexie full-text search
- Sort: updatedAt, createdAt, title
- Filters: None in MVP

**Implementation**
- Click note → Opens Edit or Study Dialog
- "New Note" button → Opens Create Mode

### UI Components (Radix UI)

- Alert Dialog: Edit or Study Dialog, confirmation prompts
- Dialog: Onboarding, settings
- Scroll Area: Note library
- Toast: Notifications (quota warnings, save confirmations)
- Tooltip: Inline help

## 10. Development Constraints

### MVP Scope (4-Week Build)

**In Scope**
- Desktop app (Tauri)
- Web app (PWA)
- Three-mode architecture (Create/Edit/Study)
- AI autocompletion with quota (Create & Edit modes)
- Auto-save with version snapshots (backend only, no UI)
- Inline diff view (Edit mode)
- Edit or Study Dialog
- Key term spotting (Study mode)
- 2-screen onboarding
- Basic note library

**Out of Scope (Fast-Follow: Week 5-8)**
- Templates and slash commands
- Shorthand expansion
- Definition-on-demand
- Cloze deletion generation
- Full version history UI
- Side-by-side diff viewer
- Mobile native apps
- Real-time collaboration
- Audio transcription
- Flashcards/quizzes
- LMS integrations

### Technical Debt Allowances

- Version snapshots stored in backend but no UI to view them (enables future features)
- Simple inline diff only (no side-by-side viewer yet)
- Basic note library (no advanced filtering or grid view)
- Single language support (English) for MVP

## 11. Monitoring & Observability

### Metrics Collection

- Firebase Analytics for user behavior
- Performance monitoring via Lighthouse CI
- Error tracking (consider Sentry integration post-MVP)

### Key Metrics

- Autocomplete latency (p95)
- Mode transition latency (p95)
- Inline diff calculation time (p95)
- Key term spotting performance (p95)
- API error rates
- Quota breach frequency
- Mode adoption rates (Create/Edit/Study)
- Inline diff usage rate (Edit Mode sessions)
- Key term spotting usage rate (Study Mode sessions)

## 12. Dependencies Summary

**Total Production Dependencies**: 32
**Total Dev Dependencies**: 24
**Critical Path**: React → Tiptap → Radix UI → Tailwind → Tauri → Firebase → OpenAI

**Key Dependencies**
- React 19.1.1
- Tiptap 3.4.2
- Radix UI (multiple primitives)
- Tailwind CSS 4.1.13
- Tauri 2.8.4
- Firebase SDK
- OpenAI SDK 5.23.1
- Zustand 5.0.8
- Dexie 4.2.0
- diff-match-patch (for inline diff)

**Version Pinning Strategy**
- Major versions locked for stability
- Automated dependency updates via Dependabot (weekly)

## 13. 4-Week Build Timeline

### Week 1: Foundation
- Set up Firebase + auth
- Build basic note editor (Tiptap)
- Mode switching logic + visual indicators (Blue/Purple/Green)
- Edit or Study Dialog

### Week 2: AI Autocomplete
- AI autocomplete integration (GPT-4.1 nano, Create + Edit)
- Auto-save logic with version snapshots (backend)
- Freemium request tracking
- Local dictionary fallback

### Week 3: Diff & Key Terms
- Inline diff button + diff view (Edit Mode)
- AI Key Term Spotting (GPT-4o-mini, Study Mode)
- Key terms sidebar UI
- Export key terms list

### Week 4: Polish & Launch Prep
- Note library + search
- 2-screen onboarding
- Polish + bug fixes
- Performance optimization
- E2E testing

### Week 5: Beta Launch
- Deploy to 20-50 nursing students
- Gather feedback for 2 weeks
- Measure success criteria
- Decide Fast-Follow priorities based on data

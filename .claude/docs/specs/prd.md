# NEXLY RN — Product Requirements Document (4-Week MVP - Next.js Stack)

## 1. Product Overview

- **Name:** NEXLY RN — AI-Powered Nursing Education Platform
- **Elevator Pitch:** NEXLY RN is a focused note editor built for nursing students that combines AI-powered autocomplete for medical terminology with nursing-specific slash commands (/template, /formula) to help students capture lecture notes faster and study more effectively
- **Problem:** Nursing students need fast note-taking tools that understand medical terminology and provide quick access to common note structures (care plans, med cards) and critical formulas (MAP, drip rates)—current tools require manual formatting and don't include nursing-specific shortcuts
- **Solution:** NEXLY RN provides:
  1. **AI Autocomplete:** GPT-4.1 nano suggests medical terms as you type, with dictionary fallback for offline use
  2. **Slash Commands:** Type /template for nursing note structures (care plans, med cards, SOAP notes) or /formula for medical calculations (MAP, BMI, dosage)
  3. **Reliable Sync:** Auto-saves every 30 seconds with offline support via IndexedDB → Firestore sync

## 2. Goals & Success Criteria

### Primary Goals (4-Week MVP)

1. **Prove note-taking speed**: Users report "this is faster than [current method]"
2. **Validate slash command adoption**: ≥60% of users use /template or /formula at least once in Week 1
3. **Measure autocomplete effectiveness**: ≥40% acceptance rate for AI suggestions
4. **Validate offline reliability**: Notes sync without data loss after offline editing
5. **Confirm nursing-specific value**: Users report templates/formulas save time vs manual entry

### Non-Goals (Out of Scope for MVP)

- **Deferred Features** (moved from original MVP scope):
  - Study Mode (read-only with AI key term spotting)
  - Inline diff view (changes since last save)
  - Version history UI and snapshots
  - Multiple editing modes (Create/Edit separation)
- **Post-MVP Features**:
  - Shorthand expansion
  - Definition-on-demand
  - Cloze deletion generator
  - Audio recording/transcription
  - Time-based lecture tracking
  - Flashcards/quizzes
  - Clinical documentation for patient care
  - Real-time collaboration
  - Native mobile apps (PWA only for MVP)
  - LMS integrations
  - Spaced repetition/scheduling
  - Full visual concept maps
  - Custom template builder
  - Interactive formula calculator

### Success Criteria (Definition of Done - 4-Week MVP)

_Note: Detailed metrics and decision matrix in Section 10_

After 2 weeks with 50 beta users, validate slash command adoption, AI autocomplete effectiveness, and gather data on note-taking speed improvements and system stability.

## 3. User Stories

### User: Pre-licensure Nursing Students (ADN/BSN)

**Pain Points:**
- Need fast note capture without UI clutter during fast-paced lectures
- Manually formatting care plans, med cards, and assessment notes wastes 5-10 minutes per note
- Forgetting critical formulas (MAP, drip rates, dosage calculations) during exams and clinicals
- AI autocomplete in generic tools doesn't understand nursing/medical terminology
- Losing work when laptop dies or internet cuts out during clinical rotations
- Need offline access to notes during clinical rotations

**As a Pre-licensure Nursing Student, I want to:**

- **Fast Note-Taking**: Capture lecture notes rapidly with AI autocomplete suggesting medical terms as I type, with auto-save so I never lose work even if my laptop dies mid-lecture
- **Nursing-Specific Shortcuts**: Type /template to instantly insert structured note formats (care plan, med card, SOAP note, assessment) instead of manually formatting every time
- **Quick Formula Access**: Type /formula to insert critical medical calculations (MAP, BMI, drip rate, dosage calculation) with placeholders I can fill in
- **Offline Access**: Access and edit my notes offline during clinical rotations, with automatic sync when I reconnect to WiFi
- **PWA Installation**: Install as PWA on my tablet for faster access during clinicals
- **Search and Organization**: Search across all my notes and organize by title, date, or last edited

### User: Advanced Practice Nursing Students (MSN/DNP)

**Pain Points:**
- Same as ADN/BSN students, but with more complex pathophysiology and pharmacology content
- Need AI that understands graduate-level medical terminology and advanced practice concepts

**As an Advanced Practice Nursing Student, I want to:**

- All the same features as ADN/BSN students, with AI autocomplete that understands advanced pathophysiology, pharmacology, and specialty-specific terminology
- Templates for advanced practice note formats (differential diagnosis, treatment plans)

### User: Free Tier Users

**As a Free Tier User, I want to:**

- Use all features with 100 AI autocomplete requests/month to validate the tool before committing financially
- Fall back to local dictionary-based autocomplete when my quota is exceeded so I'm never blocked from taking notes
- Access to all slash commands (/template, /formula) without limits

### User: Pro Tier Users

**As a Pro Tier User, I want to:**

- Unlimited AI autocomplete without quota limits, especially during exam weeks when I'm using the tool most intensively
- All slash commands and features without restrictions

## 4. Critical Edge Cases

**Offline/Connectivity**

- User loses internet → Save to IndexedDB, sync when online
- AI API fails/timeout → Fall back to local dictionary silently
- Session expires during editing → Save locally, prompt re-auth, sync after login

**Quota Management**

- Exceeds free tier quota mid-session → Seamless switch to dictionary fallback with notification
- Pro user monitoring → Track for abuse patterns, alert if unusual usage

**Data Integrity**

- Multiple tabs with same note → Last write wins, warn "Note updated elsewhere"
- Auto-save during active typing → Background save without cursor jump/lag
- Closing browser/tab with unsaved changes → Auto-save prevents data loss (30s interval)

**Performance**

- Notes with 20,000+ words → Editor remains responsive, consider lazy loading for very large notes
- 1,000+ notes in library → Virtualize list, search <500ms
- Slow network connection → Progressive enhancement, offline-first architecture handles gracefully

**AI Behavior**

- AI autocomplete timeout → Fall back to dictionary after 2s
- No autocomplete suggestions available → Fail silently, allow normal typing
- Slash command conflicts → "/" character can still be typed normally if user continues typing without selecting command

## 5. Requirements

### 5.1 Functional Requirements

_Requirements are sorted by priority: P0 (Critical) → P1 (High) → P2 (Medium)_

#### FR-001: AI Autocomplete [P0 - Critical]

_Purpose:_ Reduce typing load and catch missed terminology in real-time

- Model: GPT-4.1 nano
- Trigger after 150ms typing pause
- Cursor context (200 chars)
- Inline gray italicized suggestions
- Keyboard controls:
  - Tab: Accept suggestion
  - Escape: Reject suggestion
  - Right Arrow: Accept partial
- Cancel in-flight requests on new typing
- Log acceptance rate for monitoring
- Active during all note editing
- Performance target: <300ms (p95)
- Quota tracking:
  - **Free tier**: 100 requests/month → dictionary fallback with notification
  - **Pro tier**: Unlimited
  - Monthly reset

#### FR-002: Note Editor [P0 - Critical]

_Purpose:_ Fast, focused note editing with minimal UI distractions

**Edit Mode** (single mode for all note-taking)

- Clean, minimal UI optimized for speed
- AI autocomplete active (GPT-4.1 nano)
- Slash commands active (/template, /formula)
- Auto-save every 30 seconds
- Firestore auto-ID generation for new notes
- Metadata tracking (timestamps, word count)
- Title required before saving
- Rich text formatting (bold, italic, headings, lists)
- Preserve scroll position on save
- No mode switching - simple, consistent experience

#### FR-003: Authentication [P0 - Critical]

**MVP Scope:**
- Email/password authentication
- Email verification required
- Password reset functionality
- Session management (24hr expiry, concurrent devices supported)
- Account lockout after 5 failed attempts
- Preserve unsaved work in IndexedDB during auth flows

**Deferred to Post-MVP:**
- OAuth providers (Google, Microsoft)

**Note:** Email/password is sufficient for MVP; OAuth can be added to reduce friction in future iterations

#### FR-004: Note Management [P0 - Critical]

- List view (no grid view in MVP)
- Sort by: Last Edited, Created date, Title
- Search by title (Dexie full-text search, <500ms for 1,000+ notes)
- Delete with undo (5s window)
- Export formats: Markdown, Plain Text with formatting + metadata
- Click note → Opens in editor
- "New Note" button → Opens blank editor

#### FR-005: Slash Commands [P0 - Critical]

_Purpose:_ Fast access to nursing-specific templates and formulas

**Slash Command System:**
- Trigger: Type "/" character in editor
- Dropdown menu appears with available commands
- Filter as user types (e.g., "/temp" shows template options)
- Keyboard navigation (arrow keys + Enter) and click to select
- Execute command → insert content at cursor position
- Tiptap Suggestion extension for implementation

**/template Command:**
- **Purpose:** Insert structured note formats
- **5 Templates for MVP:**
  1. **Care Plan:** Nursing Diagnosis → Goals → Interventions → Evaluation
  2. **Med Card:** Drug Name → Classification → Action → Dose → Side Effects → Nursing Considerations
  3. **Assessment:** Head-to-toe assessment format
  4. **SOAP Note:** Subjective → Objective → Assessment → Plan
  5. **Pathophysiology:** Disease → Causes → S&S → Dx → Tx → Nursing Implications
- Templates stored as JSON with placeholder fields
- Instant insertion (<10ms)
- Works offline (bundled with app)

**/formula Command:**
- **Purpose:** Insert medical calculation formulas
- **6 Formulas for MVP:**
  1. **MAP** (Mean Arterial Pressure): (SBP + 2×DBP) / 3 | Normal: 70-100 mmHg
  2. **BMI** (Body Mass Index): Weight (kg) / Height (m)² | Normal: 18.5-24.9
  3. **IV Drip Rate:** (Volume × Drop Factor) / Time (min)
  4. **Dosage Calculation:** (Desired / Available) × Quantity
  5. **GCS** (Glasgow Coma Scale): Eye (1-4) + Verbal (1-5) + Motor (1-6) = Total (3-15)
  6. **Fluid Deficit:** Weight (kg) × % Dehydration × 1000 (mL)
- Formulas include normal ranges and clinical context
- Insert with editable placeholder fields
- No calculations performed (user fills in values)
- Works offline

**Performance Targets:**
- Menu display: <50ms after "/" typed
- Content insertion: <10ms
- No AI calls required (pure client-side)
- No quota limits (available to all users)

#### FR-006: Auto-Save [P0 - Critical]

_Purpose:_ Never lose work

**MVP Scope:**
- Auto-saves content every 30 seconds during editing
- IndexedDB-first → Firestore sync
- Exponential backoff retry (1s, 2s, 4s, 8s max)
- Save indicators:
  - "Saving..." during save
  - "Saved" for 2s after success
  - "Offline - Saved locally" when no connection
- Conflict resolution: **Last write wins** with "Note updated elsewhere" warning
- No version history/snapshots in MVP (simple autosave only)

**Deferred to Post-MVP:**
- Version snapshots and history
- Complex conflict resolution UI (Keep Local/Use Remote/View Diff options)
- Restore from previous versions

#### FR-007: Dictionary Fallback [P1 - High]

- 5,000+ nursing terms database
- Load on initialization
- Prefix match (case-insensitive)
- Ranked by relevance
- Response time: <50ms (p95)
- Activates when AI quota exceeded or offline
- Seamless transition (no UI disruption)
- Silent fallback with notification

#### FR-008: Offline/PWA Support [P1 - High]

- IndexedDB for offline access
- Create/edit/read offline (local saves only)
- Disable AI when offline with clear indicator
- Sync on reconnect
- Background Sync API for retry
- Service Worker caching (CSS/JS/fonts/icons)
- Installable (prompt after 2 visits or 5min use)
- Icons (192x192, 512x512)
- Notify on sync complete
- 3G support (1 Mbps minimum)
- Offline-first architecture with background sync

#### FR-009: Onboarding [P2 - Medium]

_Purpose:_ Help students get started quickly

**MVP Scope:**
- Simple welcome screen on first login
- Brief explanation of key features (AI autocomplete, slash commands, autosave)
- Quick demo of /template and /formula commands
- Skippable
- Mark complete in user profile

**Deferred to Post-MVP:**
- Interactive tutorial flow
- Sample note creation demo
- "Try it now" interactive demo
- "Restart Onboarding" option in Settings

**Note:** Focus on getting users into the product quickly; comprehensive onboarding can be added based on user feedback post-launch

#### FR-010: Settings [P2 - Medium]

**MVP Scope:**

**Display Settings**
- Light/dark theme toggle
- Auto-detect system preference
- Display current tier (Free/Pro)

**Deferred to Post-MVP:**

**Account Settings**
- Update email with verification
- Change password
- Delete account with confirmation + 30-day grace period

**Editor Settings**
- Font size adjustment (12-20px)
- Toggle autocomplete on/off
- Adjust auto-save interval (15-60s)

**Note:** MVP focuses on essential settings; additional preferences can be added based on user requests post-launch

### 5.2 Non-Functional Requirements

_Requirements are sorted by priority: P0 (Critical) → P1 (High) → P2 (Medium)_

**NFR-001: Performance [P0 - Critical]**

- AI Autocomplete <300ms (p95) - _Note: Accounts for OpenAI API base latency (200-500ms); local dictionary fallback <50ms_
- Dictionary Fallback <50ms (p95)
- Slash Command Menu Display <50ms (p95)
- Slash Command Content Insertion <10ms (p95)
- Search <500ms for 1k+ notes (p95)
- Editor Load <1s for 20k word note (p95)
- Auto-save <200ms (p95)
- Core Web Vitals: FCP <1.5s, LCP <2.5s, TTI <3.5s, CLS <0.1 (p75)
- Scale: 10k concurrent users, 100k+ registered users
- Max limits: 50k words/note, 10k notes/user, 1k API req/s

**NFR-002: Reliability [P0 - Critical]**

- 99.5% uptime
- Planned maintenance <4hrs/month (2-6 AM EST)
- 11-nines data durability (Firestore)
- Redundant backups across regions
- 30-day soft-delete
- Centralized error logging (Sentry)
- User-friendly errors (no stack traces)
- Graceful degradation
- Exponential backoff retry
- <0.1% error rate

**NFR-003: Security [P0 - Critical]**

- Strong passwords (min 8 chars, 1 uppercase, 1 number, 1 special)
- Bcrypt hashing (≥12 salt rounds)
- Rate limiting (5 attempts/15min)
- JWT (24hr expiry)
- HTTPS-only (TLS 1.3)
- Encrypt in-transit & at-rest (AES-256)
- Firestore row-level security
- Input sanitization (XSS/CSRF protection)
- API keys in env vars
- Rotate OpenAI keys every 90 days
- Validate all inputs

**NFR-004: Privacy [P0 - Critical]**

- NO AI training on user notes
- NO third-party sharing (except OpenAI/Firebase)
- GDPR/CCPA compliant (data export/deletion)
- Anonymized analytics (no PII)
- Educational disclaimer ("not medical advice")
- NO PHI storage

**NFR-005: Usability [P1 - High]**

- Responsive (320px-4K)
- Keyboard navigation
- Visual feedback <100ms
- Consistent design patterns
- Loading indicators >500ms
- WCAG 2.1 Level AA
- Screen reader support (NVDA/JAWS/VoiceOver)
- Keyboard shortcuts
- 4.5:1 contrast ratio
- Alt text for images
- Browser zoom 200%
- Onboarding <2min
- First note <30s post-onboarding
- Contextual tooltips
- Actionable error messages

**NFR-006: Maintainability [P1 - High]**

- TypeScript strict mode
- **>60% test coverage for MVP** (focus on critical paths: auth, save/sync, AI calls)
  - _Post-MVP target: 80% coverage_
- ESLint style guide
- JSDoc for public functions
- SemVer
- Centralized logging
- Track perf metrics
- Health check endpoints
- Real-time status dashboard
- CI/CD pipeline
- Automated rollback
- Dev/staging/prod environments

**Note:** MVP prioritizes testing critical user flows over comprehensive coverage; expand test suite post-launch based on usage patterns

**NFR-007: Compatibility [P1 - High]**

- Latest 2 versions (Chrome, Firefox, Safari, Edge)
- Mobile browsers (Safari iOS 14+, Chrome Android 10+)
- All platforms (desktop/tablet/mobile)
- PWA installable
- 3G support (1 Mbps)
- Offline-first with background sync

**NFR-008: Cost Efficiency [P2 - Medium]**

- Optimize Firestore reads/writes
- Caching
- IndexedDB for local storage
- Request batching
- GPT-4.1 nano for autocomplete
- Debouncing
- Dictionary fallback
- API cost monitoring/alerts

## 6. Technical Stack (Next.js)

### Frontend

- **Next.js 15.1** with App Router
- **React 19.1** with concurrent features
- **TypeScript 5.9.3** with strict mode
- **Tiptap 3.4** editor with extensions:
  - `@tiptap/suggestion` for slash commands
  - Core extensions (heading, bold, italic, lists)
  - Custom extensions for nursing-specific features
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

- **GPT-4.1 nano** for autocomplete during note editing
- Custom 5,000+ nursing terms DB for autocomplete fallback (offline + quota exceeded scenarios)

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

## 7. Architecture Decisions

### 7.1 Offline-First Architecture

**Strategy:** IndexedDB-first with background Firestore sync

**Data Flow:**
```
User Action (Create/Edit/Delete)
    ↓
Save to IndexedDB immediately (<10ms)
    ↓
Update UI with "Saving..." indicator
    ↓
Background sync to Firestore (with retry)
    ↓
Exponential backoff on failure (1s, 2s, 4s, 8s max)
    ↓
Update UI: "Saved" or "Offline - Saved locally"
```

**Conflict Resolution (MVP):**
- **Strategy:** Last write wins with timestamp comparison
- **Detection:** Compare `lastModified` timestamp on sync
- **Warning:** Show "Note updated elsewhere" notification
- **User Action:** Simple acknowledgment (complex merge deferred to post-MVP)

**Deferred to Post-MVP:**
- Three-way merge algorithm
- Manual conflict resolution UI (Keep Local/Use Remote/View Diff)
- Optimistic UI updates with rollback

**Implementation Libraries:**
- Dexie.js for IndexedDB abstraction
- Firebase SDK for Firestore sync
- Background Sync API for retry logic

---

### 7.2 AI Optimization Strategies

**Challenge:** Reduce AI autocomplete latency from 200-500ms to <300ms (p95)

**Optimizations:**

1. **Response Caching**
   ```typescript
   // Cache common completions by context hash
   const cache = new LRU<string, string>(maxSize: 1000);

   if (cache.has(contextHash)) {
     return cache.get(contextHash); // <10ms
   }

   const result = await openai.complete(context);
   cache.set(contextHash, result);
   ```

2. **Request Cancellation**
   - Cancel in-flight requests when user continues typing
   - Prevents stale suggestions from appearing
   - Use AbortController API

3. **Prefetching Strategy**
   - Send request on 150ms typing pause
   - Cache result before user hits Tab
   - If user accepts, suggestion appears instantly

4. **Dictionary Fallback**
   - Trigger immediately if API fails or quota exceeded
   - Prefix match on 5,000+ nursing terms
   - <50ms response time
   - Seamless transition (no UI disruption)

5. **Debouncing**
   - 150ms pause before sending request
   - Balances responsiveness with API cost

**Cost Control:**
- Free tier: 100 requests/month → dictionary fallback with notification
- Pro tier: Unlimited but monitor for abuse
- Track per-user request counts in Firestore

---

### 7.3 Slash Commands Architecture

**Strategy:** Client-side command system using Tiptap Suggestion extension

**Implementation Pattern:**
```typescript
// Slash command configuration
const slashCommands = {
  templates: [
    { id: 'care-plan', name: 'Care Plan', content: '...' },
    { id: 'med-card', name: 'Med Card', content: '...' },
    // ... more templates
  ],
  formulas: [
    { id: 'map', name: 'MAP', formula: '...', content: '...' },
    { id: 'bmi', name: 'BMI', formula: '...', content: '...' },
    // ... more formulas
  ]
}

// Tiptap Suggestion configuration
const SlashCommandsExtension = Extension.create({
  name: 'slashCommands',
  addOptions() {
    return {
      suggestion: {
        char: '/',
        items: ({ query }) => filterCommands(query),
        render: () => renderCommandMenu(),
        command: ({ editor, range, props }) => {
          insertCommandContent(editor, range, props)
        }
      }
    }
  }
})
```

**Data Storage:**
- Templates and formulas stored in JSON files
- Bundled with application (no API calls)
- ~50KB total for all templates + formulas
- Works 100% offline

**Performance:**
- Menu display: <50ms after "/" typed
- Filtering as user types: <10ms
- Content insertion: <10ms
- No quota limits (client-side only)

**User Experience:**
- Type "/" → dropdown appears
- Type to filter (e.g., "/temp" → shows templates)
- Arrow keys to navigate, Enter to select
- Escape to cancel
- Click to select

**Benefits:**
- No AI calls required (cost-free)
- Works offline
- Instant insertion
- Nursing-specific value

---

### 7.4 PWA & Service Worker Strategy

**Goals:**
- Installable on desktop and mobile
- Offline access to notes
- Background sync when reconnected

**Implementation:**
- **next-pwa** for Service Worker generation
- **workbox** for caching strategies
- **Background Sync API** for retry logic

**Caching Strategy:**
```
Static Assets (CSS/JS/fonts): Cache-first
API Routes: Network-first with fallback
Notes Data: IndexedDB (not Service Worker cache)
```

**Offline Behavior:**
- Read/write notes from IndexedDB
- Disable AI features (show "Offline" indicator)
- Queue sync requests for when online
- Notify user when sync completes

**Testing:**
- Test on real devices (Safari iOS, Chrome Android)
- Verify storage quota limits (varies by browser)
- Test offline → online transitions

---

## 8. Privacy & Compliance

**Important:** Legal review required before claiming regulatory compliance

### Data Privacy Principles

- **NO AI training on user notes** - User content is never used to train OpenAI models (verify API agreement)
- **NO third-party data sharing** - Data shared only with essential providers (OpenAI, Firebase/Google Cloud)
- **NO Protected Health Information (PHI)** - System is for educational purposes only, not for patient care documentation
- **Educational Use Disclaimer** - Notes and AI suggestions are "not medical advice" and for educational purposes only

### Regulatory Compliance Requirements

**GDPR Compliance (EU users):**
- Right to access: Data export endpoints required
- Right to erasure: Data deletion endpoints required
- Right to portability: Export in machine-readable format (JSON)
- Consent management: Clear opt-in for AI features
- Data retention policies: Define limits for version snapshots

**CCPA Compliance (California users):**
- Right to know: Disclose what data is collected
- Right to delete: Data deletion on request
- Right to opt-out: Disable AI features if requested
- Non-discrimination: Same service quality for opt-out users

**Required Implementation (MVP):**
- Data export endpoint: `/api/users/export` (returns JSON with all user notes + metadata)
- Data deletion endpoint: `/api/users/delete-account` (soft-delete with 30-day grace period)
- Privacy policy page (template to be reviewed by legal)
- Terms of service (template to be reviewed by legal)
- Cookie consent banner (for analytics)

**Deferred to Post-MVP:**
- GDPR Data Protection Impact Assessment (DPIA)
- CCPA compliance verification audit
- SOC 2 Type II certification (for enterprise customers)

**Disclaimer:** This product is NOT subject to HIPAA or FERPA regulations as it is not used for patient care or institutional educational records. System is for personal study use only.

---

## 9. Monetization Strategy

**Important!** We are adopting a **freemium SaaS model** with a **request-based cap** for autocomplete to avoid heavy token-tracking complexity while still controlling costs

### Free Tier (Baseline Adoption — $0/month)

- Unlimited note-taking
- **AI Autocompletion:** up to 100 requests/month
- After limit: fallback to dictionary-based autocomplete (5,000+ nursing terms DB, no API cost)
- **Slash Commands:** Unlimited access to /template and /formula commands
- Autosave and offline sync
- Local note storage + export (Markdown, Plain Text)
- PWA installation
- Search and organize notes

### Pro Tier (Core Value Unlock — $8.99/month or $79/year)

- Everything in Free, plus:
- **Unlimited AI Autocompletion**
- All slash commands (unlimited)
- Priority support + feature voting
- Early access to new features

### Rationale

- **Free Tier:** Showcases core product value while capping costs via request limits
- **Pro Tier:** Removes caps, adds study accelerators, ensures heavy users upgrade

### Cost & Revenue Projections

**Infrastructure Costs (Monthly, assuming 1,000 active users):**

| Service | Usage | Estimated Cost |
|---------|-------|----------------|
| Vercel Hosting | Pro plan | $20/mo |
| Firebase Firestore | ~500k reads, 200k writes | $15/mo |
| Firebase Auth | Included in free tier | $0 |
| OpenAI API | (see breakdown below) | $40-50/mo |
| Sentry (Error Tracking) | Free tier adequate for MVP | $0 |
| **Total Infrastructure** | | **$75-85/mo** |

**OpenAI API Costs (GPT-4o mini pricing):**
- Autocomplete: ~100 tokens per request × $0.15/1M tokens
- Key Term Spotting: ~3,000 tokens per request × $0.60/1M tokens
- Estimated: $40-50/mo for 1,000 users with quota limits

**Realistic Conversion Assumptions:**
- Industry standard for freemium SaaS: **2-5% conversion**
- Student demographic: price-sensitive, higher churn
- **Conservative estimate: 5-10% free-to-paid conversion**
- **Optimistic estimate: 15-20% conversion** (requires strong product-market fit)

**Break-Even Analysis:**
- Monthly costs: ~$85
- Revenue per Pro user: $8.99/mo
- **Break-even: ~10 paying users (1% of 1,000 users)**
- This is highly achievable

**Revenue Scenario (1,000 active users, 5% conversion):**
- 50 Pro users × $8.99 = $449.50/mo
- Costs: $85/mo
- **Net: $364.50/mo profit margin**

**Churn Risk Factors:**
- Seasonal usage (summer breaks, graduation after 2-4 years)
- Student budget constraints
- **Mitigation:** Annual pricing incentive ($79 vs $107.88), student success stories, NCLEX prep tie-ins

## 10. Success Metrics

### MVP Validation Metrics (2 weeks after beta launch)

**Core Workflow Metrics**

- **Note-Taking Speed:** Avg time from note creation to first save
  - **Green light**: Users report "faster than [current method]"
  - **Yellow light**: Mixed feedback
  - **Red light**: "Too slow" or "No different"
- **Slash Command Adoption:** % of users using /template or /formula at least once in week 1
  - **Green light**: ≥60%
  - **Yellow light**: 40-59%
  - **Red light**: <40% (users don't discover feature)
- **Slash Command Frequency:** Avg slash command uses per active user per week
  - **Green light**: ≥5 uses/week
  - **Yellow light**: 2-4 uses/week
  - **Red light**: <2 uses/week (low engagement)
- **Autocomplete Acceptance:** % of AI suggestions accepted
  - **Green light**: ≥40%
  - **Yellow light**: 25-39%
  - **Red light**: <25% (accuracy too low)
- **Offline Reliability:** % of notes successfully synced after offline editing
  - **Green light**: ≥99%
  - **Yellow light**: 95-98%
  - **Red light**: <95% (data loss issues)
- **Onboarding Completion:** % of users completing welcome screen
  - **Green light**: ≥80%
  - **Yellow light**: 60-79%
  - **Red light**: <60%

### Decision Matrix

**Green Light (Keep Building)**

- ≥60% use slash commands in week 1
- Users report "faster than [current method]"
- ≥40% autocomplete acceptance
- No major sync/data loss issues

**Yellow Light (Iterate)**

- Slash commands discovered but not used frequently
- Autocomplete accuracy needs improvement
- Users confused about when to use features

**Red Light (Pivot)**

- Users don't discover slash commands
- "Why not just use Google Docs?"
- High churn, low engagement
- Data loss or sync issues

### Lagging Metrics (Track but don't optimize for in MVP)

- DAU
- Retention
- Free-to-paid conversion
- Churn

## 11. Challenges & Risks

### 11.1 Technical Risks

#### **Critical Risks (High Impact, High Probability)**

| Risk | Impact | Probability | Mitigation Strategy | Status |
|------|--------|-------------|---------------------|--------|
| **React 19 Library Compatibility** | High - Core dependencies may not support React 19 yet | Medium (40%) | Budget time for dependency debugging, maintain fallback to React 18.x if critical library incompatible | Monitor |
| **AI API Rate Limits** | High - Could block users during peak usage | Medium (50%) | Request OpenAI limit increase 2 weeks pre-launch, implement graceful fallback to dictionary | Mitigate |
| **Offline Sync Complexity** | High - Data loss or corruption | High (60%) | Simplify to "last write wins", defer complex conflict resolution, extensive testing | In Progress |
| **Browser IndexedDB Quota Limits** | Medium - Users run out of storage | Medium (40%) | Monitor storage usage, implement cleanup for old versions, warn at 80% quota | Design |

#### **High Risks (Monitor Closely)**

| Risk | Impact | Probability | Mitigation Strategy | Status |
|------|--------|-------------|---------------------|--------|
| **Medical Terminology Accuracy** | Critical - Incorrect medical terms could mislead students | Medium (30%) | Validate AI suggestions against medical dictionary, user feedback loop, disclaimer "not medical advice" | Design |
| **Slash Command Template Accuracy** | Medium - Incorrect nursing templates could mislead students | Low (15%) | Review templates with nursing faculty, validate against textbooks, user feedback | Design |
| **Firebase Firestore Write Costs** | Medium - Unexpected cost spike | Low (20%) | Implement aggressive caching, batch writes, monitor costs weekly, alerts at $100/mo | Monitor |
| **PWA Installation Friction** | Medium - Low adoption if hard to install | Medium (35%) | Prompt after 2 visits OR 5min use, clear benefits messaging, test on real devices | Design |

#### **Medium Risks (Acceptable with Monitoring)**

| Risk | Impact | Probability | Mitigation Strategy | Status |
|------|--------|-------------|---------------------|--------|
| **Service Worker Cache Staleness** | Low - Users see outdated UI | Low (15%) | Workbox cache invalidation, version-based cache keys, prompt to refresh on update | Standard |
| **Third-Party API Outages** | Medium - OpenAI API downtime | Low (10%) | Dictionary fallback, retry logic, clear error messages | Designed |
| **Safari iOS Storage Quota** | Medium - Safari has stricter limits | Medium (30%) | Test on real Safari iOS, implement storage monitoring, warn users proactively | Test |

---

### 11.2 User Behavior Risks

**Primary Risk:** Users don't discover or adopt slash commands

**Issues:**
- Users unaware of slash command feature (don't type "/")
- Students stick to manual formatting instead of using /template
- Users forget available commands (don't remember /formula exists)
- Resistance to changing workflows (stick to Google Docs/Notion)
- Over-reliance on AI leading to passive note-taking (copying suggestions without understanding)

**Mitigation Strategies:**
- Simple welcome screen demonstrating slash commands (show "/" in action)
- Onboarding highlights /template and /formula with examples
- Track slash command usage metrics in first week to detect issues early
- User interviews (5-10 students) before development to validate usefulness
- Clear value proposition: "Type / for instant templates and formulas"
- In-editor hints/tooltips when users pause (e.g., "Tip: Type / for templates")

**Validation Criteria:**
- ≥60% of users use slash commands in Week 1 (Green light)
- <40% = Yellow light, improve discoverability and onboarding

---

### 11.3 Business Risks

**Competition Risk:**
- Generalist AI note apps (Notion AI, Obsidian with plugins) could add nursing-specific features
- OpenAI could integrate note-taking into ChatGPT
- Established medical education platforms (Osmosis, Picmonic) could add note features

**Mitigation:**
- Focus on nursing-specific terminology and NCLEX relevance
- Build community (student success stories, study tips)
- Faster iteration than large competitors

**API Dependency Risk:**
- OpenAI API pricing increases
- API deprecations or policy changes
- Service reliability issues

**Mitigation:**
- Abstract AI layer (easier to swap providers)
- Dictionary fallback reduces dependency
- Monitor costs weekly with alerts
- Consider alternative providers (Anthropic Claude, local models) for future

**Scope Creep Risk:**
- Users request features outside MVP scope
- Pressure to add flashcards, collaboration, LMS integrations

**Mitigation:**
- Clear communication about MVP priorities
- Public roadmap with "planned for future" items
- User voting on feature priorities (Pro tier benefit)

---

### 11.4 Summary of Mitigation Strategies

**Technical Debt Prevention:**
- Don't rush complex features (version cleanup, conflict resolution)
- Simplify to "good enough" for MVP (line-based diff, last-write-wins)
- Defer optimization until usage patterns are known

**User Validation:**
- 5-10 student interviews before development
- 1-week alpha test (10 users) to validate quotas and workflows
- Continuous feedback loop during beta

**Cost Control:**
- Request-based quotas prevent runaway costs
- Dictionary fallback for offline and over-quota users
- Monitor OpenAI spending daily during beta

**Quality Assurance:**
- 60% test coverage on critical paths
- Real device testing for PWA (Safari iOS, Chrome Android)
- Medical terminology validation against nursing dictionary

---

## 12. Pre-Development Validation

**Purpose:** Validate core assumptions before committing significant development resources

### 12.1 User Research (Week -2 to -1, Before Development)

**Objective:** Validate that the three-mode workflow resonates with target users

**Method:**
- **Participant Recruitment:** 5-10 nursing students (mix of ADN/BSN/MSN programs)
- **Interview Format:** 30-minute semi-structured interviews
- **Tools:** Figma prototype or slides showing three-mode concept

**Key Questions:**
1. "How do you currently take notes during lectures?"
2. "Do you revise your notes after class? If so, how?"
3. "How do you identify what's most important when studying?"
4. "Does separating Create/Edit/Study into distinct modes make sense? Why or why not?"
5. "What would make you switch from your current method to this tool?"

**Success Criteria:**
- ✅ **Green Light:** ≥7 out of 10 students say "This would improve my workflow"
- ⚠️ **Yellow Light:** 4-6 students interested, but confusion about when to use each mode
- 🛑 **Red Light:** <4 students interested OR feedback is "I just want one mode with everything"

**Decision:**
- Green Light → Proceed with development as planned
- Yellow Light → Simplify onboarding, add clearer mode explanations
- Red Light → Pivot to single-mode design with optional AI features

---

### 12.2 Alpha Test (Week 1 After Basic MVP, 1-Week Duration)

**Objective:** Validate AI quota assumptions and identify critical bugs before beta launch

**Participants:**
- 10 nursing students (ideally from user interviews)
- Mix of free and pro tier access (5 each)

**Test Scope:**
- Core note-taking (Create Mode)
- AI autocomplete usage patterns
- Basic editing and saving

**Metrics to Track:**
- Average autocomplete requests per user per day
- Autocomplete acceptance rate
- Notes created per user
- Time to first note creation
- Critical bugs encountered

**Success Criteria:**
- ✅ **Green Light:** No critical bugs, quotas align with usage, positive feedback
- ⚠️ **Yellow Light:** 1-2 critical bugs, quota adjustments needed, mixed feedback
- 🛑 **Red Light:** >3 critical bugs, users hitting quota in first day, negative feedback

**Quota Validation:**
- If users exceed 100 requests in first week → Increase free tier quota to 200/month OR reduce autocomplete trigger sensitivity
- If users use <30 requests → Quota is too generous, could reduce to 75/month for cost savings

---

### 12.3 Beta Launch Readiness Checklist

**Before Launching to 50+ Beta Users:**

**Infrastructure:**
- [ ] Vercel deployment configured and tested
- [ ] Firebase Firestore security rules in production
- [ ] OpenAI API keys rotated and rate limits confirmed
- [ ] Sentry error tracking configured
- [ ] Firebase Analytics configured (anonymized)

**Security:**
- [ ] HTTPS enforced (Vercel automatic)
- [ ] API routes protected with authentication
- [ ] Input sanitization implemented (XSS/CSRF protection)
- [ ] Firestore row-level security rules tested
- [ ] Password requirements enforced (min 8 chars, complexity rules)

**Privacy & Compliance:**
- [ ] Privacy policy page published
- [ ] Terms of service published
- [ ] Data export endpoint tested (`/api/users/export`)
- [ ] Data deletion endpoint tested (`/api/users/delete-account`)
- [ ] "Educational use only" disclaimer added to UI
- [ ] OpenAI API agreement verified (no training on user data)

**Functionality:**
- [ ] Email/password authentication working
- [ ] Password reset flow tested
- [ ] Create Mode + AI autocomplete working
- [ ] Dictionary fallback triggers correctly when quota exceeded
- [ ] Auto-save + IndexedDB → Firestore sync working
- [ ] Offline mode functional (notes accessible when offline)
- [ ] PWA installable on desktop and mobile

**Monitoring:**
- [ ] Error logging working (Sentry capturing errors)
- [ ] Cost monitoring dashboard configured (OpenAI + Firebase)
- [ ] Alert thresholds set ($100/mo infrastructure, 90% quota usage warnings)
- [ ] User analytics tracking mode adoption

**Testing:**
- [ ] 60% test coverage on critical paths achieved
- [ ] E2E tests passing (auth, note CRUD, AI features)
- [ ] Cross-browser testing completed (Chrome, Firefox, Safari, Edge)
- [ ] Mobile browser testing completed (Safari iOS, Chrome Android)

**User Experience:**
- [ ] Welcome screen functional and skippable
- [ ] Dark mode toggle working
- [ ] Loading indicators for AI requests
- [ ] Error messages user-friendly (no stack traces)
- [ ] Performance targets met (autocomplete <300ms, search <500ms)

---

### 12.4 Post-Launch Validation Windows

**Week 1 After Beta Launch:**
- Monitor error rates, cost spikes, user complaints
- Track mode adoption metrics
- Address critical bugs within 24 hours

**Week 2-4 After Beta Launch:**
- Collect qualitative feedback (surveys, interviews)
- Measure success metrics (mode adoption, autocomplete acceptance)
- Identify most-requested features for post-MVP roadmap

**Decision Point (End of Week 4):**
- Green Light: ≥60% mode adoption, positive feedback, low churn → Continue to post-MVP features
- Yellow Light: 40-59% mode adoption, mixed feedback → Iterate on onboarding and mode transitions
- Red Light: <40% mode adoption, high churn, negative feedback → Pivot or major redesign

---

## 13. Post-MVP Roadmap (Deferred Features)

**Not included in MVP, prioritize based on user feedback:**

### Phase 1 (v1.1) - Deferred MVP Features
**Features originally planned for MVP but simplified out:**
- **Study Mode (read-only):** Separate mode for reviewing notes without editing
- **AI Key Term Spotting:** AI-powered identification of exam-relevant terms
- **Inline Diff View:** Show changes since last save with additions/deletions highlighted
- **Version History & Snapshots:** Save and restore previous versions of notes
- **OAuth Authentication:** Google, Microsoft sign-in options

### Phase 2 (v1.2) - Editor Enhancements
- Advanced settings (font size, autocomplete toggle, auto-save interval)
- Export formats (PDF, DOCX with formatting)
- Account management (email change, password change, delete account)
- Full 2-screen interactive onboarding tutorial
- More slash commands (/table, /date, /heading, /list, /divider)
- Custom template builder (let users create their own templates)
- Interactive formula calculator (calculate results automatically)

### Phase 3 (v1.3) - Study Features
- Flashcard generation from notes
- Cloze deletion generator
- Quiz mode with AI-generated questions
- NCLEX-style practice questions
- Spaced repetition scheduling

### Phase 4 (v2.0) - Collaboration & Integrations
- Shared notes and study groups
- Real-time collaboration
- LMS integrations (Canvas, Blackboard)
- Mobile native apps (React Native)

### Phase 5 (v2.5+) - Advanced Features
- Audio recording and transcription
- Visual concept maps
- Shorthand expansion
- Time-based lecture tracking
- Definition-on-demand lookup

**Note:** Post-MVP priorities should be driven by actual user feedback, not assumptions. Track feature requests and implement highest-impact items first.

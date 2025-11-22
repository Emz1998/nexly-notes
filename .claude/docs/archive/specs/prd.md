# NEXLY RN – Product Requirements Document (4-Week MVP)

## 1. Product Overview

- **Name:** NEXLY RN – AI-Powered Nursing Education Platform
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
- Mobile app (desktop/web only for MVP)
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

## 4. User Workflow

### Flow

**New Note:** Sign Up → 2-Screen Onboarding → Create New Note → Create Note Mode (autocomplete, fast capture, minimal UI, auto-saves every 30s) → Save note

**Existing Note:** Open Note → **Edit or Study Dialog** → If Edit: Edit Mode (autocomplete, inline diff button shows changes since last save) → Save | If Study: Study Mode (AI spots key terms, sidebar shows term list) → Export key terms

### Key Screens

1. Note Editor (Tiptap-based)
2. Mode Indicator Bar (shows Create/Edit/Study state)
3. **Edit or Study Dialog** (appears when opening existing note)
4. **Inline Diff View** (Edit Mode only - simple button in toolbar)
5. **Key Terms Sidebar** (Study Mode - shows spotted terms with context)
6. Note Library (basic list view with search)
7. 2-Screen Onboarding (walk through modes)

## 5. Features (4-Week MVP)

### MVP Core Features

#### 1. Three-Mode Architecture

_Core Concept:_ Three distinct modes optimized for different stages of the note-taking and learning workflow

**Create Note Mode** (for new notes)

- Visual indicator: Blue accent
- AI autocomplete active (GPT-4.1 nano)
- Auto-save every 30 seconds
- UI: Minimal - just editor and autocomplete
- Optimized for speed and focus

**Edit Mode** (for existing notes via "Edit" choice)

- Visual indicator: Purple accent
- AI autocomplete active (GPT-4.1 nano)
- **Inline Diff Button** in toolbar: "View Changes Since Last Save"
- Clicking button shows inline diff view (additions, deletions, unchanged)
- Auto-save every 30 seconds

**Study Mode** (for existing notes via "Study" choice)

- Visual indicator: Green accent
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
  - See the Edit or Study dialog
  - Quick tour done in <2 minutes

#### 8. Note Library

_Purpose:_ Find and open notes quickly

- Simple list view (no grid view in MVP)
- Search by title
- Sort by: Last edited, Created date, Title
- Click note → Opens Edit or Study Dialog
- "New Note" button → Opens Create Mode

## 6. Fast-Follow Features (Post-MVP)

### Week 5-6 (After Beta Launch)

- **Templates**: SOAP, SBAR, Care Plans
- **Slash Commands**: Quick template insertion
- **Shorthand Expansion**: AI converts abbreviations to full text
- **Definition-on-Demand**: Highlight text → AI defines term

### Week 7-8 (Based on User Feedback)

- **Cloze Deletion Generator**: AI suggests fill-in-the-blank questions
- **Full Version History UI**: Timeline view with snapshots
- **Side-by-Side Diff Viewer**: Compare any two versions

### Month 2+ (Phase 2)

- Custom template designer
- Advanced diff features (three-way diff, annotations)
- Spaced repetition for cloze cards
- Audio sync
- Flashcards from key terms
- Quiz generation
- Visual concept mapping
- Mobile companion app

### Phase 3 (Q4 2025–Q1 2026)

- LMS integration
- Advanced analytics
- Educator dashboard in production

### Stretch (2026+)

- SimPatient builder
- AR/VR integration
- NCLEX readiness
- Personalized study guidance

## 7. Technical Requirements

### Frontend

- Next.js 15.1.0
- Tiptap 3.4 editor
- Tailwind 4.1 + Shadcn UI
- PWA (Progressive Web App)
- Diff library: diff-match-patch for inline diff

### Backend

- Firebase (Auth, Firestore, Functions, Storage)
- Firestore schema: Add `noteMode` field ("create", "edit", "study")
- Version snapshots stored but no UI in MVP
- Auto-save creates snapshots every 30s

### AI

- **GPT-4.1 nano** for autocomplete (Create + Edit modes)
- **GPT-4o-mini with Structured Outputs** for key term spotting (Study Mode)
- Custom 5,000+ nursing terms DB for autocomplete fallback

### Performance

- Autocomplete: <100ms
- Mode transitions: <50ms
- Dialog display: <100ms
- Inline diff calculation (Edit Mode): <200ms
- Key term spotting: <5s for 3,000-word note

## 8. Monetization Strategy

**Important!** We are adopting a **freemium SaaS model** with a **request-based cap** for autocomplete to avoid heavy token-tracking complexity while still controlling costs

### Free Tier (Baseline Adoption – $0/month)

- Unlimited note-taking in all three modes
- Create Note Mode + Edit Mode + Study Mode
- **AI Autocompletion:** up to 100 requests/month (Create + Edit modes)
- After limit: fallback to dictionary-based autocomplete (5,000+ nursing terms DB, no API cost)
- **AI Key Term Spotting:** up to 10 uses/month
- Version snapshots: Last 5 per note (backend only, no UI in MVP)
- Inline diff view (Edit Mode): Available
- Local note storage + export (PDF/DOCX)

### Pro Tier (Core Value Unlock – $8.99/month or $79/year)

- Everything in Free, plus:
- **Unlimited AI Autocompletion** (Create + Edit modes)
- **Unlimited AI Key Term Spotting** (Study Mode)
- Unlimited version snapshots (backend)
- Early access to Fast-Follow features (templates, expansion, definitions, cloze)
- Advanced diff features when shipped (three-way diff, annotations)
- Export key terms list
- Advanced Note Library search
- Priority support + feature voting

### Team/Educator Tier (Institutional – $19.99/month per seat)

- Everything in Pro, plus:
- Educator Dashboard for validation workflows (future)
- Institution-level note sharing + analytics (future)
- Bulk license management
- Early access to beta features

### Rationale

- **Free Tier:** Showcases core product value while capping costs via request limits
- **Pro Tier:** Removes caps, adds study accelerators, ensures heavy users upgrade
- **Team/Educator Tier:** Supports institutional adoption and credibility-building

## 9. Success Metrics

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

## 10. Challenges & Risks

### Technical

- Autocomplete accuracy in Create and Edit modes
- Inline diff performance with very large notes
- AI accuracy for key term detection (false positives/negatives)
- Latency at scale

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

## 11. Timeline

### 4-Week Build Plan

**Week 1**

- Set up Firebase + auth
- Build basic note editor (Tiptap)
- Mode switching logic + visual indicators
- Edit or Study Dialog

**Week 2**

- AI autocomplete integration (GPT-4.1 nano, Create + Edit)
- Auto-save logic with version snapshots (backend)
- Freemium request tracking

**Week 3**

- Inline diff button + diff view (Edit Mode)
- AI Key Term Spotting (GPT-4o-mini, Study Mode)
- Key terms sidebar UI

**Week 4**

- Note library + search
- 2-screen onboarding
- Polish + bug fixes

**Week 5**

- Beta launch to 20-50 nursing students
- Gather feedback for 2 weeks
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

## 12. What We'll Learn From This MVP

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

## 13. Why This 4-Week MVP Works

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

This validates your core hypothesis without the scope creep. You'll have a working product in a month instead of three months, and you'll learn what actually matters to nursing students.

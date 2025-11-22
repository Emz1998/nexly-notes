# Design Specifications (4-Week MVP)

## 1. Design Principles

**Core Philosophy**
- Mode-specific visual language separates workflows (Create/Edit/Study)
- Minimal UI in Create Mode maximizes focus
- Instant change visibility in Edit Mode builds confidence
- Read-only Study Mode prevents accidental edits during learning
- Accessibility-first with WCAG AA compliance

**Design System Foundation**
- Base unit: 4px spacing grid
- Typography: Inter (UI), JetBrains Mono (code/timestamps)
- Type scale: 12px-36px with 1.2-1.6 line heights
- Border radius: 4px (small), 8px (medium), 12px (large)
- Shadows: sm/md/lg/xl for elevation hierarchy

## 2. Color System

### Mode Colors

- **Create Mode**: Blue (`#3B82F6`) - Fast capture state
- **Edit Mode**: Purple (`#A855F7`) - Revision state with change visibility
- **Study Mode**: Green (`#10B981`) - AI-powered learning state

**Note**: Edit Mode changed from Red to Purple to distinguish from error states

### Semantic Colors

- Success: `#10B981` (validated, saved)
- Warning: `#F59E0B` (quota warnings, unvalidated)
- Error: `#EF4444` (validation errors, failures)
- Info: `#3B82F6` (tips, help)

### Diff Colors (Edit Mode Inline Diff)

- Additions: Green background (`#86EFAC`) with dark green text
- Deletions: Red background (`#FCA5A5`) with dark red text
- Unchanged: Gray background with muted text

**Dark Mode**: CSS variables for all tokens with system preference detection

## 3. Three-Mode Architecture (MVP)

### Mode Selector

- **Type**: 3-way segmented control (not binary switch)
- **Position**: Top bar (desktop), bottom (mobile)
- **Height**: 56px (desktop), 64px (mobile)
- **Visual feedback**: Active segment shows mode color background + white text
- **Animation**: 300ms transitions with smooth color fade
- **Accessibility**: ARIA tablist, keyboard navigation (arrows + Enter)

### Edit or Study Dialog

- **Trigger**: Opening existing note from library
- **Purpose**: Explicit mode selection for intentional workflow
- **Layout**: Modal dialog with two large buttons (Edit | Study)
- **Metadata display**: Created date, last edited, word count
- **Actions**: Click button → Opens note in selected mode
- **Optional**: "Always open in [mode]" checkbox to skip dialog (future enhancement)

### Mode-Specific Behaviors (MVP)

**Create Mode (Blue)**
- Active: Rich text editor, AI autocomplete (GPT-4.1 nano), auto-save
- Disabled: Inline diff button, key terms sidebar
- Purpose: Distraction-free fast capture
- Auto-save: Creates snapshots every 30s (backend only, no UI)

**Edit Mode (Purple)**
- Active: Full editor, AI autocomplete (GPT-4.1 nano), inline diff button
- New element: "View Changes" button in toolbar (opens inline diff view)
- Purpose: Confident revision with instant change visibility
- Diff trigger: Button click shows unsaved changes vs last save

**Study Mode (Green)**
- Active: Read-only editor, key terms sidebar (right), AI key term spotting (GPT-4o-mini)
- Disabled: Text editing, formatting toolbar, autocomplete
- Purpose: AI-powered key term identification without accidental edits
- Features: Spot key terms, click to jump, export list

## 4. Core Components (MVP)

### Rich Text Editor (Tiptap)

- **Container**: Max-width 900px, centered, 32px padding
- **Font**: 18px Inter with 1.6 line-height for readability
- **Placeholder**: "Start typing your notes..." (italic, gray)
- **Selection color**: Mode-specific with 20% opacity
- **States**: Loading (skeleton), empty (placeholder), error (red border), disabled (Study Mode)

**Toolbars**
- Create: Minimal floating toolbar (bold, italic, headings, lists)
- Edit: Full fixed toolbar (all formatting + "View Changes" button)
- Study: Read-only banner with "Switch to Edit Mode" link

### AI Autocomplete Popup

- **Trigger**: 150ms typing pause, 3+ characters typed
- **Active in**: Create Mode + Edit Mode only (disabled in Study Mode)
- **Position**: 4px below cursor
- **Layout**: Max 5 visible suggestions, scrollable
- **Keyboard**: Arrow up/down to select, Enter/Tab to accept, Esc to dismiss
- **Quota**: Switches to dictionary fallback when AI quota exceeded (100/month Free tier)
- **Performance**: <100ms response time (GPT-4.1 nano)

### Inline Diff View (Edit Mode Only)

- **Trigger**: "View Changes Since Last Save" button in Edit Mode toolbar
- **Layout**: Inline highlighting within editor (not side-by-side)
- **Highlighting**: Additions (green), deletions (red), unchanged (gray)
- **Update frequency**: Debounced 500ms as user types
- **Actions**: Keep editing, Discard changes, Save now
- **Performance**: <200ms diff calculation
- **NOT available in Create Mode** (keeps UI minimal for speed)

### Key Terms Sidebar (Study Mode Only)

- **Layout**: Fixed right sidebar (360px desktop, bottom drawer mobile)
- **Trigger**: AI Key Term Spotting button (GPT-4o-mini)
- **Content**: Spotted terms with context snippets, importance level
- **Actions**: Click term to jump to location in note, Export key terms list
- **Performance**: <5s for 3,000-word note
- **Quota**: 10 uses/month (Free tier), unlimited (Pro tier)
- **Structure**:
  - Header with "Key Terms" title and quota display
  - AI action button: "Spot Key Terms"
  - Term list with term name, context snippet, importance badge (High/Medium/Low)
  - Export button

### Edit or Study Dialog

- **Trigger**: Opening any existing note from library
- **Layout**: Modal dialog (600px desktop, 90vw mobile)
- **Content**:
  - Title: "How do you want to open this note?"
  - Note metadata: Created, last edited, word count
  - Two large buttons with icons:
    - "Edit this note" (purple icon)
    - "Study this note" (green icon)
- **Actions**: Click button → Opens note in selected mode
- **Keyboard**: Tab to navigate, Enter to select

## 5. Application Screens (MVP)

### 2-Screen Onboarding

**Screen 1: "Welcome to NEXLY RN"**
- Title: "Three modes for better learning"
- Visual: Three mode cards (Blue/Purple/Green) with icons
- Description: Quick explanation of each mode
- Button: "Next" → Screen 2

**Screen 2: "Try it now"**
- Interactive demo with pre-seeded note
- User types with autocomplete demo
- Shows Edit or Study Dialog
- Quick tour completes in <2 minutes
- Button: "Start creating" → Note library

### Note Library

- **Layout**: Simple list view (no grid view in MVP)
- **Header**: Title, note count, "New Note" button, Search input, Sort dropdown
- **Note items**: Title, preview text (first 100 chars), metadata (last edited, word count), mode badge
- **Actions**: Click note → Opens Edit or Study Dialog
- **Search**: Local full-text search via Dexie
- **Sort**: Last edited (default), Created date, Title
- **NO filters in MVP** (defer to Fast-Follow)

## 6. Responsive Design

### Breakpoints

- Mobile: <640px
- Tablet: 640px-1024px
- Desktop: >1024px

### Adaptations

- **Mode selector**: Horizontal (all), bottom position (mobile), stacked icon+label (mobile)
- **Dialogs**: 90vw (mobile) vs fixed width (desktop)
- **Key terms sidebar**: Bottom drawer (mobile) vs right sidebar (desktop)
- **Touch targets**: 44px minimum (mobile), 48px optimal

## 7. Accessibility (MVP)

### Standards

- WCAG AA contrast ratios (all modes)
- Semantic HTML with ARIA roles
- Keyboard navigation for all interactions
- Focus indicators: 2px outline in mode color with 4px offset
- Screen reader announcements for mode changes, quota warnings

### Keyboard Shortcuts (MVP)

- **Global**: Ctrl/Cmd+S (save), Escape (close modals)
- **Editor**: Ctrl/Cmd+B (bold), Ctrl/Cmd+I (italic)
- **Autocomplete**: Arrow up/down (navigate), Enter/Tab (accept), Esc (dismiss)

## 8. Animation Guidelines

### Transitions

- Duration: 150-300ms for UI state changes
- Easing: cubic-bezier(0.4, 0.0, 0.2, 1)
- Mode transitions: 300ms with smooth color fade
- Modal entry: Fade backdrop (150ms) → Scale content 95%-100% (200ms)
- Modal exit: Scale out (150ms) → Fade backdrop (100ms)

### Micro-interactions

- Button hover: 150ms background color transition
- Autocomplete popup: 100ms fade + 150ms slide
- Feedback flash: 1s highlight animation

## 9. Performance Targets (MVP)

### Critical Metrics

- Autocomplete: <100ms (GPT-4.1 nano)
- Mode transitions: <50ms
- Dialog display: <100ms
- Inline diff: <200ms
- Key term spotting: <5s (GPT-4o-mini)

### Optimization Strategies

- Debounce autocomplete (150ms)
- Debounce diff calculation (500ms)
- Virtual scrolling for long lists (>20 items)
- Lazy load images and non-critical components

## 10. Implementation Notes

### Component Library

- Base: Radix UI primitives
- Patterns: Shadcn UI
- Custom: `/src/components`

### Key Radix Components (MVP)

- Alert Dialog: Edit or Study Dialog, confirmations
- Dialog: Onboarding, settings
- Popover: Tooltips (future)
- Scroll Area: Lists, note library
- Toast: Notifications, quota warnings

### State Management

- Mode state: Zustand store
- Editor state: Tiptap internal
- UI state: React hooks + Zustand

### Styling Approach

- Tailwind utilities for layout and spacing
- CSS variables for theme tokens (colors, mode-specific values)
- Class-variance-authority for component variants
- Dark mode: CSS variables with system preference detection

## 11. Deferred UI Features (Fast-Follow: Week 5-8)

### Week 5-6

- Templates UI (SOAP, SBAR, Care Plans)
- Slash commands menu
- Shorthand expansion before/after view
- Definition popup

### Week 7-8

- Cloze deletion testing interface
- Full version history panel (timeline view)
- Side-by-side diff viewer (compare any two versions)

## 12. MVP Design Checklist

Before beta launch (Week 5):
- ✓ Three-mode architecture with visual indicators (Blue/Purple/Green)
- ✓ Edit or Study Dialog
- ✓ Autocomplete popup (Create + Edit modes)
- ✓ Inline diff view (Edit Mode only)
- ✓ Key terms sidebar (Study Mode only)
- ✓ 2-screen onboarding
- ✓ Note library (simple list view)
- ✓ Mobile responsive
- ✓ WCAG AA compliant
- ✓ Dark mode support

**Focus**: Lean, fast, focused. Ship the minimum UI needed to validate the three-mode hypothesis.

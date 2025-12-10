# UX Specifications - NEXLY RN

## 1. Design Philosophy

### Core Principles

1. **Speed-First**: Every interaction optimized for fast note capture during lectures
2. **Focus**: Minimal chrome, maximum content area
3. **Discoverable**: Features reveal themselves at the right moment
4. **Trustworthy**: Clear feedback for save/sync status builds confidence
5. **Accessible**: Usable by everyone, WCAG AA compliant

### Design Personality

- **Clean**: Generous whitespace, clear hierarchy
- **Professional**: Serious tool for serious students
- **Helpful**: Guides without being intrusive
- **Reliable**: Consistent patterns throughout

---

## 2. Visual Design System

### Typography

| Element         | Size | Weight   | Line Height |
| --------------- | ---- | -------- | ----------- |
| Page Title      | 30px | Bold     | 1.2         |
| Section Heading | 24px | Semibold | 1.3         |
| Card Title      | 18px | Semibold | 1.4         |
| Body Text       | 16px | Regular  | 1.5         |
| Editor Content  | 18px | Regular  | 1.6         |
| Small/Caption   | 14px | Regular  | 1.4         |
| Label           | 12px | Medium   | 1.3         |

**Font Stack**: System sans-serif (SF Pro, Segoe UI, Roboto)

### Color Palette

**Brand**

- Primary Blue: `#3B82F6`
- Primary Hover: `#2563EB`

**Neutral (Light)**

- Background: `#FFFFFF`
- Surface: `#F8FAFC`
- Border: `#E2E8F0`
- Text Primary: `#0F172A`
- Text Secondary: `#64748B`
- Text Muted: `#94A3B8`

**Neutral (Dark)**

- Background: `#0F172A`
- Surface: `#1E293B`
- Border: `#334155`
- Text Primary: `#F8FAFC`
- Text Secondary: `#94A3B8`
- Text Muted: `#64748B`

**Status**

- Success: `#10B981`
- Warning: `#F59E0B`
- Error: `#EF4444`
- Info: `#3B82F6`

### Spacing Scale

Based on 4px grid:

- `xs`: 4px
- `sm`: 8px
- `md`: 16px
- `lg`: 24px
- `xl`: 32px
- `2xl`: 48px
- `3xl`: 64px

### Border Radius

- Tight: 4px (buttons, inputs)
- Medium: 6px (cards, dropdowns)
- Large: 8px (modals, panels)
- Full: 9999px (pills, avatars)

### Elevation

- Level 1: `0 1px 2px rgba(0,0,0,0.05)` — Cards, dropdowns
- Level 2: `0 4px 6px rgba(0,0,0,0.1)` — Popovers, menus
- Level 3: `0 10px 15px rgba(0,0,0,0.1)` — Modals, dialogs

---

## 3. User Journeys

### Journey 1: First-Time User

```
Landing → Sign Up → Onboarding (2 screens) → Empty Notes Library → Create First Note
```

**Emotional Goal**: Feel confident and excited to start taking notes

**Key Moments**:

1. Sign up is fast (email + password only)
2. Onboarding introduces AI autocomplete and slash commands
3. Interactive demo lets user try `/template` before committing
4. Empty state encourages immediate action

### Journey 2: Lecture Note-Taking

```
Open App → New Note → Type with AI Autocomplete → Use /template → Auto-Save → Close
```

**Emotional Goal**: Feel fast and supported, never miss information

**Key Moments**:

1. New note opens instantly with cursor ready
2. AI suggestions appear as user types medical terms
3. Slash commands insert templates without breaking flow
4. Save indicator provides peace of mind
5. Closing is frictionless (auto-saved)

### Journey 3: Review & Organize

```
Open Notes Library → Search/Filter → Open Note → Edit → Categorize → Return to Library
```

**Emotional Goal**: Feel organized and in control

**Key Moments**:

1. Notes are easy to find via search and categories
2. Note preview helps identify content quickly
3. Category assignment is quick (dropdown in toolbar)
4. Changes auto-save without manual action

### Journey 4: Offline Clinical Rotation

```
Open Note (offline) → Edit → See "Offline" indicator → Reconnect → Auto-Sync → Confirmation
```

**Emotional Goal**: Feel secure that work won't be lost

**Key Moments**:

1. Offline indicator is visible but not alarming
2. All features work normally offline
3. Sync happens automatically when back online
4. Success confirmation builds trust

---

## 4. Screen Designs

### 4.1 Authentication

#### Login Screen

**Layout**

- Centered card (max-width 400px)
- App logo at top
- Form fields vertically stacked
- Full-width buttons

**Content**

- Headline: "Welcome back"
- Fields: Email, Password (with show/hide)
- Primary CTA: "Log in"
- Secondary links: "Forgot password?", "Sign up"

**States**

- Default: Clean form
- Loading: Button shows spinner, fields disabled
- Error: Inline message below field, red border

#### Sign Up Screen

**Layout**: Same as login

**Content**

- Headline: "Create your account"
- Fields: Name, Email, Password, Confirm Password
- Password requirements shown as checklist below field
- Primary CTA: "Create account"

**Password Requirements Display**

- 8+ characters ✓/✗
- 1 uppercase ✓/✗
- 1 lowercase ✓/✗
- 1 number ✓/✗
- 1 special character ✓/✗

### 4.2 Onboarding

#### Screen 1: Welcome

**Layout**

- Centered content (max-width 800px)
- Large headline
- Two feature cards side-by-side (stack on mobile)

**Content**

- Headline: "Welcome to NEXLY RN"
- Subheadline: "Type faster with AI autocomplete and nursing templates"
- Card 1: AI Autocomplete (sparkle icon)
- Card 2: Slash Commands (slash icon)
- CTA: "Try it now"

#### Screen 2: Interactive Demo

**Layout**

- Centered content
- Embedded mini-editor
- Instructional text below

**Content**

- Headline: "Try typing /template"
- Mini-editor with sample text
- Instruction: "Type / to see available commands"
- CTA: "Start creating" (appears after successful demo)

**Interaction**

- User types "/" in demo editor
- Slash menu appears
- User selects template
- Template inserts with celebration animation
- CTA button becomes enabled

### 4.3 Notes Library

**Layout**

- Full-width page
- Header with title and actions
- Filter bar below header
- Note cards in vertical list

**Header**

- Left: "My Notes" title + count badge
- Right: Search input + "New Note" button

**Filter Bar**

- Category filter (dropdown or chips)
- Sort dropdown (Last edited, Created, Title)

**Note Card**

- Title (bold, truncate 2 lines)
- Content preview (first 100 chars, muted)
- Bottom row: Category badge | Date | Word count
- Sync status dot (corner)

**Card Interactions**

- Hover: Slight lift + shadow
- Click: Opens note in editor
- Right-click: Context menu

**Context Menu Options**

- Rename
- Duplicate
- Export (Markdown, Plain Text)
- Delete

**Empty State**

- Centered illustration (notepad icon)
- "No notes yet"
- "Create your first note to get started"
- "Create Note" button

### 4.4 Note Editor

**Layout Structure**

```
┌─────────────────────────────────────┐
│ Navbar                              │
├─────────────────────────────────────┤
│ Toolbar                             │
├─────────────────────────────────────┤
│                                     │
│         Editor Content              │
│         (max-width 900px)           │
│         (centered)                  │
│                                     │
└─────────────────────────────────────┘
```

**Navbar**

- Left: Back arrow + "Notes" breadcrumb
- Center: (empty)
- Right: User avatar menu

**Toolbar**

- Left section:
  - Note title (inline editable)
  - Category dropdown
- Center section:
  - Formatting buttons (Bold, Italic, Heading, List, Link)
- Right section:
  - AI quota badge ("85 AI" or "Dictionary")
  - Sync status ("Synced" / "Offline" / "Syncing...")
  - Save status ("Saved 2m ago")

**Editor Area**

- Max-width 900px, centered
- 32px horizontal padding (16px on mobile)
- Placeholder: "Start typing your notes... Type / for commands"

### 4.5 Slash Command Menu

**Appearance**

- Floating menu below cursor
- Width: 320px
- Max height: 400px (scrollable)
- Subtle shadow and border

**Menu Structure**

```
Commands
─────────────────
📄 /template
   Care Plan
   Medication Card
   SOAP Note
   Head-to-Toe Assessment
   Pathophysiology Outline
─────────────────
🔢 /formula
   MAP (Mean Arterial Pressure)
   BMI (Body Mass Index)
   IV Drip Rate
   Dosage Calculation
   Glasgow Coma Scale
   Fluid Deficit
```

**Item Design**

- Icon + Label + Description (muted)
- 44px height
- Hover: Light blue background
- Selected (keyboard): Darker blue background

**Behavior**

- Opens when user types "/"
- Filters as user continues typing
- Arrow keys navigate
- Enter/click selects
- Escape dismisses

### 4.6 AI Autocomplete Popup

**Appearance**

- Floating below cursor
- Width: 300px
- 5 suggestions max visible

**Suggestion Item**

- Medical term (medium weight)
- Source badge: "AI" (blue) or "Dictionary" (gray)
- 40px height

**Behavior**

- Appears after brief typing pause
- Shows when typing medical terms
- Arrow keys navigate
- Tab/Enter accepts
- Escape dismisses

**Fallback States**

- Normal: "AI" badge, blue accent
- Over quota: "Dictionary" badge, gray accent
- Offline: "Dictionary" badge, gray accent
- Loading: Spinner + "Getting suggestions..."

### 4.7 Trash Folder

**Header**

- Title: "Trash"
- Subtitle: "Items are permanently deleted after 30 days"
- Action: "Empty Trash" (destructive outline button)

**Trash Item Card**

- Same as note card but muted appearance
- "Deleted X days ago" instead of "Last edited"
- Actions: "Restore" (primary) | "Delete Forever" (destructive)

**Empty State**

- Empty trash bin illustration
- "Trash is empty"
- "Deleted notes will appear here"

### 4.8 Settings

**Layout**

- Sidebar navigation (desktop)
- Tab navigation (mobile)
- Content area with sections

**Sections**

1. **Account**

   - Email (read-only with copy)
   - Display name (editable)
   - "Change password" link

2. **Subscription**

   - Current tier badge
   - Quota usage bar ("X of 100 AI requests")
   - "Upgrade to Pro" button (free) or "Manage Subscription" (pro)

3. **Preferences**

   - Theme: Light / Dark / System (radio or segmented)
   - Auto-save: Toggle (on by default)

4. **Data**
   - "Export all notes" button
   - "Delete account" button (destructive)

### 4.9 Upgrade Modal

**Trigger**: Quota badge click (free tier) or "Upgrade" button

**Content**

- Header: "Upgrade to Pro"
- Feature comparison table
- Pricing: $8.99/month or $79/year (save 27%)
- CTA: "Upgrade Now"
- Footer: "Cancel anytime"

**Comparison Table**
| Feature | Free | Pro |
|---------|------|-----|
| AI Autocomplete | 100/month | Unlimited |
| Templates | ✓ | ✓ |
| Formulas | ✓ | ✓ |
| Offline Sync | ✓ | ✓ |

---

## 5. Component Behaviors

### Buttons

| Type        | Use Case            | Appearance                  |
| ----------- | ------------------- | --------------------------- |
| Primary     | Main actions        | Blue background, white text |
| Secondary   | Alternative actions | Gray background, dark text  |
| Outline     | Tertiary actions    | Border only, no fill        |
| Ghost       | Subtle actions      | No border, no fill          |
| Destructive | Dangerous actions   | Red background/border       |

**States**: Default → Hover → Active → Disabled

### Form Inputs

- Height: 40px
- Border: 1px gray, 4px radius
- Focus: Blue border, subtle shadow
- Error: Red border, error message below
- Disabled: Gray background, muted text

### Dropdowns

- Same height as inputs
- Chevron icon on right
- Menu appears below with shadow
- Selected item shows checkmark

### Tooltips

- Appear on hover (desktop) or long-press (mobile)
- Dark background, white text
- Small arrow pointing to trigger
- Max-width 200px

### Toast Notifications

- Position: Bottom-center
- Auto-dismiss: 4 seconds
- Types: Success (green), Error (red), Info (blue), Warning (amber)
- Dismissible with X button

---

## 6. Interaction Patterns

### Auto-Save

**User Perception**: "I never have to think about saving"

**Visual Feedback**:

- Typing: No indicator change
- Saving: "Saving..." appears briefly
- Saved: "Saved just now" → "Saved 1m ago" → "Saved 5m ago"

### Sync Status

**States & Messaging**:

- Online + Synced: Green dot + "Synced"
- Syncing: Blue spinner + "Syncing..."
- Offline: Amber dot + "Offline" (tooltip: "Changes will sync when online")
- Sync Error: Red dot + "Sync error" (clickable to retry)

### AI Quota

**Display**: Badge showing remaining count or "Dictionary"

**Behavior**:

- Updates after each AI request
- Color changes: Green (>50) → Amber (10-50) → Red (<10) → Gray (0)
- Click opens upgrade modal (free tier only)

### Navigation

**Back Button Behavior**:

- Unsaved changes: Save first, then navigate
- Mid-save: Wait for save, then navigate
- No changes: Navigate immediately

---

## 7. Responsive Behavior

### Breakpoints

| Name    | Width      | Layout Changes               |
| ------- | ---------- | ---------------------------- |
| Mobile  | < 640px    | Single column, bottom sheets |
| Tablet  | 640-1023px | Adjusted spacing             |
| Desktop | 1024px+    | Full layout                  |

### Mobile Adaptations

**Navbar**

- Hamburger menu instead of full nav
- Condensed logo

**Editor Toolbar**

- Formatting buttons in overflow menu
- Essential items only visible

**Notes Library**

- Search expands on tap
- Filters in bottom sheet

**Slash Command Menu**

- Full-width bottom sheet
- Larger touch targets (52px items)

**Settings**

- Tab navigation instead of sidebar

---

## 8. Accessibility

### Keyboard Navigation

- All interactive elements focusable via Tab
- Logical tab order (left-to-right, top-to-bottom)
- Visible focus indicators on all elements
- Escape closes modals/menus

### Screen Reader Support

- All images have alt text
- Icons have aria-labels
- Form inputs have associated labels
- Status changes announced via aria-live
- Headings create proper document outline

### Visual Accessibility

- Minimum 4.5:1 contrast ratio for text
- Focus indicators never removed
- Color not sole indicator of state
- Support for 200% browser zoom

### Motor Accessibility

- Touch targets minimum 44x44px
- Adequate spacing between interactive elements
- No time-limited interactions (except auto-dismiss toasts)

---

## 9. Motion & Animation

### Principles

1. **Purposeful**: Animation serves UX, not decoration
2. **Quick**: Most transitions under 300ms
3. **Subtle**: Enhance without distracting
4. **Respectful**: Honor `prefers-reduced-motion`

### Timing

- Micro-interactions: 100-150ms
- Component transitions: 200-300ms
- Page transitions: 300-400ms

### Key Animations

**Button Press**: Scale to 98% instantly

**Card Hover**: Lift shadow + scale 102% over 200ms

**Modal Entry**: Fade backdrop (150ms) + scale content 95%→100% (200ms)

**Menu Open**: Fade + slide up (150ms)

**Save Confirmation**: Brief checkmark pulse

**Sync Spinner**: Continuous rotation

### Reduced Motion

When `prefers-reduced-motion` is enabled:

- Replace animations with instant state changes
- Keep essential feedback (save confirmation)
- Remove decorative motion

---

## 10. Empty & Error States

### Empty States

| Screen          | Illustration | Headline                 | Subtext                                               | Action        |
| --------------- | ------------ | ------------------------ | ----------------------------------------------------- | ------------- |
| Notes Library   | Notepad      | "No notes yet"           | "Create your first note to get started"               | "Create Note" |
| Search Results  | Magnifier    | "No results"             | "Try a different search term"                         | —             |
| Trash           | Empty bin    | "Trash is empty"         | "Deleted notes will appear here"                      | —             |
| Category Filter | Folder       | "No notes in [category]" | "Notes you categorize as [category] will appear here" | —             |

### Error States

| Error           | Message                                                      | Recovery Action    |
| --------------- | ------------------------------------------------------------ | ------------------ |
| Network offline | "You're offline. Changes will sync when you're back online." | Automatic          |
| Save failed     | "Couldn't save. Retrying..."                                 | Automatic retry    |
| AI unavailable  | "AI unavailable. Using dictionary suggestions."              | Automatic fallback |
| Session expired | "Session expired. Please log in again."                      | Redirect to login  |
| Note not found  | "Note not found. It may have been deleted."                  | Return to library  |

---

## 11. Design Checklist

### MVP Completion Criteria

**Core Experience**

- [ ] Clean, focused editor
- [ ] AI autocomplete with dictionary fallback
- [ ] Slash command menu for templates/formulas
- [ ] Auto-save with visual feedback
- [ ] Offline indicator and sync status

**Note Management**

- [ ] Notes library with cards
- [ ] Search and category filtering
- [ ] Note CRUD (create, read, update, delete)
- [ ] Trash with 30-day recovery

**User Management**

- [ ] Authentication (login, signup, reset)
- [ ] Settings page
- [ ] Subscription display and upgrade flow

**Polish**

- [ ] Onboarding flow (2 screens)
- [ ] Loading states (skeletons)
- [ ] Error states and recovery
- [ ] Empty states with guidance
- [ ] Dark mode
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Keyboard navigation
- [ ] Screen reader compatibility

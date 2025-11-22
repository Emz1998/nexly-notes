# UI/UX Specifications - NEXLY RN (4-Week MVP)

## 1. Design Principles

**Core Philosophy**

- Mode-specific visual language separates workflows (Create/Edit/Study)
- Minimal UI in Create Mode maximizes focus
- Instant change visibility in Edit Mode builds confidence
- Read-only Study Mode prevents accidental edits during learning
- Accessibility-first with WCAG AA compliance

**Design System Foundation**

- Base unit: 4px spacing grid
- Typography: Sans-serif (default), Monospace (code/timestamps)
- Type scale: 14px to 36px with appropriate line heights
- Border radius: 2px (tight), 6px (medium), 8px (loose)
- Elevation: Subtle shadows for layering and depth

## 2. Color System

### Mode Colors

**Create Mode - Blue**
- Primary: `#3B82F6` (HSL: 217 91% 60%)
- Foreground: White
- Use: Active state, accents, focus indicators

**Edit Mode - Purple**
- Primary: `#A855F7` (HSL: 271 81% 68%)
- Foreground: White
- Use: Active state, accents, diff highlights

**Study Mode - Green**
- Primary: `#10B981` (HSL: 160 84% 39%)
- Foreground: White
- Use: Active state, accents, term importance

### Semantic Colors

**Light Theme**
- Background: White
- Foreground: Near-black (`#0F172A`)
- Card: White
- Border: Light gray (`#E2E8F0`)
- Muted: Light gray backgrounds for subtle elements
- Destructive: Red for dangerous actions

**Dark Theme**
- Background: Dark navy (`#0F172A`)
- Foreground: Off-white
- Card: Slightly lighter navy
- Border: Dark gray
- Muted: Dark gray backgrounds
- Destructive: Lighter red for visibility

### Diff Colors (Edit Mode)

**Additions**
- Light: Light green background (`#86EFAC`), dark green text
- Dark: Dark green background, light green text
- Styling: Background highlight

**Deletions**
- Light: Light red background (`#FCA5A5`), dark red text
- Dark: Dark red background, light red text
- Styling: Background highlight + strikethrough

**Unchanged**
- Muted gray text, no special background

## 3. Three-Mode Architecture

### Mode Selector

**Visual Design**
- Type: 3-way segmented control (horizontal pills)
- Position: Top bar (desktop), bottom navigation (mobile)
- Container: 56px height, 8px border radius, muted background
- Buttons: 40px height, equal width, 8px gap
- Active state: Mode-specific color background, white text, subtle shadow
- Inactive state: Transparent background, muted text
- Hover: Subtle accent background
- Animation: 300ms smooth color transition

**Behavior**
- Single selection only
- Keyboard navigation with arrow keys
- Tab focus visible with ring indicator
- Click or Enter to switch modes

### Edit or Study Dialog

**Visual Design**
- Trigger: When user opens an existing note from library
- Layout: Modal dialog, centered
  - Desktop: 600px max-width
  - Mobile: 90vw width
- Header: "How do you want to open this note?"
- Metadata: Created date, last edited date, word count (muted text, 14px)
- Actions: Two large buttons side-by-side
  - Height: 96px each
  - Layout: Icon above label (vertical stack)
  - Edit: Purple background, pencil icon
  - Study: Green background, book icon
  - Hover: Slight darkening (90% opacity)
- Backdrop: Semi-transparent overlay (60% black)

**Behavior**
- Auto-shows when clicking note card from library
- Cannot be dismissed without selecting a mode
- Keyboard: Tab to navigate, Enter to select
- Selection immediately opens note in chosen mode

## 4. Core Components

### Rich Text Editor

**Visual Design**
- Container: Max-width 900px, horizontally centered
- Padding: 32px horizontal, responsive vertical
- Font: 18px size, 1.6 line-height, sans-serif
- Placeholder: "Start typing your notes..." (italic, muted color)
- Selection highlight: Mode-specific color at 20% opacity
- Prose styling: Standard heading hierarchy, list indentation

**Mode-Specific States**
- Create: Editable, blue accent color
- Edit: Editable, purple accent color
- Study: Read-only, green accent color, cursor shows "not allowed"

**States**
- Empty: Placeholder visible
- Loading: Skeleton animation with shimmer
- Disabled: Grayed out, no cursor

### AI Autocomplete Popup

**Visual Design**
- Width: 300px
- Position: 4px below cursor, aligned left
- Max items: 5 visible, scrollable for more
- Item height: 40px each
- Border: Subtle border, 6px radius
- Background: Card color with slight shadow
- Selected item: Accent background highlight
- Font: 14px, medium weight

**Behavior**
- Trigger: After 150ms pause in typing, minimum 3 characters
- Active in: Create and Edit modes only
- Keyboard: Arrow keys to navigate, Enter/Tab to accept, Escape to dismiss
- Mouse: Hover highlights, click to accept
- Disappears: On selection, focus loss, or Escape

**Performance**
- Target: <100ms to display suggestions
- Debounce: 150ms typing pause before triggering

### Inline Diff View (Edit Mode)

**Visual Design**
- Trigger: "View Changes" button in toolbar
- Layout: Full-width panel within editor
- Header: Eye icon + "Changes since last save" label
- Content area:
  - Bordered container, 8px radius
  - 16px padding
  - Line-by-line diff display
  - Green highlight for additions
  - Red highlight + strikethrough for deletions
  - Gray for unchanged text
- Actions:
  - "Save now" button (primary, with save icon)
  - "Discard changes" button (outline, with trash icon)
  - 8px gap between buttons

**Behavior**
- Shows line-by-line comparison of current vs. last saved version
- Debounced 500ms to avoid excessive recalculation
- Target: <200ms to calculate and display diff
- Scrollable if content is long

### Key Terms Sidebar (Study Mode)

**Visual Design**
- Desktop: Fixed right sidebar, 360px width
- Mobile: Bottom sheet drawer, 70vh height
- Background: Card color
- Border: Left border on desktop, top border on mobile
- Padding: 16px all sides

**Header**
- Title: "Key Terms" (semibold, 16px)
- Quota badge: "X remaining" (secondary badge, right-aligned)

**Action Button**
- Full width
- Text: "Spot Key Terms" with sparkle icon
- Style: Primary button with mode color

**Term List**
- Scrollable area: calc(100vh - 200px)
- Items: Card-style buttons with:
  - 12px padding
  - Border with rounded corners
  - Hover: Subtle accent background
  - Layout: Term name (bold) + importance badge (right)
  - Context snippet below (muted text, 14px)
  - 12px gap between items

**Importance Badges**
- High: Red/destructive variant
- Medium: Default variant
- Low: Secondary/muted variant

**Export Button**
- Full width, outline style
- Text: "Export key terms" with download icon
- Only visible when terms exist

**Behavior**
- Click term to jump to position in note
- Smooth scroll animation to term location
- Highlight term briefly after jump

## 5. Application Screens

### 2-Screen Onboarding

**Screen 1: Mode Introduction**
- Container: Max-width 1024px, centered, 64px vertical padding
- Headline: "Welcome to NEXLY RN" (36px, bold, centered)
- Subheadline: "Three modes for better learning" (20px, muted, centered)
- Cards: 3-column grid (responsive stack on mobile)
  - Each card: 24px padding, centered content
  - Mode icon: 48px square, mode color background, 8px radius
  - Mode name: Semibold, 16px
  - Description: 14px, muted color
  - 24px gap between cards
- CTA: Full-width "Next" button (large size)

**Screen 2: Interactive Demo**
- Headline: "Try it now" (30px, bold, centered)
- Content: Pre-seeded note with sample content for user to interact with
- CTA: Full-width "Start creating" button (large size)

### Note Library

**Header Section**
- Title: "My Notes" (30px, bold)
- Count: "X notes" (muted text below title)
- Action: "New Note" button (primary, with plus icon, right-aligned)

**Search & Filter Bar**
- Search input: Full width with magnifying glass icon, placeholder "Search notes..."
- Sort dropdown: 180px width, options for "Last edited", "Created date", "Title"
- 16px gap between elements

**Note Cards Grid**
- Layout: Vertical list, 16px gap
- Each card:
  - Padding: 16px
  - Border: Subtle, rounded corners
  - Hover: Elevated shadow, subtle scale
  - Title: Bold, 18px
  - Metadata: Course code, date, word count (muted, 14px)
  - Tags: Chips/badges if present

**Behavior**
- Click card → Shows Edit/Study Dialog
- Keyboard: Tab navigation, Enter to open
- Loading: Skeleton cards during fetch

## 6. Responsive Design

### Breakpoints

- Mobile: < 640px
- Tablet: 640px - 1023px
- Desktop: 1024px+
- Large Desktop: 1280px+

### Responsive Adaptations

**Mode Selector**
- Desktop: Horizontal in top bar
- Mobile: Horizontal in bottom navigation bar (sticky)

**Key Terms Sidebar**
- Desktop: Fixed right sidebar (360px)
- Mobile: Bottom drawer/sheet (70vh height)

**Onboarding Cards**
- Desktop: 3-column grid
- Tablet: 3-column grid (smaller gaps)
- Mobile: Single column stack

**Note Library**
- Desktop: Full feature set
- Mobile: Simplified cards, bottom sheet for filters

**Editor**
- Desktop: Full width up to 900px
- Mobile: Reduced horizontal padding (16px vs 32px)

## 7. Accessibility

### Keyboard Navigation

**Shortcuts**
- Cmd/Ctrl + S: Save note
- Cmd/Ctrl + B: Bold text
- Cmd/Ctrl + I: Italic text
- Escape: Dismiss popups/dialogs
- Tab: Navigate interactive elements
- Enter: Activate focused element
- Arrow keys: Navigate lists and suggestions

**Focus Indicators**
- Visible ring around all interactive elements
- Mode-specific color for focus ring
- 2px width, 4px offset
- Never remove focus indicators

### ARIA Attributes

**Mode Selector**
- Role: tablist
- Each button: role="tab", aria-selected, aria-controls

**Autocomplete**
- Role: listbox for suggestions
- Role: option for each item
- aria-activedescendant for keyboard selection

**Dialogs**
- Role: dialog
- aria-labelledby for title
- aria-describedby for description
- Focus trap within dialog

**Key Terms**
- Role: list for term container
- Role: listitem for each term
- Proper heading hierarchy

### Screen Reader Support

- All icons have text labels or aria-label
- All images have alt text
- Loading states announced
- Error messages announced
- Form inputs properly labeled

## 8. Animation & Motion

### Transition Timing

- Instant: < 50ms (mode switches, immediate feedback)
- Quick: 150ms (fades, small UI changes)
- Standard: 300ms (mode colors, larger transitions)
- Slow: 500ms (page transitions, complex animations)

### Animation Principles

**Mode Transitions**
- Color changes: 300ms smooth transition
- No layout shift during transition
- Text remains readable throughout

**Modal Animations**
- Fade in backdrop: 150ms
- Scale + fade content: 200ms
- Exit: Same timing in reverse
- Easing: ease-out for entry, ease-in for exit

**Micro-interactions**
- Button hover: Scale 105% over 150ms
- Button press: Scale 95% instantly
- Card hover: Lift shadow over 200ms
- Focus ring: Fade in 100ms

**Performance Considerations**
- Use CSS transforms (translate, scale) over position changes
- Avoid animating layout properties (width, height, padding)
- Prefer opacity over visibility for fades
- Respect `prefers-reduced-motion` setting

## 9. Dark Mode

### Theme Switching

**Controls**
- Toggle button in top navigation
- Icon: Sun (light) / Moon (dark)
- Smooth icon transition (rotate + scale)
- Persists choice to local storage

**System Integration**
- Default: Follow system preference
- Options: Light, Dark, System
- No flash of wrong theme on page load

**Color Adaptations**
- Mode colors remain consistent (same hues)
- Background/foreground inverted
- Reduced contrast in dark mode to prevent eye strain
- Adjusted shadows (lighter, more subtle)

## 10. Performance Targets

### Critical Metrics

- **Autocomplete response**: < 100ms
- **Mode transition**: < 50ms (instant feel)
- **Dialog display**: < 100ms
- **Diff calculation**: < 200ms
- **Key term spotting**: < 5s (AI processing)
- **Initial page load**: < 2.5s (LCP)
- **Time to interactive**: < 3.5s

### Optimization Strategies

- Lazy load editor component
- Debounce autocomplete (150ms)
- Debounce diff calculation (500ms)
- Virtual scrolling for >50 terms
- Server-side initial render
- Progressive enhancement
- Skeleton loading states

## 11. Design Checklist (MVP)

**Before Beta Launch (Week 5)**

- [ ] Three-mode architecture with clear visual indicators
- [ ] Edit or Study Dialog with mode selection
- [ ] Autocomplete popup in Create/Edit modes
- [ ] Inline diff view in Edit Mode
- [ ] Key terms sidebar in Study Mode
- [ ] 2-screen onboarding flow
- [ ] Note library with search and filters
- [ ] Fully responsive (mobile, tablet, desktop)
- [ ] WCAG AA compliant
- [ ] Dark mode support
- [ ] Keyboard navigation throughout
- [ ] Loading and error states for all components
- [ ] Smooth transitions and animations
- [ ] Performance targets met

---

**Design System**: Built on Shadcn UI components with Tailwind CSS for styling consistency and accessibility compliance.

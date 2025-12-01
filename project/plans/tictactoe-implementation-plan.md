# Tic-Tac-Toe Implementation Plan

## Overview

**Feature Name:** Tic-Tac-Toe Game Component

**Purpose:** Add a simple, interactive tic-tac-toe game as a prototype/demo component within the NEXLY RN application to demonstrate React component architecture, state management, and UI patterns.

**Location:** `/prototype/tictactoe-game.tsx` (following existing prototype pattern)

**Estimated Effort:** 2-4 hours

**Priority:** Low (Prototype/Learning Feature)

---

## Architecture Design

### Component Structure

```
prototype/
└── tictactoe-game.tsx          # Main game component
    ├── TicTacToeGame           # Container component
    ├── Board                   # Game board component
    ├── Square                  # Individual square component
    └── GameStatus              # Status display component
```

### State Management

**Game State:**
- `board: Array<'X' | 'O' | null>` - 9 squares representing the game board
- `isXNext: boolean` - Tracks whose turn it is
- `winner: 'X' | 'O' | 'draw' | null` - Game outcome
- `winningLine: number[] | null` - Indices of winning squares for highlighting

**State Location:** Local component state using `useState` hook (no global state needed)

### UI Design

**Layout:**
- 3x3 grid of interactive squares
- Each square: 80x80px (mobile: 60x60px)
- Status banner showing current player or game result
- Reset button to start new game

**Styling:**
- Use Tailwind CSS classes following project conventions
- Support dark/light mode using existing theme variables
- Responsive design for mobile/tablet/desktop
- Hover states and click feedback
- Winning line highlight animation

---

## Implementation Tasks

### Phase 1: Core Game Logic (1 hour)

**T001: Create base component structure**
- Create `/prototype/tictactoe-game.tsx`
- Set up TicTacToeGame component with initial state
- Add TypeScript types for game state

**T002: Implement game logic helpers**
- Create `calculateWinner()` function to check for wins
- Create `checkDraw()` function to detect stalemate
- Create `getWinningLine()` to identify winning squares
- Add unit tests for game logic functions

**T003: Implement Square component**
- Create clickable square component
- Handle click events and update board state
- Disable clicks on filled squares or after game ends
- Add proper TypeScript types for props

**T004: Implement Board component**
- Create 3x3 grid layout
- Render 9 Square components
- Pass click handlers and state to squares
- Add winning line highlighting

### Phase 2: UI & Styling (1 hour)

**T005: Style game board**
- Apply Tailwind grid layout
- Style squares with borders, padding, hover states
- Implement responsive sizing for mobile
- Add dark mode support using theme variables

**T006: Create GameStatus component**
- Display "X's turn" or "O's turn" when game active
- Display "X wins!" or "O wins!" when game over
- Display "Draw!" when no winner
- Style with appropriate colors and spacing

**T007: Add Reset button**
- Create reset button below game board
- Implement reset functionality to clear board
- Style consistently with project button patterns
- Add hover and active states

**T008: Add animations**
- Add subtle hover animation on squares
- Add winning line highlight animation
- Add X/O appearance animation
- Respect `prefers-reduced-motion` setting

### Phase 3: Polish & Testing (1 hour)

**T009: Accessibility**
- Add ARIA labels to all interactive elements
- Ensure keyboard navigation works (Tab, Enter)
- Add screen reader announcements for moves
- Test with VoiceOver/NVDA
- Verify 4.5:1 contrast ratio

**T010: Add route/page**
- Create route at `/prototype/tictactoe` or add to existing prototype page
- Add navigation link from prototype section
- Test routing and component loading

**T011: Write tests**
- Unit tests for `calculateWinner()` logic
- Unit tests for `checkDraw()` logic
- Component tests for Square click handling
- Component tests for game reset
- E2E test for complete game flow

**T012: Documentation**
- Add JSDoc comments to functions
- Document component props with TypeScript
- Add README section explaining the prototype
- Document any learnings or patterns used

---

## Technical Specifications

### Game Logic

**Win Conditions:**
```typescript
const WINNING_LINES = [
  [0, 1, 2], // Top row
  [3, 4, 5], // Middle row
  [6, 7, 8], // Bottom row
  [0, 3, 6], // Left column
  [1, 4, 7], // Center column
  [2, 5, 8], // Right column
  [0, 4, 8], // Diagonal \
  [2, 4, 6], // Diagonal /
];
```

**Calculate Winner Algorithm:**
1. Iterate through all winning lines
2. Check if all three squares in a line are the same and not null
3. Return winner ('X' or 'O') and winning line indices
4. If no winner and board full, return 'draw'
5. Otherwise, return null (game continues)

### State Updates

**Square Click Handler:**
1. Check if square is already filled → ignore click
2. Check if game is over → ignore click
3. Create new board array with X or O in clicked position
4. Toggle `isXNext` to switch turns
5. Calculate winner from new board state
6. Update state in single operation

**Reset Handler:**
1. Set board to array of 9 nulls
2. Set `isXNext` to true (X starts)
3. Set `winner` to null
4. Set `winningLine` to null

### TypeScript Types

```typescript
type Player = 'X' | 'O';
type SquareValue = Player | null;
type Board = SquareValue[];
type Winner = Player | 'draw' | null;
type WinningLine = number[] | null;

interface GameState {
  board: Board;
  isXNext: boolean;
  winner: Winner;
  winningLine: WinningLine;
}

interface SquareProps {
  value: SquareValue;
  onClick: () => void;
  isWinning: boolean;
  disabled: boolean;
}

interface GameStatusProps {
  winner: Winner;
  isXNext: boolean;
}
```

---

## File Structure

```
/home/emhar/nexly-notes/
├── prototype/
│   └── tictactoe-game.tsx          # Main implementation
├── src/
│   ├── app/
│   │   └── prototype/
│   │       └── tictactoe/
│   │           └── page.tsx         # Route page (optional)
│   └── tests/
│       └── components/
│           └── tictactoe.test.tsx   # Component tests
```

---

## Testing Strategy

### Unit Tests (Vitest)

**Test `calculateWinner()`:**
- Returns null for empty board
- Returns 'X' for X winning horizontally
- Returns 'O' for O winning vertically
- Returns 'X' for X winning diagonally
- Returns 'draw' for full board with no winner
- Returns correct winning line indices

**Test `checkDraw()`:**
- Returns false for empty board
- Returns false for board with moves but winner
- Returns true for full board with no winner

### Component Tests (React Testing Library)

**Test Square component:**
- Renders empty square correctly
- Renders X when value is 'X'
- Renders O when value is 'O'
- Calls onClick when clicked
- Does not call onClick when disabled
- Has correct ARIA labels

**Test Board component:**
- Renders 9 squares
- Highlights winning squares correctly
- Passes correct values to each square

**Test TicTacToeGame integration:**
- Starts with empty board and X to move
- Places X on first click
- Places O on second click
- Detects winner correctly
- Detects draw correctly
- Reset button clears board

### E2E Test (Playwright)

**Complete game flow:**
1. Navigate to tic-tac-toe page
2. Verify empty board displayed
3. Click squares in winning pattern for X
4. Verify "X wins!" message displayed
5. Verify winning line highlighted
6. Click reset button
7. Verify board cleared
8. Play to a draw
9. Verify "Draw!" message displayed

---

## Styling Guidelines

### Color Tokens

**Light Mode:**
- Background: `bg-white`
- Border: `border-gray-300`
- X color: `text-blue-600`
- O color: `text-red-600`
- Winning highlight: `bg-green-100`
- Status text: `text-gray-900`

**Dark Mode:**
- Background: `dark:bg-gray-800`
- Border: `dark:border-gray-600`
- X color: `dark:text-blue-400`
- O color: `dark:text-red-400`
- Winning highlight: `dark:bg-green-900`
- Status text: `dark:text-gray-100`

### Layout

**Desktop (≥1024px):**
- Square size: 80x80px
- Font size for X/O: 2.5rem
- Gap between squares: 2px
- Board centered with max-width

**Mobile (<640px):**
- Square size: 60x60px
- Font size for X/O: 2rem
- Gap between squares: 1px
- Full width with padding

### Animations

**Hover (if not reduced motion):**
```css
transition: background-color 150ms ease-in-out
hover:bg-gray-50 dark:hover:bg-gray-700
```

**Winning line (if not reduced motion):**
```css
animate-pulse (1 cycle)
```

**X/O appearance (if not reduced motion):**
```css
animate-fadeIn (200ms)
```

---

## Acceptance Criteria

**Functionality:**
- [ ] User can click empty squares to place X or O
- [ ] Game correctly alternates between X and O
- [ ] Game detects all 8 winning conditions
- [ ] Game detects draw when board is full
- [ ] Winning squares are highlighted
- [ ] Reset button clears board and starts new game
- [ ] Filled squares cannot be clicked again
- [ ] Squares cannot be clicked after game ends

**UI/UX:**
- [ ] Clear visual distinction between X and O
- [ ] Status message clearly shows whose turn it is
- [ ] Game result clearly displayed when game ends
- [ ] Board is responsive on mobile, tablet, desktop
- [ ] Dark mode fully supported
- [ ] Animations smooth and subtle
- [ ] Reduced motion preference respected

**Code Quality:**
- [ ] TypeScript types defined for all state and props
- [ ] Components properly separated and reusable
- [ ] Game logic extracted into testable functions
- [ ] No TypeScript errors
- [ ] All tests passing
- [ ] Code follows project style guidelines

**Accessibility:**
- [ ] All interactive elements keyboard accessible
- [ ] ARIA labels on all squares and buttons
- [ ] Screen reader announces game state changes
- [ ] Contrast ratios meet WCAG AA (4.5:1)
- [ ] Focus indicators visible
- [ ] Works with VoiceOver/NVDA

---

## Integration Points

### With Existing Project

**Styling:**
- Uses existing Tailwind configuration
- Follows Shadcn UI color token patterns
- Respects theme context (dark/light)
- Uses project typography scale

**Routing:**
- Can be added to existing prototype routes
- Or standalone at `/prototype/tictactoe`
- Follows Next.js 15 App Router conventions

**Testing:**
- Uses existing Vitest configuration
- Uses existing Playwright setup
- Follows project test file structure

**Not Required:**
- No Firebase integration needed
- No authentication needed
- No API routes needed
- No external data storage needed

---

## Future Enhancements (Optional)

**Beyond MVP:**
- [ ] AI opponent with difficulty levels
- [ ] Score tracking across multiple games
- [ ] Multiplayer via WebSocket
- [ ] Game history and replay
- [ ] Custom board sizes (4x4, 5x5)
- [ ] Different win conditions
- [ ] Sound effects (with mute option)
- [ ] Animations for X/O placement
- [ ] Tournament bracket mode

---

## Development Workflow

**TDD Approach:**
1. Write test for `calculateWinner()` with empty board → should return null
2. Implement minimal logic to pass test
3. Write test for X horizontal win → should return 'X'
4. Implement win detection logic
5. Continue for all win conditions
6. Write component tests for Square
7. Implement Square component to pass tests
8. Write integration tests for full game
9. Implement game state management
10. Refactor and clean up

**Commit Strategy:**
- Commit 1: "feat(prototype): add tic-tac-toe game logic and tests"
- Commit 2: "feat(prototype): add tic-tac-toe UI components"
- Commit 3: "feat(prototype): add tic-tac-toe styling and animations"
- Commit 4: "feat(prototype): add tic-tac-toe accessibility features"
- Commit 5: "test(prototype): add E2E tests for tic-tac-toe"
- Commit 6: "docs(prototype): add tic-tac-toe documentation"

---

## Risk Assessment

**Low Risk:**
- Self-contained prototype feature
- No database or API dependencies
- No impact on production features
- Easily removable if not needed

**Potential Issues:**
- None identified (simple, well-understood problem domain)

**Mitigation:**
- Comprehensive testing prevents logic bugs
- TypeScript prevents type errors
- Accessibility testing ensures inclusivity
- Responsive design testing ensures cross-device compatibility

---

## Success Metrics

**Implementation Success:**
- All 12 tasks completed
- All tests passing (100% coverage on game logic)
- Zero TypeScript errors
- Lighthouse accessibility score 100
- No console errors or warnings

**Code Quality:**
- Functions under 20 lines
- Components under 150 lines
- Cyclomatic complexity < 10
- No code duplication
- Clear, descriptive naming

**User Experience:**
- Game loads in <100ms
- Moves register instantly (<50ms)
- No visual glitches
- Intuitive without instructions
- Fun and satisfying to play

---

## Timeline

**Total Estimated Time:** 2-4 hours

**Phase 1 (Core Logic):** 1 hour
- T001-T004: Component structure and game logic

**Phase 2 (UI & Styling):** 1 hour
- T005-T008: Visual design and animations

**Phase 3 (Polish & Testing):** 1-2 hours
- T009-T012: Accessibility, testing, documentation

**Buffer:** 30 minutes for unexpected issues

---

## Notes

- This is a prototype/learning feature, not part of core NEXLY RN functionality
- Follows project architecture patterns for consistency
- Can serve as reference for future interactive components
- Demonstrates clean component composition and state management
- Good candidate for pairing/mentoring sessions
- Can be removed later without affecting production features

---

## References

**React Patterns:**
- [React Tic-Tac-Toe Tutorial](https://react.dev/learn/tutorial-tic-tac-toe)
- [Thinking in React](https://react.dev/learn/thinking-in-react)

**Project Documentation:**
- CLAUDE.md: Project structure and conventions
- specs/tasks.md: Task formatting and structure
- specs/architecture/tech-specs.md: Technical standards

**Testing Resources:**
- Vitest configuration: `vitest.config.ts`
- Playwright configuration: `playwright.config.ts`
- React Testing Library: Existing test examples in `src/tests/`

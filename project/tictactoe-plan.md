# Tic-Tac-Toe Game Implementation Plan

## Overview

Build a simple, MVP Tic-Tac-Toe game for the NEXLY RN project using Next.js, React 19, TypeScript, and Tailwind CSS v4.

## Project Context

- **Framework**: Next.js 16.0.0 with App Router
- **React Version**: 19.2.0
- **Styling**: Tailwind CSS v4
- **TypeScript**: ^5
- **Approach**: Simple/Lean MVP (as per project rules)
- **Testing**: TDD approach with Vitest

## Implementation Strategy

### Location
- Route: `src/app/(dashboard)/game/page.tsx`
- Components: `src/components/game/`
- Types: `src/types/game/`
- Tests: `src/tests/components/game/`

### Architecture

**Component Structure**:
```
src/components/game/
├── tic-tac-toe-board.tsx      # Main game board component
├── tic-tac-toe-cell.tsx       # Individual cell component
├── game-status.tsx            # Status display (winner, turn, reset)
└── index.ts                   # Barrel export
```

**Type Definitions**:
```typescript
// src/types/game/index.ts
type Player = 'X' | 'O' | null
type Board = Player[]
type GameStatus = 'playing' | 'winner' | 'draw'
```

**State Management**:
- React `useState` for game state (simple, no external libraries)
- Local component state (board array, current player, winner)

## Implementation Steps (TDD Approach)

### Phase 1: Setup & Foundation
**T001**: Create type definitions
- File: `src/types/game/index.ts`
- Define: `Player`, `Board`, `GameStatus`, `GameState` types

**T002**: Create base component structure
- File: `src/components/game/tic-tac-toe-cell.tsx`
- Props: `value: Player`, `onClick: () => void`, `disabled: boolean`
- Render: Empty cell or X/O with Tailwind styling

**T003**: Create game board component skeleton
- File: `src/components/game/tic-tac-toe-board.tsx`
- Initialize state: 9-cell array, current player
- Render: 3x3 grid using CSS Grid

### Phase 2: Core Game Logic (TDD)
**T004**: Write test for cell click
- File: `src/tests/components/game/tic-tac-toe-cell.test.tsx`
- Test: Click triggers onClick handler
- Red → Green → Refactor

**T005**: Implement cell click handler
- Update board state on click
- Switch player turn
- Prevent clicking filled cells

**T006**: Write test for win detection
- File: `src/tests/components/game/game-logic.test.ts`
- Test: Horizontal, vertical, diagonal wins
- Test helper function: `checkWinner(board: Board): Player`

**T007**: Implement win detection logic
- Create `src/lib/game/check-winner.ts`
- Check all 8 win conditions
- Return winning player or null

**T008**: Write test for draw detection
- Test: All cells filled, no winner
- Test helper: `checkDraw(board: Board): boolean`

**T009**: Implement draw detection
- Check if board is full and no winner

### Phase 3: Game Status & Controls
**T010**: Create game status component
- File: `src/components/game/game-status.tsx`
- Display: Current turn, winner message, or draw
- Include: Reset button

**T011**: Write test for game reset
- Test: Reset clears board and resets to player X

**T012**: Implement reset functionality
- Clear board state
- Reset to player X
- Clear winner status

### Phase 4: Styling & Polish
**T013**: Apply Tailwind v4 styles to board
- Use CSS Grid for 3x3 layout
- Responsive design
- Theme-aware colors (light/dark mode)

**T014**: Style cells with hover effects
- Border styling
- Hover states
- Click feedback
- Disabled state styling

**T015**: Style game status component
- Typography
- Button styling
- Winner announcement styling

### Phase 5: Integration & Route
**T016**: Create game page route
- File: `src/app/(dashboard)/game/page.tsx`
- Import `TicTacToeBoard`
- Add page layout and title

**T017**: Create barrel exports
- File: `src/components/game/index.ts`
- Export all game components

### Phase 6: Testing & Validation
**T018**: Write integration tests
- Full game flow test
- Win scenario test
- Draw scenario test
- Multiple games test

**T019**: Run all tests
- Execute: `npm test`
- Ensure all tests pass

**T020**: Manual testing
- Test in browser
- Verify responsive design
- Test light/dark mode
- Verify all win conditions

## Detailed Component Design

### TicTacToeCell Component
```typescript
interface CellProps {
  value: Player
  onClick: () => void
  disabled: boolean
  index: number
}
```

### TicTacToeBoard Component
```typescript
interface GameState {
  board: Board          // Array of 9 cells
  currentPlayer: 'X' | 'O'
  winner: Player
  gameStatus: GameStatus
}
```

### Game Logic Helper Functions
```typescript
// src/lib/game/check-winner.ts
export function checkWinner(board: Board): Player

// src/lib/game/check-draw.ts
export function checkDraw(board: Board): boolean

// src/lib/game/get-winning-line.ts (optional)
export function getWinningLine(board: Board): number[] | null
```

## Styling Guidelines (Tailwind v4)

- Use CSS Grid: `grid grid-cols-3 gap-2`
- Cell sizing: `w-24 h-24` or `aspect-square`
- Borders: Theme-aware border colors
- Hover effects: `hover:bg-gray-100 dark:hover:bg-gray-800`
- Typography: `text-4xl font-bold` for X/O
- Colors: Use theme variables from Tailwind v4

## Success Criteria

- All tests pass (100% coverage for game logic)
- Game correctly detects all 8 win conditions
- Draw detection works properly
- Reset functionality clears game state
- Responsive design works on all screen sizes
- Accessible (keyboard navigation, ARIA labels)
- Clean, readable code following project standards

## Out of Scope (MVP)
- AI opponent
- Score tracking/persistence
- Multiplayer/online play
- Animations (can add post-MVP)
- Sound effects
- Different board sizes
- Time limits

## Estimated Complexity
- **Components**: 4 files
- **Logic helpers**: 2-3 files
- **Types**: 1 file
- **Tests**: 3-4 test files
- **Total**: ~10-12 files
- **Complexity**: Low (simple state management, pure functions)

## Dependencies
No additional dependencies needed. Using existing:
- React 19.2.0
- Next.js 16.0.0
- TypeScript ^5
- Tailwind CSS v4
- Vitest (for testing)

## Notes
- Follow TDD strictly: Write test → See it fail → Write code → See it pass → Refactor
- Keep it simple: No over-engineering
- Use semantic HTML and TypeScript types
- Follow project's coding standards
- Prioritize readability over cleverness

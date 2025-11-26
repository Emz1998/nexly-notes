# Implementation Plan: Note Sorting Preferences Hook System Test

## Objective

Implement and validate a simple "Note Sorting Preferences" feature that persists user's preferred sort order (date, title, or category) in local storage. This feature will serve as a realistic test case to verify that the hook triggering mechanism works correctly within the NEXLY RN architecture.

## Scope

**In-Scope:**
- Create a custom `useSortPreference` hook that manages sorting state and persistence
- Add a sort order selector UI component in the notes library header
- Persist sorting preference to localStorage
- Retrieve and apply saved preference on component mount
- Implement three sort options: "Date Modified", "Title (A-Z)", "Category"
- Unit test the hook logic
- Integration test the persistence mechanism

**Out-of-Scope:**
- Cloud sync of preferences (MVP only uses localStorage)
- Advanced sorting algorithms
- Multi-column sorting
- Sort preference synchronization across browser tabs
- User preference API endpoint (for future cloud sync)
- UI animations or transitions

---

## Technical Setup & Requirements

- **Stack:** React 19, TypeScript, Vitest 3.2.4
- **Hook Location:** `src/hooks/ui/useSortPreference.ts`
- **Component Location:** `src/components/notes/SortSelector.tsx`
- **Test Files:** `src/tests/hooks/useSortPreference.test.ts` and `src/tests/components/SortSelector.test.ts`
- **Storage Key:** `nexly:notes:sortPreference` (prefixed to avoid collisions)
- **Type Definition Location:** `src/types/ui/index.ts`
- **Default Preference:** `{ field: "dateModified", order: "desc" }`

---

## Implementation Phases

### Phase 1: Type Definitions and Hook Architecture

**Tasks:**
- Define TypeScript types for sort preferences: `SortField`, `SortOrder`, `SortPreference`
- Add type definitions to `src/types/ui/index.ts`
- Create the custom hook skeleton with proper TypeScript interfaces
- Document hook props, return values, and behavior in JSDoc comments

**Deliverables:**
- `src/types/ui/index.ts` - Type definitions
- `src/hooks/ui/useSortPreference.ts` - Hook skeleton with types

---

### Phase 2: Hook Implementation

**Tasks:**
- Implement `useSortPreference` hook with the following features:
  - Read preference from localStorage on mount
  - Provide `sortPreference` state getter
  - Provide `setSortPreference` function to update preference and persist
  - Handle localStorage errors gracefully (fallback to default)
  - Return array of available sort options for UI rendering
- Add error handling for corrupted localStorage data
- Implement `useEffect` for localStorage sync
- Add memoization to prevent unnecessary renders

**Deliverables:**
- Fully functional `useSortPreference` hook with error handling

---

### Phase 3: UI Component Implementation

**Tasks:**
- Create `SortSelector.tsx` component that:
  - Consumes the `useSortPreference` hook
  - Renders a dropdown/menu with sort options
  - Displays current sort selection
  - Handles sort option selection and updates hook state
  - Uses Shadcn UI components (Button + DropdownMenu)
- Implement TypeScript prop interfaces
- Add accessibility attributes (ARIA labels, keyboard navigation)
- Add descriptive labels for each sort option

**Deliverables:**
- `src/components/notes/SortSelector.tsx` component
- Accessibility-compliant implementation

---

### Phase 4: Hook and Component Testing

**Tasks:**
- Write unit tests for `useSortPreference` hook:
  - Test default value initialization
  - Test localStorage read on mount
  - Test setSortPreference updates state and persists
  - Test error handling when localStorage is corrupted
  - Test localStorage quota exceeded scenario
  - Test hook with multiple instances
- Write integration tests for `SortSelector` component:
  - Test dropdown renders correctly
  - Test selecting a sort option updates hook state
  - Test selected option is reflected in UI
  - Test localStorage is updated when user selects option
- Ensure all tests pass with >90% code coverage

**Deliverables:**
- `src/tests/hooks/useSortPreference.test.ts` - Hook tests
- `src/tests/components/SortSelector.test.ts` - Component tests

---

### Phase 5: Integration and Documentation

**Tasks:**
- Integrate `SortSelector` component into the Notes Library page (add to header)
- Verify component displays correctly in the layout
- Update the notes list to apply sorting preference from hook
- Add JSDoc comments explaining hook usage
- Create minimal documentation showing:
  - How to use the hook in other components
  - Example usage patterns
  - Error handling behavior
  - localStorage key and format
- Run full test suite to ensure no regressions
- Validate that feature works in offline mode

**Deliverables:**
- Integration of SortSelector into Notes Library
- Complete test coverage passing
- Documentation for future developers

---

## Quality Gates

- All unit and integration tests pass with >90% code coverage
- No TypeScript compilation errors
- Hook properly handles edge cases (corrupted data, localStorage errors, quota exceeded)
- Component is keyboard accessible and has proper ARIA labels
- localStorage persistence verified in browser DevTools
- Default preference loads correctly on fresh browser session
- Feature works with offline-first architecture (localStorage available even when offline)
- Code follows project conventions (naming, structure, comments)
- No console errors or warnings during test execution

---

## Files to Be Modified/Created

**New Files:**
- `src/hooks/ui/useSortPreference.ts`
- `src/components/notes/SortSelector.tsx`
- `src/tests/hooks/useSortPreference.test.ts`
- `src/tests/components/SortSelector.test.ts`

**Modified Files:**
- `src/types/ui/index.ts` - Add SortPreference types
- `src/components/notes/NotesLibrary.tsx` (or similar) - Integrate SortSelector component
- `src/types/index.ts` - Export new types from barrel export

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| localStorage quota exceeded | Hook fails silently, preference lost | Implement try-catch, provide fallback to in-memory state, log warnings |
| Corrupted localStorage data | Hook throws error on parse | Validate JSON with schema validation, clear corrupted data, use default |
| Multiple browser tabs out of sync | User expects sync but changes don't propagate | Document limitation, focus on MVP scope (single-tab testing first) |
| Hook called during SSR | localStorage undefined error | Guard hook with `typeof window !== 'undefined'`, provide conditional logic |
| TypeScript type complexity | Hard to maintain or extend | Use discriminated unions for sort options, keep types simple and focused |
| Test environment lacks localStorage | Tests fail in test runner | Mock localStorage with vitest setup file, provide proper test utilities |

---

## Validation Checklist

- [ ] Hook properly reads from and writes to localStorage
- [ ] Component renders without errors
- [ ] Sort preference persists across page refreshes
- [ ] Default preference loads when localStorage is empty
- [ ] All edge cases handled (corrupted data, quota exceeded)
- [ ] TypeScript strict mode passes
- [ ] 100% test coverage for hook logic
- [ ] Accessibility requirements met (ARIA labels, keyboard nav)
- [ ] Documentation clear and comprehensive
- [ ] Ready for hook invocation system testing

---

## Key Implementation Details

### Hook Return Type
```typescript
{
  sortPreference: SortPreference;
  setSortPreference: (preference: SortPreference) => void;
  sortOptions: SortOption[];
}
```

### Storage Format
```json
{
  "field": "dateModified" | "title" | "category",
  "order": "asc" | "desc"
}
```

### Error Handling Strategy
- localStorage write errors: Log warning, keep state in memory
- Corrupted data on read: Use default, clear localStorage key
- SSR environment: Defer to client-side only via useEffect

### Component Integration
The `SortSelector` will be placed in the Notes Library header next to search/filter controls, providing users immediate access to sort preferences without disrupting their workflow.

---

## Success Metrics for Hook System Test

1. Hook can be successfully invoked and executed without errors
2. State management works correctly (read/write/persist)
3. Component integrates seamlessly into existing UI
4. Tests pass reliably in CI/CD pipeline
5. localStorage persistence verified and validated
6. No console errors during execution
7. Feature demonstrates realistic hook usage patterns for NEXLY RN architecture

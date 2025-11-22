# Testing Specifications - Next.js Stack (4-Week MVP)

## 1. Testing Strategy

### Philosophy

- **Test-Driven Development (TDD)**: Write tests before implementation
- **Testing Pyramid**: 70% unit, 20% integration, 10% end-to-end
- **Continuous Testing**: Automated tests on every commit
- **Coverage Target**: 90%+ for MVP critical paths, 60%+ overall

### Frameworks and Tools

**Unit Testing**

- Vitest 3.2.4 for test runner
- React Testing Library 16.3.0 for component tests
- jsdom 25.x for DOM simulation (lightweight alternative to Happy DOM)
- fake-indexeddb 6.x for Dexie mocking
- @testing-library/jest-dom 6.x for extended matchers

**Integration Testing**

- Firebase Emulator Suite for backend testing
- Vitest for API route testing
- MSW (Mock Service Worker) for API mocking

**End-to-End Testing**

- Playwright 1.55.0 for browser automation
- Cross-browser testing: Chromium, Firefox, WebKit

## 2. Unit Testing Configuration

### Vitest Setup

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./tests/setup.ts"],
    globals: true,
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      exclude: [
        "node_modules/",
        "tests/",
        "**/*.d.ts",
        "**/*.config.*",
        "**/mockData",
        ".next/",
        "out/",
      ],
      include: [
        "app/**/*.{ts,tsx}",
        "components/**/*.{ts,tsx}",
        "lib/**/*.{ts,tsx}",
        "hooks/**/*.{ts,tsx}",
      ],
      thresholds: {
        statements: 60,
        branches: 60,
        functions: 60,
        lines: 60,
      },
    },
    testTimeout: 10000,
    hookTimeout: 10000,
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./"),
    },
  },
});
```

### Test Setup File

```typescript
// tests/setup.ts
import "@testing-library/jest-dom";
import { expect, afterEach, vi } from "vitest";
import { cleanup } from "@testing-library/react";
import "fake-indexeddb/auto";

// Cleanup after each test
afterEach(() => {
  cleanup();
});

// Mock Next.js router
vi.mock("next/navigation", () => ({
  useRouter() {
    return {
      push: vi.fn(),
      replace: vi.fn(),
      prefetch: vi.fn(),
      back: vi.fn(),
      pathname: "/",
      query: {},
      asPath: "/",
    };
  },
  useSearchParams() {
    return new URLSearchParams();
  },
  usePathname() {
    return "/";
  },
}));

// Mock Firebase
vi.mock("@/lib/firebase/client", () => ({
  db: {},
  auth: {},
}));

// Global test utilities
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));
```

## 3. Component Testing (MVP Features)

### Note Editor Component

```typescript
// components/editor/tiptap-editor.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, describe, vi } from "vitest";
import { TiptapEditor } from "./tiptap-editor";

describe("TiptapEditor", () => {
  test("renders editor in Create mode", () => {
    render(<TiptapEditor mode="create" />);
    expect(screen.getByPlaceholder("Start typing...")).toBeInTheDocument();
  });

  test("displays mode-specific UI (Blue accent for Create)", () => {
    const { container } = render(<TiptapEditor mode="create" />);
    const editor = container.querySelector(".editor-container");
    expect(editor).toHaveClass("mode-create"); // Blue accent class
  });

  test("switches between Create/Edit/Study modes", async () => {
    const { rerender } = render(<TiptapEditor mode="create" />);
    expect(screen.getByText("Create Mode")).toBeInTheDocument();

    rerender(<TiptapEditor mode="edit" />);
    await waitFor(() => {
      expect(screen.getByText("Edit Mode")).toBeInTheDocument();
    });

    rerender(<TiptapEditor mode="study" />);
    await waitFor(() => {
      expect(screen.getByText("Study Mode")).toBeInTheDocument();
    });
  });

  test("shows autocomplete in Create and Edit modes only", async () => {
    const user = userEvent.setup();

    const { rerender } = render(<TiptapEditor mode="create" />);
    const input = screen.getByRole("textbox");

    await user.type(input, "car");
    await waitFor(() => {
      expect(screen.getByText("Autocomplete suggestions")).toBeInTheDocument();
    });

    // Switch to Study mode
    rerender(<TiptapEditor mode="study" />);
    await user.type(input, "nur");

    // Autocomplete should NOT appear in Study mode
    await waitFor(() => {
      expect(
        screen.queryByText("Autocomplete suggestions")
      ).not.toBeInTheDocument();
    });
  });

  test("disables editing in Study Mode", () => {
    render(<TiptapEditor mode="study" />);
    const editor = screen.getByRole("textbox");
    expect(editor).toHaveAttribute("contenteditable", "false");
  });

  test("handles content updates with debouncing", async () => {
    const onUpdate = vi.fn();
    const user = userEvent.setup();

    render(<TiptapEditor mode="create" onUpdate={onUpdate} />);
    const input = screen.getByRole("textbox");

    await user.type(input, "Hello");

    // onUpdate should be debounced (not called immediately)
    expect(onUpdate).not.toHaveBeenCalled();

    // Wait for debounce
    await waitFor(
      () => {
        expect(onUpdate).toHaveBeenCalledWith(
          expect.objectContaining({
            content: expect.any(Object),
          })
        );
      },
      { timeout: 2000 }
    );
  });
});
```

### Mode Toggle Component

```typescript
// components/mode-selector.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { expect, test, describe, vi } from "vitest";
import { ModeSelector } from "./mode-selector";

describe("ModeSelector", () => {
  test("toggles between Create/Edit/Study modes", async () => {
    const onModeChange = vi.fn();

    render(<ModeSelector currentMode="create" onModeChange={onModeChange} />);

    // Click Edit button
    fireEvent.click(screen.getByText("Edit"));
    expect(onModeChange).toHaveBeenCalledWith("edit");

    // Click Study button
    fireEvent.click(screen.getByText("Study"));
    expect(onModeChange).toHaveBeenCalledWith("study");
  });

  test("updates visual indicators (accent colors)", () => {
    const { rerender, container } = render(
      <ModeSelector currentMode="create" onModeChange={vi.fn()} />
    );

    let activeButton = container.querySelector(".mode-active");
    expect(activeButton).toHaveClass("mode-create"); // Blue

    rerender(<ModeSelector currentMode="edit" onModeChange={vi.fn()} />);
    activeButton = container.querySelector(".mode-active");
    expect(activeButton).toHaveClass("mode-edit"); // Purple

    rerender(<ModeSelector currentMode="study" onModeChange={vi.fn()} />);
    activeButton = container.querySelector(".mode-active");
    expect(activeButton).toHaveClass("mode-study"); // Green
  });

  test("fires mode change events", () => {
    const onModeChange = vi.fn();
    render(<ModeSelector currentMode="create" onModeChange={onModeChange} />);

    fireEvent.click(screen.getByText("Edit"));
    expect(onModeChange).toHaveBeenCalledTimes(1);
    expect(onModeChange).toHaveBeenCalledWith("edit");
  });

  test("transition animation completes within 300ms", async () => {
    const { rerender } = render(
      <ModeSelector currentMode="create" onModeChange={vi.fn()} />
    );

    const startTime = Date.now();
    rerender(<ModeSelector currentMode="edit" onModeChange={vi.fn()} />);

    await waitFor(() => {
      const elapsedTime = Date.now() - startTime;
      expect(elapsedTime).toBeLessThan(300);
    });
  });
});
```

### Inline Diff Component (Edit Mode Only)

```typescript
// components/editor/inline-diff.test.tsx
import { render, screen } from "@testing-library/react";
import { expect, test, describe } from "vitest";
import { InlineDiff } from "./inline-diff";

describe("InlineDiff", () => {
  const currentContent = "Hello world this is new content";
  const savedContent = "Hello world this is old content";

  test("displays diff between current and saved content", () => {
    render(<InlineDiff current={currentContent} saved={savedContent} />);

    // Should show additions in green
    expect(screen.getByText("new")).toHaveClass("diff-addition");

    // Should show deletions in red
    expect(screen.getByText("old")).toHaveClass("diff-deletion");
  });

  test("highlights additions (green), deletions (red), unchanged (gray)", () => {
    const { container } = render(
      <InlineDiff current={currentContent} saved={savedContent} />
    );

    const additions = container.querySelectorAll(".diff-addition");
    const deletions = container.querySelectorAll(".diff-deletion");
    const unchanged = container.querySelectorAll(".diff-unchanged");

    expect(additions.length).toBeGreaterThan(0);
    expect(deletions.length).toBeGreaterThan(0);
    expect(unchanged.length).toBeGreaterThan(0);
  });

  test("shows toolbar button only in Edit Mode", () => {
    const { rerender } = render(<TiptapEditor mode="create" />);

    expect(screen.queryByText("View Changes")).not.toBeInTheDocument();

    rerender(<TiptapEditor mode="edit" />);
    expect(screen.getByText("View Changes")).toBeInTheDocument();
  });

  test("calculates diff within 200ms", async () => {
    const largeContent = "word ".repeat(3000); // 3000 words
    const startTime = Date.now();

    render(<InlineDiff current={largeContent} saved={largeContent} />);

    const elapsedTime = Date.now() - startTime;
    expect(elapsedTime).toBeLessThan(200);
  });
});
```

### Autocomplete Popup

```typescript
// components/editor/autocomplete-popup.test.tsx
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { expect, test, describe, vi } from "vitest";
import { AutocompletePopup } from "./autocomplete-popup";

describe("AutocompletePopup", () => {
  const mockSuggestions = ["cardiac", "cardiology", "cardiomyopathy"];

  test("appears after 150ms typing pause", async () => {
    const user = userEvent.setup({ delay: null });
    render(<AutocompletePopup />);

    const input = screen.getByRole("textbox");
    await user.type(input, "car");

    // Should not appear immediately
    expect(screen.queryByRole("listbox")).not.toBeInTheDocument();

    // Should appear after 150ms
    await waitFor(
      () => {
        expect(screen.getByRole("listbox")).toBeInTheDocument();
      },
      { timeout: 200 }
    );
  });

  test("displays max 5 suggestions", async () => {
    const manySuggestions = Array.from({ length: 10 }, (_, i) => `term${i}`);
    render(<AutocompletePopup suggestions={manySuggestions} />);

    const suggestions = screen.getAllByRole("option");
    expect(suggestions).toHaveLength(5);
  });

  test("keyboard navigation (Arrow Up/Down, Enter/Tab, Escape)", async () => {
    const user = userEvent.setup();
    const onSelect = vi.fn();

    render(
      <AutocompletePopup suggestions={mockSuggestions} onSelect={onSelect} />
    );

    // Arrow down to select first
    await user.keyboard("{ArrowDown}");
    expect(screen.getByRole("option", { name: "cardiac" })).toHaveClass(
      "selected"
    );

    // Arrow down to select second
    await user.keyboard("{ArrowDown}");
    expect(screen.getByRole("option", { name: "cardiology" })).toHaveClass(
      "selected"
    );

    // Enter to select
    await user.keyboard("{Enter}");
    expect(onSelect).toHaveBeenCalledWith("cardiology");

    // Escape to dismiss
    await user.keyboard("{Escape}");
    expect(screen.queryByRole("listbox")).not.toBeInTheDocument();
  });

  test("falls back to local dictionary when quota exceeded", async () => {
    const { rerender } = render(<AutocompletePopup quotaRemaining={10} />);

    // With quota
    expect(screen.getByText(/AI suggestions/)).toBeInTheDocument();

    // Quota exceeded
    rerender(<AutocompletePopup quotaRemaining={0} />);
    expect(screen.getByText(/Offline suggestions/)).toBeInTheDocument();
  });
});
```

### Key Terms Sidebar (Study Mode Only)

```typescript
// components/study/key-terms-sidebar.test.tsx
import { render, screen, fireEvent } from "@testing-library/react";
import { expect, test, describe, vi } from "vitest";
import { KeyTermsSidebar } from "./key-terms-sidebar";

describe("KeyTermsSidebar", () => {
  const mockTerms = [
    {
      term: "Hypertension",
      context: "blood pressure",
      importance: "high",
      position: 100,
    },
    {
      term: "Diabetes",
      context: "insulin management",
      importance: "medium",
      position: 200,
    },
  ];

  test("displays spotted terms with context", () => {
    render(<KeyTermsSidebar terms={mockTerms} />);

    expect(screen.getByText("Hypertension")).toBeInTheDocument();
    expect(screen.getByText(/blood pressure/)).toBeInTheDocument();
    expect(screen.getByText("Diabetes")).toBeInTheDocument();
  });

  test("click term to jump to location in note", () => {
    const onJumpTo = vi.fn();
    render(<KeyTermsSidebar terms={mockTerms} onJumpTo={onJumpTo} />);

    fireEvent.click(screen.getByText("Hypertension"));
    expect(onJumpTo).toHaveBeenCalledWith(100);
  });

  test("shows importance level (high/medium/low)", () => {
    render(<KeyTermsSidebar terms={mockTerms} />);

    expect(screen.getByText("High")).toBeInTheDocument();
    expect(screen.getByText("Medium")).toBeInTheDocument();
  });

  test("only visible in Study Mode", () => {
    const { rerender } = render(<TiptapEditor mode="create" />);

    expect(screen.queryByText("Key Terms")).not.toBeInTheDocument();

    rerender(<TiptapEditor mode="study" />);
    expect(screen.getByText("Key Terms")).toBeInTheDocument();
  });
});
```

## 4. API Route Testing

### Autocomplete API Route

```typescript
// app/api/ai/autocomplete/route.test.ts
import { describe, test, expect, vi, beforeEach } from "vitest";
import { POST } from "./route";
import { NextRequest } from "next/server";

describe("POST /api/ai/autocomplete", () => {
  beforeEach(() => {
    vi.resetAllMocks();
  });

  test("returns suggestions for valid request", async () => {
    const mockToken = "valid-token";
    const request = new NextRequest("http://localhost/api/ai/autocomplete", {
      method: "POST",
      headers: {
        authorization: `Bearer ${mockToken}`,
      },
      body: JSON.stringify({
        context: "patient has hyper",
        cursorPosition: 18,
      }),
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.suggestions).toBeInstanceOf(Array);
    expect(data.suggestions.length).toBeGreaterThan(0);
    expect(data.quotaRemaining).toBeGreaterThanOrEqual(0);
  });

  test("enforces quota limits for free tier", async () => {
    // Mock user with exceeded quota
    const request = new NextRequest("http://localhost/api/ai/autocomplete", {
      method: "POST",
      headers: {
        authorization: "Bearer free-user-token",
      },
      body: JSON.stringify({
        context: "test",
        cursorPosition: 4,
      }),
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.fallback).toBe(true);
    expect(data.quotaRemaining).toBe(0);
  });

  test("returns 401 for missing auth token", async () => {
    const request = new NextRequest("http://localhost/api/ai/autocomplete", {
      method: "POST",
      body: JSON.stringify({
        context: "test",
        cursorPosition: 4,
      }),
    });

    const response = await POST(request);
    expect(response.status).toBe(401);
  });

  test("completes within 100ms performance target", async () => {
    const request = new NextRequest("http://localhost/api/ai/autocomplete", {
      method: "POST",
      headers: {
        authorization: "Bearer valid-token",
      },
      body: JSON.stringify({
        context: "cardiac",
        cursorPosition: 7,
      }),
    });

    const startTime = Date.now();
    await POST(request);
    const elapsedTime = Date.now() - startTime;

    expect(elapsedTime).toBeLessThan(100);
  });
});
```

### Key Term Spotting API Route

```typescript
// app/api/ai/spot-terms/route.test.ts
import { describe, test, expect, vi } from "vitest";
import { POST } from "./route";
import { NextRequest } from "next/server";

describe("POST /api/ai/spot-terms", () => {
  test("spots key terms in note content", async () => {
    const request = new NextRequest("http://localhost/api/ai/spot-terms", {
      method: "POST",
      headers: {
        authorization: "Bearer valid-token",
      },
      body: JSON.stringify({
        noteId: "note-123",
        content: {
          type: "doc",
          content: [
            {
              type: "paragraph",
              content: [
                { type: "text", text: "Important: Hypertension management" },
              ],
            },
          ],
        },
      }),
    });

    const response = await POST(request);
    const data = await response.json();

    expect(response.status).toBe(200);
    expect(data.terms).toBeInstanceOf(Array);
    expect(data.terms[0]).toHaveProperty("term");
    expect(data.terms[0]).toHaveProperty("importance");
    expect(data.terms[0]).toHaveProperty("reason");
  });

  test("enforces quota for free tier", async () => {
    // Mock user with exceeded quota
    const request = new NextRequest("http://localhost/api/ai/spot-terms", {
      method: "POST",
      headers: {
        authorization: "Bearer free-user-exceeded",
      },
      body: JSON.stringify({
        noteId: "note-123",
        content: { type: "doc", content: [] },
      }),
    });

    const response = await POST(request);
    expect(response.status).toBe(429); // Too Many Requests
  });

  test("completes within 5s for 3000-word note", async () => {
    const largeContent = {
      type: "doc",
      content: Array.from({ length: 100 }, () => ({
        type: "paragraph",
        content: [{ type: "text", text: "word ".repeat(30) }],
      })),
    };

    const request = new NextRequest("http://localhost/api/ai/spot-terms", {
      method: "POST",
      headers: {
        authorization: "Bearer valid-token",
      },
      body: JSON.stringify({
        noteId: "note-123",
        content: largeContent,
      }),
    });

    const startTime = Date.now();
    await POST(request);
    const elapsedTime = Date.now() - startTime;

    expect(elapsedTime).toBeLessThan(5000);
  });
});
```

## 5. Integration Testing

### Firebase Integration Tests

```typescript
// tests/integration/firebase.test.ts
import { describe, test, expect, beforeAll, afterAll } from 'vitest';
import { initializeTestEnvironment, RulesTestEnvironment } from '@firebase/rules-unit-testing';

let testEnv: RulesTestEnvironment;

beforeAll(async () => {
  testEnv = await initializeTestEnvironment({
    projectId: 'test-project',
    firestore: {
      rules: /* load firestore.rules */,
    },
  });
});

afterAll(async () => {
  await testEnv.cleanup();
});

describe('Firestore Security Rules', () => {
  test('user can read their own notes', async () => {
    const alice = testEnv.authenticatedContext('alice');
    const notesRef = alice.firestore().collection('users/alice/notes');

    await testEnv.withSecurityRulesDisabled(async (context) => {
      await context.firestore().doc('users/alice/notes/note1').set({
        userId: 'alice',
        title: 'Test Note'
      });
    });

    await alice.firestore().doc('users/alice/notes/note1').get();
    // Should not throw permission error
  });

  test('user cannot read other users notes', async () => {
    const alice = testEnv.authenticatedContext('alice');

    await expect(
      alice.firestore().doc('users/bob/notes/note1').get()
    ).rejects.toThrow();
  });

  test('snapshots inherit parent note permissions', async () => {
    const alice = testEnv.authenticatedContext('alice');

    await testEnv.withSecurityRulesDisabled(async (context) => {
      await context.firestore().doc('users/alice/notes/note1/snapshots/snap1').set({
        userId: 'alice',
        noteId: 'note1',
        content: {}
      });
    });

    await alice.firestore().doc('users/alice/notes/note1/snapshots/snap1').get();
    // Should not throw permission error
  });
});
```

### Dexie Integration Tests

```typescript
// tests/integration/dexie.test.ts
import { describe, test, expect, beforeEach } from "vitest";
import { db } from "@/lib/dexie/db";
import "fake-indexeddb/auto";

describe("Dexie Operations", () => {
  beforeEach(async () => {
    await db.notes.clear();
    await db.syncQueue.clear();
  });

  test("stores notes in IndexedDB", async () => {
    await db.notes.add({
      id: "note-1",
      userId: "user-1",
      title: "Test Note",
      content: { type: "doc", content: [] },
      mode: "create",
      createdAt: Date.now(),
      updatedAt: Date.now(),
      metadata: {},
      tags: [],
      stats: { wordCount: 0, characterCount: 0 },
      syncStatus: {
        synced: false,
        pendingChanges: true,
        lastSyncedAt: Date.now(),
      },
    });

    const note = await db.notes.get("note-1");
    expect(note).toBeDefined();
    expect(note?.title).toBe("Test Note");
  });

  test("adds operations to sync queue", async () => {
    await db.syncQueue.add({
      operation: "create",
      collection: "notes",
      documentId: "note-1",
      data: { title: "Test" },
      createdAt: Date.now(),
      retryCount: 0,
    });

    const queue = await db.syncQueue.toArray();
    expect(queue).toHaveLength(1);
    expect(queue[0].operation).toBe("create");
  });

  test("performs full-text search", async () => {
    await db.notes.bulkAdd([
      {
        id: "note-1",
        userId: "user-1",
        title: "Hypertension Management",
        content: { type: "doc", content: [] },
        mode: "create",
        createdAt: Date.now(),
        updatedAt: Date.now(),
        metadata: {},
        tags: [],
        stats: { wordCount: 0, characterCount: 0 },
        syncStatus: {
          synced: true,
          pendingChanges: false,
          lastSyncedAt: Date.now(),
        },
      },
      {
        id: "note-2",
        userId: "user-1",
        title: "Diabetes Care",
        content: { type: "doc", content: [] },
        mode: "create",
        createdAt: Date.now(),
        updatedAt: Date.now(),
        metadata: {},
        tags: [],
        stats: { wordCount: 0, characterCount: 0 },
        syncStatus: {
          synced: true,
          pendingChanges: false,
          lastSyncedAt: Date.now(),
        },
      },
    ]);

    const results = await db.notes
      .where("userId")
      .equals("user-1")
      .filter((note) => note.title.toLowerCase().includes("hyper"))
      .toArray();

    expect(results).toHaveLength(1);
    expect(results[0].title).toBe("Hypertension Management");
  });
});
```

## 6. End-to-End Testing (MVP)

### Critical User Workflows

```typescript
// tests/e2e/onboarding.spec.ts
import { test, expect } from "@playwright/test";

test.describe("New User Onboarding", () => {
  test("completes 2-screen onboarding flow", async ({ page }) => {
    await page.goto("/signup");

    // Sign up
    await page.fill('[name="email"]', "test@example.com");
    await page.fill('[name="password"]', "Password123!");
    await page.click('button[type="submit"]');

    // Screen 1: Learn about modes
    await expect(page.locator("h1")).toContainText(
      "Three modes for better learning"
    );
    await page.click('button:has-text("Next")');

    // Screen 2: Interactive demo
    await expect(page.locator("h2")).toContainText("Try it now");
    await page.fill('[role="textbox"]', "Test note content");
    await page.click('button:has-text("Start creating")');

    // Should redirect to note library
    await expect(page).toHaveURL(/\/notes/);
  });
});

test.describe("Create Note Workflow", () => {
  test("creates note with AI autocomplete", async ({ page }) => {
    await page.goto("/notes");
    await page.click('button:has-text("New Note")');

    // Should open in Create mode
    await expect(page.locator(".mode-indicator")).toHaveClass(/mode-create/);

    // Type with autocomplete
    await page.fill('[role="textbox"]', "car");
    await page.waitForTimeout(200); // Wait for autocomplete debounce

    // Autocomplete should appear
    await expect(page.locator('[role="listbox"]')).toBeVisible();

    // Select suggestion
    await page.keyboard.press("ArrowDown");
    await page.keyboard.press("Enter");

    // Auto-save should create snapshots
    await page.waitForTimeout(30000); // Wait for auto-save interval

    // Verify note appears in library
    await page.goto("/notes");
    await expect(page.locator(".note-card").first()).toBeVisible();
  });
});

test.describe("Edit Note Workflow", () => {
  test("edits note and views inline diff", async ({ page }) => {
    await page.goto("/notes");

    // Open existing note
    await page.click(".note-card:first-child");

    // Edit or Study Dialog should appear
    await expect(page.locator('[role="dialog"]')).toBeVisible();
    await expect(page.locator("h2")).toContainText("How do you want to open");

    // Select Edit
    await page.click('button:has-text("Edit this note")');

    // Should open in Edit mode
    await expect(page.locator(".mode-indicator")).toHaveClass(/mode-edit/);

    // Make changes
    await page.fill('[role="textbox"]', "Updated content");

    // Click inline diff button
    await page.click('button:has-text("View Changes")');

    // Diff view should appear
    await expect(page.locator(".diff-view")).toBeVisible();
    await expect(page.locator(".diff-addition")).toBeVisible();

    // Save changes
    await page.click('button:has-text("Save")');
    await expect(page.locator(".toast")).toContainText("Saved");
  });
});

test.describe("Study Note Workflow", () => {
  test("opens note in Study mode and spots key terms", async ({ page }) => {
    await page.goto("/notes");

    // Open existing note
    await page.click(".note-card:first-child");

    // Select Study
    await page.click('button:has-text("Study this note")');

    // Should open in Study mode (read-only)
    await expect(page.locator(".mode-indicator")).toHaveClass(/mode-study/);
    await expect(page.locator('[role="textbox"]')).toHaveAttribute(
      "contenteditable",
      "false"
    );

    // Spot key terms
    await page.click('button:has-text("Spot Key Terms")');
    await page.waitForTimeout(5000); // Wait for AI processing

    // Key terms sidebar should appear
    await expect(page.locator(".key-terms-sidebar")).toBeVisible();
    await expect(page.locator(".key-term").first()).toBeVisible();

    // Click term to jump
    await page.click(".key-term:first-child");
    // Should scroll to term location

    // Export key terms
    await page.click('button:has-text("Export")');
    const download = await page.waitForEvent("download");
    expect(download.suggestedFilename()).toMatch(/key-terms\.txt/);
  });
});
```

## 7. Performance Testing

```typescript
// tests/performance/metrics.spec.ts
import { test, expect } from "@playwright/test";

test.describe("Performance Metrics", () => {
  test("autocomplete latency <100ms", async ({ page }) => {
    await page.goto("/notes/new");

    const startTime = Date.now();
    await page.fill('[role="textbox"]', "car");
    await page.waitForSelector('[role="listbox"]');
    const latency = Date.now() - startTime;

    expect(latency).toBeLessThan(100);
  });

  test("mode transition <50ms", async ({ page }) => {
    await page.goto("/notes/note-123");

    const startTime = Date.now();
    await page.click('button[data-mode="edit"]');
    await page.waitForSelector(".mode-edit");
    const transitionTime = Date.now() - startTime;

    expect(transitionTime).toBeLessThan(50);
  });

  test("inline diff calculation <200ms for 3000 words", async ({ page }) => {
    await page.goto("/notes/large-note");

    const startTime = Date.now();
    await page.click('button:has-text("View Changes")');
    await page.waitForSelector(".diff-view");
    const diffTime = Date.now() - startTime;

    expect(diffTime).toBeLessThan(200);
  });

  test("key term spotting <5s for 3000 words", async ({ page }) => {
    await page.goto("/notes/large-note?mode=study");

    const startTime = Date.now();
    await page.click('button:has-text("Spot Key Terms")');
    await page.waitForSelector(".key-terms-sidebar .key-term");
    const spottingTime = Date.now() - startTime;

    expect(spottingTime).toBeLessThan(5000);
  });
});
```

## 8. Test Coverage Requirements (MVP)

### Critical Paths (90%+ coverage required)

- Three-mode workflow (Create/Edit/Study)
- Mode transitions and visual indicators
- AI autocomplete with quota (GPT-4.1 nano)
- Inline diff calculation (Edit Mode)
- Key term spotting (Study Mode, GPT-4o-mini)
- Auto-save with version snapshots (backend)
- Sync functionality
- Security rules enforcement

### Important Paths (80%+ coverage required)

- Edit or Study Dialog
- 2-screen onboarding
- Note library with search
- Offline functionality
- Error handling and recovery

### Supporting Features (60%+ coverage required)

- UI components
- Utility functions
- Analytics and logging

## 9. CI/CD Integration

### GitHub Actions Workflow

```yaml
# .github/workflows/test.yml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Node.js
        uses: actions/setup-node@v3
        with:
          node-version: "20"

      - name: Install dependencies
        run: npm ci

      - name: Run linter
        run: npm run lint

      - name: Type check
        run: npm run type-check

      - name: Run unit tests
        run: npm run test:coverage

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/coverage-final.json

      - name: Install Playwright
        run: npx playwright install --with-deps

      - name: Run E2E tests
        run: npm run test:e2e

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: playwright-results
          path: playwright-report/
```

## 10. MVP Testing Checklist

Before beta launch (Week 5), all critical paths must have:

- ✓ Unit tests written and passing (90%+ coverage)
- ✓ API route tests passing
- ✓ Integration tests passing
- ✓ E2E tests for complete workflows passing
- ✓ Performance tests meeting targets
- ✓ Security tests passing
- ✓ Accessibility tests passing (WCAG AA)
- ✓ Cross-browser tests passing (Chromium, Firefox, WebKit)
- ✓ Offline functionality tests passing
- ✓ Quota enforcement tests passing

**No Exceptions**: MVP launches with 90%+ test coverage on critical paths.

This completes the revised testing specifications for Next.js/Vitest stack.

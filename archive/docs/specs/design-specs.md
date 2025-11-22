# Design Specifications - Next.js/Shadcn Stack (4-Week MVP)

## 1. Design Principles

**Core Philosophy**

- Mode-specific visual language separates workflows (Create/Edit/Study)
- Minimal UI in Create Mode maximizes focus
- Instant change visibility in Edit Mode builds confidence
- Read-only Study Mode prevents accidental edits during learning
- Accessibility-first with WCAG AA compliance

**Design System Foundation**

- Base unit: 4px spacing grid (Tailwind spacing scale)
- Typography: `font-sans` (default), `font-mono` (code/timestamps)
- Type scale: `text-sm` to `text-4xl` with appropriate line heights
- Border radius: `rounded-sm` (2px), `rounded-md` (6px), `rounded-lg` (8px)
- Shadows: Shadcn UI elevation tokens

## 2. Color System

### Mode Colors (CSS Variables)

```css
/* app/globals.css */
:root {
  /* Create Mode - Blue */
  --mode-create: 217 91% 60%; /* #3B82F6 */
  --mode-create-foreground: 0 0% 100%;

  /* Edit Mode - Purple */
  --mode-edit: 271 81% 68%; /* #A855F7 */
  --mode-edit-foreground: 0 0% 100%;

  /* Study Mode - Green */
  --mode-study: 160 84% 39%; /* #10B981 */
  --mode-study-foreground: 0 0% 100%;
}

.dark {
  --mode-create: 217 91% 60%;
  --mode-edit: 271 81% 68%;
  --mode-study: 160 84% 39%;
}
```

### Semantic Colors (Shadcn Tokens)

```css
:root {
  --background: 0 0% 100%;
  --foreground: 222.2 84% 4.9%;

  --card: 0 0% 100%;
  --card-foreground: 222.2 84% 4.9%;

  --popover: 0 0% 100%;
  --popover-foreground: 222.2 84% 4.9%;

  --primary: 222.2 47.4% 11.2%;
  --primary-foreground: 210 40% 98%;

  --secondary: 210 40% 96.1%;
  --secondary-foreground: 222.2 47.4% 11.2%;

  --muted: 210 40% 96.1%;
  --muted-foreground: 215.4 16.3% 46.9%;

  --accent: 210 40% 96.1%;
  --accent-foreground: 222.2 47.4% 11.2%;

  --destructive: 0 84.2% 60.2%;
  --destructive-foreground: 210 40% 98%;

  --border: 214.3 31.8% 91.4%;
  --input: 214.3 31.8% 91.4%;
  --ring: 222.2 84% 4.9%;

  --radius: 0.5rem;
}

.dark {
  --background: 222.2 84% 4.9%;
  --foreground: 210 40% 98%;

  --card: 222.2 84% 4.9%;
  --card-foreground: 210 40% 98%;

  /* ... dark mode values ... */
}
```

### Diff Colors (Edit Mode Inline Diff)

```css
:root {
  /* Additions */
  --diff-addition-bg: 142 76% 86%; /* #86EFAC */
  --diff-addition-fg: 142 71% 25%; /* Dark green */

  /* Deletions */
  --diff-deletion-bg: 0 86% 86%; /* #FCA5A5 */
  --diff-deletion-fg: 0 72% 35%; /* Dark red */

  /* Unchanged */
  --diff-unchanged-bg: 214.3 31.8% 91.4%;
  --diff-unchanged-fg: 215.4 16.3% 46.9%;
}

.dark {
  --diff-addition-bg: 142 71% 20%;
  --diff-addition-fg: 142 76% 86%;

  --diff-deletion-bg: 0 72% 30%;
  --diff-deletion-fg: 0 86% 86%;

  --diff-unchanged-bg: 217.2 32.6% 17.5%;
  --diff-unchanged-fg: 215 20.2% 65.1%;
}
```

## 3. Three-Mode Architecture (MVP)

### Mode Selector Component

```typescript
// components/mode-selector.tsx
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

interface ModeSelectorProps {
  currentMode: "create" | "edit" | "study";
  onModeChange: (mode: "create" | "edit" | "study") => void;
}

export function ModeSelector({ currentMode, onModeChange }: ModeSelectorProps) {
  return (
    <div className="flex gap-2 p-1 bg-muted rounded-lg">
      <Button
        variant={currentMode === "create" ? "default" : "ghost"}
        size="sm"
        onClick={() => onModeChange("create")}
        className={cn(
          "transition-colors duration-300",
          currentMode === "create" && "bg-[hsl(var(--mode-create))] text-white"
        )}
      >
        Create
      </Button>
      <Button
        variant={currentMode === "edit" ? "default" : "ghost"}
        size="sm"
        onClick={() => onModeChange("edit")}
        className={cn(
          "transition-colors duration-300",
          currentMode === "edit" && "bg-[hsl(var(--mode-edit))] text-white"
        )}
      >
        Edit
      </Button>
      <Button
        variant={currentMode === "study" ? "default" : "ghost"}
        size="sm"
        onClick={() => onModeChange("study")}
        className={cn(
          "transition-colors duration-300",
          currentMode === "study" && "bg-[hsl(var(--mode-study))] text-white"
        )}
      >
        Study
      </Button>
    </div>
  );
}
```

**Visual Design**:

- **Type**: 3-way segmented control (not binary switch)
- **Position**: Top bar (desktop), bottom (mobile)
- **Height**: 56px container, 40px buttons
- **Active state**: Mode color background + white text
- **Animation**: 300ms transitions with smooth color fade
- **Accessibility**: Proper button semantics, keyboard navigation

### Edit or Study Dialog

```typescript
// components/notes/edit-study-dialog.tsx
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { FileEdit, BookOpen } from "lucide-react";

interface EditStudyDialogProps {
  open: boolean;
  note: {
    title: string;
    createdAt: Date;
    updatedAt: Date;
    wordCount: number;
  };
  onEdit: () => void;
  onStudy: () => void;
}

export function EditStudyDialog({
  open,
  note,
  onEdit,
  onStudy,
}: EditStudyDialogProps) {
  return (
    <AlertDialog open={open}>
      <AlertDialogContent className="sm:max-w-[600px]">
        <AlertDialogHeader>
          <AlertDialogTitle>
            How do you want to open this note?
          </AlertDialogTitle>
          <AlertDialogDescription className="space-y-2">
            <div className="text-sm text-muted-foreground">
              <p>Created: {note.createdAt.toLocaleDateString()}</p>
              <p>Last edited: {note.updatedAt.toLocaleDateString()}</p>
              <p>Word count: {note.wordCount}</p>
            </div>
          </AlertDialogDescription>
        </AlertDialogHeader>

        <div className="grid grid-cols-2 gap-4 py-4">
          <AlertDialogAction
            onClick={onEdit}
            className="h-24 flex-col gap-2 bg-[hsl(var(--mode-edit))] hover:bg-[hsl(var(--mode-edit))]/90"
          >
            <FileEdit className="h-6 w-6" />
            <span>Edit this note</span>
          </AlertDialogAction>

          <AlertDialogAction
            onClick={onStudy}
            className="h-24 flex-col gap-2 bg-[hsl(var(--mode-study))] hover:bg-[hsl(var(--mode-study))]/90"
          >
            <BookOpen className="h-6 w-6" />
            <span>Study this note</span>
          </AlertDialogAction>
        </div>
      </AlertDialogContent>
    </AlertDialog>
  );
}
```

**Visual Design**:

- **Trigger**: Opening any existing note
- **Layout**: Modal dialog (600px desktop, 90vw mobile)
- **Buttons**: Large (96px height) with icons and text
- **Metadata**: Created, last edited, word count in muted text
- **Actions**: Click button → Opens note in selected mode

## 4. Core Components (MVP)

### Rich Text Editor (Tiptap)

```typescript
// components/editor/tiptap-editor.tsx
"use client";

import { useEditor, EditorContent } from "@tiptap/react";
import StarterKit from "@tiptap/starter-kit";
import Placeholder from "@tiptap/extension-placeholder";
import { cn } from "@/lib/utils";

interface TiptapEditorProps {
  content: JSONContent;
  mode: "create" | "edit" | "study";
  onUpdate?: (content: JSONContent) => void;
}

export function TiptapEditor({ content, mode, onUpdate }: TiptapEditorProps) {
  const editor = useEditor({
    extensions: [
      StarterKit,
      Placeholder.configure({
        placeholder: "Start typing your notes...",
      }),
    ],
    content,
    editable: mode !== "study",
    onUpdate: ({ editor }) => {
      onUpdate?.(editor.getJSON());
    },
  });

  return (
    <div
      className={cn(
        "w-full max-w-[900px] mx-auto px-8",
        "prose prose-lg dark:prose-invert",
        mode === "create" && "[--tw-prose-primary:hsl(var(--mode-create))]",
        mode === "edit" && "[--tw-prose-primary:hsl(var(--mode-edit))]",
        mode === "study" && "[--tw-prose-primary:hsl(var(--mode-study))]"
      )}
    >
      <EditorContent editor={editor} />
    </div>
  );
}
```

**Styling**:

- **Container**: Max-width 900px, centered, 32px padding
- **Font**: `prose-lg` (18px) with 1.6 line-height
- **Placeholder**: Italic, `text-muted-foreground`
- **Selection**: Mode-specific color with 20% opacity
- **States**: Loading (skeleton), empty (placeholder), disabled (Study)

### AI Autocomplete Popup

```typescript
// components/editor/autocomplete-popup.tsx
"use client";

import {
  Command,
  CommandGroup,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { Popover, PopoverContent } from "@/components/ui/popover";

interface AutocompletePopupProps {
  open: boolean;
  suggestions: string[];
  position: { top: number; left: number };
  selectedIndex: number;
  onSelect: (suggestion: string) => void;
}

export function AutocompletePopup({
  open,
  suggestions,
  position,
  selectedIndex,
  onSelect,
}: AutocompletePopupProps) {
  return (
    <Popover open={open}>
      <PopoverContent
        className="w-[300px] p-0"
        style={{ top: position.top + 4, left: position.left }}
      >
        <Command>
          <CommandList>
            <CommandGroup>
              {suggestions.slice(0, 5).map((suggestion, index) => (
                <CommandItem
                  key={suggestion}
                  onSelect={() => onSelect(suggestion)}
                  className={cn(selectedIndex === index && "bg-accent")}
                >
                  {suggestion}
                </CommandItem>
              ))}
            </CommandGroup>
          </CommandList>
        </Command>
      </PopoverContent>
    </Popover>
  );
}
```

**Behavior**:

- **Trigger**: 150ms typing pause, 3+ characters
- **Active in**: Create + Edit modes only
- **Position**: 4px below cursor
- **Max suggestions**: 5 visible, scrollable
- **Keyboard**: Arrow keys, Enter/Tab, Escape

### Inline Diff View (Edit Mode Only)

```typescript
// components/editor/inline-diff.tsx
"use client";

import { Button } from "@/components/ui/button";
import { Eye, Save, Trash } from "lucide-react";
import { useMemo } from "react";
import { diff_match_patch } from "diff-match-patch";

interface InlineDiffProps {
  currentContent: string;
  savedContent: string;
  onSave: () => void;
  onDiscard: () => void;
}

export function InlineDiff({
  currentContent,
  savedContent,
  onSave,
  onDiscard,
}: InlineDiffProps) {
  const diff = useMemo(() => {
    const dmp = new diff_match_patch();
    const diffs = dmp.diff_main(savedContent, currentContent);
    dmp.diff_cleanupSemantic(diffs);
    return diffs;
  }, [currentContent, savedContent]);

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <Eye className="h-4 w-4" />
        <span className="text-sm font-medium">Changes since last save</span>
      </div>

      <div className="rounded-lg border p-4 space-y-1">
        {diff.map(([operation, text], index) => (
          <span
            key={index}
            className={cn(
              operation === 1 &&
                "bg-[hsl(var(--diff-addition-bg))] text-[hsl(var(--diff-addition-fg))]",
              operation === -1 &&
                "bg-[hsl(var(--diff-deletion-bg))] text-[hsl(var(--diff-deletion-fg))] line-through",
              operation === 0 && "text-muted-foreground"
            )}
          >
            {text}
          </span>
        ))}
      </div>

      <div className="flex gap-2">
        <Button onClick={onSave} className="gap-2">
          <Save className="h-4 w-4" />
          Save now
        </Button>
        <Button onClick={onDiscard} variant="outline" className="gap-2">
          <Trash className="h-4 w-4" />
          Discard changes
        </Button>
      </div>
    </div>
  );
}
```

**Visual Design**:

- **Trigger**: "View Changes" button in Edit Mode toolbar
- **Layout**: Inline within editor, full width
- **Highlighting**: Additions (green bg), deletions (red bg + strikethrough), unchanged (gray)
- **Actions**: Save now, Discard changes, Continue editing
- **Performance**: Debounced 500ms, <200ms calculation

### Key Terms Sidebar (Study Mode Only)

```typescript
// components/study/key-terms-sidebar.tsx
"use client";

import { ScrollArea } from "@/components/ui/scroll-area";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Download, Sparkles } from "lucide-react";

interface KeyTerm {
  term: string;
  context: string;
  importance: "high" | "medium" | "low";
  position: number;
}

interface KeyTermsSidebarProps {
  terms: KeyTerm[];
  quotaRemaining: number | null;
  onSpotTerms: () => void;
  onJumpTo: (position: number) => void;
  onExport: () => void;
}

export function KeyTermsSidebar({
  terms,
  quotaRemaining,
  onSpotTerms,
  onJumpTo,
  onExport,
}: KeyTermsSidebarProps) {
  return (
    <aside className="w-[360px] border-l bg-card">
      <div className="p-4 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold">Key Terms</h3>
          {quotaRemaining !== null && (
            <Badge variant="secondary">{quotaRemaining} remaining</Badge>
          )}
        </div>

        <Button onClick={onSpotTerms} className="w-full gap-2">
          <Sparkles className="h-4 w-4" />
          Spot Key Terms
        </Button>

        <ScrollArea className="h-[calc(100vh-200px)]">
          <div className="space-y-3">
            {terms.map((term, index) => (
              <button
                key={index}
                onClick={() => onJumpTo(term.position)}
                className="w-full text-left p-3 rounded-lg border hover:bg-accent transition-colors"
              >
                <div className="flex items-start justify-between gap-2">
                  <span className="font-medium">{term.term}</span>
                  <Badge
                    variant={
                      term.importance === "high"
                        ? "destructive"
                        : term.importance === "medium"
                        ? "default"
                        : "secondary"
                    }
                  >
                    {term.importance}
                  </Badge>
                </div>
                <p className="text-sm text-muted-foreground mt-1">
                  {term.context}
                </p>
              </button>
            ))}
          </div>
        </ScrollArea>

        {terms.length > 0 && (
          <Button onClick={onExport} variant="outline" className="w-full gap-2">
            <Download className="h-4 w-4" />
            Export key terms
          </Button>
        )}
      </div>
    </aside>
  );
}
```

**Visual Design**:

- **Layout**: Fixed right sidebar (360px desktop), bottom drawer (mobile)
- **Header**: Title + quota badge
- **Action button**: "Spot Key Terms" with AI icon
- **Term list**: Clickable cards with term, context snippet, importance badge
- **Export**: Download button at bottom

## 5. Application Screens (MVP)

### 2-Screen Onboarding

```typescript
// app/(auth)/onboarding/page.tsx
"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";

export default function OnboardingPage() {
  const [step, setStep] = useState(1);

  if (step === 1) {
    return (
      <div className="container max-w-4xl py-16">
        <h1 className="text-4xl font-bold text-center mb-8">
          Welcome to NEXLY RN
        </h1>
        <p className="text-xl text-center text-muted-foreground mb-12">
          Three modes for better learning
        </p>

        <div className="grid grid-cols-3 gap-6 mb-12">
          <Card className="p-6 text-center space-y-4">
            <div className="w-12 h-12 mx-auto bg-[hsl(var(--mode-create))] rounded-lg" />
            <h3 className="font-semibold">Create</h3>
            <p className="text-sm text-muted-foreground">
              Fast capture with AI autocomplete
            </p>
          </Card>

          <Card className="p-6 text-center space-y-4">
            <div className="w-12 h-12 mx-auto bg-[hsl(var(--mode-edit))] rounded-lg" />
            <h3 className="font-semibold">Edit</h3>
            <p className="text-sm text-muted-foreground">
              Revise with instant change preview
            </p>
          </Card>

          <Card className="p-6 text-center space-y-4">
            <div className="w-12 h-12 mx-auto bg-[hsl(var(--mode-study))] rounded-lg" />
            <h3 className="font-semibold">Study</h3>
            <p className="text-sm text-muted-foreground">
              AI-powered key term spotting
            </p>
          </Card>
        </div>

        <Button onClick={() => setStep(2)} className="w-full" size="lg">
          Next
        </Button>
      </div>
    );
  }

  return (
    <div className="container max-w-4xl py-16">
      <h2 className="text-3xl font-bold text-center mb-8">Try it now</h2>
      {/* Interactive demo with pre-seeded note */}
      <Button
        onClick={() => router.push("/notes")}
        className="w-full"
        size="lg"
      >
        Start creating
      </Button>
    </div>
  );
}
```

### Note Library

```typescript
// app/(dashboard)/notes/page.tsx
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Plus, Search } from "lucide-react";
import { NoteCard } from "@/components/notes/note-card";

export default function NotesPage() {
  return (
    <div className="container py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-bold">My Notes</h1>
          <p className="text-muted-foreground">24 notes</p>
        </div>
        <Button className="gap-2">
          <Plus className="h-4 w-4" />
          New Note
        </Button>
      </div>

      <div className="flex items-center gap-4 mb-8">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Input placeholder="Search notes..." className="pl-10" />
        </div>
        <Select defaultValue="updated">
          <SelectTrigger className="w-[180px]">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="updated">Last edited</SelectItem>
            <SelectItem value="created">Created date</SelectItem>
            <SelectItem value="title">Title</SelectItem>
          </SelectContent>
        </Select>
      </div>

      <div className="space-y-4">{/* Note cards */}</div>
    </div>
  );
}
```

## 6. Responsive Design

### Breakpoints (Tailwind)

```typescript
// tailwind.config.ts
export default {
  theme: {
    screens: {
      sm: "640px", // Mobile landscape
      md: "768px", // Tablet
      lg: "1024px", // Desktop
      xl: "1280px", // Large desktop
      "2xl": "1536px", // Extra large
    },
  },
};
```

### Responsive Adaptations

```typescript
// Example: Responsive mode selector
<div className="flex lg:flex-row flex-col lg:gap-2 gap-4">
  {/* Horizontal on desktop, vertical on mobile */}
</div>

// Example: Responsive sidebar
<aside className="lg:w-[360px] lg:block hidden">
  {/* Sidebar on desktop */}
</aside>
<Sheet> {/* Mobile drawer */}
  <SheetContent side="bottom">
    {/* Sidebar content */}
  </SheetContent>
</Sheet>
```

## 7. Accessibility (MVP)

### Shadcn Components (Built-in A11y)

- All Shadcn components have proper ARIA attributes
- Keyboard navigation built-in
- Focus management automatic
- Screen reader support included

### Custom Accessibility

```typescript
// Mode selector with ARIA
<div role="tablist" aria-label="Note modes">
  <Button
    role="tab"
    aria-selected={currentMode === "create"}
    aria-controls="editor-panel"
  >
    Create
  </Button>
</div>

// Focus indicators (automatic with Shadcn)
// All interactive elements have visible focus rings
```

### Keyboard Shortcuts

```typescript
// hooks/use-keyboard-shortcuts.ts
"use client";

import { useEffect } from "react";

export function useKeyboardShortcuts() {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Save: Cmd/Ctrl + S
      if ((e.metaKey || e.ctrlKey) && e.key === "s") {
        e.preventDefault();
        // Save logic
      }

      // Bold: Cmd/Ctrl + B
      if ((e.metaKey || e.ctrlKey) && e.key === "b") {
        e.preventDefault();
        // Bold logic
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);
}
```

## 8. Animation Guidelines

### Transitions (Tailwind + Shadcn)

```typescript
// Mode transitions
<Button className="transition-colors duration-300">

// Modal animations (built into Shadcn Dialog)
<AlertDialog>
  {/* Automatic fade + scale animations */}
</AlertDialog>

// Micro-interactions
<Button className="transition-all hover:scale-105 active:scale-95">
```

### Animation Utilities

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      animation: {
        "fade-in": "fadeIn 150ms ease-in",
        "slide-in": "slideIn 200ms ease-out",
      },
      keyframes: {
        fadeIn: {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
        slideIn: {
          "0%": { transform: "translateY(-10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
      },
    },
  },
};
```

## 9. Dark Mode (next-themes)

### Theme Provider

```typescript
// components/theme-provider.tsx
"use client";

import { ThemeProvider as NextThemesProvider } from "next-themes";

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <NextThemesProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      {children}
    </NextThemesProvider>
  );
}
```

### Theme Toggle

```typescript
// components/theme-toggle.tsx
"use client";

import { Moon, Sun } from "lucide-react";
import { useTheme } from "next-themes";
import { Button } from "@/components/ui/button";

export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
      <span className="sr-only">Toggle theme</span>
    </Button>
  );
}
```

## 10. Implementation Notes

### Shadcn UI Installation

```bash
# Initialize Shadcn
npx shadcn@latest init

# Add components as needed
npx shadcn@latest add button
npx shadcn@latest add dialog
npx shadcn@latest add alert-dialog
npx shadcn@latest add command
npx shadcn@latest add popover
npx shadcn@latest add scroll-area
npx shadcn@latest add toast
npx shadcn@latest add badge
npx shadcn@latest add card
npx shadcn@latest add input
npx shadcn@latest add select
```

### Component Structure

```
components/
├── ui/              # Shadcn components (auto-generated)
│   ├── button.tsx
│   ├── dialog.tsx
│   └── ...
├── editor/          # Editor components
│   ├── tiptap-editor.tsx
│   ├── autocomplete-popup.tsx
│   └── inline-diff.tsx
├── notes/           # Note components
│   ├── note-list.tsx
│   ├── note-card.tsx
│   └── edit-study-dialog.tsx
└── study/           # Study mode components
    └── key-terms-sidebar.tsx
```

## 11. Performance Targets (MVP)

### Critical Metrics

- Autocomplete: <100ms
- Mode transitions: <50ms
- Dialog display: <100ms
- Inline diff: <200ms
- Key term spotting: <5s

### Optimization

- Server Components for initial renders
- Lazy load Tiptap editor
- Debounce autocomplete (150ms)
- Debounce diff calculation (500ms)
- Virtual scrolling for long term lists

## 12. MVP Design Checklist

Before beta launch (Week 5):

- ✓ Three-mode architecture with visual indicators
- ✓ Edit or Study Dialog (Shadcn AlertDialog)
- ✓ Autocomplete popup (Shadcn Command + Popover)
- ✓ Inline diff view (Edit Mode only)
- ✓ Key terms sidebar (Study Mode only)
- ✓ 2-screen onboarding
- ✓ Note library (simple list view)
- ✓ Mobile responsive (Tailwind breakpoints)
- ✓ WCAG AA compliant (Shadcn built-in)
- ✓ Dark mode support (next-themes)

This completes the revised design specifications for Next.js/Shadcn UI stack.

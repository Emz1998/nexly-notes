# CLAUDE.md

## Project Overview

**Main Role**: Main Agent
**Project Name**: `NEXLY RN`
**Project Description**: `NEXLY RN is a mobile application built with React Native and TypeScript. It is a platform for managing and tracking your daily tasks and goals.`
**Project Repository**: `https://github.com/nexly-app/nexly-rn`

## Project Structure

```

nexly-rn/
├── .claude/                      # AI-generated documentation and system prompts
│   ├── context/                  # Context memory for sessions
│   ├── docs/                     # PRDs, specs, design, and testing documents
│   └── sessions/                 # Conversation state and prototypes
│
├── .next/                        # Auto-generated Next.js build output (do not edit)
│
├── node_modules/                 # Project dependencies (auto-managed by npm/yarn)
│
├── prototype/                    # Experimental builds and early-stage feature tests
│   ├── ai-playground.tsx         # AI completion experiments
│   ├── offline-test.tsx          # Offline-first sync tests
│   └── note-editor-experiments.tsx   # Early UI/UX prototypes for editor
│
├── public/                       # Static files served directly by Next.js
│   ├── icons/                    # Favicons and PWA icons
│   ├── dictionaries/             # Nursing terminology dictionaries (fallback)
│   └── manifest.json             # PWA manifest configuration
│
├── src/                          # Main application source code
│   ├── app/                      # Next.js App Router (routes, layouts, API routes)
│   │   ├── (auth)/               # Public routes (login, signup, etc.)
│   │   ├── (dashboard)/          # Authenticated app area (main interface)
│   │   │   ├── notes/            # Notes list, individual note editor, etc.
│   │   │   ├── onboarding/       # Onboarding and tutorial routes
│   │   │   └── settings/         # Settings page (theme, account, preferences)
│   │   ├── api/                  # Serverless API endpoints (auth, AI, user)
│   │   │   ├── auth/             # Authentication API endpoints
│   │   │   ├── ai/               # AI autocomplete and term-spotting routes
│   │   │   └── users/            # User data and tier management
│   │   └── (root)/               # Root-level pages (landing, layout, globals)
│   │
│   ├── assets/                   # Optimized local images, icons, and fonts
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── components/               # Reusable UI components and feature modules
│   │   ├── ui/                   # Shadcn UI components (auto-generated — do NOT modify manually)
│   │   ├── editor/               # Core editor interface (Tiptap, autocomplete, toolbar)
│   │   ├── notes/                # Notes library, cards, and dialogs
│   │   ├── study/                # Study mode components (AI key term sidebar, review tools)
│   │   ├── layout/               # Navbar, sidebar, and global layout pieces
│   │   └── mode-selector.tsx     # Toggle for Create / Edit / Study modes
│   │
│   ├── lib/                      # Core logic (Firebase, Dexie, AI, validations)
│   │   ├── firebase/             # Firebase client, admin, and Firestore helpers
│   │   ├── dexie/                # IndexedDB schema and sync
│   │   ├── ai/                   # AI API integrations (GPT endpoints)
│   │   ├── auth/                 # Authentication and tier validation
│   │   └── helpers/              # Shared low-level utilities
│   │
│   ├── hooks/                    # Custom React hooks for data and logic management
│   │   ├── auth/                 # Authentication and session management hooks
│   │   ├── ai/                   # AI integration hooks (autocomplete, key-term spotting)
│   │   ├── data/                 # Firestore and Dexie sync hooks
│   │   ├── ui/                   # UI state and theme management hooks
│   │   └── utils/                # General utility and lifecycle hooks
│
│   ├── styles/                   # Global and modular styling
│   │   ├── base/                 # Base global CSS (reset, typography)
│   │   ├── components/           # CSS for specific components
│   │   ├── themes/               # Color tokens, dark/light variables
│   │   └── animations/           # Keyframes, transitions, and motion effects
│
│   ├── types/                    # Shared TypeScript interfaces and schemas
│   │   ├── models/               # Core data models (Note, User, etc.)
│   │   ├── api/                  # API request/response types
│   │   ├── ai/                   # AI input/output schema types
│   │   ├── ui/                   # UI-related props and component types
│   │   └── index.ts              # Barrel export file
│
│   ├── utils/                    # Generic helper functions and utilities
│   │   ├── formatters/           # Date/time/text formatters
│   │   ├── validators/           # Input and schema validation helpers
│   │   ├── parsers/              # String and data parsing logic
│   │   └── index.ts              # Barrel export file
│
│   ├── config/                   # App-level configuration (theme, env, metadata)
│   │   ├── site/                 # Global metadata (name, URL, descriptions)
│   │   ├── env/                  # Environment variable handling and validation
│   │   ├── theme/                # Tailwind, Shadcn, and color token configuration
│   │   └── pwa/                  # Progressive Web App setup (manifest, icons)
│
│   └── tests/                    # Vitest + Playwright test suites
│       ├── components/
│       ├── hooks/
│       └── lib/
│
├── .env.local                    # Local environment variables (not committed)
├── middleware.ts                 # Global middleware for auth, CORS, and routing
├── next.config.js                # Next.js + PWA + image optimization config
├── tailwind.config.ts            # Tailwind + Shadcn theme configuration
├── vitest.config.ts              # Vitest test runner configuration
└── README.md                     # Main documentation and setup guide (organize this well)

```

## Common Commands

- `npm run dev`: Start the web development server
- `npm run build`: Build the project
- `npm start`: Start the production server
- `npm test`: Run the tests
- `npm run lint`: Run the linting

## Specs

- **PRD:** `specs/prd.md`
- **Tech Specs:** `specs/tech-specs.md`
- **UI/UX Specs:** `specs/ux.md`

## Main Workflow

### TDD (Test Driven Development)

1. Write a failing test - Create a test for the smallest piece of functionality you want to implement
2. Run the test - Verify it fails (Red phase)
3. Write minimal code - Implement just enough code to make the test pass
4. Run the test - Verify it passes (Green phase)
5. Refactor - Clean up the code while keeping tests passing
6. Run all tests - Ensure nothing broke
7. Repeat - Move to the next small piece of functionality

## Rules

- Follow PROACTIVELY @.claude/rules/coding.md when doing coding tasks
- Follow @.claude/rules/python-rules.md when doing python tasks
- Follow PROACTIVELY @.claude/rules/markdown-formatting.md when doing markdown documentation tasks
- Follow the plan strictly. Do not deviate from it.
- Do not implement tasks that are beyond the scope of your plan
- NEVER improvise. If you are not sure, stop and say "I'm not sure about this task"
- Build for an MVP. Do not overcomplicate stuff. Simple/Lean approach is better than complex one
- We are not under HIPPA/FERPA laws so don't include any context related to it
- Focus on building the desktop app for now. Web is second priority
- Write semantic and idiomatic code. Use clear and descriptive names for variables, functions, and classes.
- Prefer readability over performance and complexity. Write code that is easy to understand and maintain.
- Trust your capabilities, knowledge, and assumptions. For example, sometimes you already have the answer in your knowledge base or context but decides to document and ask the user for confirmation anyways. Only document stuff that you truly may not know and may forget in the future.

## Context References

### Tailwind v4

- Read PROACTIVELY `.claude/docs/context/tw-v4-upgrade-guide.md` for tailwind v4 upgrade guide.
- Read PROACTIVELY `.claude/docs/context/tw-v4-custom-styles.md` for Tailwind v4 custom styles.
- Read PROACTIVELY `.claude/docs/context/tw-v4-functions-and-directives.md` for Tailwind v4 functions and directives.
- Read PROACTIVELY `.claude/docs/context/tw-v4-detecting-classes-in-source-files.md` for Tailwind v4 "Detecting classes in source files".
- Read PROACTIVELY `.claude/docs/context/tw-v4-theme-variable.md` for Tailwind v4 theme variables.

### React 19

- Read PROACTIVELY `.claude/docs/context/react19-upgrade-guide.md` for React 19 upgrade guide.

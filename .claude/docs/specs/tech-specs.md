# Technical Specifications - NEXLY RN

## 1. System Overview

**Architecture**: Progressive Web App (PWA) with Next.js
**Primary Stack**: Next.js 15.1 + React 19.1 + TypeScript 5.9 + Tailwind 4.1 + Tiptap 3.4
**Deployment**: Vercel (recommended) or Firebase Hosting
**Core Concept**: Three-mode workflow (Create, Edit, Study) separating fast capture, confident revision, and AI-powered key term identification

### Technology Stack

- **Frontend**: Next.js 15.1 with App Router, React 19.1, TypeScript 5.9
- **UI Framework**: Shadcn UI + Radix UI primitives, Tailwind CSS 4.1
- **Rich Text**: Tiptap 3.4 with custom extensions
- **State Management**: Zustand 5.0.8 + Immer 10.1.3
- **Authentication**: Firebase Auth (Client SDK + Admin SDK)
- **Database**: Firestore (primary) + Dexie (IndexedDB for offline)
- **AI Integration**: OpenAI API via Next.js API routes
- **PWA**: next-pwa 5.6.0 for offline support

---

## 2. Architecture Decisions

### Frontend Architecture

**Next.js App Router Pattern**
- Server Components for initial page loads (SEO, performance)
- Client Components for interactive features (`'use client'` directive)
- API Routes for serverless backend functions
- Middleware for authentication and routing guards

**Component Strategy**
- Shadcn UI components in `/components/ui` (auto-generated, do not modify)
- Custom app components in `/components` (editor, notes, study)
- Server Components by default, Client Components only when needed

**State Management**
- Zustand for client-side state (editor mode, preferences, quota)
- React Server Components for server-side data fetching
- Optimistic UI updates with `React.useOptimistic`
- LocalStorage persistence for user preferences

### Backend Architecture

**Hybrid Next.js + Firebase**
- Next.js API Routes for AI features and business logic
- Firebase Client SDK for direct Firestore access (real-time)
- Firebase Admin SDK for server-side operations (API routes)
- Firestore security rules enforce user isolation

**API Endpoints**
```
POST /api/auth/initialize       # Create user doc after signup
POST /api/ai/autocomplete        # GPT-4.1 nano autocomplete
POST /api/ai/spot-terms          # GPT-4o-mini key term spotting
GET  /api/users/quota            # Check usage quota
POST /api/users/update-tier      # Update subscription
```

---

## 3. Data Models

### Firestore Collections

#### Users Collection
**Path**: `/users/{userId}`

```typescript
interface UserProfile {
  userId: string;
  email: string;
  displayName: string;
  tier: "free" | "pro" | "team";

  usage: {
    autocompleteRequests: number;    // Free: 100/month
    keyTermSpottingUses: number;     // Free: 10/month
    resetDate: Timestamp;
  };

  settings: {
    theme: "light" | "dark" | "system";
    autoSave: boolean;
    defaultMode: "create" | "edit" | "study";
  };

  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

**Indexes**: `email`, `tier`, `createdAt`

#### Notes Collection
**Path**: `/users/{userId}/notes/{noteId}`

```typescript
interface Note {
  id: string;
  userId: string;
  title: string;
  content: JSONContent;              // Tiptap JSON document
  mode: "create" | "edit" | "study";

  metadata: {
    lectureDate?: Timestamp;
    courseCode?: string;              // e.g., "NURS 301"
    timestamps: Array<{
      time: string;                   // e.g., "14:23"
      position: number;
    }>;
  };

  tags: string[];

  stats: {
    wordCount: number;
    characterCount: number;
  };

  syncStatus: {
    lastSyncedAt: Timestamp;
    version: number;
    deviceId: string;
  };

  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

**Composite Indexes**:
- `userId` + `updatedAt` (note library sorting)
- `userId` + `metadata.courseCode` + `updatedAt` (filtering)
- `userId` + `tags` (tag filtering)

**Tiptap Content Structure**
```typescript
import { JSONContent } from "@tiptap/core";

// Tiptap stores content as ProseMirror JSON
const content: JSONContent = {
  type: "doc",
  content: [
    { type: "paragraph", content: [{ type: "text", text: "..." }] },
    { type: "heading", attrs: { level: 2 }, content: [...] }
  ]
};
```

#### Version Snapshots (Backend Only in MVP)
**Path**: `/users/{userId}/notes/{noteId}/snapshots/{snapshotId}`

```typescript
interface VersionSnapshot {
  id: string;
  noteId: string;
  content: JSONContent;
  mode: "create" | "edit" | "study";
  timestamp: Timestamp;

  changesSummary: {
    addedWords: number;
    removedWords: number;
  };

  snapshotType: "auto" | "manual" | "mode_switch";
}
```

**MVP Note**: Snapshots stored but **no UI** to view/manage them in 4-week MVP. Enables Fast-Follow features (Week 7-8).

**Retention Policy**:
- Free tier: Last 5 snapshots per note (auto-deleted)
- Pro tier: Unlimited snapshots
- Team tier: Unlimited + 3-year guarantee

### Dexie (IndexedDB) Schema

**Tables**: `notes`, `syncQueue`, `versionSnapshots`, `definitions`, `userPreferences`

```typescript
export class NexlyDatabase extends Dexie {
  notes!: Table<LocalNote, string>;
  syncQueue!: Table<SyncQueueItem, number>;
  versionSnapshots!: Table<LocalSnapshot, string>;

  constructor() {
    super("nexly_rn");
    this.version(1).stores({
      notes: "id, userId, updatedAt, [userId+updatedAt], *tags",
      syncQueue: "++id, createdAt, [operation+collection]",
      versionSnapshots: "id, [userId+noteId+timestamp], noteId, timestamp",
    });
  }
}
```

**Purpose**: Offline-first storage, sync queue, full-text search

---

## 4. Authentication & Security

### Authentication Flow

**Client-Side** (Firebase Client SDK)
- Email/password signup and login
- Session management with cookies (httpOnly, secure)
- Auto token refresh (1-hour expiry)

**Server-Side** (Firebase Admin SDK)
- Token verification in middleware and API routes
- User ID extraction from JWT tokens
- Route protection via middleware

**Token Verification Pattern**
```typescript
// middleware.ts or API routes
const token = request.headers.get("authorization")?.split("Bearer ")[1];
const decodedToken = await adminAuth.verifyIdToken(token);
const userId = decodedToken.uid;
```

### Firestore Security Rules

**Key Principles**:
- Users can only read/write their own data
- Snapshots are immutable (no updates allowed)
- User deletion prevented (soft delete only)
- Tier-based permissions for team features

```javascript
// Helper functions
function isAuthenticated() { return request.auth != null; }
function isOwner(userId) { return request.auth.uid == userId; }

// Users collection
match /users/{userId} {
  allow read, create, update: if isAuthenticated() && isOwner(userId);
  allow delete: if false;  // Prevent accidental deletion
}

// Notes subcollection
match /users/{userId}/notes/{noteId} {
  allow read, create, update, delete: if isAuthenticated() && isOwner(userId);

  // Snapshots (immutable)
  match /snapshots/{snapshotId} {
    allow read, create: if isAuthenticated() && isOwner(userId);
    allow update: if false;  // Immutable
    allow delete: if isAuthenticated() && isOwner(userId);
  }
}
```

### API Security

- HTTPS only (automatic with Vercel)
- Firebase Auth token validation on all API routes
- Input validation via Zod schemas
- Rate limiting per user (100 autocomplete/month, 10 key terms/month)
- No AI training on user data

---

## 5. AI Integration

### Autocomplete (GPT-4.1 nano)

**API Route**: `POST /api/ai/autocomplete`

**Request**: `{ context: string, cursorPosition: number }`
**Response**: `{ suggestions: string[], quotaRemaining: number }`

**Specifications**:
- Model: GPT-4.1 nano (fast, cost-effective)
- Performance target: <100ms
- Quota: 100 requests/month (Free), unlimited (Pro)
- Fallback: Local nursing dictionary (5000+ terms)

### Key Term Spotting (GPT-4o-mini)

**API Route**: `POST /api/ai/spot-terms`

**Request**: `{ noteId: string, content: JSONContent }`
**Response**:
```typescript
{
  terms: Array<{
    term: string;
    position: number;
    context: string;
    importance: "high" | "medium" | "low";
    reason: string;
  }>;
  quotaRemaining: number;
}
```

**Specifications**:
- Model: GPT-4o-mini with Structured Outputs
- Performance target: <5s for 3000-word note
- Quota: 10 uses/month (Free), unlimited (Pro)

### Quota Management

**Tracking**: Firestore `users` collection (`usage` field)
**Enforcement**: Client-side pre-check + Server-side validation
**Fallback**: Local dictionary for autocomplete, upgrade prompt for key terms

---

## 6. Offline & Sync Strategy

### Data Flow Pattern

1. **Write Path**: User edits → Dexie (instant) → Sync queue → Firestore (background)
2. **Read Path**: Dexie first (instant) → Firestore real-time updates (merge)
3. **Conflict Resolution**: Last-write-wins with version tracking

### Sync Queue

**Purpose**: Queue operations when offline, replay when online
**Retry Logic**: Max 5 retries with exponential backoff
**Operations**: `create`, `update`, `delete` for notes and snapshots

### PWA Configuration

**Manifest**: `/public/manifest.json` (installable app)
**Service Worker**: next-pwa with strategies:
- NetworkFirst for API calls
- CacheFirst for static assets
- StaleWhileRevalidate for pages

**Features**:
- Offline note editing
- Background sync for note updates
- Install prompt for desktop/mobile

---

## 7. Performance Optimization

### Next.js Optimizations

**Code Splitting**:
- Automatic route-based splitting
- Dynamic imports for heavy components (Tiptap editor)
- Lazy loading with `React.lazy` and `Suspense`

**Example**:
```typescript
const TiptapEditor = dynamic(() => import("@/components/editor/tiptap-editor"), {
  ssr: false,
  loading: () => <EditorSkeleton />
});
```

**Caching Strategy**:
- Server-side: Time-based ISR, Firestore query caching (5-min TTL)
- Client-side: Dexie for notes, Service Worker for static assets

### Performance Targets (MVP)

**Core Web Vitals**:
- First Contentful Paint (FCP): <1.5s
- Largest Contentful Paint (LCP): <2.5s
- Time to Interactive (TTI): <3.5s
- Cumulative Layout Shift (CLS): <0.1
- First Input Delay (FID): <100ms

**Feature Targets**:
- Autocomplete: <100ms (GPT-4.1 nano)
- Mode transitions: <50ms
- Inline diff: <200ms
- Key term spotting: <5s (GPT-4o-mini)

**Optimization Strategies**:
- Server Components for initial renders
- Debounce autocomplete (150ms)
- Debounce diff calculation (500ms)
- Virtual scrolling for long note lists
- Lighthouse score >90

---

## 8. Project Structure

```
nexly-rn/
├── src/app/                      # Next.js App Router
│   ├── (auth)/                   # Public routes (login, signup)
│   ├── (dashboard)/              # Authenticated app (notes, settings)
│   ├── api/                      # Serverless API routes
│   │   ├── auth/initialize/
│   │   ├── ai/autocomplete/
│   │   ├── ai/spot-terms/
│   │   └── users/quota/
│   ├── layout.tsx                # Root layout
│   └── globals.css               # Global styles
│
├── src/components/               # UI components
│   ├── ui/                       # Shadcn components (auto-generated)
│   ├── editor/                   # Tiptap editor, autocomplete, toolbar
│   ├── notes/                    # Notes library, cards, dialogs
│   └── study/                    # Study mode (key terms sidebar)
│
├── src/lib/                      # Core logic
│   ├── firebase/                 # Client + Admin SDK setup
│   ├── dexie/                    # IndexedDB schema + sync
│   ├── ai/                       # OpenAI integrations
│   └── validations.ts            # Zod schemas
│
├── src/hooks/                    # Custom React hooks
│   ├── auth/                     # Auth hooks
│   ├── ai/                       # AI integration hooks
│   └── data/                     # Firestore + Dexie sync hooks
│
├── src/types/                    # TypeScript types
│   ├── models/                   # Note, User, Snapshot interfaces
│   └── api/                      # API request/response types
│
├── public/                       # Static files
│   ├── manifest.json             # PWA manifest
│   ├── icons/                    # App icons
│   └── dictionaries/             # Nursing terms (fallback)
│
├── middleware.ts                 # Auth middleware
├── next.config.js                # Next.js + PWA config
└── tailwind.config.ts            # Tailwind + Shadcn theme
```

---

## 9. Environment Variables

```env
# Firebase (Client - Public)
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NEXT_PUBLIC_FIREBASE_APP_ID=

# Firebase Admin (Server-only)
FIREBASE_ADMIN_PROJECT_ID=
FIREBASE_ADMIN_CLIENT_EMAIL=
FIREBASE_ADMIN_PRIVATE_KEY=

# OpenAI
OPENAI_API_KEY=

# App Config
NEXT_PUBLIC_APP_URL=https://nexly-rn.vercel.app
```

---

## 10. Dependencies

### Core Dependencies
```json
{
  "next": "15.1.0",
  "react": "19.1.1",
  "typescript": "5.9.3",
  "@tiptap/react": "3.4.2",
  "firebase": "^10.x",
  "firebase-admin": "^12.x",
  "openai": "5.23.1",
  "dexie": "4.2.0",
  "zustand": "5.0.8",
  "tailwindcss": "4.1.13",
  "next-pwa": "5.6.0",
  "zod": "3.25.67"
}
```

### Dev Dependencies
```json
{
  "vitest": "3.2.4",
  "@testing-library/react": "16.3.0",
  "playwright": "1.55.0",
  "prettier": "^3.x"
}
```

---

## 11. Testing Strategy

### Unit Testing (Vitest)
- Component tests for UI components
- Hook tests for custom React hooks
- Utility function tests

### E2E Testing (Playwright)
- Critical user flows (signup, create note, AI features)
- Cross-browser testing (Chromium, Firefox, WebKit)

---

## 12. Deployment

### Vercel (Recommended)
- Automatic deployments on `git push`
- Environment variables in dashboard
- Edge functions for API routes
- Global CDN for static assets

### Firebase Hosting (Alternative)
- `firebase deploy --only hosting`
- Custom domain support
- SSL certificates included

---

## 13. 4-Week Build Timeline

### Week 1: Foundation
- Next.js setup + App Router
- Firebase integration (Client + Admin SDK)
- Shadcn UI components
- Auth flow (signup, login, logout)
- Mode switching logic
- Edit/Study dialog

### Week 2: AI Autocomplete
- Tiptap editor integration
- AI autocomplete API route (GPT-4.1 nano)
- Auto-save with version snapshots (backend only)
- Quota tracking
- Local dictionary fallback

### Week 3: Diff & Key Terms
- Inline diff button + diff view (Edit Mode)
- AI Key Term Spotting API route (GPT-4o-mini)
- Key terms sidebar UI
- Export key terms list

### Week 4: Polish & Launch
- Note library + search
- 2-screen onboarding
- PWA configuration
- Performance optimization
- E2E testing
- Deployment to Vercel

---

## 14. Fast-Follow Features (Week 5-8)

### Week 5-6
- Templates API
- Shorthand expansion
- Definition lookup

### Week 7-8
- Cloze generation
- Full version history UI
- Side-by-side snapshot comparison

### Month 2+
- Export notes (PDF, Markdown)
- Analytics dashboard
- Team collaboration features

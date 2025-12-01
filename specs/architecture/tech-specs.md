# Technical Specifications - NEXLY RN

## 1. System Overview

**Architecture**: Progressive Web App (PWA) with Next.js
**Primary Stack**: Next.js 15.1 + React 19.1 + TypeScript 5.9 + Tailwind 4.1 + Tiptap 3.4
**Deployment**: Vercel (recommended) or Firebase Hosting
**Core Concept**: Distraction-free note-taking with AI-powered medical autocomplete, nursing-specific templates, and bulletproof offline sync

### Technology Stack

- **Frontend**: Next.js 15.1 with App Router, React 19.1, TypeScript 5.9
- **UI Framework**: Shadcn UI + Radix UI primitives, Tailwind CSS 4.1
- **Rich Text**: Tiptap 3.4 with custom extensions
- **State Management**: Zustand 5.0.8 + Immer 10.1.3
- **Authentication**: Firebase Auth (Client SDK + Admin SDK)
- **Database**: Firestore (primary) + Dexie (IndexedDB for offline)
- **AI Integration**: OpenAI API (GPT-4.1 nano) via Next.js API routes
- **Payment Processing**: Stripe (subscriptions and checkout)
- **PWA**: next-pwa 5.6.0 for offline support
- **Analytics**: Vercel Analytics
- **Error Tracking**: Sentry

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
- Custom app components in `/components` (editor, notes, layout)
- Server Components by default, Client Components only when needed

**State Management**
- Zustand for client-side state (editor state, preferences, quota)
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
POST /api/ai/autocomplete       # GPT-4.1 nano autocomplete
GET  /api/users/quota           # Check usage quota
POST /api/users/update-tier     # Update subscription
POST /api/stripe/checkout       # Create Stripe checkout session
POST /api/stripe/webhook        # Handle Stripe webhooks
POST /api/stripe/portal         # Create customer portal session
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
  tier: "free" | "pro";

  usage: {
    autocompleteRequests: number;    // Free: 100/month
    resetDate: Timestamp;
  };

  settings: {
    theme: "light" | "dark" | "system";
    autoSave: boolean;
  };

  stripe: {
    customerId?: string;
    subscriptionId?: string;
    subscriptionStatus?: "active" | "canceled" | "past_due";
    currentPeriodEnd?: Timestamp;
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

  category: "pharmacology" | "med-surg" | "pediatrics" | "ob" | "mental-health" | "clinical-rotation" | "other";

  metadata: {
    wordCount: number;
    characterCount: number;
  };

  syncStatus: {
    lastSyncedAt: Timestamp;
    version: number;
    deviceId: string;
  };

  isDeleted: boolean;                // Soft delete flag
  deletedAt?: Timestamp;             // When moved to trash

  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

**Composite Indexes**:
- `userId` + `isDeleted` + `updatedAt` (note library sorting)
- `userId` + `isDeleted` + `category` + `updatedAt` (category filtering)
- `userId` + `isDeleted` + `deletedAt` (trash management)

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

#### Version Snapshots (Backend Only - No UI in MVP)
**Path**: `/users/{userId}/notes/{noteId}/snapshots/{snapshotId}`

```typescript
interface VersionSnapshot {
  id: string;
  noteId: string;
  content: JSONContent;
  timestamp: Timestamp;

  changesSummary: {
    addedWords: number;
    removedWords: number;
  };

  snapshotType: "auto" | "manual" | "sync_conflict";
  conflictSource?: string;           // Device ID if sync conflict
}
```

**MVP Note**: Snapshots stored for sync conflict recovery but **no UI** to browse version history. Enables Fast-Follow features.

**Retention Policy**:
- Free tier: Last 10 snapshots per note (auto-deleted)
- Pro tier: Unlimited snapshots

### Dexie (IndexedDB) Schema

**Tables**: `notes`, `syncQueue`, `versionSnapshots`, `userPreferences`

```typescript
export class NexlyDatabase extends Dexie {
  notes!: Table<LocalNote, string>;
  syncQueue!: Table<SyncQueueItem, number>;
  versionSnapshots!: Table<LocalSnapshot, string>;

  constructor() {
    super("nexly_rn");
    this.version(1).stores({
      notes: "id, userId, updatedAt, category, isDeleted, [userId+updatedAt], [userId+category]",
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
- Password requirements: 8+ chars, 1 uppercase, 1 lowercase, 1 number, 1 special char

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
- Tier-based quota enforcement via API routes

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
- Rate limiting: 60 requests/min per user (excluding AI which has quota)
- AI quota: 100 requests/month (Free), unlimited (Pro)
- Stripe webhook signature validation
- Environment variables never exposed to client

---

## 5. AI Integration

### Autocomplete (GPT-4.1 nano)

**API Route**: `POST /api/ai/autocomplete`

**Request**:
```typescript
{
  context: string;          // Text before cursor (last 500 chars)
  cursorPosition: number;
  partialWord: string;      // Current word being typed
}
```

**Response**:
```typescript
{
  suggestions: string[];    // Max 5 suggestions
  quotaRemaining: number;
  source: "ai" | "dictionary";
}
```

**Specifications**:
- Model: GPT-4.1 nano (fast, cost-effective)
- Performance target: <200ms
- Quota: 100 requests/month (Free), unlimited (Pro)
- Fallback: Local nursing dictionary (5,000+ terms from OpenMD)
- Request throttling: Max 1 request per 3 seconds per user

### Dictionary Fallback

**Local Dictionary**: 5,000+ nursing terms (JSON format)
- Source: OpenMD Nursing Terminology Database (CC BY-SA 4.0)
- Categories: Medications, conditions, procedures, anatomy, abbreviations
- Stored in `/public/dictionaries/nursing-terms.json`
- Loaded into memory on app init, cached in IndexedDB

**Fallback Triggers**:
- AI quota exceeded
- Offline mode detected
- AI API timeout (>500ms)
- AI API error

### Quota Management

**Tracking**: Firestore `users` collection (`usage` field)
**Enforcement**: Client-side pre-check + Server-side validation
**Reset**: Monthly on user's signup anniversary date
**Display**: Quota badge in editor toolbar

---

## 6. Slash Commands System

### Command Architecture

**Trigger**: User types "/" in editor
**Parser**: Tiptap extension with custom slash command handler
**Menu**: Floating menu with command options

### Available Commands

#### /template
Inserts pre-formatted nursing document templates.

**Options**:
| Template | Description |
|----------|-------------|
| Care Plan | Nursing Diagnosis → Goals → Interventions → Evaluation |
| Medication Card | Drug → Classification → Action → Dose → Side Effects → Nursing Considerations |
| SOAP Note | Subjective → Objective → Assessment → Plan |
| Head-to-Toe Assessment | Systematic body assessment structure |
| Pathophysiology Outline | Disease → Etiology → Pathophysiology → Clinical Manifestations → Treatment |

**Implementation**:
```typescript
const templates: Record<string, JSONContent> = {
  "care-plan": {
    type: "doc",
    content: [
      { type: "heading", attrs: { level: 2 }, content: [{ type: "text", text: "Nursing Diagnosis" }] },
      { type: "paragraph", content: [] },
      { type: "heading", attrs: { level: 2 }, content: [{ type: "text", text: "Goals" }] },
      // ... more sections
    ]
  },
  // ... more templates
};
```

#### /formula
Inserts clinical formulas with normal ranges.

**Options**:
| Formula | Normal Range |
|---------|--------------|
| MAP (Mean Arterial Pressure) | 70-100 mmHg |
| BMI (Body Mass Index) | 18.5-24.9 |
| IV Drip Rate (gtt/min) | Calculated |
| Dosage Calculation (mg/kg) | Calculated |
| Glasgow Coma Scale | 3-15 |
| Fluid Deficit | Calculated |

**Implementation**:
```typescript
const formulas: Record<string, JSONContent> = {
  "map": {
    type: "doc",
    content: [
      { type: "heading", attrs: { level: 3 }, content: [{ type: "text", text: "Mean Arterial Pressure (MAP)" }] },
      { type: "paragraph", content: [
        { type: "text", text: "Formula: MAP = (SBP + 2×DBP) / 3" }
      ]},
      { type: "paragraph", content: [
        { type: "text", marks: [{ type: "bold" }], text: "Normal Range: 70-100 mmHg" }
      ]},
    ]
  },
  // ... more formulas
};
```

---

## 7. Offline & Sync Strategy

### Data Flow Pattern

1. **Write Path**: User edits → Dexie (instant) → Sync queue → Firestore (background)
2. **Read Path**: Dexie first (instant) → Firestore real-time updates (merge)
3. **Conflict Resolution**: Last-write-wins with version tracking

### Auto-Save

**Frequency**: Every 30 seconds of inactivity
**Indicator**: "Saved" badge in toolbar with timestamp
**Local**: Always saves to Dexie immediately
**Cloud**: Syncs to Firestore when online

### Sync Queue

**Purpose**: Queue operations when offline, replay when online
**Retry Logic**: Max 5 retries with exponential backoff (5s, 15s, 30s, 60s, 120s)
**Operations**: `create`, `update`, `delete` for notes

### Conflict Resolution

**Algorithm**: Last-write-wins (most recent timestamp)
**Conflict Detection**: Compare `version` and `updatedAt` fields
**Recovery**: Overwritten version saved as snapshot with `snapshotType: "sync_conflict"`
**User Notification**: Toast notification indicating which device's version was kept

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

## 8. Payment Integration (Stripe)

### Subscription Tiers

| Tier | Price | AI Autocomplete | Features |
|------|-------|-----------------|----------|
| Free | $0 | 100/month | Core editor, templates, formulas, offline sync |
| Pro | $8.99/month or $79/year | Unlimited | All Free features + unlimited AI |

### Stripe Integration

**Checkout Flow**:
1. User clicks "Upgrade to Pro"
2. `POST /api/stripe/checkout` creates Stripe Checkout session
3. User redirected to Stripe-hosted payment page
4. On success, webhook updates user tier in Firestore

**Webhook Events**:
- `checkout.session.completed`: Create subscription, update tier to Pro
- `customer.subscription.updated`: Handle plan changes
- `customer.subscription.deleted`: Downgrade to Free
- `invoice.payment_failed`: Handle failed payments

**Customer Portal**:
- Users manage subscription via Stripe Customer Portal
- `POST /api/stripe/portal` creates portal session
- Handles cancellation, plan changes, payment method updates

### Security

- Webhook signature validation with `STRIPE_WEBHOOK_SECRET`
- Never expose Stripe secret key to client
- Use Stripe.js for PCI-compliant card handling

---

## 9. Note Organization

### Categories

**Predefined Categories**:
- Pharmacology
- Med-Surg
- Pediatrics
- OB
- Mental Health
- Clinical Rotation
- Other

**Implementation**: Enum field on Note model, filterable in notes library

### Search

**Client-Side**: Full-text search on title and content (Dexie)
**Performance**: <300ms for libraries up to 1,000 notes

### Trash System

**Soft Delete**: `isDeleted: true`, `deletedAt: Timestamp`
**Recovery Period**: 30 days
**Permanent Deletion**: Cloud Function runs daily, deletes notes where `deletedAt` > 30 days ago
**User Actions**: View trash, restore note, permanently delete

---

## 10. Performance Optimization

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
- AI Autocomplete: <200ms
- Auto-save: <500ms (non-blocking)
- Search: <300ms
- Slash command menu: <100ms

**Optimization Strategies**:
- Server Components for initial renders
- Debounce autocomplete (150ms)
- Virtual scrolling for long note lists
- Lighthouse score >90

---

## 11. Project Structure

```
nexly-rn/
├── src/app/                      # Next.js App Router
│   ├── (auth)/                   # Public routes (login, signup, reset-password)
│   ├── (dashboard)/              # Authenticated app
│   │   ├── notes/                # Notes library and editor
│   │   ├── trash/                # Trash folder
│   │   ├── settings/             # User settings
│   │   └── onboarding/           # First-time user experience
│   ├── api/                      # Serverless API routes
│   │   ├── auth/initialize/
│   │   ├── ai/autocomplete/
│   │   ├── users/quota/
│   │   ├── stripe/checkout/
│   │   ├── stripe/webhook/
│   │   └── stripe/portal/
│   ├── layout.tsx                # Root layout
│   └── globals.css               # Global styles
│
├── src/components/               # UI components
│   ├── ui/                       # Shadcn components (auto-generated)
│   ├── editor/                   # Tiptap editor, autocomplete, toolbar, slash commands
│   ├── notes/                    # Notes library, cards, dialogs
│   └── layout/                   # Navbar, sidebar
│
├── src/lib/                      # Core logic
│   ├── firebase/                 # Client + Admin SDK setup
│   ├── dexie/                    # IndexedDB schema + sync
│   ├── ai/                       # OpenAI integrations
│   ├── stripe/                   # Stripe client + helpers
│   └── validations.ts            # Zod schemas
│
├── src/hooks/                    # Custom React hooks
│   ├── auth/                     # Auth hooks
│   ├── ai/                       # AI integration hooks
│   └── data/                     # Firestore + Dexie sync hooks
│
├── src/types/                    # TypeScript types
│   ├── models/                   # Note, User interfaces
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

## 12. Environment Variables

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

# Stripe
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

# App Config
NEXT_PUBLIC_APP_URL=https://nexly-rn.vercel.app

# Monitoring
SENTRY_DSN=
```

---

## 13. Dependencies

### Core Dependencies
```json
{
  "next": "15.1.0",
  "react": "19.1.1",
  "typescript": "5.9.3",
  "@tiptap/react": "3.4.2",
  "@tiptap/starter-kit": "3.4.2",
  "@tiptap/extension-placeholder": "3.4.2",
  "firebase": "^10.x",
  "firebase-admin": "^12.x",
  "openai": "5.23.1",
  "dexie": "4.2.0",
  "zustand": "5.0.8",
  "immer": "10.1.3",
  "tailwindcss": "4.1.13",
  "next-pwa": "5.6.0",
  "zod": "3.25.67",
  "stripe": "^14.x",
  "@stripe/stripe-js": "^2.x"
}
```

### Dev Dependencies
```json
{
  "vitest": "3.2.4",
  "@testing-library/react": "16.3.0",
  "playwright": "1.55.0",
  "prettier": "^3.x",
  "@sentry/nextjs": "^7.x"
}
```

---

## 14. Testing Strategy

### Unit Testing (Vitest)
- Component tests for UI components
- Hook tests for custom React hooks
- Utility function tests
- Slash command parser tests

### E2E Testing (Playwright)
- Critical user flows (signup, create note, save, sync)
- Offline mode testing
- Slash command insertion
- AI autocomplete flow
- Cross-browser testing (Chromium, Firefox, WebKit)

---

## 15. Deployment

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

## 16. 4-Week Build Timeline

### Week 1: Foundation
- Next.js setup + App Router
- Firebase integration (Client + Admin SDK)
- Shadcn UI components
- Auth flow (signup, login, logout, password reset)
- Basic note CRUD (create, read, update, delete)
- Dexie offline storage setup

### Week 2: Editor & AI
- Tiptap editor integration
- Slash command system (/template, /formula)
- AI autocomplete API route (GPT-4.1 nano)
- Local dictionary fallback (5,000+ terms)
- Auto-save with 30-second interval
- Quota tracking and display

### Week 3: Sync & Organization
- Offline sync queue implementation
- Conflict resolution (last-write-wins)
- Note categories and filtering
- Search functionality
- Trash folder with recovery
- Export to Markdown/Plain Text

### Week 4: Payment & Polish
- Stripe integration (checkout, webhooks, portal)
- PWA configuration
- Onboarding flow
- Performance optimization
- E2E testing
- Deployment to Vercel

---

## 17. Fast-Follow Features (Post-MVP)

### Phase 1 (Week 5-6)
- Study Mode (read-only with AI key term spotting)
- Inline diff view (changes since last save)
- Version history UI

### Phase 2 (Week 7-8)
- Shorthand expansion
- Definition-on-demand lookup
- Cloze deletion generator

### Future Roadmap
- Export notes (PDF)
- Analytics dashboard
- NCLEX prep integration
- Team collaboration features

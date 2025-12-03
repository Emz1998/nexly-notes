# Technical Specifications - NEXLY RN

## 1. System Overview

**Architecture**: Progressive Web App (PWA) with Next.js
**Primary Stack**: Next.js 15.1 + React 19.1 + TypeScript 5.9 + Tailwind 4.1 + Tiptap 3.4
**Deployment**: Vercel (recommended)
**Core Concept**: Distraction-free note-taking with AI-powered medical autocomplete, nursing-specific templates, and bulletproof offline sync

### Technology Stack

- **Frontend**: Next.js 15.1 with App Router, React 19.1, TypeScript 5.9
- **UI Framework**: Shadcn UI + Radix UI primitives, Tailwind CSS 4.1
- **Rich Text**: Tiptap 3.4 with custom extensions
- **State Management**: Zustand 5.0.8 + Immer 10.1.3
- **Authentication**: Supabase Auth
- **Database**: Supabase PostgreSQL (primary) + PowerSync (SQLite for offline)
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

**Hybrid Next.js + Supabase**
- Next.js API Routes for AI features and business logic
- Supabase Client SDK for direct PostgreSQL access (real-time)
- Supabase Service Role for server-side operations (API routes)
- PostgreSQL Row Level Security (RLS) enforces user isolation
- PowerSync for offline-first sync with SQLite local storage

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

### PostgreSQL Tables

#### Users Table

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  email TEXT UNIQUE NOT NULL,
  display_name TEXT,
  tier TEXT DEFAULT 'free' CHECK (tier IN ('free', 'pro')),

  -- Usage tracking
  autocomplete_requests INT DEFAULT 0,
  reset_date TIMESTAMPTZ DEFAULT NOW(),

  -- Settings
  theme TEXT DEFAULT 'system' CHECK (theme IN ('light', 'dark', 'system')),
  auto_save BOOLEAN DEFAULT true,

  -- Stripe
  stripe_customer_id TEXT,
  stripe_subscription_id TEXT,
  stripe_subscription_status TEXT CHECK (stripe_subscription_status IN ('active', 'canceled', 'past_due')),
  stripe_current_period_end TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_tier ON users(tier);
CREATE INDEX idx_users_created_at ON users(created_at);
```

#### Notes Table

```sql
CREATE TABLE notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title TEXT NOT NULL DEFAULT 'Untitled',
  content JSONB,  -- Tiptap JSON document

  category TEXT CHECK (category IN (
    'pharmacology', 'med-surg', 'pediatrics', 'ob',
    'mental-health', 'clinical-rotation', 'other'
  )),

  -- Metadata
  word_count INT DEFAULT 0,
  character_count INT DEFAULT 0,

  -- Sync status
  last_synced_at TIMESTAMPTZ,
  version INT DEFAULT 1,
  device_id TEXT,

  -- Soft delete
  is_deleted BOOLEAN DEFAULT false,
  deleted_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX idx_notes_user_id ON notes(user_id);
CREATE INDEX idx_notes_user_deleted_updated ON notes(user_id, is_deleted, updated_at DESC);
CREATE INDEX idx_notes_user_deleted_category ON notes(user_id, is_deleted, category, updated_at DESC);
CREATE INDEX idx_notes_user_deleted_at ON notes(user_id, is_deleted, deleted_at);
```

**Tiptap Content Structure**
```typescript
import { JSONContent } from "@tiptap/core";

// Tiptap stores content as ProseMirror JSON (stored in JSONB column)
const content: JSONContent = {
  type: "doc",
  content: [
    { type: "paragraph", content: [{ type: "text", text: "..." }] },
    { type: "heading", attrs: { level: 2 }, content: [...] }
  ]
};
```

#### Snapshots Table (Backend Only - No UI in MVP)

```sql
CREATE TABLE snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  note_id UUID NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
  content JSONB NOT NULL,

  -- Changes summary
  added_words INT DEFAULT 0,
  removed_words INT DEFAULT 0,

  snapshot_type TEXT NOT NULL CHECK (snapshot_type IN ('auto', 'manual', 'sync_conflict')),
  conflict_source TEXT,  -- Device ID if sync conflict

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_snapshots_note_id ON snapshots(note_id);
CREATE INDEX idx_snapshots_note_created ON snapshots(note_id, created_at DESC);
```

**MVP Note**: Snapshots stored for sync conflict recovery but **no UI** to browse version history. Enables Fast-Follow features.

**Retention Policy**:
- Free tier: Last 10 snapshots per note (enforced via database trigger)
- Pro tier: Unlimited snapshots

### TypeScript Interfaces

```typescript
// Matches PostgreSQL schema
interface User {
  id: string;
  email: string;
  display_name: string | null;
  tier: 'free' | 'pro';
  autocomplete_requests: number;
  reset_date: string;
  theme: 'light' | 'dark' | 'system';
  auto_save: boolean;
  stripe_customer_id: string | null;
  stripe_subscription_id: string | null;
  stripe_subscription_status: 'active' | 'canceled' | 'past_due' | null;
  stripe_current_period_end: string | null;
  created_at: string;
  updated_at: string;
}

interface Note {
  id: string;
  user_id: string;
  title: string;
  content: JSONContent | null;
  category: 'pharmacology' | 'med-surg' | 'pediatrics' | 'ob' | 'mental-health' | 'clinical-rotation' | 'other' | null;
  word_count: number;
  character_count: number;
  last_synced_at: string | null;
  version: number;
  device_id: string | null;
  is_deleted: boolean;
  deleted_at: string | null;
  created_at: string;
  updated_at: string;
}

interface Snapshot {
  id: string;
  note_id: string;
  content: JSONContent;
  added_words: number;
  removed_words: number;
  snapshot_type: 'auto' | 'manual' | 'sync_conflict';
  conflict_source: string | null;
  created_at: string;
}
```

### PowerSync Schema (Local SQLite)

PowerSync automatically syncs the PostgreSQL tables to local SQLite. The sync rules define which data each user can access:

```yaml
# powersync.yaml
bucket_definitions:
  user_data:
    parameters: SELECT id as user_id FROM users WHERE id = token_parameters.user_id
    data:
      - SELECT * FROM users WHERE id = bucket.user_id
      - SELECT * FROM notes WHERE user_id = bucket.user_id
      - SELECT s.* FROM snapshots s
        JOIN notes n ON s.note_id = n.id
        WHERE n.user_id = bucket.user_id
```

**Purpose**: Offline-first storage with automatic bi-directional sync

---

## 4. Authentication & Security

### Authentication Flow

**Client-Side** (Supabase Client SDK)
- Email/password signup and login
- Session management via Supabase Auth (secure cookies)
- Auto token refresh (JWTs with configurable expiry)
- Password requirements: 8+ chars, 1 uppercase, 1 lowercase, 1 number, 1 special char

**Server-Side** (Supabase Service Role)
- Token verification in middleware and API routes
- User ID extraction from JWT tokens
- Route protection via middleware

**Token Verification Pattern**
```typescript
// middleware.ts
import { createServerClient } from '@supabase/ssr';

const supabase = createServerClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  { cookies }
);

const { data: { user } } = await supabase.auth.getUser();
const userId = user?.id;
```

```typescript
// API routes (service role for admin operations)
import { createClient } from '@supabase/supabase-js';

const supabaseAdmin = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL!,
  process.env.SUPABASE_SERVICE_ROLE_KEY!
);
```

### Row Level Security (RLS) Policies

**Key Principles**:
- Users can only read/write their own data
- Snapshots are immutable (no updates allowed)
- User deletion prevented (soft delete only)
- Tier-based quota enforcement via API routes

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE notes ENABLE ROW LEVEL SECURITY;
ALTER TABLE snapshots ENABLE ROW LEVEL SECURITY;

-- Users table policies
CREATE POLICY "Users can read own profile"
  ON users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
  ON users FOR UPDATE
  USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile"
  ON users FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Prevent user deletion (soft delete only)
CREATE POLICY "Prevent user deletion"
  ON users FOR DELETE
  USING (false);

-- Notes table policies
CREATE POLICY "Users can CRUD own notes"
  ON notes FOR ALL
  USING (auth.uid() = user_id);

-- Snapshots table policies
CREATE POLICY "Users can read own snapshots"
  ON snapshots FOR SELECT
  USING (
    note_id IN (SELECT id FROM notes WHERE user_id = auth.uid())
  );

CREATE POLICY "Users can insert own snapshots"
  ON snapshots FOR INSERT
  WITH CHECK (
    note_id IN (SELECT id FROM notes WHERE user_id = auth.uid())
  );

-- Snapshots are immutable (no updates)
CREATE POLICY "Snapshots are immutable"
  ON snapshots FOR UPDATE
  USING (false);

CREATE POLICY "Users can delete own snapshots"
  ON snapshots FOR DELETE
  USING (
    note_id IN (SELECT id FROM notes WHERE user_id = auth.uid())
  );
```

### API Security

- HTTPS only (automatic with Vercel)
- Supabase Auth token validation on all API routes
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

**Tracking**: PostgreSQL `users` table (`autocomplete_requests` column)
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

### PowerSync Architecture

PowerSync provides offline-first sync between Supabase PostgreSQL and local SQLite:

```
┌─────────────┐    ┌─────────────┐    ┌──────────────────┐
│   Browser   │◄──►│  PowerSync  │◄──►│ Supabase Postgres│
│   SQLite    │    │   Service   │    │                  │
└─────────────┘    └─────────────┘    └──────────────────┘
```

**Key Features**:
- SQLite local database (replaces IndexedDB/Dexie)
- Bi-directional sync with conflict resolution
- Works completely offline
- Official Supabase partnership

### Data Flow Pattern

1. **Write Path**: User edits → SQLite (instant) → PowerSync queue → Supabase (background)
2. **Read Path**: SQLite first (instant) → PowerSync sync (merge from Supabase)
3. **Conflict Resolution**: Last-write-wins with version tracking

### PowerSync Configuration

```typescript
// lib/powersync/schema.ts
import { column, Schema, Table } from '@powersync/web';

const notes = new Table({
  id: column.text,
  user_id: column.text,
  title: column.text,
  content: column.text, // JSON stringified
  category: column.text,
  word_count: column.integer,
  character_count: column.integer,
  version: column.integer,
  is_deleted: column.integer, // SQLite boolean
  created_at: column.text,
  updated_at: column.text,
});

export const schema = new Schema({ notes });
```

```typescript
// lib/powersync/db.ts
import { PowerSyncDatabase } from '@powersync/web';
import { schema } from './schema';

export const db = new PowerSyncDatabase({
  schema,
  database: { dbFilename: 'nexly.db' }
});
```

### Auto-Save

**Frequency**: Every 30 seconds of inactivity
**Indicator**: "Saved" badge in toolbar with timestamp
**Local**: Always saves to SQLite immediately
**Cloud**: PowerSync syncs to Supabase when online

### Sync Queue

**Purpose**: PowerSync handles queuing automatically
**Retry Logic**: Built-in with exponential backoff
**Operations**: `create`, `update`, `delete` for notes
**Status**: `db.currentStatus` provides sync state

### Conflict Resolution

**Algorithm**: Last-write-wins (most recent timestamp)
**Conflict Detection**: Compare `version` and `updated_at` fields
**Recovery**: Overwritten version saved as snapshot with `snapshot_type: 'sync_conflict'`
**User Notification**: Toast notification indicating which device's version was kept

### PWA Configuration

**Manifest**: `/public/manifest.json` (installable app)
**Service Worker**: next-pwa with strategies:
- NetworkFirst for API calls
- CacheFirst for static assets
- StaleWhileRevalidate for pages

**Features**:
- Offline note editing (via PowerSync SQLite)
- Background sync (via PowerSync)
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
4. On success, webhook updates user tier in Supabase

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

**Client-Side**: Full-text search on title and content (SQLite via PowerSync)
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
- Server-side: Time-based ISR, Supabase query caching (5-min TTL)
- Client-side: PowerSync SQLite for notes, Service Worker for static assets

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
│   ├── supabase/                 # Supabase client + server setup
│   ├── powersync/                # PowerSync schema + sync
│   ├── ai/                       # OpenAI integrations
│   ├── stripe/                   # Stripe client + helpers
│   └── validations.ts            # Zod schemas
│
├── src/hooks/                    # Custom React hooks
│   ├── auth/                     # Auth hooks
│   ├── ai/                       # AI integration hooks
│   └── data/                     # Supabase + PowerSync sync hooks
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
# Supabase (Client - Public)
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=

# Supabase (Server-only)
SUPABASE_SERVICE_ROLE_KEY=

# PowerSync
NEXT_PUBLIC_POWERSYNC_URL=
POWERSYNC_PRIVATE_KEY=

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
  "@supabase/supabase-js": "^2.x",
  "@supabase/ssr": "^0.x",
  "@powersync/web": "^1.x",
  "openai": "5.23.1",
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

### Supabase Edge Functions (Alternative)
- Deploy serverless functions via Supabase
- Custom domain support
- Built-in SSL certificates

---

## 16. 4-Week Build Timeline

### Week 1: Foundation
- Next.js setup + App Router
- Supabase integration (Client + Server SDK)
- Shadcn UI components
- Auth flow (signup, login, logout, password reset)
- Basic note CRUD (create, read, update, delete)
- PowerSync offline storage setup

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

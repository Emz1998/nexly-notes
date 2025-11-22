# Database Specifications - Next.js Stack

## 1. Database Overview (4-Week MVP)

### Primary Database

**Firestore** (NoSQL document database)

- Real-time sync across devices
- Offline support with local cache
- Automatic scaling
- Strong security rules enforcement
- Accessed via:
  - **Client SDK**: Direct access from React components
  - **Admin SDK**: Server-side access from Next.js API routes

### Local Database

**Dexie 4.2.0** (IndexedDB wrapper)

- Offline-first note storage
- Fast local queries and full-text search
- Sync queue for Firebase replication
- Schema versioning and migrations
- React hooks for data access (dexie-react-hooks)

### MVP Scope Note

**Backend Infrastructure vs UI**

- Version snapshots: Stored in Firestore/Dexie but **no UI in MVP** (enables Fast-Follow features)
- Definitions & Validations collections: **Deferred to Fast-Follow** (Week 5-6)

### Data Flow Pattern

1. User actions write to local Dexie database first (instant response)
2. Background sync process replicates to Firestore
3. Firestore changes trigger real-time updates via `onSnapshot` listeners
4. Conflict resolution: Last-write-wins with timestamp comparison

### Next.js Specific Patterns

**Server Components** (Initial Data Load)

```typescript
// app/(dashboard)/notes/page.tsx
import { adminDb } from "@/lib/firebase/admin";

async function getNotes(userId: string) {
  const snapshot = await adminDb
    .collection("users")
    .doc(userId)
    .collection("notes")
    .orderBy("updatedAt", "desc")
    .limit(20)
    .get();

  return snapshot.docs.map((doc) => doc.data());
}

export default async function NotesPage() {
  const notes = await getNotes(userId);
  return <NotesList initialNotes={notes} />;
}
```

**Client Components** (Real-time Updates)

```typescript
// components/notes/note-list.tsx
"use client";

import { useEffect, useState } from "react";
import { db } from "@/lib/firebase/client";
import { collection, query, orderBy, onSnapshot } from "firebase/firestore";

export function NotesList({ initialNotes }) {
  const [notes, setNotes] = useState(initialNotes);

  useEffect(() => {
    const q = query(
      collection(db, `users/${userId}/notes`),
      orderBy("updatedAt", "desc")
    );

    const unsubscribe = onSnapshot(q, (snapshot) => {
      setNotes(snapshot.docs.map((doc) => doc.data()));
    });

    return () => unsubscribe();
  }, [userId]);

  return <div>{/* Render notes */}</div>;
}
```

## 2. Firestore Collections

### Users Collection

**Path**: `/users/{userId}`

**Document Schema**

```typescript
interface UserProfile {
  userId: string; // Firebase Auth UID
  email: string; // User email address
  displayName: string; // Full name
  photoURL?: string; // Profile picture URL
  tier: "free" | "pro" | "team";
  createdAt: Timestamp;
  updatedAt: Timestamp;

  usage: {
    autocompleteRequests: number; // Current month count (Free: 100/month)
    keyTermSpottingUses: number; // Current month count (Free: 10/month)
    resetDate: Timestamp; // Next quota reset date
  };

  settings: {
    theme: "light" | "dark" | "system";
    autoSave: boolean;
    defaultMode: "create" | "edit" | "study";
    shortcuts: Record<string, string>;
  };

  metadata: {
    lastLoginAt: Timestamp;
    onboardingCompleted: boolean;
    institution?: string; // For team tier
  };
}
```

**Indexes**

- `email` (unique constraint via Auth)
- `tier` (for analytics queries)
- `createdAt` (for cohort analysis)

**Access Patterns**

- **Server-side** (API routes): `adminDb.collection('users').doc(userId).get()`
- **Client-side** (components): `getDoc(doc(db, 'users', userId))`
- **Real-time** (client): `onSnapshot(doc(db, 'users', userId), callback)`

### Notes Collection

**Path**: `/users/{userId}/notes/{noteId}`

**Document Schema**

```typescript
interface Note {
  id: string; // UUID v4
  userId: string; // Owner reference
  title: string; // Note title (max 200 chars)
  content: JSONContent; // Tiptap JSON document (from @tiptap/core)
  mode: "create" | "edit" | "study"; // Last active mode
  createdAt: Timestamp;
  updatedAt: Timestamp;

  metadata: {
    lectureDate?: Timestamp; // When lecture occurred
    courseCode?: string; // e.g., "NURS 301"
    timestamps: Array<{
      // Time markers within note
      time: string; // e.g., "14:23"
      position: number; // Character position in content
    }>;
  };

  tags: string[]; // User-defined tags

  stats: {
    wordCount: number;
    characterCount: number;
    // MVP: Only basic stats, no AI action tracking
    // Fast-Follow (Week 5-6): expansionCount, definitionCount
  };

  syncStatus: {
    lastSyncedAt: Timestamp;
    version: number; // Optimistic concurrency control
    deviceId: string; // Last device that modified
  };
}
```

**Indexes**

- `userId` + `updatedAt` (for note library sorting)
- `userId` + `metadata.courseCode` (for filtering)
- `userId` + `tags` (array-contains for tag filtering)
- `userId` + `createdAt` (for chronological view)

**Composite Index Configuration** (firestore.indexes.json)

```json
{
  "indexes": [
    {
      "collectionGroup": "notes",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "userId", "order": "ASCENDING" },
        { "fieldPath": "updatedAt", "order": "DESCENDING" }
      ]
    },
    {
      "collectionGroup": "notes",
      "queryScope": "COLLECTION",
      "fields": [
        { "fieldPath": "userId", "order": "ASCENDING" },
        { "fieldPath": "metadata.courseCode", "order": "ASCENDING" },
        { "fieldPath": "updatedAt", "order": "DESCENDING" }
      ]
    }
  ]
}
```

**Content Structure** (Tiptap JSON)

```typescript
import { JSONContent } from "@tiptap/core";

// Example Tiptap document
const exampleContent: JSONContent = {
  type: "doc",
  content: [
    {
      type: "paragraph",
      content: [
        { type: "text", text: "Normal text" },
        {
          type: "text",
          text: "bold text",
          marks: [{ type: "bold" }],
        },
      ],
    },
    {
      type: "heading",
      attrs: { level: 2 },
      content: [{ type: "text", text: "Heading" }],
    },
  ],
};
```

**Access Patterns**

```typescript
// Create note (client-side)
import { collection, addDoc } from "firebase/firestore";

const noteRef = await addDoc(
  collection(db, `users/${userId}/notes`),
  newNoteData
);

// Real-time subscription (client-side)
import { onSnapshot } from "firebase/firestore";

const unsubscribe = onSnapshot(
  doc(db, `users/${userId}/notes`, noteId),
  (snapshot) => {
    const noteData = snapshot.data();
    // Update UI
  }
);

// Query with filter (client-side)
import { query, where, orderBy, getDocs } from "firebase/firestore";

const q = query(
  collection(db, `users/${userId}/notes`),
  where("metadata.courseCode", "==", "NURS 301"),
  orderBy("updatedAt", "desc")
);
const snapshot = await getDocs(q);
```

### Version Snapshots Collection (Backend Only in MVP)

**Path**: `/users/{userId}/notes/{noteId}/snapshots/{snapshotId}`

**MVP Note**: Snapshots stored in backend but **no UI to view/manage** them in 4-week MVP. This enables Fast-Follow features (Week 7-8): full version history UI, side-by-side diff viewer.

**Document Schema**

```typescript
interface VersionSnapshot {
  id: string; // UUID v4
  noteId: string; // Parent note reference
  userId: string; // Owner reference
  content: JSONContent; // Tiptap JSON document (snapshot)
  mode: "create" | "edit" | "study"; // Mode when snapshot was created
  timestamp: Timestamp;

  changesSummary: {
    addedWords: number;
    removedWords: number;
    wordCountChange: number;
  };

  snapshotType: "auto" | "manual" | "mode_switch";
}
```

**Indexes**

- `userId` + `noteId` + `timestamp` (for chronological retrieval)
- `snapshotType` (for analytics)
- `timestamp` (for cleanup queries)

**Snapshot Triggers**

- Auto-save interval: Every 30 seconds
- Manual save: User clicks save button
- Mode switch: Transitioning between Create/Edit/Study modes

**Retention Policy**

- Free tier: Last 5 snapshots per note (oldest auto-deleted)
- Pro tier: Unlimited snapshots
- Team tier: Unlimited snapshots + extended retention

**Access Patterns**

```typescript
// Create snapshot (client-side)
import { collection, addDoc } from "firebase/firestore";

await addDoc(
  collection(db, `users/${userId}/notes/${noteId}/snapshots`),
  snapshotData
);

// Get last saved snapshot for inline diff (client-side)
import { query, where, orderBy, limit, getDocs } from "firebase/firestore";

const q = query(
  collection(db, `users/${userId}/notes/${noteId}/snapshots`),
  where("snapshotType", "in", ["manual", "auto"]),
  orderBy("timestamp", "desc"),
  limit(1)
);
const snapshot = await getDocs(q);
const lastSaved = snapshot.docs[0]?.data();
```

### Definitions Collection (Deferred to Fast-Follow: Week 5-6)

**Path**: `/definitions/{termId}`

**MVP Note**: Definitions feature **not in 4-week MVP**. Schema defined here for Fast-Follow implementation.

**Document Schema**

```typescript
interface Definition {
  id: string; // Normalized term slug
  term: string; // Medical/nursing term
  definition: string; // Plain-language explanation
  example?: string; // Clinical usage example
  aliases: string[]; // Alternative names
  category: string; // e.g., "medication", "procedure", "anatomy"

  validation: {
    status: "pending" | "validated" | "rejected";
    validatedBy?: string; // Educator user ID
    validatedAt?: Timestamp;
    source?: string; // Reference source
  };

  usage: {
    lookupCount: number; // Times definition accessed
    lastAccessedAt: Timestamp;
  };

  createdAt: Timestamp;
  updatedAt: Timestamp;
}
```

**Indexes**

- `term` (for exact match lookups)
- `category` (for filtering)
- `validation.status` (for educator dashboard)
- `usage.lookupCount` (for popularity ranking)

### Validations Collection (Deferred to Post-MVP)

**Path**: `/validations/{validationId}`

**MVP Note**: Educator validation workflows **not in 4-week MVP**. Schema defined here for future implementation.

**Purpose**: Track educator validation workflows (beta only)

**Document Schema**

```typescript
interface Validation {
  id: string;
  definitionId: string; // Reference to definition
  submittedBy: string; // User ID who requested validation
  reviewedBy?: string; // Educator user ID
  status: "pending" | "approved" | "rejected" | "needs_revision";

  feedback?: {
    comments: string;
    suggestedChanges?: string;
  };

  createdAt: Timestamp;
  reviewedAt?: Timestamp;
}
```

**Indexes**

- `status` (for pending queue)
- `reviewedBy` + `reviewedAt` (for educator history)
- `submittedBy` (for user submission tracking)

## 3. Dexie (IndexedDB) Schema

### Database Setup

```typescript
// lib/dexie/db.ts
import Dexie, { Table } from "dexie";
import { JSONContent } from "@tiptap/core";

export interface LocalNote {
  id: string;
  userId: string;
  title: string;
  content: JSONContent;
  mode: "create" | "edit" | "study";
  createdAt: number;
  updatedAt: number;
  metadata: {
    courseCode?: string;
  };
  tags: string[];
  stats: {
    wordCount: number;
    characterCount: number;
  };
  syncStatus: {
    synced: boolean;
    pendingChanges: boolean;
    lastSyncedAt: number;
  };
}

export interface SyncQueueItem {
  id?: number;
  operation: "create" | "update" | "delete";
  collection: string;
  documentId: string;
  data: any;
  createdAt: number;
  retryCount: number;
  lastError?: string;
}

export interface LocalSnapshot {
  id: string;
  noteId: string;
  userId: string;
  content: JSONContent;
  mode: "create" | "edit" | "study";
  timestamp: number;
  changesSummary: {
    addedWords: number;
    removedWords: number;
    wordCountChange: number;
  };
  snapshotType: "auto" | "manual" | "mode_switch";
  synced: boolean;
}

export interface LocalDefinition {
  id: string;
  term: string;
  definition: string;
  example?: string;
  category: string;
  validationStatus: string;
  cachedAt: number;
}

export interface UserPreferences {
  userId: string;
  settings: {
    theme: "light" | "dark" | "system";
    autoSave: boolean;
  };
  usage: {
    autocompleteRequests: number;
    keyTermSpottingUses: number;
    resetDate: number;
  };
  lastSyncedAt: number;
}

export class NexlyDatabase extends Dexie {
  notes!: Table<LocalNote, string>;
  syncQueue!: Table<SyncQueueItem, number>;
  versionSnapshots!: Table<LocalSnapshot, string>;
  definitions!: Table<LocalDefinition, string>;
  userPreferences!: Table<UserPreferences, string>;

  constructor() {
    super("nexly_rn");

    this.version(1).stores({
      notes: "id, userId, updatedAt, [userId+updatedAt], *tags",
      syncQueue: "++id, createdAt, [operation+collection]",
      versionSnapshots: "id, [userId+noteId+timestamp], noteId, timestamp",
      definitions: "id, term, category",
      userPreferences: "userId",
    });
  }
}

export const db = new NexlyDatabase();
```

### React Hooks for Dexie

```typescript
// lib/dexie/hooks.ts
"use client";

import { useLiveQuery } from "dexie-react-hooks";
import { db } from "./db";

export function useNotes(userId: string) {
  const notes = useLiveQuery(
    () => db.notes.where("userId").equals(userId).reverse().sortBy("updatedAt"),
    [userId]
  );

  return notes || [];
}

export function useNote(noteId: string) {
  const note = useLiveQuery(() => db.notes.get(noteId), [noteId]);

  return note;
}

export function useSyncQueue() {
  const queue = useLiveQuery(() => db.syncQueue.orderBy("createdAt").toArray());

  return queue || [];
}
```

### Dexie Indexes

```typescript
const db = new Dexie("nexly_rn");

db.version(1).stores({
  notes: "id, userId, updatedAt, [userId+updatedAt], *tags",
  syncQueue: "++id, createdAt, [operation+collection]",
  versionSnapshots: "id, [userId+noteId+timestamp], noteId, timestamp",
  definitions: "id, term, category",
  userPreferences: "userId",
});
```

**Index Explanations**:

- `id`: Primary key (unique identifier)
- `userId`: Index for user-specific queries
- `updatedAt`: Index for sorting by recency
- `[userId+updatedAt]`: Compound index for filtered sorting
- `*tags`: Multi-entry index for array-contains queries
- `++id`: Auto-incrementing primary key

## 4. Security Rules

### Firestore Rules

```javascript
// firestore.rules
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {

    // Helper functions
    function isAuthenticated() {
      return request.auth != null;
    }

    function isOwner(userId) {
      return request.auth.uid == userId;
    }

    function hasRole(role) {
      return get(/databases/$(database)/documents/users/$(request.auth.uid))
        .data.tier == role;
    }

    // Users collection
    match /users/{userId} {
      allow read: if isAuthenticated() && isOwner(userId);
      allow create: if isAuthenticated() && isOwner(userId);
      allow update: if isAuthenticated() && isOwner(userId);
      allow delete: if false; // Prevent accidental deletion
    }

    // Notes subcollection
    match /users/{userId}/notes/{noteId} {
      allow read: if isAuthenticated() && isOwner(userId);
      allow create: if isAuthenticated() && isOwner(userId)
        && request.resource.data.userId == userId;
      allow update: if isAuthenticated() && isOwner(userId);
      allow delete: if isAuthenticated() && isOwner(userId);

      // Version Snapshots subcollection
      match /snapshots/{snapshotId} {
        allow read: if isAuthenticated() && isOwner(userId);
        allow create: if isAuthenticated() && isOwner(userId)
          && request.resource.data.userId == userId
          && request.resource.data.noteId == noteId;
        allow update: if false; // Snapshots are immutable
        allow delete: if isAuthenticated() && isOwner(userId); // Allow cleanup
      }
    }

    // Definitions collection (read-only for students)
    match /definitions/{termId} {
      allow read: if isAuthenticated();
      allow write: if hasRole('team'); // Educators only
    }

    // Validations collection
    match /validations/{validationId} {
      allow read: if isAuthenticated() && (
        request.auth.uid == resource.data.submittedBy ||
        hasRole('team')
      );
      allow create: if isAuthenticated();
      allow update: if hasRole('team'); // Educators only
    }
  }
}
```

### Storage Rules

```javascript
// storage.rules
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {

    // User avatars
    match /avatars/{userId}/{fileName} {
      allow read: if true; // Public read
      allow write: if request.auth.uid == userId
        && request.resource.size < 5 * 1024 * 1024 // 5MB limit
        && request.resource.contentType.matches('image/.*');
    }

    // Note attachments
    match /attachments/{userId}/{noteId}/{fileName} {
      allow read: if request.auth.uid == userId;
      allow write: if request.auth.uid == userId
        && request.resource.size < 10 * 1024 * 1024; // 10MB limit
    }

    // Exported notes
    match /exports/{userId}/{exportId} {
      allow read: if request.auth.uid == userId;
      allow write: if request.auth.uid == userId;
      allow delete: if request.auth.uid == userId;
    }
  }
}
```

## 5. Query Patterns

### Common Queries (Client-side with Firebase SDK)

**Fetch user's recent notes**

```typescript
import { collection, query, orderBy, limit, getDocs } from "firebase/firestore";

const q = query(
  collection(db, `users/${userId}/notes`),
  orderBy("updatedAt", "desc"),
  limit(20)
);
const snapshot = await getDocs(q);
const notes = snapshot.docs.map((doc) => doc.data());
```

**Filter notes by course**

```typescript
import { where } from "firebase/firestore";

const q = query(
  collection(db, `users/${userId}/notes`),
  where("metadata.courseCode", "==", "NURS 301"),
  orderBy("createdAt", "desc")
);
```

**Search notes by tag**

```typescript
const q = query(
  collection(db, `users/${userId}/notes`),
  where("tags", "array-contains", "pharmacology"),
  orderBy("updatedAt", "desc")
);
```

**Local full-text search** (Dexie)

```typescript
import { db } from "@/lib/dexie/db";

const results = await db.notes
  .where("userId")
  .equals(userId)
  .filter(
    (note) =>
      note.title.toLowerCase().includes(query.toLowerCase()) ||
      JSON.stringify(note.content).toLowerCase().includes(query.toLowerCase())
  )
  .toArray();
```

**Fetch version snapshots for a note**

```typescript
import { collection, query, orderBy, limit, getDocs } from "firebase/firestore";

const q = query(
  collection(db, `users/${userId}/notes/${noteId}/snapshots`),
  orderBy("timestamp", "desc"),
  limit(20)
);
const snapshots = await getDocs(q);
```

**Get last saved snapshot** (for quick diff in Edit Mode)

```typescript
import { where } from "firebase/firestore";

const q = query(
  collection(db, `users/${userId}/notes/${noteId}/snapshots`),
  where("snapshotType", "in", ["manual", "auto"]),
  orderBy("timestamp", "desc"),
  limit(1)
);
const lastSaved = (await getDocs(q)).docs[0]?.data();
```

### Server-side Queries (Admin SDK in API Routes)

```typescript
// app/api/notes/route.ts
import { adminDb } from "@/lib/firebase/admin";

export async function GET(request: NextRequest) {
  const userId = request.headers.get("x-user-id");

  const snapshot = await adminDb
    .collection("users")
    .doc(userId)
    .collection("notes")
    .orderBy("updatedAt", "desc")
    .limit(20)
    .get();

  const notes = snapshot.docs.map((doc) => doc.data());
  return NextResponse.json(notes);
}
```

## 6. Sync Strategy

### Offline-First Approach

**Write Path**

1. User modifies note in editor
2. Immediately write to Dexie (instant UI update)
3. Add sync operation to `syncQueue` table
4. Background worker processes queue when online
5. On success, mark as synced and update `lastSyncedAt`
6. On failure, retry with exponential backoff

**Read Path**

1. Always read from Dexie first (instant display)
2. Subscribe to Firestore real-time updates in background
3. Merge remote changes with local data
4. Update Dexie cache with latest remote data

### Conflict Resolution

**Strategy**: Last-write-wins with version tracking

```typescript
// lib/dexie/sync.ts
async function syncNote(localNote: LocalNote, remoteNote: any) {
  if (!remoteNote) {
    // No remote version, upload local
    return uploadToFirestore(localNote);
  }

  if (localNote.syncStatus.version > remoteNote.syncStatus.version) {
    // Local is newer, upload
    return uploadToFirestore(localNote);
  }

  if (localNote.syncStatus.version < remoteNote.syncStatus.version) {
    // Remote is newer, download
    return updateLocalFromRemote(remoteNote);
  }

  // Same version, compare timestamps
  if (localNote.updatedAt > remoteNote.updatedAt.toMillis()) {
    return uploadToFirestore(localNote);
  } else {
    return updateLocalFromRemote(remoteNote);
  }
}
```

### Sync Queue Processing

```typescript
// lib/dexie/sync.ts
import { db } from "./db";
import { doc, setDoc, updateDoc, deleteDoc } from "firebase/firestore";
import { db as firebaseDb } from "@/lib/firebase/client";

export async function processSyncQueue() {
  const pendingOperations = await db.syncQueue
    .orderBy("createdAt")
    .limit(10)
    .toArray();

  for (const op of pendingOperations) {
    try {
      await executeOperation(op);
      await db.syncQueue.delete(op.id!);
    } catch (error) {
      await db.syncQueue.update(op.id!, {
        retryCount: op.retryCount + 1,
        lastError: (error as Error).message,
      });

      // Max 5 retries
      if (op.retryCount >= 5) {
        await db.syncQueue.delete(op.id!);
        console.error("Sync failed after 5 retries", op);
      }
    }
  }
}

async function executeOperation(op: SyncQueueItem) {
  const docRef = doc(firebaseDb, op.collection, op.documentId);

  switch (op.operation) {
    case "create":
      await setDoc(docRef, op.data);
      break;
    case "update":
      await updateDoc(docRef, op.data);
      break;
    case "delete":
      await deleteDoc(docRef);
      break;
  }
}

// Background sync worker (runs in useEffect)
export function startSyncWorker() {
  const intervalId = setInterval(async () => {
    if (navigator.onLine) {
      await processSyncQueue();
    }
  }, 5000); // Run every 5 seconds

  return () => clearInterval(intervalId);
}
```

## 7. Data Retention

### User Data

- Active users: Indefinite retention
- Deleted accounts: 30-day grace period before permanent deletion
- Exported notes: 90 days in Storage, then auto-deleted

### Version Snapshots

**Free Tier**

- Last 5 snapshots per note
- Automatic cleanup when limit exceeded
- Oldest snapshots deleted first
- Local Dexie cache: Last 20 snapshots per note

**Pro Tier**

- Unlimited snapshots
- No automatic deletion
- Local Dexie cache: Last 50 snapshots per note

**Team Tier**

- Unlimited snapshots
- Extended retention guarantee (3 years minimum)
- Institution-level backup and export capabilities

**Cleanup Strategy**

- Automated cleanup runs on snapshot creation (Free tier)
- Cloud Function runs daily cleanup batch job
- Orphaned snapshots (parent note deleted): 7-day grace period

### Definitions Cache

- Local cache: Max 1000 definitions, LRU eviction
- Remote: Permanent storage

### Logs and Analytics

- User activity logs: 90 days
- Error logs: 30 days
- Anonymous analytics: Aggregated, indefinite

## 8. Performance Optimization

### Firestore Optimization

- Denormalize frequently accessed data (avoid joins)
- Use composite indexes for common filter combinations
- Pagination: Limit queries to 20-50 documents, use cursor-based pagination
- Cache validated definitions locally to reduce reads

### Dexie Optimization

- Index frequently queried fields (`userId`, `updatedAt`, `tags`)
- Bulk operations for sync queue processing
- Periodic cleanup of old cached data
- Use transactions for multi-table updates

### Next.js Specific Optimizations

**Server Components for Initial Data**

```typescript
// Fetch data server-side (no loading state needed)
async function NotesPage() {
  const notes = await getNotesFromFirestore(userId);
  return <NotesList initialNotes={notes} />;
}
```

**Client Components for Real-time**

```typescript
// Real-time updates with optimistic UI
"use client";

export function NoteEditor({ noteId }) {
  const [note, setNote] = useState(initialNote);

  useEffect(() => {
    const unsubscribe = onSnapshot(
      doc(db, `users/${userId}/notes`, noteId),
      (snapshot) => setNote(snapshot.data())
    );
    return unsubscribe;
  }, [noteId]);

  return <Editor content={note.content} />;
}
```

### Cost Control

- Free tier users: Rate limit sync to every 5 seconds
- Pro tier users: Real-time sync
- Definitions: Cache aggressively, update monthly
- Implement query result caching with 5-minute TTL
- Version snapshots: Automatic cleanup for Free tier (5 snapshot limit)
- Batch snapshot deletions to reduce write operations
- Use Firestore document bundling for snapshot reads (reduce read costs)

## 9. Migration Strategy

### Schema Versioning

**Dexie Migrations**

```typescript
// lib/dexie/db.ts
import Dexie from "dexie";

export class NexlyDatabase extends Dexie {
  constructor() {
    super("nexly_rn");

    this.version(1).stores({
      notes: "id, userId, updatedAt",
      syncQueue: "++id, createdAt",
      userPreferences: "userId",
    });

    this.version(2)
      .stores({
        notes: "id, userId, updatedAt, *tags",
      })
      .upgrade((trans) => {
        return trans.notes.toCollection().modify((note) => {
          note.tags = note.tags || [];
        });
      });

    this.version(3)
      .stores({
        notes: "id, userId, updatedAt, *tags",
        versionSnapshots: "id, [userId+noteId+timestamp], noteId, timestamp",
      })
      .upgrade((trans) => {
        // Add version snapshots table
        // Migrate existing notes to include mode field
        return trans.notes.toCollection().modify((note) => {
          note.mode = note.mode || "create"; // Default to create mode
        });
      });
  }
}
```

**Firestore Migrations**

- Use Cloud Functions for batch updates
- Version field in documents for gradual rollout
- Backward-compatible schema changes only

### Data Import

- CSV import for bulk note creation
- Evernote/Notion export compatibility (post-MVP)
- Institution data migration tools for team tier

This completes the revised database specifications for Next.js stack.

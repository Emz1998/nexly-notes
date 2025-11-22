# Database Specifications

## 1. Database Overview (4-Week MVP)

### Primary Database

**Firestore** (NoSQL document database)
- Real-time sync across devices
- Offline support with local cache
- Automatic scaling
- Strong security rules enforcement

### Local Database

**Dexie 4.2.0** (IndexedDB wrapper)
- Offline-first note storage
- Fast local queries and full-text search
- Sync queue for Firebase replication
- Schema versioning and migrations

### MVP Scope Note

**Backend Infrastructure vs UI**
- Version snapshots: Stored in Firestore/Dexie but **no UI in MVP** (enables Fast-Follow features)
- Definitions & Validations collections: **Deferred to Fast-Follow** (Week 5-6)

### Data Flow Pattern

1. User actions write to local Dexie database first (instant response)
2. Background sync process replicates to Firestore
3. Firestore changes trigger real-time updates to other devices
4. Conflict resolution: Last-write-wins with timestamp comparison

## 2. Firestore Collections

### Users Collection

**Path**: `/users/{userId}`

**Document Schema**
```typescript
{
  userId: string              // Firebase Auth UID
  email: string               // User email address
  displayName: string         // Full name
  photoURL?: string           // Profile picture URL
  tier: 'free' | 'pro' | 'team'
  createdAt: Timestamp
  updatedAt: Timestamp

  usage: {
    autocompleteRequests: number        // Current month count (Free: 100/month)
    keyTermSpottingUses: number         // Current month count (Free: 10/month)
    resetDate: Timestamp                // Next quota reset date
  }

  settings: {
    theme: 'light' | 'dark' | 'system'
    autoSave: boolean
    defaultMode: 'create' | 'edit' | 'study'
    shortcuts: Record<string, string>
  }

  metadata: {
    lastLoginAt: Timestamp
    onboardingCompleted: boolean
    institution?: string            // For team tier
  }
}
```

**Indexes**
- `email` (unique constraint via Auth)
- `tier` (for analytics queries)
- `createdAt` (for cohort analysis)

### Notes Collection

**Path**: `/users/{userId}/notes/{noteId}`

**Document Schema**
```typescript
{
  id: string                  // UUID v4
  userId: string              // Owner reference
  title: string               // Note title (max 200 chars)
  content: object             // Tiptap JSON document
  mode: 'create' | 'edit' | 'study'  // Last active mode
  createdAt: Timestamp
  updatedAt: Timestamp

  metadata: {
    lectureDate?: Timestamp   // When lecture occurred
    courseCode?: string       // e.g., "NURS 301"
    timestamps: Array<{       // Time markers within note
      time: string            // e.g., "14:23"
      position: number        // Character position in content
    }>
  }

  tags: string[]              // User-defined tags

  stats: {
    wordCount: number
    characterCount: number
    // MVP: Only basic stats, no AI action tracking
    // Fast-Follow (Week 5-6): expansionCount, definitionCount
  }

  syncStatus: {
    lastSyncedAt: Timestamp
    version: number           // Optimistic concurrency control
    deviceId: string          // Last device that modified
  }
}
```

**Indexes**
- `userId` + `updatedAt` (for note library sorting)
- `userId` + `metadata.courseCode` (for filtering)
- `userId` + `tags` (array-contains for tag filtering)
- `userId` + `createdAt` (for chronological view)

**Content Structure** (Tiptap JSON)
```typescript
{
  type: 'doc',
  content: [
    {
      type: 'paragraph' | 'heading' | 'bulletList' | 'orderedList' | 'codeBlock',
      attrs?: object,
      content?: Array<TextNode | InlineNode>
    }
  ]
}

type TextNode = {
  type: 'text',
  text: string,
  marks?: Array<{ type: 'bold' | 'italic' | 'code' }>
}
```

### Version Snapshots Collection (Backend Only in MVP)

**Path**: `/users/{userId}/notes/{noteId}/snapshots/{snapshotId}`

**MVP Note**: Snapshots stored in backend but **no UI to view/manage** them in 4-week MVP. This enables Fast-Follow features (Week 7-8): full version history UI, side-by-side diff viewer.

**Document Schema**
```typescript
{
  id: string                  // UUID v4
  noteId: string              // Parent note reference
  userId: string              // Owner reference
  content: object             // Tiptap JSON document (snapshot)
  mode: 'create' | 'edit' | 'study'  // Mode when snapshot was created
  timestamp: Timestamp

  changesSummary: {
    addedWords: number
    removedWords: number
    wordCountChange: number
  }

  snapshotType: 'auto' | 'manual' | 'mode_switch'
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

### Definitions Collection (Deferred to Fast-Follow: Week 5-6)

**Path**: `/definitions/{termId}`

**MVP Note**: Definitions feature **not in 4-week MVP**. Schema defined here for Fast-Follow implementation.

**Document Schema**
```typescript
{
  id: string                  // Normalized term slug
  term: string                // Medical/nursing term
  definition: string          // Plain-language explanation
  example?: string            // Clinical usage example
  aliases: string[]           // Alternative names
  category: string            // e.g., "medication", "procedure", "anatomy"

  validation: {
    status: 'pending' | 'validated' | 'rejected'
    validatedBy?: string      // Educator user ID
    validatedAt?: Timestamp
    source?: string           // Reference source
  }

  usage: {
    lookupCount: number       // Times definition accessed
    lastAccessedAt: Timestamp
  }

  createdAt: Timestamp
  updatedAt: Timestamp
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
{
  id: string
  definitionId: string        // Reference to definition
  submittedBy: string         // User ID who requested validation
  reviewedBy?: string         // Educator user ID
  status: 'pending' | 'approved' | 'rejected' | 'needs_revision'

  feedback?: {
    comments: string
    suggestedChanges?: string
  }

  createdAt: Timestamp
  reviewedAt?: Timestamp
}
```

**Indexes**
- `status` (for pending queue)
- `reviewedBy` + `reviewedAt` (for educator history)
- `submittedBy` (for user submission tracking)

## 3. Dexie (IndexedDB) Schema

### Local Tables

**notes**
```typescript
{
  id: string (primary key)
  userId: string (indexed)
  title: string
  content: object
  mode: string
  createdAt: number (timestamp)
  updatedAt: number (timestamp)
  metadata: object
  tags: string[] (multi-entry index)
  stats: object
  syncStatus: {
    synced: boolean
    pendingChanges: boolean
    lastSyncedAt: number
  }
}
```

**syncQueue**
```typescript
{
  id: string (primary key, auto-increment)
  operation: 'create' | 'update' | 'delete'
  collection: string
  documentId: string
  data: object
  createdAt: number (timestamp)
  retryCount: number
  lastError?: string
}
```

**versionSnapshots**
```typescript
{
  id: string (primary key)
  noteId: string (indexed)
  userId: string (indexed)
  content: object
  mode: 'create' | 'edit' | 'study'
  timestamp: number (timestamp, indexed)
  changesSummary: {
    addedWords: number
    removedWords: number
    wordCountChange: number
  }
  snapshotType: 'auto' | 'manual' | 'mode_switch'
  synced: boolean
}
```

**definitions (cache)**
```typescript
{
  id: string (primary key)
  term: string (indexed, for search)
  definition: string
  example?: string
  category: string (indexed)
  validationStatus: string
  cachedAt: number (timestamp)
}
```

**userPreferences**
```typescript
{
  userId: string (primary key)
  settings: object
  usage: object
  lastSyncedAt: number
}
```

### Dexie Indexes

```typescript
const db = new Dexie('nexly_rn');

db.version(1).stores({
  notes: 'id, userId, updatedAt, [userId+updatedAt], *tags',
  syncQueue: '++id, createdAt, [operation+collection]',
  versionSnapshots: 'id, [userId+noteId+timestamp], noteId, timestamp',
  definitions: 'id, term, category',
  userPreferences: 'userId'
});
```

## 4. Security Rules

### Firestore Rules

```javascript
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

### Common Queries

**Fetch user's recent notes**
```typescript
db.collection('users')
  .doc(userId)
  .collection('notes')
  .orderBy('updatedAt', 'desc')
  .limit(20);
```

**Filter notes by course**
```typescript
db.collection('users')
  .doc(userId)
  .collection('notes')
  .where('metadata.courseCode', '==', 'NURS 301')
  .orderBy('createdAt', 'desc');
```

**Search notes by tag**
```typescript
db.collection('users')
  .doc(userId)
  .collection('notes')
  .where('tags', 'array-contains', 'pharmacology')
  .orderBy('updatedAt', 'desc');
```

**Lookup definition**
```typescript
db.collection('definitions')
  .where('term', '==', normalizedTerm)
  .where('validation.status', '==', 'validated')
  .limit(1);
```

**Local full-text search** (Dexie)
```typescript
await db.notes
  .where('userId').equals(userId)
  .filter(note =>
    note.title.toLowerCase().includes(query.toLowerCase()) ||
    JSON.stringify(note.content).toLowerCase().includes(query.toLowerCase())
  )
  .toArray();
```

**Fetch version snapshots for a note**
```typescript
db.collection('users')
  .doc(userId)
  .collection('notes')
  .doc(noteId)
  .collection('snapshots')
  .orderBy('timestamp', 'desc')
  .limit(20);
```

**Get last saved snapshot** (for quick diff in Edit Mode)
```typescript
db.collection('users')
  .doc(userId)
  .collection('notes')
  .doc(noteId)
  .collection('snapshots')
  .where('snapshotType', 'in', ['manual', 'auto'])
  .orderBy('timestamp', 'desc')
  .limit(1);
```

**Compare two snapshots** (side-by-side diff)
```typescript
const snapshot1 = await db.collection('users')
  .doc(userId)
  .collection('notes')
  .doc(noteId)
  .collection('snapshots')
  .doc(snapshotId1)
  .get();

const snapshot2 = await db.collection('users')
  .doc(userId)
  .collection('notes')
  .doc(noteId)
  .collection('snapshots')
  .doc(snapshotId2)
  .get();
```

**Local version snapshots query** (Dexie)
```typescript
await db.versionSnapshots
  .where('[userId+noteId+timestamp]')
  .between([userId, noteId, Dexie.minKey], [userId, noteId, Dexie.maxKey])
  .reverse()
  .limit(20)
  .toArray();
```

**Cleanup old snapshots** (Free tier retention)
```typescript
// Get snapshots beyond retention limit
const excessSnapshots = await db.collection('users')
  .doc(userId)
  .collection('notes')
  .doc(noteId)
  .collection('snapshots')
  .orderBy('timestamp', 'desc')
  .offset(5) // Keep last 5
  .get();

// Delete excess snapshots
const batch = db.batch();
excessSnapshots.forEach(snapshot => {
  batch.delete(snapshot.ref);
});
await batch.commit();
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
async function syncNote(localNote, remoteNote) {
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
  if (localNote.updatedAt > remoteNote.updatedAt) {
    return uploadToFirestore(localNote);
  } else {
    return updateLocalFromRemote(remoteNote);
  }
}
```

### Version Snapshot Sync Workflow

**Snapshot Creation Triggers**
1. **Auto-save interval** (every 30 seconds)
   - Check if note content has changed
   - Create snapshot in local Dexie
   - Add to sync queue for Firestore upload

2. **Manual save** (user clicks save button)
   - Immediately create snapshot in Dexie
   - Priority sync to Firestore
   - Show save confirmation to user

3. **Mode switch** (Create ↔ Edit ↔ Study)
   - Create snapshot before mode transition
   - Include mode metadata in snapshot
   - Sync to Firestore in background

**Snapshot Sync Process**
```typescript
async function createSnapshot(noteId: string, snapshotType: SnapshotType) {
  const note = await db.notes.get(noteId);
  const previousSnapshot = await getLastSnapshot(noteId);

  // Calculate changes
  const changesSummary = calculateDiff(previousSnapshot?.content, note.content);

  // Create local snapshot
  const snapshot = {
    id: generateUUID(),
    noteId,
    userId: note.userId,
    content: note.content,
    mode: note.mode,
    timestamp: Date.now(),
    changesSummary,
    snapshotType,
    synced: false
  };

  await db.versionSnapshots.add(snapshot);

  // Add to sync queue
  await db.syncQueue.add({
    operation: 'create',
    collection: 'snapshots',
    documentId: snapshot.id,
    data: snapshot,
    createdAt: Date.now(),
    retryCount: 0
  });

  // Enforce retention policy (Free tier)
  if (userTier === 'free') {
    await cleanupOldSnapshots(noteId, 5);
  }
}
```

**Snapshot Retention Enforcement**
```typescript
async function cleanupOldSnapshots(noteId: string, keepCount: number) {
  const snapshots = await db.versionSnapshots
    .where('noteId').equals(noteId)
    .reverse()
    .sortBy('timestamp');

  if (snapshots.length > keepCount) {
    const excessSnapshots = snapshots.slice(keepCount);

    for (const snapshot of excessSnapshots) {
      // Delete from local
      await db.versionSnapshots.delete(snapshot.id);

      // Queue remote deletion
      await db.syncQueue.add({
        operation: 'delete',
        collection: 'snapshots',
        documentId: snapshot.id,
        createdAt: Date.now(),
        retryCount: 0
      });
    }
  }
}
```

### Sync Queue Processing

```typescript
async function processSyncQueue() {
  const pendingOperations = await db.syncQueue
    .orderBy('createdAt')
    .limit(10)
    .toArray();

  for (const op of pendingOperations) {
    try {
      await executeOperation(op);
      await db.syncQueue.delete(op.id);
    } catch (error) {
      await db.syncQueue.update(op.id, {
        retryCount: op.retryCount + 1,
        lastError: error.message
      });

      // Max 5 retries
      if (op.retryCount >= 5) {
        await db.syncQueue.delete(op.id);
        logError('Sync failed after 5 retries', op);
      }
    }
  }
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

## 8. Backup Strategy

### Firestore Backups
- Automated daily backups (Firebase built-in)
- 30-day retention for point-in-time recovery
- Export to Cloud Storage weekly for long-term archival

### User Export
- Manual export via UI: PDF, DOCX, Markdown
- Bulk export API for institutional users
- Include all notes + metadata in JSON format

## 9. Performance Optimization

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

### Version Snapshot & Diff Optimization

**Quick Diff Performance** (Edit Mode)
- Target: <200ms calculation time
- Debounce user input: 500ms before recalculating diff
- Use Web Worker for diff calculation to avoid UI blocking
- Cache last comparison result to avoid redundant calculations
- Implement incremental diff: Only compare changed paragraphs

**Side-by-Side Diff Performance**
- Target: <300ms loading time
- Lazy load diff library (code-splitting)
- Render viewport-visible diffs first, lazy load rest
- Use virtual scrolling for large documents (>5000 words)
- Optimize diff algorithm: Word-level for small changes, line-level for large

**Snapshot Storage Optimization**
- Compress Tiptap JSON content before storage (gzip)
- Consider incremental snapshots: Store only deltas for Pro tier
- Batch snapshot uploads to reduce Firestore write operations
- Use Firestore offline cache for recent snapshots

**Diff Algorithm Selection**
- Quick diff (Edit Mode): Fast word-level diff using diff-match-patch
- Side-by-side diff: More accurate line-level diff with context
- Character-level diff for small selections (<100 chars)
- Paragraph-level diff for large documents (>3000 words)

### Cost Control
- Free tier users: Rate limit sync to every 5 seconds
- Pro tier users: Real-time sync
- Definitions: Cache aggressively, update monthly
- Implement query result caching with 5-minute TTL
- Version snapshots: Automatic cleanup for Free tier (5 snapshot limit)
- Batch snapshot deletions to reduce write operations
- Use Firestore document bundling for snapshot reads (reduce read costs)

## 10. Migration Strategy

### Schema Versioning

**Dexie Migrations**
```typescript
db.version(1).stores({
  notes: 'id, userId, updatedAt'
});

db.version(2).stores({
  notes: 'id, userId, updatedAt, *tags'
}).upgrade(trans => {
  return trans.notes.toCollection().modify(note => {
    note.tags = note.tags || [];
  });
});

db.version(3).stores({
  notes: 'id, userId, updatedAt, *tags',
  versionSnapshots: 'id, [userId+noteId+timestamp], noteId, timestamp'
}).upgrade(trans => {
  // Add version snapshots table
  // Migrate existing notes to include mode field
  return trans.notes.toCollection().modify(note => {
    note.mode = note.mode || 'create'; // Default to create mode
  });
});
```

**Firestore Migrations**
- Use Cloud Functions for batch updates
- Version field in documents for gradual rollout
- Backward-compatible schema changes only

### Data Import
- CSV import for bulk note creation
- Evernote/Notion export compatibility (post-MVP)
- Institution data migration tools for team tier

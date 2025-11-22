# API Specifications (4-Week MVP)

## 1. API Architecture

### Technology Stack

- **Firebase Authentication**: User authentication and session management
- **Firestore Client SDK**: Direct database operations from client
- **Firebase Cloud Functions**: Server-side API endpoints (Node.js 20)
- **OpenAI API**: AI features via Cloud Functions
- **REST**: HTTP/JSON for Cloud Functions
- **Real-time**: Firestore listeners for live updates

### Base URLs

- **Cloud Functions**: `https://us-central1-nexly-rn.cloudfunctions.net/`
- **Firestore**: Direct SDK access via Firebase config
- **Auth**: Firebase Auth SDK

### Authentication

All API requests require Firebase Auth token in header:
```
Authorization: Bearer <firebase-id-token>
```

## 2. Authentication APIs

### Sign Up

**Client SDK**: `firebase.auth().createUserWithEmailAndPassword(email, password)`

**Post-signup Cloud Function**: `POST /api/users/initialize`

Creates user document in Firestore after successful signup

**Request Body**:
```typescript
{
  displayName: string
  email: string
}
```

**Response**:
```typescript
{
  userId: string
  tier: 'free'
  createdAt: Timestamp
}
```

### Sign In

**Client SDK**: `firebase.auth().signInWithEmailAndPassword(email, password)`

### Sign Out

**Client SDK**: `firebase.auth().signOut()`

### Password Reset

**Client SDK**: `firebase.auth().sendPasswordResetEmail(email)`

## 3. User Management APIs

### Get User Profile

**Firestore**: Read from `/users/{userId}`

**Client SDK**: Direct document read with Firestore SDK

### Update User Settings

**Firestore**: Update `/users/{userId}`

**Fields**:
```typescript
{
  settings: {
    theme: 'light' | 'dark' | 'system'
    autoSave: boolean
  }
}
```

### Get Usage Quota

**Firestore**: Read from `/users/{userId}`

**Response**:
```typescript
{
  usage: {
    autocompleteRequests: number
    keyTermSpottingUses: number
    resetDate: Timestamp
  }
  tier: 'free' | 'pro' | 'team'
}
```

### Update Subscription Tier

**Cloud Function**: `POST /api/users/updateTier`

**Request Body**:
```typescript
{
  tier: 'free' | 'pro' | 'team'
  paymentIntentId?: string
}
```

## 4. Notes APIs

### Create Note

**Firestore**: Create document in `/users/{userId}/notes/{noteId}`

**Schema**:
```typescript
{
  id: string
  userId: string
  title: string
  content: object // Tiptap JSON
  mode: 'create' | 'edit' | 'study'
  createdAt: Timestamp
  updatedAt: Timestamp
  metadata: {
    courseCode?: string
  }
  tags: string[]
  stats: {
    wordCount: number
    characterCount: number
  }
}
```

### Get Note

**Firestore**: Read from `/users/{userId}/notes/{noteId}`

### Update Note

**Firestore**: Update `/users/{userId}/notes/{noteId}`

**Updatable Fields**: title, content, mode, metadata, tags, stats

### Delete Note

**Firestore**: Delete `/users/{userId}/notes/{noteId}`

**Note**: Cascade deletes snapshots via Cloud Function trigger

### List Notes

**Firestore Query**: `/users/{userId}/notes` ordered by `updatedAt desc`

**Filters**:
- Course: `where('metadata.courseCode', '==', courseCode)`
- Tags: `where('tags', 'array-contains', tag)`
- Date range: `where('createdAt', '>=', startDate)`

**Pagination**: `limit(20)` with cursor-based pagination

### Search Notes

**Local Dexie**: Full-text search in IndexedDB

**Cloud Function**: `POST /api/notes/search` (future enhancement)

## 5. Version Snapshot APIs (Backend Only - No UI in MVP)

### Create Snapshot

**Firestore**: Create in `/users/{userId}/notes/{noteId}/snapshots/{snapshotId}`

**Schema**:
```typescript
{
  id: string
  noteId: string
  userId: string
  content: object // Tiptap JSON
  mode: 'create' | 'edit' | 'study'
  timestamp: Timestamp
  changesSummary: {
    addedWords: number
    removedWords: number
    wordCountChange: number
  }
  snapshotType: 'auto' | 'manual' | 'mode_switch'
}
```

**Triggers**: Auto-save (30s), manual save, mode switch

**Note**: Snapshots stored in backend but no UI to view/manage them in MVP

### Get Last Saved Snapshot

**Firestore Query**: Filter by `snapshotType in ['manual', 'auto']`, order by `timestamp desc`, limit 1

**Used for**: Inline diff comparison in Edit Mode

### Delete Snapshot

**Firestore**: Delete `/users/{userId}/notes/{noteId}/snapshots/{snapshotId}`

**Retention Policy**: Auto-cleanup via Cloud Function (Free tier: keep last 5)

## 6. AI Feature APIs (MVP Only)

### Autocomplete (GPT-4.1 nano)

**Cloud Function**: `POST /api/ai/autocomplete`

**Request Body**:
```typescript
{
  context: string // Last 200 characters
  cursorPosition: number
}
```

**Response**:
```typescript
{
  suggestions: string[]
  quotaRemaining: number
}
```

**Model**: GPT-4.1 nano
**Performance Target**: <100ms
**Quota**: 100 requests/month (Free tier), unlimited (Pro tier)
**Fallback**: Local dictionary (5000+ terms)

### Key Term Spotting (GPT-4o-mini)

**Cloud Function**: `POST /api/ai/spotTerms`

**Request Body**:
```typescript
{
  noteId: string
  content: object // Tiptap JSON
}
```

**Response**:
```typescript
{
  terms: Array<{
    term: string
    position: number
    context: string
    importance: 'high' | 'medium' | 'low'
    reason: string
  }>
  quotaRemaining: number
}
```

**Model**: GPT-4o-mini with Structured Outputs
**Performance Target**: <5s for 3000-word note
**Quota**: 10 uses/month (Free tier), unlimited (Pro tier)

## 7. Fast-Follow APIs (Post-MVP, Week 5-8)

### Shorthand Expansion (Week 5-6)

**Cloud Function**: `POST /api/ai/expand` (deferred)

### Definition Lookup (Week 5-6)

**Cloud Function**: `POST /api/ai/define` (deferred)

### Cloze Deletion Generation (Week 7-8)

**Cloud Function**: `POST /api/ai/generateCloze` (deferred)

### Full Version History (Week 7-8)

**Firestore Query**: List all snapshots with UI (deferred)

**Compare Snapshots API**: Side-by-side diff (deferred)

## 8. Error Handling

### Error Response Format

```typescript
{
  error: {
    code: string
    message: string
    details?: object
  }
}
```

### Error Codes

- `AUTH_REQUIRED`: Missing or invalid auth token
- `PERMISSION_DENIED`: Insufficient permissions
- `NOT_FOUND`: Resource not found
- `QUOTA_EXCEEDED`: AI feature quota limit reached
- `INVALID_INPUT`: Validation error
- `RATE_LIMIT`: Too many requests
- `SERVER_ERROR`: Internal server error

### Rate Limiting

**Free Tier**: 100 autocomplete/month, 10 key term spotting/month
**Pro Tier**: Unlimited
**Rate Limit Headers**:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 42
X-RateLimit-Reset: 1234567890
```

## 9. Performance & Security

### Performance Targets (MVP)

- Autocomplete: <100ms
- Inline diff calculation (client-side): <200ms
- Key term spotting: <5s

### Security

- HTTPS only
- Firebase Auth tokens (1-hour refresh)
- Firestore security rules enforce user isolation
- Input validation via Zod schemas
- CORS restrictions on Cloud Functions
- Rate limiting per user
- No AI training on user data

### Caching Strategy

- User settings: Local storage
- Recent notes: Dexie cache with Firestore sync
- AI responses: No caching (always fresh)
- Local dictionary: Cached in JSON file (autocomplete fallback)

## 10. Quota Management

### Tracking Implementation

**Firestore `users` collection**:
- `usage.autocompleteRequests`: monthly counter, resets on `resetDate`
- `usage.keyTermSpottingUses`: monthly counter
- `usage.resetDate`: first day of next month

### Enforcement Strategy

**Client-side**:
- Check quota before API call
- Display usage badge when >80% consumed
- Show upgrade modal at 100%

**Server-side** (Firebase Functions):
- Validate quota on every request
- Return 429 status if exceeded
- Log quota breaches for analytics

### Fallback Behavior

**Autocomplete quota exceeded**:
- Switch to local dictionary automatically
- Show subtle indicator: "Using offline mode"
- No user workflow disruption

**Key term spotting quota exceeded**:
- Display upgrade prompt with feature comparison
- Allow preview of Pro features (1 free try)
- Offer annual discount in modal

## 11. Future Enhancements (Post-MVP)

### Week 5-6

- **Templates API**: Create/read/update/delete nursing templates
- **Slash Commands**: Template insertion shortcuts
- **Shorthand Expansion API**: AI converts abbreviations
- **Definition API**: Lookup term definitions

### Week 7-8

- **Cloze Generation API**: AI suggests fill-in-the-blank questions
- **Full Version History API**: List/compare/restore snapshots with UI
- **Side-by-Side Diff API**: Compare any two versions

### Month 2+

- **Export API**: Generate PDF/DOCX exports
- **Educator Validation API**: Definition review workflow
- **Analytics API**: Usage insights and performance tracking

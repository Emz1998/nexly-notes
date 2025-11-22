# API Specifications - Next.js Stack (4-Week MVP)

## 1. API Architecture

### Technology Stack

- **Next.js API Routes**: Serverless functions using App Router (`app/api/**/route.ts`)
- **Firebase Authentication**: User authentication via Client SDK + Admin SDK for verification
- **Firestore Client SDK**: Direct database operations from client
- **Firebase Admin SDK**: Server-side operations in API routes
- **OpenAI API**: AI features via Next.js API routes
- **REST**: HTTP/JSON for API routes
- **Real-time**: Firestore listeners for live updates

### Base URLs

- **API Routes**: `/api/*` (same-origin, no CORS needed)
- **Firestore**: Direct SDK access via Firebase config
- **Auth**: Firebase Auth SDK (client) + Admin SDK (server)

### Authentication

All API requests require Firebase Auth token in header:

```
Authorization: Bearer <firebase-id-token>
```

**Token Verification** (Server-side in API routes):

```typescript
import { adminAuth } from "@/lib/firebase/admin";

const token = request.headers.get("authorization")?.split("Bearer ")[1];
const decodedToken = await adminAuth.verifyIdToken(token);
const userId = decodedToken.uid;
```

## 2. Authentication APIs

### Sign Up

**Client SDK**: `firebase.auth().createUserWithEmailAndPassword(email, password)`

**Post-signup API Route**: `POST /api/auth/initialize`

Creates user document in Firestore after successful signup

**Request Body**:

```typescript
{
  displayName: string;
  email: string;
}
```

**Response**:

```typescript
{
  userId: string;
  tier: "free";
  createdAt: Timestamp;
}
```

**Implementation**:

```typescript
// app/api/auth/initialize/route.ts
import { NextRequest, NextResponse } from "next/server";
import { adminAuth, adminDb } from "@/lib/firebase/admin";

export async function POST(request: NextRequest) {
  try {
    const token = request.headers.get("authorization")?.split("Bearer ")[1];
    if (!token) {
      return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
    }

    const decodedToken = await adminAuth.verifyIdToken(token);
    const userId = decodedToken.uid;

    const { displayName, email } = await request.json();

    const userData = {
      userId,
      email,
      displayName,
      tier: "free",
      usage: {
        autocompleteRequests: 0,
        keyTermSpottingUses: 0,
        resetDate: new Date(new Date().setMonth(new Date().getMonth() + 1)),
      },
      settings: {
        theme: "system",
        autoSave: true,
      },
      createdAt: new Date(),
      updatedAt: new Date(),
    };

    await adminDb.collection("users").doc(userId).set(userData);

    return NextResponse.json({
      userId,
      tier: "free",
      createdAt: userData.createdAt,
    });
  } catch (error) {
    return NextResponse.json(
      { error: "Failed to initialize user" },
      { status: 500 }
    );
  }
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

**Method 1: Firestore Client SDK** (Recommended for real-time)

```typescript
// Client-side
import { doc, getDoc } from "firebase/firestore";
import { db } from "@/lib/firebase/client";

const userDoc = await getDoc(doc(db, "users", userId));
```

**Method 2: API Route** (For server-side needs)

```typescript
// GET /api/users/[userId]/route.ts
export async function GET(
  request: NextRequest,
  { params }: { params: { userId: string } }
) {
  const token = request.headers.get("authorization")?.split("Bearer ")[1];
  const decodedToken = await adminAuth.verifyIdToken(token);

  // Verify user can only access their own data
  if (decodedToken.uid !== params.userId) {
    return NextResponse.json({ error: "Forbidden" }, { status: 403 });
  }

  const userDoc = await adminDb.collection("users").doc(params.userId).get();
  return NextResponse.json(userDoc.data());
}
```

### Update User Settings

**Firestore Client SDK**: Update `/users/{userId}`

```typescript
import { doc, updateDoc } from "firebase/firestore";

await updateDoc(doc(db, "users", userId), {
  "settings.theme": "dark",
  "settings.autoSave": true,
});
```

**Fields**:

```typescript
{
  settings: {
    theme: "light" | "dark" | "system";
    autoSave: boolean;
  }
}
```

### Get Usage Quota

**API Route**: `GET /api/users/quota`

**Response**:

```typescript
{
  usage: {
    autocompleteRequests: number;
    keyTermSpottingUses: number;
    resetDate: Timestamp;
  }
  tier: "free" | "pro" | "team";
  quotaRemaining: {
    autocomplete: number; // null if unlimited
    keyTermSpotting: number; // null if unlimited
  }
}
```

**Implementation**:

```typescript
// app/api/users/quota/route.ts
export async function GET(request: NextRequest) {
  const token = request.headers.get("authorization")?.split("Bearer ")[1];
  const decodedToken = await adminAuth.verifyIdToken(token);
  const userId = decodedToken.uid;

  const userDoc = await adminDb.collection("users").doc(userId).get();
  const userData = userDoc.data();

  const quotaLimits = {
    free: { autocomplete: 100, keyTermSpotting: 10 },
    pro: { autocomplete: null, keyTermSpotting: null },
    team: { autocomplete: null, keyTermSpotting: null },
  };

  const limits = quotaLimits[userData.tier];

  return NextResponse.json({
    usage: userData.usage,
    tier: userData.tier,
    quotaRemaining: {
      autocomplete: limits.autocomplete
        ? limits.autocomplete - userData.usage.autocompleteRequests
        : null,
      keyTermSpotting: limits.keyTermSpotting
        ? limits.keyTermSpotting - userData.usage.keyTermSpottingUses
        : null,
    },
  });
}
```

### Update Subscription Tier

**API Route**: `POST /api/users/update-tier`

**Request Body**:

```typescript
{
  tier: 'free' | 'pro' | 'team';
  paymentIntentId?: string;
}
```

**Implementation**:

```typescript
// app/api/users/update-tier/route.ts
export async function POST(request: NextRequest) {
  const token = request.headers.get("authorization")?.split("Bearer ")[1];
  const decodedToken = await adminAuth.verifyIdToken(token);
  const userId = decodedToken.uid;

  const { tier, paymentIntentId } = await request.json();

  // Verify payment if upgrading (integrate with Stripe)
  if (tier !== "free" && !paymentIntentId) {
    return NextResponse.json({ error: "Payment required" }, { status: 400 });
  }

  await adminDb.collection("users").doc(userId).update({
    tier,
    updatedAt: new Date(),
  });

  return NextResponse.json({ success: true, tier });
}
```

## 4. Notes APIs

### Create Note

**Firestore Client SDK**: Create document in `/users/{userId}/notes/{noteId}`

```typescript
import { collection, addDoc } from "firebase/firestore";

const noteRef = await addDoc(collection(db, `users/${userId}/notes`), {
  id: crypto.randomUUID(),
  userId,
  title: "Untitled Note",
  content: { type: "doc", content: [] },
  mode: "create",
  createdAt: new Date(),
  updatedAt: new Date(),
  metadata: {},
  tags: [],
  stats: {
    wordCount: 0,
    characterCount: 0,
  },
});
```

**Schema**:

```typescript
{
  id: string;
  userId: string;
  title: string;
  content: object; // Tiptap JSON
  mode: 'create' | 'edit' | 'study';
  createdAt: Timestamp;
  updatedAt: Timestamp;
  metadata: {
    courseCode?: string;
  };
  tags: string[];
  stats: {
    wordCount: number;
    characterCount: number;
  };
}
```

### Get Note

**Firestore Client SDK**: Read from `/users/{userId}/notes/{noteId}`

```typescript
import { doc, getDoc } from "firebase/firestore";

const noteDoc = await getDoc(doc(db, `users/${userId}/notes`, noteId));
```

### Update Note

**Firestore Client SDK**: Update `/users/{userId}/notes/{noteId}`

```typescript
import { doc, updateDoc } from "firebase/firestore";

await updateDoc(doc(db, `users/${userId}/notes`, noteId), {
  title: "Updated Title",
  content: updatedContent,
  updatedAt: new Date(),
});
```

**Updatable Fields**: title, content, mode, metadata, tags, stats

### Delete Note

**Firestore Client SDK**: Delete `/users/{userId}/notes/{noteId}`

```typescript
import { doc, deleteDoc } from "firebase/firestore";

await deleteDoc(doc(db, `users/${userId}/notes`, noteId));
```

**Note**: Cascade deletes snapshots via Cloud Function trigger

### List Notes

**Firestore Client SDK**: Query `/users/{userId}/notes` ordered by `updatedAt desc`

```typescript
import { collection, query, orderBy, limit, getDocs } from "firebase/firestore";

const q = query(
  collection(db, `users/${userId}/notes`),
  orderBy("updatedAt", "desc"),
  limit(20)
);
const snapshot = await getDocs(q);
```

**Filters**:

```typescript
// By course
import { where } from "firebase/firestore";

const q = query(
  collection(db, `users/${userId}/notes`),
  where("metadata.courseCode", "==", "NURS 301"),
  orderBy("updatedAt", "desc")
);

// By tag
const q = query(
  collection(db, `users/${userId}/notes`),
  where("tags", "array-contains", "pharmacology"),
  orderBy("updatedAt", "desc")
);

// By date range
const q = query(
  collection(db, `users/${userId}/notes`),
  where("createdAt", ">=", startDate),
  where("createdAt", "<=", endDate)
);
```

**Pagination**: Use `startAfter()` for cursor-based pagination

```typescript
import { startAfter, limitToLast } from "firebase/firestore";

const lastDoc = snapshot.docs[snapshot.docs.length - 1];
const nextPage = query(
  collection(db, `users/${userId}/notes`),
  orderBy("updatedAt", "desc"),
  startAfter(lastDoc),
  limit(20)
);
```

### Search Notes

**Local Dexie**: Full-text search in IndexedDB

```typescript
import { db } from "@/lib/dexie/db";

const results = await db.notes
  .where("userId")
  .equals(userId)
  .filter(
    (note) =>
      note.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      JSON.stringify(note.content)
        .toLowerCase()
        .includes(searchTerm.toLowerCase())
  )
  .toArray();
```

**API Route** (future enhancement): `POST /api/notes/search`

## 5. Version Snapshot APIs (Backend Only - No UI in MVP)

### Create Snapshot

**Firestore Client SDK**: Create in `/users/{userId}/notes/{noteId}/snapshots/{snapshotId}`

```typescript
import { collection, addDoc } from "firebase/firestore";

await addDoc(collection(db, `users/${userId}/notes/${noteId}/snapshots`), {
  id: crypto.randomUUID(),
  noteId,
  userId,
  content: currentContent,
  mode: currentMode,
  timestamp: new Date(),
  changesSummary: {
    addedWords: 10,
    removedWords: 5,
    wordCountChange: 5,
  },
  snapshotType: "auto",
});
```

**Schema**:

```typescript
{
  id: string;
  noteId: string;
  userId: string;
  content: object; // Tiptap JSON
  mode: "create" | "edit" | "study";
  timestamp: Timestamp;
  changesSummary: {
    addedWords: number;
    removedWords: number;
    wordCountChange: number;
  }
  snapshotType: "auto" | "manual" | "mode_switch";
}
```

**Triggers**: Auto-save (30s), manual save, mode switch

**Note**: Snapshots stored in backend but no UI to view/manage them in MVP

### Get Last Saved Snapshot

**Firestore Client SDK**: Filter by `snapshotType in ['manual', 'auto']`, order by `timestamp desc`, limit 1

```typescript
import {
  collection,
  query,
  where,
  orderBy,
  limit,
  getDocs,
} from "firebase/firestore";

const q = query(
  collection(db, `users/${userId}/notes/${noteId}/snapshots`),
  where("snapshotType", "in", ["manual", "auto"]),
  orderBy("timestamp", "desc"),
  limit(1)
);
const snapshot = await getDocs(q);
const lastSaved = snapshot.docs[0]?.data();
```

**Used for**: Inline diff comparison in Edit Mode

### Delete Snapshot

**Firestore Client SDK**: Delete `/users/{userId}/notes/{noteId}/snapshots/{snapshotId}`

```typescript
await deleteDoc(
  doc(db, `users/${userId}/notes/${noteId}/snapshots`, snapshotId)
);
```

**Retention Policy**: Auto-cleanup via Cloud Function (Free tier: keep last 5)

## 6. AI Feature APIs (MVP Only)

### Autocomplete (GPT-4.1 nano)

**API Route**: `POST /api/ai/autocomplete`

**Request Body**:

```typescript
{
  context: string; // Last 200 characters
  cursorPosition: number;
}
```

**Response**:

```typescript
{
  suggestions: string[];
  quotaRemaining: number;
}
```

**Implementation**:

```typescript
// app/api/ai/autocomplete/route.ts
import { NextRequest, NextResponse } from "next/server";
import { adminAuth, adminDb } from "@/lib/firebase/admin";
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(request: NextRequest) {
  try {
    // Verify auth token
    const token = request.headers.get("authorization")?.split("Bearer ")[1];
    const decodedToken = await adminAuth.verifyIdToken(token);
    const userId = decodedToken.uid;

    // Check quota
    const userDoc = await adminDb.collection("users").doc(userId).get();
    const userData = userDoc.data();

    const quotaLimit = userData.tier === "free" ? 100 : null;
    if (quotaLimit && userData.usage.autocompleteRequests >= quotaLimit) {
      // Use local dictionary fallback
      const localSuggestions = await getLocalDictionarySuggestions(
        request.body.context
      );
      return NextResponse.json({
        suggestions: localSuggestions,
        quotaRemaining: 0,
        fallback: true,
      });
    }

    // Get OpenAI suggestions
    const { context, cursorPosition } = await request.json();

    const completion = await openai.chat.completions.create({
      model: "gpt-4o-nano-realtime-preview-2024-12-17",
      messages: [
        {
          role: "system",
          content:
            "You are a nursing terminology autocomplete assistant. Suggest 3-5 contextually relevant nursing terms or phrases.",
        },
        {
          role: "user",
          content: `Context: ${context}\nCursor position: ${cursorPosition}`,
        },
      ],
      max_tokens: 50,
      temperature: 0.7,
    });

    const suggestions =
      completion.choices[0].message.content
        ?.split("\n")
        .filter((s) => s.trim())
        .slice(0, 5) || [];

    // Increment quota
    await adminDb
      .collection("users")
      .doc(userId)
      .update({
        "usage.autocompleteRequests": userData.usage.autocompleteRequests + 1,
      });

    const quotaRemaining = quotaLimit
      ? quotaLimit - userData.usage.autocompleteRequests - 1
      : null;

    return NextResponse.json({
      suggestions,
      quotaRemaining,
    });
  } catch (error) {
    console.error("Autocomplete error:", error);
    return NextResponse.json(
      { error: "Failed to generate suggestions" },
      { status: 500 }
    );
  }
}

async function getLocalDictionarySuggestions(context: string) {
  // Load local nursing terms dictionary
  const dictionary = require("@/public/dictionaries/nursing-terms.json");
  // Simple prefix matching
  const lastWord = context.split(/\s+/).pop()?.toLowerCase() || "";
  return dictionary
    .filter((term) => term.toLowerCase().startsWith(lastWord))
    .slice(0, 5);
}
```

**Model**: GPT-4.1 nano
**Performance Target**: <100ms
**Quota**: 100 requests/month (Free tier), unlimited (Pro tier)
**Fallback**: Local dictionary (5000+ terms)

### Key Term Spotting (GPT-4o-mini)

**API Route**: `POST /api/ai/spot-terms`

**Request Body**:

```typescript
{
  noteId: string;
  content: object; // Tiptap JSON
}
```

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

**Implementation**:

```typescript
// app/api/ai/spot-terms/route.ts
import { NextRequest, NextResponse } from "next/server";
import { adminAuth, adminDb } from "@/lib/firebase/admin";
import OpenAI from "openai";

const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY,
});

export async function POST(request: NextRequest) {
  try {
    const token = request.headers.get("authorization")?.split("Bearer ")[1];
    const decodedToken = await adminAuth.verifyIdToken(token);
    const userId = decodedToken.uid;

    // Check quota
    const userDoc = await adminDb.collection("users").doc(userId).get();
    const userData = userDoc.data();

    const quotaLimit = userData.tier === "free" ? 10 : null;
    if (quotaLimit && userData.usage.keyTermSpottingUses >= quotaLimit) {
      return NextResponse.json(
        { error: "Quota exceeded", quotaRemaining: 0 },
        { status: 429 }
      );
    }

    const { noteId, content } = await request.json();

    // Convert Tiptap JSON to plain text
    const plainText = extractTextFromTiptap(content);

    // Use GPT-4o-mini with Structured Outputs
    const completion = await openai.chat.completions.create({
      model: "gpt-4o-mini-2024-07-18",
      messages: [
        {
          role: "system",
          content: `You are a nursing education assistant. Identify exam-relevant key terms and concepts in student notes. Look for:
1. Professor emphasis cues ("important", "remember", "test will cover", "focus on")
2. Medical terminology
3. Clinical procedures
4. Medications and treatments
5. Disease processes
6. Nursing interventions

Return terms with their importance level and reason for identification.`,
        },
        {
          role: "user",
          content: plainText,
        },
      ],
      response_format: {
        type: "json_schema",
        json_schema: {
          name: "key_terms",
          schema: {
            type: "object",
            properties: {
              terms: {
                type: "array",
                items: {
                  type: "object",
                  properties: {
                    term: { type: "string" },
                    position: { type: "number" },
                    context: { type: "string" },
                    importance: {
                      type: "string",
                      enum: ["high", "medium", "low"],
                    },
                    reason: { type: "string" },
                  },
                  required: [
                    "term",
                    "position",
                    "context",
                    "importance",
                    "reason",
                  ],
                },
              },
            },
            required: ["terms"],
          },
        },
      },
      max_tokens: 2000,
    });

    const result = JSON.parse(completion.choices[0].message.content);

    // Increment quota
    await adminDb
      .collection("users")
      .doc(userId)
      .update({
        "usage.keyTermSpottingUses": userData.usage.keyTermSpottingUses + 1,
      });

    const quotaRemaining = quotaLimit
      ? quotaLimit - userData.usage.keyTermSpottingUses - 1
      : null;

    return NextResponse.json({
      terms: result.terms,
      quotaRemaining,
    });
  } catch (error) {
    console.error("Key term spotting error:", error);
    return NextResponse.json(
      { error: "Failed to spot terms" },
      { status: 500 }
    );
  }
}

function extractTextFromTiptap(content: any): string {
  // Recursively extract text from Tiptap JSON
  if (typeof content === "string") return content;
  if (content.text) return content.text;
  if (content.content && Array.isArray(content.content)) {
    return content.content.map(extractTextFromTiptap).join(" ");
  }
  return "";
}
```

**Model**: GPT-4o-mini with Structured Outputs
**Performance Target**: <5s for 3000-word note
**Quota**: 10 uses/month (Free tier), unlimited (Pro tier)

## 7. Error Handling

### Error Response Format

```typescript
{
  error: {
    code: string;
    message: string;
    details?: object;
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

**Rate Limit Headers** (returned in responses):

```typescript
{
  'X-RateLimit-Limit': '100',
  'X-RateLimit-Remaining': '42',
  'X-RateLimit-Reset': '1234567890'
}
```

**Implementation**:

```typescript
// lib/rate-limit.ts
export function addRateLimitHeaders(
  response: NextResponse,
  limit: number | null,
  remaining: number | null,
  resetDate: Date
) {
  if (limit !== null) {
    response.headers.set("X-RateLimit-Limit", limit.toString());
    response.headers.set("X-RateLimit-Remaining", remaining?.toString() || "0");
    response.headers.set("X-RateLimit-Reset", resetDate.getTime().toString());
  }
  return response;
}
```

## 8. Performance & Security

### Performance Targets (MVP)

- Autocomplete: <100ms
- Inline diff calculation (client-side): <200ms
- Key term spotting: <5s

### Security

- HTTPS only (automatic with Vercel/Next.js)
- Firebase Auth tokens (1-hour refresh)
- Firestore security rules enforce user isolation
- Input validation via Zod schemas in API routes
- CORS automatic (same-origin)
- Rate limiting per user
- No AI training on user data

### Caching Strategy

**API Route Caching**

```typescript
export const dynamic = "force-dynamic"; // Disable caching for auth-protected routes
export const revalidate = 0; // No caching
```

**Client-Side Caching**

- User settings: localStorage via Zustand persist
- Recent notes: Dexie cache with Firestore sync
- AI responses: No caching (always fresh)
- Local dictionary: Static JSON file

## 9. Quota Management

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

**Server-side** (Next.js API routes):

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

## 10. Middleware Configuration

### Auth Middleware

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-token")?.value;

  // Protected routes
  const protectedPaths = ["/notes", "/api/ai", "/api/users"];
  const isProtected = protectedPaths.some((path) =>
    request.nextUrl.pathname.startsWith(path)
  );

  if (isProtected && !token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/notes/:path*", "/api/ai/:path*", "/api/users/:path*"],
};
```

## 11. Environment Variables

```env
# .env.local

# Firebase (Client)
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

## 12. Fast-Follow APIs (Post-MVP, Week 5-8)

### Week 5-6

- **Templates API**: `GET /api/templates`, `POST /api/templates`
- **Shorthand Expansion**: `POST /api/ai/expand`
- **Definition Lookup**: `POST /api/ai/define`

### Week 7-8

- **Cloze Generation**: `POST /api/ai/generate-cloze`
- **Full Version History**: `GET /api/notes/[noteId]/snapshots`
- **Compare Snapshots**: `POST /api/notes/[noteId]/compare`

### Month 2+

- **Export API**: `POST /api/notes/[noteId]/export`
- **Analytics API**: `GET /api/analytics/usage`

This completes the revised API specifications for Next.js API routes.

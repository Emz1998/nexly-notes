# Security Specifications - Next.js Stack

## 1. Authentication & Authorization

### Firebase Authentication

**Email/Password Authentication**

- Password requirements: Minimum 8 characters, must include uppercase, lowercase, number
- Password hashing: Firebase Auth handles bcrypt with salt
- Account verification: Email verification required before full access
- Password reset: Firebase password reset flow with email confirmation

**Session Management**

- Session tokens: Firebase ID tokens with 1-hour expiration
- Token refresh: Automatic refresh using refresh tokens (valid 30 days)
- Cookie storage: HttpOnly, Secure, SameSite=Strict flags
- Session revocation: Immediate on logout or password change

**Next.js Middleware for Auth**

```typescript
// middleware.ts
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
import { adminAuth } from "@/lib/firebase/admin";

export async function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-token")?.value;

  if (!token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  try {
    const decodedToken = await adminAuth.verifyIdToken(token);
    const requestHeaders = new Headers(request.headers);
    requestHeaders.set("x-user-id", decodedToken.uid);
    requestHeaders.set("x-user-tier", decodedToken.tier || "free");

    return NextResponse.next({
      request: {
        headers: requestHeaders,
      },
    });
  } catch (error) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
}

export const config = {
  matcher: ["/notes/:path*", "/api/ai/:path*", "/api/users/:path*"],
};
```

**API Route Protection**

```typescript
// lib/auth/verify-token.ts
import { NextRequest } from "next/server";
import { adminAuth } from "@/lib/firebase/admin";

export async function verifyAuthToken(request: NextRequest) {
  const authHeader = request.headers.get("authorization");
  if (!authHeader || !authHeader.startsWith("Bearer ")) {
    throw new Error("No auth token provided");
  }

  const token = authHeader.split("Bearer ")[1];
  const decodedToken = await adminAuth.verifyIdToken(token);
  return decodedToken;
}

// Usage in API routes
export async function POST(request: NextRequest) {
  try {
    const decodedToken = await verifyAuthToken(request);
    const userId = decodedToken.uid;
    // ... process request
  } catch (error) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
}
```

### Role-Based Access Control

**Tier-Based Permissions (4-Week MVP)**

- Free tier: 100 autocomplete requests/month, 10 key term spotting uses/month, 5 snapshots per note
- Pro tier: Unlimited autocomplete and key term spotting, unlimited snapshots
- Team tier: Pro features plus future educator dashboard access

**Permission Enforcement**

- Client-side: UI restrictions based on user tier (Zustand store)
- Server-side: Next.js API routes validate tier before processing requests
- Firestore rules: Enforce document-level access based on userId and tier

```typescript
// lib/auth/check-tier.ts
export async function checkUserTier(
  userId: string,
  requiredTier: "free" | "pro" | "team"
) {
  const userDoc = await adminDb.collection("users").doc(userId).get();
  const userTier = userDoc.data()?.tier || "free";

  const tierHierarchy = { free: 0, pro: 1, team: 2 };
  return tierHierarchy[userTier] >= tierHierarchy[requiredTier];
}
```

## 2. Data Security

### Encryption

**Encryption in Transit**

- All Firebase communication over TLS 1.3
- HTTPS enforcement (automatic with Vercel/Next.js)
- Next.js API routes use HTTPS only
- No unencrypted data transmission

**Encryption at Rest**

- Firestore: AES-256 encryption (Firebase managed)
- Cloud Storage: AES-256 encryption (Firebase managed)
- IndexedDB: Browser-level encryption (OS dependent)

**Key Management**

- Firebase handles encryption keys automatically
- API keys stored in environment variables (`.env.local`), never in code
- Rotation policy: API keys rotated every 90 days
- No user-managed encryption keys in MVP

**Environment Variable Security**

```typescript
// lib/env.ts
import { z } from "zod";

const envSchema = z.object({
  // Public (client-side)
  NEXT_PUBLIC_FIREBASE_API_KEY: z.string(),
  NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN: z.string(),
  NEXT_PUBLIC_FIREBASE_PROJECT_ID: z.string(),

  // Private (server-side only)
  FIREBASE_ADMIN_PROJECT_ID: z.string(),
  FIREBASE_ADMIN_CLIENT_EMAIL: z.string(),
  FIREBASE_ADMIN_PRIVATE_KEY: z.string(),
  OPENAI_API_KEY: z.string(),
});

export const env = envSchema.parse(process.env);
```

### Data Isolation

**User Data Separation**

- Firestore security rules enforce userId-based access
- Notes stored in user-specific subcollections: `/users/{userId}/notes/{noteId}`
- No cross-user queries allowed
- Version snapshots isolated per note and user
- Next.js API routes verify userId matches authenticated user

**Server Component Data Fetching**

```typescript
// app/(dashboard)/notes/page.tsx
import { adminDb } from "@/lib/firebase/admin";
import { cookies } from "next/headers";
import { adminAuth } from "@/lib/firebase/admin";

async function getUserNotes(userId: string) {
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
  // Verify user from cookie
  const token = cookies().get("auth-token")?.value;
  if (!token) redirect("/login");

  const decodedToken = await adminAuth.verifyIdToken(token);
  const userId = decodedToken.uid;

  // Fetch only user's notes
  const notes = await getUserNotes(userId);
  return <NotesList initialNotes={notes} />;
}
```

## 3. Application Security

### Input Validation & Sanitization

**Zod Schema Validation**

```typescript
// lib/validations/note.ts
import { z } from "zod";

export const noteSchema = z.object({
  title: z.string().min(1).max(200),
  content: z.object({
    type: z.literal("doc"),
    content: z.array(z.any()).optional(),
  }),
  mode: z.enum(["create", "edit", "study"]),
  tags: z.array(z.string()).max(20),
  metadata: z
    .object({
      courseCode: z.string().optional(),
    })
    .optional(),
});

export const autocompleteRequestSchema = z.object({
  context: z.string().max(200),
  cursorPosition: z.number().min(0),
});

export const keyTermsRequestSchema = z.object({
  noteId: z.string().uuid(),
  content: z.object({
    type: z.literal("doc"),
    content: z.array(z.any()),
  }),
});
```

**API Route Validation**

```typescript
// app/api/ai/autocomplete/route.ts
import { NextRequest, NextResponse } from "next/server";
import { autocompleteRequestSchema } from "@/lib/validations/note";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const validatedData = autocompleteRequestSchema.parse(body);

    // Process validated data
  } catch (error) {
    if (error instanceof z.ZodError) {
      return NextResponse.json(
        { error: "Invalid input", details: error.errors },
        { status: 400 }
      );
    }
    return NextResponse.json({ error: "Server error" }, { status: 500 });
  }
}
```

**Content Validation**

- Note titles: Max 200 characters, alphanumeric and common punctuation only
- Note content: Tiptap JSON schema validation
- Tags: Max 20 tags per note, max 50 characters per tag
- File uploads: Type and size validation (avatars: 5MB, attachments: 10MB)

**Sanitization Strategy**

- React: Default XSS protection via JSX escaping
- Tiptap content: Sanitized on render using ProseMirror schema
- User-generated HTML: Stripped before storage
- URL inputs: Protocol validation (http/https only)

### Cross-Site Scripting (XSS) Prevention

**Defense Layers**

- React automatic escaping for all rendered content
- Content Security Policy (CSP) headers via Next.js
- Tiptap editor: Schema-based content validation
- No `dangerouslySetInnerHTML` usage
- Sanitize user input before storing in Firestore

**CSP Configuration**

```typescript
// next.config.js
const securityHeaders = [
  {
    key: "Content-Security-Policy",
    value: `
      default-src 'self';
      script-src 'self' 'unsafe-eval' 'unsafe-inline' https://www.gstatic.com;
      style-src 'self' 'unsafe-inline';
      img-src 'self' data: https: blob:;
      connect-src 'self' https://*.firebaseio.com https://firestore.googleapis.com https://identitytoolkit.googleapis.com;
      font-src 'self';
      frame-ancestors 'none';
      base-uri 'self';
      form-action 'self';
    `
      .replace(/\s{2,}/g, " ")
      .trim(),
  },
];

module.exports = {
  async headers() {
    return [
      {
        source: "/:path*",
        headers: securityHeaders,
      },
    ];
  },
};
```

### Cross-Site Request Forgery (CSRF) Prevention

**CSRF Tokens**

- Firebase Auth tokens include CSRF protection
- Custom state parameter for OAuth flows
- SameSite cookie attribute set to Strict
- Verify origin header on sensitive operations

**Next.js Built-in Protection**

- Server Actions use built-in CSRF protection
- Same-origin policy enforced by default
- Origin validation in middleware

### Security Headers

```typescript
// next.config.js
const securityHeaders = [
  {
    key: "X-DNS-Prefetch-Control",
    value: "on",
  },
  {
    key: "Strict-Transport-Security",
    value: "max-age=63072000; includeSubDomains; preload",
  },
  {
    key: "X-Content-Type-Options",
    value: "nosniff",
  },
  {
    key: "X-Frame-Options",
    value: "DENY",
  },
  {
    key: "X-XSS-Protection",
    value: "1; mode=block",
  },
  {
    key: "Referrer-Policy",
    value: "strict-origin-when-cross-origin",
  },
  {
    key: "Permissions-Policy",
    value: "camera=(), microphone=(), geolocation=()",
  },
];
```

## 4. API & Third-Party Integration Security

### Next.js API Routes Security

**Route Handler Authentication**

```typescript
// app/api/ai/autocomplete/route.ts
import { NextRequest, NextResponse } from "next/server";
import { verifyAuthToken } from "@/lib/auth/verify-token";
import { checkRateLimit } from "@/lib/security/rate-limit";

export async function POST(request: NextRequest) {
  try {
    // Verify authentication
    const decodedToken = await verifyAuthToken(request);
    const userId = decodedToken.uid;

    // Check rate limit
    await checkRateLimit(userId, "autocomplete");

    // Process request
    // ...
  } catch (error) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }
}
```

**Environment Variables**

- Store API keys and secrets in `.env.local` (gitignored)
- Never commit secrets to version control
- Use Vercel environment variables for production
- Separate production and development configurations

### OpenAI API Security

**API Key Protection**

- Store OpenAI API key in Next.js environment variables (server-only)
- Never expose API key to client-side code
- Proxy all OpenAI requests through Next.js API routes
- Rotate API keys quarterly

**Request Validation**

```typescript
// app/api/ai/autocomplete/route.ts
export async function POST(request: NextRequest) {
  // Validate user tier and quota before OpenAI calls
  const userDoc = await adminDb.collection("users").doc(userId).get();
  const userData = userDoc.data();

  if (userData.tier === "free" && userData.usage.autocompleteRequests >= 100) {
    // Use local dictionary fallback
    return NextResponse.json({
      suggestions: getLocalDictionarySuggestions(context),
      quotaRemaining: 0,
      fallback: true,
    });
  }

  // Sanitize prompts to prevent prompt injection
  const sanitizedContext = sanitizePrompt(context);

  // Limit request size and token count
  const truncatedContext = sanitizedContext.slice(-200);

  // Implement timeout for API calls
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);

  try {
    const response = await openai.chat.completions.create(
      {
        // ... OpenAI config
      },
      { signal: controller.signal }
    );

    clearTimeout(timeoutId);
    return NextResponse.json(response);
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
}
```

**Data Privacy**

- Configure OpenAI to not train on user data
- Strip personally identifiable information from prompts
- Log API usage without storing note content
- Implement data retention policy for logs (30 days)

### Rate Limiting & Quota Enforcement

**User Quotas**

```typescript
// lib/security/quota.ts
export async function checkQuota(
  userId: string,
  feature: "autocomplete" | "keyTermSpotting"
) {
  const userDoc = await adminDb.collection("users").doc(userId).get();
  const userData = userDoc.data();

  const limits = {
    free: { autocomplete: 100, keyTermSpotting: 10 },
    pro: { autocomplete: null, keyTermSpotting: null },
    team: { autocomplete: null, keyTermSpotting: null },
  };

  const limit = limits[userData.tier][feature];
  if (limit === null) return true; // Unlimited

  const usage = userData.usage[`${feature}Uses`] || 0;
  return usage < limit;
}

export async function incrementQuota(
  userId: string,
  feature: "autocomplete" | "keyTermSpotting"
) {
  await adminDb
    .collection("users")
    .doc(userId)
    .update({
      [`usage.${feature}Uses`]: admin.firestore.FieldValue.increment(1),
    });
}
```

**Rate Limiting**

```typescript
// lib/security/rate-limit.ts
import { LRUCache } from "lru-cache";

const rateLimitCache = new LRUCache({
  max: 500,
  ttl: 60000, // 1 minute
});

export async function checkRateLimit(userId: string, endpoint: string) {
  const key = `${userId}:${endpoint}`;
  const requests = (rateLimitCache.get(key) as number) || 0;

  const limits = {
    autocomplete: 60, // 60 requests per minute
    keyTermSpotting: 5, // 5 requests per minute
  };

  if (requests >= limits[endpoint]) {
    throw new Error("Rate limit exceeded");
  }

  rateLimitCache.set(key, requests + 1);
}
```

## 5. Client-Side Security

### PWA Security

**Service Worker Security**

- HTTPS requirement for service worker registration
- Cache validation and integrity checks
- Limited cache scope to app resources only
- Periodic cache invalidation

```typescript
// next.config.js with next-pwa
const withPWA = require("next-pwa")({
  dest: "public",
  disable: process.env.NODE_ENV === "development",
  register: true,
  skipWaiting: true,
  sw: "/sw.js",
  runtimeCaching: [
    {
      urlPattern: /^https:\/\/firestore\.googleapis\.com/,
      handler: "NetworkFirst",
      options: {
        cacheName: "firestore-cache",
        expiration: {
          maxEntries: 50,
          maxAgeSeconds: 60 * 60, // 1 hour
        },
      },
    },
  ],
});
```

**Local Storage Security**

- IndexedDB for structured data storage (Dexie)
- No sensitive data in localStorage
- Clear storage on logout
- Implement storage quota management

**Token Storage**

```typescript
// lib/auth/token-storage.ts
"use client";

import { auth } from "@/lib/firebase/client";
import Cookies from "js-cookie";

export async function storeAuthToken(user: User) {
  const token = await user.getIdToken();

  // Store in httpOnly cookie via API route
  await fetch("/api/auth/set-cookie", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ token }),
  });
}

export function clearAuthToken() {
  Cookies.remove("auth-token");
}
```

## 6. Privacy & Compliance

### Data Privacy Guarantees

**User Note Privacy**

- Notes never used to train AI models (OpenAI policy configuration)
- No third-party analytics tracking note content
- Firebase Analytics: Aggregate usage data only
- User notes encrypted at rest and in transit

**Data Minimization**

- Collect only essential user information (email, name)
- No tracking of IP addresses or device fingerprints
- Optional profile information (institution for team tier)
- Anonymize analytics data

### User Consent & Transparency

**Privacy Policy**

- Clear explanation of data collection and usage
- Opt-in for non-essential analytics
- Cookie consent banner (GDPR-style)
- Privacy policy version tracking

**User Rights**

- Export all user data in JSON format
- Delete account and all associated data
- Modify personal information at any time
- Opt-out of email communications

### Data Retention Policies

**User Data**

- Active accounts: Indefinite retention
- Deleted accounts: 30-day grace period before permanent deletion
- Account recovery available during grace period

**Version Snapshots**

- Free tier: Last 5 snapshots per note, automatic cleanup
- Pro tier: Unlimited snapshots, no automatic deletion
- Team tier: 3-year minimum retention guarantee
- Orphaned snapshots: 7-day grace period after note deletion

**Logs and Analytics**

- User activity logs: 90 days
- Error logs: 30 days
- Anonymous analytics: Aggregated, indefinite
- Security logs: 1 year retention

## 7. Monitoring & Incident Response

### Security Logging

**Audit Logging**

```typescript
// lib/logging/audit.ts
export async function logSecurityEvent(event: {
  type: "auth" | "permission" | "quota" | "rate_limit";
  userId?: string;
  action: string;
  success: boolean;
  metadata?: Record<string, any>;
}) {
  await adminDb.collection("security_logs").add({
    ...event,
    timestamp: new Date(),
    ip: "...",
  });
}
```

**Error Tracking**

- Generic error messages to users
- Detailed error logs server-side (without sensitive data)
- Error categorization (client, server, network, validation)
- Consider Sentry integration (post-MVP)

### Anomaly Detection

**Behavioral Patterns**

- Unusual login patterns (location, time, frequency)
- Quota abuse detection (rapid API calls)
- Failed authentication attempts (brute force detection)
- Abnormal data access patterns

**Alerting Thresholds**

- 5 failed login attempts in 5 minutes: Account lockout
- Quota exceeded by 50%: Warning notification
- API error rate above 10%: Alert development team
- Unusual spike in requests: DDoS investigation

## 8. Secure Development Practices

### Code Review Requirements

**Security-Focused Reviews**

- All code changes reviewed by at least one other developer
- Mandatory review for authentication and authorization code
- Check for hardcoded secrets or credentials
- Verify input validation and error handling

### Dependency Management

**Vulnerability Scanning**

```json
// package.json
{
  "scripts": {
    "audit": "npm audit",
    "audit:fix": "npm audit fix"
  }
}
```

- Automated npm audit on every commit
- Dependabot for automated dependency updates
- Weekly dependency review and updates
- Pin major versions for stability

### CI/CD Security

```yaml
# .github/workflows/security.yml
name: Security Checks

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run dependency audit
        run: npm audit

      - name: Check for secrets
        uses: trufflesecurity/trufflehog@main

      - name: SAST scan
        uses: github/codeql-action/analyze@v2
```

This completes the revised security specifications for Next.js stack.

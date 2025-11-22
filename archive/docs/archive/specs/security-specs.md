# Security Specifications

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
- Secure cookie storage: HttpOnly, Secure, SameSite=Strict flags
- Session revocation: Immediate on logout or password change

**OAuth Integration** (future)
- Google OAuth 2.0 for simplified signup
- Scope limitations: Email and profile information only
- Token validation: Verify OAuth tokens server-side

### Role-Based Access Control

**Tier-Based Permissions (4-Week MVP)**
- Free tier: 100 autocomplete requests/month, 10 key term spotting uses/month, 5 snapshots per note (backend only, no UI)
- Pro tier: Unlimited autocomplete and key term spotting, unlimited snapshots
- Team tier: Pro features plus future educator dashboard access

**Permission Enforcement**
- Client-side: UI restrictions based on user tier
- Server-side: Cloud Functions validate tier before processing requests
- Firestore rules: Enforce document-level access based on userId and tier

### Multi-Factor Authentication** (post-MVP)
- SMS-based verification
- Authenticator app support (TOTP)
- Backup codes for recovery

## 2. Data Security

### Encryption

**Encryption in Transit**
- All Firebase communication over TLS 1.3
- HTTPS enforcement for web application
- Certificate pinning in Tauri desktop app
- No unencrypted data transmission

**Encryption at Rest**
- Firestore: AES-256 encryption (Firebase managed)
- Cloud Storage: AES-256 encryption (Firebase managed)
- IndexedDB: Browser-level encryption (OS dependent)
- Tauri local storage: Consider encryption for sensitive tokens (future enhancement)

**Key Management**
- Firebase handles encryption keys automatically
- API keys stored in environment variables, never in code
- Rotation policy: API keys rotated every 90 days
- No user-managed encryption keys in MVP

### Data Isolation

**User Data Separation**
- Firestore security rules enforce userId-based access
- Notes stored in user-specific subcollections: `/users/{userId}/notes/{noteId}`
- No cross-user queries allowed
- Version snapshots isolated per note and user

**Data Access Patterns (4-Week MVP)**
- Read access: User can only read their own data
- Write access: User can only create/update/delete their own data
- Educator access: Team tier users can access educator features (future, post-MVP)
- Definitions and validations: Deferred to Fast-Follow (Week 5-6)

## 3. Application Security

### Input Validation & Sanitization

**Zod Schema Validation**
- All user inputs validated with Zod schemas
- Type-safe validation for API requests and form submissions
- Custom validators for note content, titles, tags
- Validation errors returned with safe error messages (no stack traces)

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
- Content Security Policy (CSP) headers
- Tiptap editor: Schema-based content validation
- No `dangerouslySetInnerHTML` usage
- Sanitize user input before storing in Firestore

**CSP Configuration**
```
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'unsafe-inline' https://www.gstatic.com;
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://*.firebaseio.com https://firestore.googleapis.com;
  font-src 'self';
  frame-ancestors 'none';
```

### Cross-Site Request Forgery (CSRF) Prevention

**CSRF Tokens**
- Firebase Auth tokens include CSRF protection
- Custom state parameter for OAuth flows
- SameSite cookie attribute set to Strict
- Verify origin header on sensitive operations

**Additional Protections**
- Double-submit cookie pattern for state-changing operations
- Validate referer header for API requests
- Short-lived tokens for sensitive actions

### Security Headers

**HTTP Response Headers**
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`
- `Permissions-Policy: geolocation=(), microphone=(), camera=()`

## 4. API & Third-Party Integration Security

### Firebase Cloud Functions Security

**Function Authentication**
- All functions require Firebase Auth token validation
- Verify token signature and expiration server-side
- Reject requests with invalid or missing tokens
- Rate limiting per user and endpoint

**Environment Variables**
- Store API keys and secrets in Firebase Functions config
- Never commit secrets to version control
- Use `.env` files for local development (gitignored)
- Separate production and development configurations

**Input Validation**
- Validate all function parameters with Zod schemas
- Reject malformed requests with 400 status
- Log validation failures for security monitoring
- Return generic error messages to clients

### OpenAI API Security

**API Key Protection**
- Store OpenAI API key in Firebase Functions environment
- Never expose API key to client-side code
- Proxy all OpenAI requests through Cloud Functions
- Rotate API keys quarterly

**Request Validation**
- Validate user tier and quota before OpenAI calls
- Sanitize prompts to prevent prompt injection
- Limit request size and token count
- Implement timeout for API calls (30 seconds max)

**Data Privacy**
- Configure OpenAI to not train on user data
- Strip personally identifiable information from prompts
- Log API usage without storing note content
- Implement data retention policy for logs (30 days)

### Rate Limiting & Quota Enforcement

**User Quotas**
- Free tier: 100 autocomplete requests/month, 10 AI study actions/month
- Quota tracking in Firestore `users` collection
- Reset quota on first day of each month
- Fallback to dictionary-based autocomplete when quota exceeded

**Rate Limiting**
- Per-user rate limits: 60 requests per minute
- Per-IP rate limits: 100 requests per minute (web only)
- Exponential backoff for repeated limit violations
- 429 status code returned when limits exceeded

**DDoS Protection**
- Firebase App Check for bot detection
- Cloudflare or Cloud Armor for DDoS mitigation (future)
- Request throttling at Cloud Functions level

## 5. Client-Side Security

### Tauri Desktop Application Security

**IPC Security**
- Command whitelisting: Only specific commands allowed
- Input validation for all IPC messages
- No shell command execution from renderer
- Sandboxed renderer process

**File System Access**
- Restrict file operations to app data directory
- Validate file paths to prevent directory traversal
- Limit file types for uploads
- Secure file permissions (user-only read/write)

**Update Security**
- Code signing for app updates
- Verify update signatures before installation
- Secure update channel (HTTPS only)
- Rollback mechanism for failed updates

### Web Application Security (PWA)

**Service Worker Security**
- HTTPS requirement for service worker registration
- Cache validation and integrity checks
- Limited cache scope to app resources only
- Periodic cache invalidation

**Local Storage Security**
- IndexedDB for structured data storage
- No sensitive data in localStorage (use secure cookies)
- Clear storage on logout
- Implement storage quota management

**Token Storage**
- Firebase tokens stored in secure HttpOnly cookies
- Refresh tokens encrypted before storage
- Automatic token cleanup on session end
- No tokens in URL parameters or localStorage

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
- Cookie consent banner for web application
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

**Compliance Notes**
- *Not subject to HIPAA or FERPA regulations per project requirements*
- General data protection best practices followed
- GDPR-style user rights implemented (export, deletion)

## 7. Monitoring & Incident Response

### Security Logging

**Audit Logging**
- Authentication events (login, logout, failed attempts)
- Authorization failures (permission denied)
- Data access patterns (note creation, modification, deletion)
- API quota usage and limit violations
- Configuration changes in Cloud Functions

**Log Security**
- No sensitive data logged (passwords, note content)
- Structured logging with consistent format
- Centralized log aggregation (Firebase Logging)
- Log integrity protection (append-only)

### Error Tracking

**Error Handling**
- Generic error messages to users
- Detailed error logs server-side (without sensitive data)
- Error categorization (client, server, network, validation)
- Sentry integration for error tracking (post-MVP consideration)

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

### Incident Response

**Response Plan**
- Severity classification (critical, high, medium, low)
- Incident response team roles and contact information
- Communication plan for user notifications
- Post-incident review process

**Recovery Procedures**
- Automated backups: Daily Firestore backups (30-day retention)
- Point-in-time recovery available
- Rollback procedures for failed deployments
- User notification templates for security incidents

## 8. Threat Model & Mitigation

### Key Threats

**Unauthorized Access**
- Threat: Attacker gains access to user account
- Mitigation: Strong password requirements, rate limiting, session expiration, MFA (future)

**Data Breach**
- Threat: Attacker accesses user notes or personal information
- Mitigation: Encryption at rest/transit, Firestore security rules, user data isolation

**API Abuse**
- Threat: Attacker bypasses quota limits or abuses AI features
- Mitigation: Rate limiting, quota tracking, Cloud Functions validation, token validation

**Injection Attacks**
- Threat: SQL injection, XSS, prompt injection
- Mitigation: Zod validation, React escaping, parameterized queries (Firestore), prompt sanitization

**Man-in-the-Middle (MITM)**
- Threat: Attacker intercepts data in transit
- Mitigation: TLS 1.3 enforcement, certificate pinning (Tauri), HTTPS-only

**Credential Theft**
- Threat: Attacker steals authentication tokens or passwords
- Mitigation: HttpOnly cookies, secure token storage, short token expiration, password hashing

### Attack Vectors

**Client-Side Attacks**
- XSS via user-generated content: Mitigated by React escaping and CSP
- Local storage tampering: Mitigated by server-side validation
- Malicious browser extensions: Mitigated by CSP and secure token storage

**Server-Side Attacks**
- Brute force login: Mitigated by rate limiting and account lockout
- API enumeration: Mitigated by authentication requirements and rate limiting
- DoS attacks: Mitigated by Firebase rate limiting and DDoS protection

**Third-Party Risks**
- OpenAI API compromise: Mitigated by key rotation and request proxying
- Firebase service outage: Mitigated by offline-first architecture with Dexie
- Dependency vulnerabilities: Mitigated by automated scanning and updates

## 9. Security Testing Requirements

### Testing Strategy

**Unit Testing**
- Test authentication functions (login, logout, token validation)
- Test authorization checks (tier-based permissions)
- Test input validation (Zod schemas)
- Test encryption/decryption utilities

**Integration Testing**
- Test complete authentication flows (signup, login, password reset)
- Test Firestore security rules enforcement
- Test API quota enforcement
- Test cross-device sync security

**Security Testing**
- Penetration testing before production launch
- Automated vulnerability scanning (npm audit, Dependabot)
- OWASP Top 10 validation
- Security code review for sensitive operations

**Test Coverage**
- Target: 80% coverage for security-critical code paths
- Mandatory tests for authentication, authorization, validation
- Mock external services (Firebase, OpenAI) in tests

## 10. Secure Development Practices

### Code Review Requirements

**Security-Focused Reviews**
- All code changes reviewed by at least one other developer
- Mandatory review for authentication and authorization code
- Check for hardcoded secrets or credentials
- Verify input validation and error handling

### Dependency Management

**Vulnerability Scanning**
- Automated npm audit on every commit
- Dependabot for automated dependency updates
- Weekly dependency review and updates
- Pin major versions for stability

**Trusted Dependencies**
- Use only well-maintained, popular libraries
- Verify package integrity (npm signatures)
- Minimize dependency count
- Regular security audits of critical dependencies

### Environment Configuration

**Development Environment**
- Separate Firebase projects for dev, staging, production
- Use .env files for local development (gitignored)
- Never commit secrets to version control
- Use environment-specific API keys

**CI/CD Security**
- Run security linters (ESLint security rules)
- Automated tests must pass before merge
- Secrets managed via GitHub Actions secrets
- Code signing for production builds

### Security Training

**Developer Guidelines**
- Security best practices documentation
- Regular security training sessions
- Incident response drills
- Stay updated on common vulnerabilities (OWASP Top 10)

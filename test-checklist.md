#### **MS-001:** PowerSync Offline Sync (Week 3-4)

**Goal:** Implement PowerSync for offline-first sync between SQLite and Supabase

**Tasks:**

- [x] T178: Install and configure PowerSync (@powersync/web)
- [x] T179: Create PowerSync schema matching PostgreSQL tables
- [x] T180: Configure PowerSync bucket definitions for user data isolation
- [x] T181: Replace local storage layer with PowerSync SQLite
- [x] T182: Implement useOnlineStatus hook to detect connectivity changes
- [x] T183: Create sync status indicator connected to PowerSync state
- [x] T184: Implement auto-sync when network restored
- [x] T185: Create feature flag to toggle mock vs real sync
- [x] T186: Write integration tests for offline/online sync scenarios

**Acceptance Criteria:**

- [x] Notes save to local SQLite instantly
- [x] Notes sync to Supabase automatically when online (FR-017)
- [x] Offline editing works with all features (FR-018)
- [x] Sync status indicator reflects real state

**Verification:**

- Edit note offline, restore network, verify sync completes
- Check Supabase database for synced notes

---

#### **MS-020:** Sync Conflict Resolution (Week 4)

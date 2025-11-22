---
name: Reaearch Workflow
description: Research solutions to a problem
model: claude-opus-4-1-20250805
---

# Lean Research Workflow for Feature Implementation

**Important!** Use Firecrawl MCP server for Web research

## 1. Define the Feature Goal
- Describe the feature in one sentence (what it should do, not how).
- Identify **key requirements** (functional + non-functional).
- Note constraints (performance, security, compatibility).

## 2. Identify Knowledge Gaps
- What don’t we know yet? (APIs, libraries, design patterns, system limits).
- What assumptions are we making?  
  *e.g., “Library X supports offline mode,” “Database Y can handle this query pattern.”*

## 3. Explore Options
- Research potential solutions:
  - Official docs and API references. **Important!** Use context7 MCP for this. Do not skip this!
  - Community best practices, tutorials, blog posts.
  - Code samples, open-source repos.
- List at least 2–3 candidate approaches.

## 4. Evaluate Quickly
- Compare options against constraints:
  - **Feasibility**: Can we integrate it with current stack?
  - **Complexity**: How hard to implement and maintain?
  - **Scalability**: Will it break at higher loads?
  - **Trade-offs**: What do we gain/lose?
- Summarize in a quick pros/cons table.

## 5. Prototype / Spike
- Build the smallest proof-of-concept (PoC) to test critical assumptions.
- Validate integration points (e.g., API calls, DB queries, UI component rendering).
- Document results with logs, screenshots, or benchmarks.

## 6. Decide & Document
- Select the most viable approach.
- Record:
  - Problem & requirements.
  - Options considered.
  - Why the chosen solution won.
- Store your report in @tmp/ folder
- Store in issue tracker, feature doc, or README for team reference.

## 7. Act & Iterate
- Start implementation with confidence in chosen path.
- Revisit assumptions if blockers arise.
- Feed back insights into documentation for future features.

### Key Principles and Rules
- **Bias for action**: Move from research → spike → decision fast.
- **Just enough depth**: Don’t over-analyze; test assumptions with small PoCs.
- **Transparent decisions**: Document why you picked one approach over others.
- **Reusable knowledge**: Make notes so the next developer doesn’t repeat the same research.

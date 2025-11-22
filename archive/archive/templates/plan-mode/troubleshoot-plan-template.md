# Troubleshooting Workflow

## Phase 1: EXPLORE

**Purpose**: Gather information, understand context, analyze requirements through deep thinking and systematic research
**Sub-agent Needed**: `research-specialist`

### 1.1 Tasks Difficulty Analysis

**Ask yourself these 5 quick checks**:

#### 1. Clarity  
Can I explain the task in one sentence without needing follow-ups?  
- Simple: “Fix typo in the README”  
- Complex: “Refactor API handler for scalability” (too vague / broad)  

#### 2. Scope  
Does the task only touch **one file / one module / one config**?  
- Simple: “Update button color in Tailwind config”  
- Complex: “Rework sidebar + dashboard state management” (multi-module)  

#### 3. Risk  
If I mess this up, will it break production or cause data loss?  
- Simple: “Add missing import” (low risk)  
- Complex: “Change Firestore security rule” (could block users)  

#### 4. Speed  
Can it be finished in **a single agent run or short sequence of runs** (typically under 5 minutes of agent execution)?  
- Simple: “Update placeholder text in editor component” (quick one-pass fix)  
- Complex: “Implement new authentication flow with OAuth” (multi-step, requires retries and coordination)  
 

#### 5. Dependencies  
Does it require coordination with others or multiple approvals?  
- Simple: “Fix broken link in onboarding docs”  
- Complex: “Change core API schema (needs frontend + backend sync)”  

**If the task is simple enough to be completed, proceed to execution phase**
**If the task is complex enough, proceed to 1.2 Deep Analysis**

### 1.2 Deep Analysis

- Use `mcp__sequentialthinking__sequentialthinking` to think deeply about the task
- Start with 5-10 thoughts minimum to understand problem space
- Question assumptions and explore edge cases
- Branch thinking when multiple approaches are viable
- Document confidence level in understanding

### 1.2 Context Sufficiency Check

1. Is the task simple enough to be completed with local context?
2. Can I fully understand the requirements?
3. Are there domain-specific details missing?
4. Do I need current/external information?
5. Is the technical approach clear from existing docs?

If context is **insufficient** → proceed to External Research
If context is **sufficient** → proceed directly to PLAN phase

### 1.3 External Research

**Only proceed here if references and local exploration are insufficient**

- **`firecrawl_search`**: Find specific information across multiple websites
- **`firecrawl_deep_research`**: Conduct comprehensive research on complex topics (use for complex unknowns)
- **`firecrawl_map`**: Discover all URLs on documentation sites before exploration
- **`firecrawl_scrape`**: Extract content from specific documentation pages
- **`firecrawl_extract`**: Pull structured data from web resources (APIs, specs, examples)
- **`firecrawl_crawl`**: Comprehensive multi-page content extraction when needed

## 2. PLAN Phase

**Purpose**: Create structured approach with review and validation through deep thinking

### Create a Detailed Plan

- Use `mcp__sequentialthinking__sequentialthinking` for plan development
- Follow the plan structure below:

#### Plan Mode Template Structure

***Follow this template during `plan mode`***

1. Situation & Problem Statement  

- What’s happening, who/what is affected, and how urgent is it?  
*(Be concise, but capture scope + impact.)*  

2. Objective  
- What does “fixed” look like for this situation?  
*(Can be time-bound, outcome-based, or simply “restore X to working state.”)*  

3. Strategic Approach (choose what fits)  

- Stabilize: contain the issue, stop further damage.  
- Diagnose: gather info, form hypotheses, isolate cause.  
- Intervene: try the lowest-risk, highest-likelihood fixes first.  
- Validate: confirm the issue is gone through tests/logs.  
- Document & Prevent: record findings, update docs, add guardrails.  

4. Resources & Roles  

- Which tools, subagents, or docs are relevant here?  
*(Example: `debug-assistant` for log parsing, `research-specialist` for root-cause research.)*  

5. Success Criteria  
- How will you know the issue is fully resolved?  

6. Risks & Constraints  
- What could go wrong with certain fixes?  
- Are there time, resource, or compliance constraints?  

7. Mitigation & Guardrails  

- How will you reduce risk and prevent future recurrence?
- How will you avoid further damage during fix?  
- How to prevent the troubleshoot process from going south?

8. Action Plan (adaptable milestones)  

**Phase 1 Immediate Actions** 
- Provide a list of immediate actions to be taken

**Phase 2 Root Cause Analysis** 
- Formulate 2–3 hypotheses ranked by likelihood.

**Phase 3 Fix Deployment** 
- Choose a candidate fix (Example: restart service, reinstall deps, adjust config).
***If failure → rollback to baseline → test next hypothesis.***

**Phase 4 Validation** 
- Formulate a validation strategy to confirm if the issue is resolved

**Phase 5 Prevention** 
- Create a prevention strategy to prevent the issue from recurring

### Validate the Plan
 
- Validate the plan with GPT 5 and Gemini 2.5 pro model using `Zen MCP Server`
- Use ExitPlanMode tool to exit plan mode and present task to the user
- Proceed to EXECUTE phase if plan is approved

## 3. EXECUTE Phase

**Purpose**: Implement solution with appropriate agent deployment

### Execution Strategy

- **Agent Selection**: Choose from specialized agents (max 5 parallel)
- **Implementation**: Deploy agents based on task requirements
- **Reporting**: Track progress in agent reports
- **Coordination**: Use `ceo-assistant` for complex multi-agent tasks
- Monitor execution with systematic progress updates

## 4. Version Control and Reporting

### Reporting

- Use the reporting template to create a report
- Save the report to `docs/reports/[yyyy-mm-dd]/[category]/[task-name]-[timestamp].md`
- Add the report to the commit message

### Version Control Checklist

**Ask yourself these questions before committing or pushing:**

### 1. Clarity of Commit
- Is my commit message **clear, concise, and meaningful**?
- Does it describe **what changed** and **why**?

### 2. Size & Scope
- Does this commit cover **one logical change only** (not a grab-bag of unrelated edits)?
- Would it be easy for someone else (or me later) to review and understand?

### 3. Code State
- Did I run the code/tests and confirm it works as expected?
- Are there any **debug statements** (`console.log`, print, etc.) I should remove?
- Did I run **linting/formatting** tools?

### 4. Branch & Context
- Am I on the **correct branch**?
- Is this commit part of a **feature branch, hotfix, or experiment** (not directly on `main`)?
- Do I need to **pull/rebase** first to avoid conflicts?

### 5. Timing of Push
- Should I **commit locally** and wait until the feature is more complete?
- Or is this the right time to **push upstream** (to share, collaborate, or back up work)?
- Is this a **work-in-progress** (WIP) commit that needs a special prefix/tag?

### 6. Risk & Safety
- If I push this, could it **break CI/CD or production**?
- Do I need a **quality gate** (tests, review, approval) before pushing?


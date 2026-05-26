---
name: automate-dev
description: "Autonomous development workflow with iterative self-correction loops. Orchestrates the full build-review-test-fix cycle for any development task: delegates work to specialised subagents, runs code review and simplification passes, executes automated testing, detects and rejects band-aid fixes, enforces zero breaking changes, and loops until all issues are permanently resolved with production-ready, backwards-compatible code. Use whenever building features, fixing bugs, refactoring, or performing any multi-step development work. Triggers on: 'build', 'implement', 'develop', 'create feature', 'fix bug', 'refactor', 'automate', 'iterate until done', 'development workflow', 'build and test', or any task requiring autonomous code production with quality enforcement."
---

# Automated Development Skill

Autonomous, iterative development workflow that builds, reviews, tests, simplifies, and self-corrects code in a continuous loop until all quality gates pass. Zero tolerance for breaking changes, band-aid fixes, or workarounds.

## Core Principles

1. **Iterate Until Done**: Work loops through build → review → test → fix cycles until every issue is permanently resolved
2. **No Band-Aids**: Every fix must address root cause. Workarounds, suppressions, and temporary patches are rejected
3. **No Breaking Changes**: Existing functionality is preserved unconditionally. Any removal or signature change halts the workflow
4. **Simplicity Is Strength**: Code is simplified for clarity and maintainability without sacrificing capability
5. **Production-Ready Always**: Every output is deployable — complete error handling, security, validation, and documentation
6. **Backwards Compatible**: New code integrates with existing codebases without modification to dependents

## Workflow Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   AUTOMATE-DEV WORKFLOW                      │
│                                                              │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐ │
│  │ PHASE 1  │──▸│ PHASE 2  │──▸│ PHASE 3  │──▸│ PHASE 4  │ │
│  │ ANALYSE  │   │  BUILD   │   │ REVIEW   │   │  TEST    │ │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘ │
│       │                                             │        │
│       │         ┌──────────┐   ┌──────────┐         │        │
│       │         │ PHASE 6  │◂──│ PHASE 5  │◂────────┘        │
│       │         │ SIMPLIFY │   │   FIX    │                  │
│       │         └──────────┘   └──────────┘                  │
│       │              │                                       │
│       │         ┌──────────┐                                 │
│       │         │ PHASE 7  │                                 │
│       │         │ VALIDATE │──▸ ALL PASS? ──▸ PHASE 8: SHIP │
│       │         └──────────┘        │                        │
│       │                        NO   │                        │
│       └◂────────────────────────────┘                        │
│                 (iteration loop)                             │
└─────────────────────────────────────────────────────────────┘
```

## Workflow Modes

### Mode 1: Core Loop (Default)

For bug fixes, well-defined modifications, and refactoring with clear scope.
Enters directly at Phase 1 (Analyse) and runs the full build-review-test-fix loop.

### Mode 2: Feature Development (Guided)

For new features requiring codebase exploration, architecture decisions, and
user clarification before building. Adds structured discovery phases before
the core loop:

```
FD-1: Discovery → FD-2: Codebase Exploration → FD-3: Clarifying Questions
    → FD-4: Architecture Design → FD-5: Implementation
    → Core Loop (Phase 3 onward) takes over automatically
```

Read `references/feature-development.md` when entering Feature Development mode.

### Mode Selection

| Task Type | Mode | Entry Point |
|-----------|------|-------------|
| New feature in unfamiliar area | Feature Development | FD-1: Discovery |
| Bug fix with known location | Core Loop | Phase 1: Analyse |
| Refactor with clear scope | Core Loop | Phase 1: Analyse |
| New feature, architecture known | Core Loop | Phase 1: Analyse |
| Ambiguous request needing exploration | Feature Development | FD-1: Discovery |

## Model Deployment Strategy

Optimised for **Claude Opus 4.7** (`claude-opus-4-7`) as the flagship model
for high-difficulty workflows, with Sonnet retained for exploration and
breadth-focused work.

### Difficulty-Based Routing

| Difficulty | Model | Effort | Examples |
|-----------|-------|--------|----------|
| low | sonnet | default | Simple reads, formatting |
| medium | sonnet | high | Multi-file tracing, routine refactors |
| **high** | **claude-opus-4-7** | **xhigh** | Code review, architecture, self-assessment, quality gates |
| xhigh | **claude-opus-4-7** | **xhigh** | Complex refactoring, subtle debugging |
| max | **claude-opus-4-7** | **max** | Formal verification, security audits |

### Opus 4.7 Is Required For

- **Agent output self-review** — any agent reviewing work produced by another agent
- **Code quality assessment** — simplicity, DRY, elegance judgment
- **Linting judgment** — subjective quality gates beyond rule-based scripts
- **Architectural decisions** — choosing between implementation approaches
- **Final validation (Phase 7)** — comprehensive quality gate before ship
- **Any task classified as `high` difficulty or above**

### Retained Sonnet Usage

- **code-explorer agents** — breadth-focused codebase tracing (medium difficulty)
- **Initial inventory and dependency mapping** — rule-based, high-volume work
- **Test execution orchestration** — mostly deterministic
- **Deployment readiness checks** — script-based validation

See `references/model-deployment.md` for complete strategy, migration guide,
and prompt adjustments for Opus 4.7's literal instruction following.

## Specialised Agents

Three agent types can be launched via the `delegation` skill for
judgment-intensive analysis. Use alongside automated scripts for
comprehensive coverage.

| Agent | Role | Model | Effort | Primary Phase |
|-------|------|-------|--------|--------------|
| **code-explorer** | Deep codebase tracing and pattern discovery | sonnet | high | 1 (Analyse) |
| **code-architect** | Architecture design and implementation blueprints | **claude-opus-4-7** | **xhigh** | 2 (Build) |
| **code-reviewer** | Quality review — simplicity, correctness, conventions | **claude-opus-4-7** | **xhigh** | 3 (Review), 7 (Validate) |

Read `references/agents.md` for full agent definitions, prompts, and
orchestration patterns.

### Agent + Script Combination

Agents provide **judgment**. Scripts provide **rule enforcement**. Use both:

```
Phase 3 (Review):
├── Agent: code-reviewer (simplicity)     ─┐
├── Agent: code-reviewer (correctness)     │──▸ Consolidated quality report
├── Agent: code-reviewer (conventions)    ─┘
├── Script: code_reviewer.py (band-aids, security, breaking changes)
└── Script: fix_validator.py (preservation check)
```

## Token Budgeting

Opus 4.7 uses a new tokenizer (1.0–1.35× tokens vs 4.6) and `xhigh` effort
increases reasoning depth. Cost control is enforced at three layers:

1. **Phase budgets** — default caps per workflow phase
2. **Agent budgets** — per-invocation limits (instructed in agent prompts)
3. **Task budgets** — total workflow cap (via `token_budget_monitor.py`
   and Opus 4.7's `task_budget` API feature)

### Default Budgets (medium difficulty)

| Phase | Budget | Typical Cost (Opus 4.7) |
|-------|--------|------------------------|
| 1 Analyse | 80,000 | ~$0.50 |
| 2 Build | 150,000 | ~$0.95 |
| 3 Review | 120,000 | ~$0.75 |
| 4 Test | 40,000 | ~$0.25 |
| 5 Fix | 60,000/iter | ~$0.38/iter |
| 6 Simplify | 40,000 | ~$0.25 |
| 7 Validate | 80,000 | ~$0.50 |
| 8 Ship | 20,000 | ~$0.13 |
| **Total (1 pass)** | **~590,000** | **~$3.70** |

Budgets scale by difficulty multiplier: low 0.5× / medium 1.0× / high 1.5× /
xhigh 2.0× / max 3.0×.

### Usage

```bash
# Initialise at workflow start
python scripts/token_budget_monitor.py init <project_root> --difficulty high

# Before each phase
python scripts/token_budget_monitor.py check <project_root> \
    --phase review --requested 120000

# After each phase
python scripts/token_budget_monitor.py record <project_root> \
    --phase review --tokens 115000 --model claude-opus-4-7

# Generate report at end
python scripts/token_budget_monitor.py report <project_root>
```

### Alert Thresholds

| Threshold | Action |
|-----------|--------|
| 50% | Log warning, continue |
| 75% | Log warning, flag in iteration plan |
| 90% | Halt new parallel launches, serialise work |
| 100% | Escalate to user with usage report |

See `references/token-budgeting.md` for caching strategies, cost patterns,
and detailed monitoring guidance.

## Phase Execution

### Phase 1: Analyse

Before writing any code:

1. **Inventory existing code** in target files — catalogue every function, class, export, route, model, and integration point
2. **Map dependencies** — identify what imports the target files and what they import
3. **Document current behaviour** — capture what the code does today as the preservation baseline
4. **Define acceptance criteria** — establish clear, testable conditions for "done"
5. **Create iteration plan** — write `.automate-dev/iteration_plan.md` with tasks, dependencies, and quality gates

**Agent-Enhanced Analysis** (when subagents available):
Launch 2-3 code-explorer agents in parallel for deep codebase understanding:
```javascript
await startAsyncSubagent({
    task: 'Find features similar to [feature] and trace their implementation. Return 5-10 key files.',
    relevantFiles: ['app/', 'src/']
});
await startAsyncSubagent({
    task: 'Map architecture and abstractions for [area]. Return 5-10 key files.',
    relevantFiles: ['app/', 'src/']
});
```
After agents return, read all identified files to build context.

Run: `python scripts/dev_orchestrator.py analyse <project_root> --targets <file1> <file2>`

### Phase 2: Build

Implement the feature or fix:

1. Write production-ready code following project conventions
2. Include complete error handling with specific exceptions
3. Add type hints, docstrings, and inline comments for complex logic only
4. Ensure backwards compatibility — never remove or rename public APIs
5. Use the simplest correct implementation — avoid over-engineering

**Agent-Enhanced Architecture** (when subagents available):
Before implementation, launch code-architect agents to explore trade-offs:
```javascript
await startAsyncSubagent({
    task: 'Design MINIMAL implementation for [feature] — smallest change, max reuse.',
    relevantFiles: ['app/', '.CLAUDE.md']
});
await startAsyncSubagent({
    task: 'Design CLEAN ARCHITECTURE for [feature] — maintainability, proper separation.',
    relevantFiles: ['app/', '.CLAUDE.md']
});
```
Compare approaches, form recommendation, present to user for approval.

For delegated tasks (when `subagent` / `startAsyncSubagent` is available):
- Create `.local/session_plan.md` with task breakdown
- Launch independent tasks in parallel via `startAsyncSubagent`
- Use `subagent` for sequential dependencies
- Pass skill files via `relevantFiles` when subagents need skill context

### Phase 3: Review

Automated code review against quality gates:

Run: `python scripts/code_reviewer.py <file> --project-root <root> [--original <original_file>]`

**Agent-Enhanced Review** (when subagents available):
Launch 3 code-reviewer agents in parallel with different focuses:
```javascript
await startAsyncSubagent({
    task: 'Review [files] for SIMPLICITY, DRY, ELEGANCE. Top 3-5 issues.',
    relevantFiles: [/* modified files */]
});
await startAsyncSubagent({
    task: 'Review [files] for BUGS, FUNCTIONAL CORRECTNESS. Top 3-5 issues.',
    relevantFiles: [/* modified files */]
});
await startAsyncSubagent({
    task: 'Review [files] for PROJECT CONVENTIONS, ABSTRACTIONS. Top 3-5 issues.',
    relevantFiles: [/* modified files */, '.CLAUDE.md']
});
```
Consolidate agent findings with script results into a unified quality report.

Review checks:
- **Breaking changes**: Any detected → HALT, do not proceed
- **Functionality preservation**: 100% required
- **Compatibility score**: ≥95 required
- **Code quality**: Complexity ≤10 per function, no bare excepts, no TODOs in deliverables
- **Security**: Input validation, parameterised queries, no credential exposure
- **Band-aid detection**: Pattern matching for suppressed errors, commented-out code, hardcoded workarounds

### Phase 4: Test

Execute automated testing:

1. **Unit tests** — run existing test suite, verify no regressions
2. **Integration tests** — verify new code works with existing components
3. **End-to-end tests** (when Playwright/testing subagent available) — validate user-facing flows

For Playwright-based testing, write focused test plans:
```text
1. [New Context] Create a new browser context
2. [Browser] Navigate to the target page
3. [Browser] Perform user actions
4. [Verify] Assert expected outcomes
```

Run: `python scripts/dev_orchestrator.py test <project_root> --targets <file1> <file2>`

### Phase 5: Fix

When tests or review reveal issues:

1. **Root cause analysis** — identify the actual source, not just the symptom
2. **Permanent fix** — address the root cause directly
3. **Regression check** — verify the fix doesn't break other functionality
4. **Band-aid rejection** — automatically reject fixes that:
   - Suppress or swallow exceptions
   - Add `try/except: pass` blocks
   - Comment out failing code
   - Hardcode values to bypass logic
   - Add conditional branches that skip broken paths
   - Use `# noqa`, `# type: ignore`, or similar suppressions as the fix itself

Run: `python scripts/fix_validator.py <original> <fixed> --project-root <root>`

### Phase 6: Simplify

After fixes pass validation:

1. **Reduce complexity** — flatten nested conditionals, extract helper functions
2. **Eliminate redundancy** — remove duplicate logic, consolidate related code
3. **Improve naming** — use descriptive, project-consistent names
4. **Remove dead code** — strip unreachable paths and unused imports
5. **Preserve behaviour** — simplification must not alter functionality

Run: `python scripts/code_simplifier.py <file> --project-root <root> [--original <original_file>]`

Simplification rules:
- Prefer `if/elif/else` over nested ternaries
- Prefer explicit over clever
- Prefer readability over line count
- Never combine unrelated concerns into single functions
- Maintain project naming conventions

### Phase 7: Validate

Final gate before delivery:

Run: `python scripts/dev_orchestrator.py validate <project_root> --targets <file1> <file2>`

Validation checks:
- All Phase 3 review checks pass
- All Phase 4 tests pass
- No band-aid patterns detected
- Compatibility score ≥95
- Zero breaking changes
- 100% functionality preservation
- Code simplified to project standards

**If ANY check fails**: Loop back to Phase 5 with the specific failure details. Update `.automate-dev/iteration_plan.md` with:
- Iteration number
- What failed
- Root cause identified
- Fix strategy
- Expected outcome

**Maximum iterations**: 10 (configurable). If unresolved after max iterations:
- Document all attempted fixes
- Document the blocking issue
- Present findings to user with clear options

### Phase 8: Ship

When all validation passes:

1. **Generate assessment report** with scores and verification status
2. **Confirm deployment readiness** — run `python scripts/deployment_readiness.py <project_root>`
3. **Deliver code** with assessment summary

## Reference Documentation

Load these as needed during workflow execution:

| Reference | Path | When to Read |
|-----------|------|-------------|
| Workflow Phases | `references/workflow-phases.md` | Detailed phase instructions with examples |
| Iteration Protocols | `references/iteration-protocols.md` | Loop management, max iterations, escalation |
| Quality Gates | `references/quality-gates.md` | Thresholds, scoring, pass/fail criteria |
| Code Simplification | `references/code-simplification.md` | Simplification rules and patterns |
| Agents | `references/agents.md` | Agent definitions, prompts, orchestration patterns |
| Feature Development | `references/feature-development.md` | Guided feature development workflow (FD-1 through FD-7) |
| Model Deployment | `references/model-deployment.md` | Opus 4.7 strategy, difficulty classification, routing |
| Token Budgeting | `references/token-budgeting.md` | Phase budgets, caching, monitoring, cost patterns |

## Script Reference

| Script | Purpose | Phase |
|--------|---------|-------|
| `dev_orchestrator.py` | Main workflow orchestration | All |
| `code_reviewer.py` | Automated code review with band-aid detection | 3, 7 |
| `code_simplifier.py` | Code refinement and clarity improvement | 6 |
| `fix_validator.py` | Validates fixes are permanent, not workarounds | 5 |
| `iteration_planner.py` | Creates and updates iteration plans | 1, 7 |
| `deployment_readiness.py` | Pre-deployment verification | 8 |
| `token_budget_monitor.py` | Tracks token usage, enforces budgets, cost reporting | All |

## Integration with Existing Skills

This skill orchestrates and delegates to other skills:

- **production-code-quality**: Called during Phase 3 and Phase 7 for assessment
- **delegation**: Used across all phases for parallel task execution via subagents and specialised agents (code-explorer, code-architect, code-reviewer)
- **testing**: Used in Phase 4 for end-to-end Playwright-based testing
- **code_review (architect)**: Used in Phase 3 for deep architectural analysis via the `architect()` function
- **deployment**: Used in Phase 8 for deployment configuration

### Agent Integration Summary

| Workflow Phase | Agent Type | Script Complement |
|---------------|------------|-------------------|
| Phase 1 (Analyse) | code-explorer × 2-3 | `dev_orchestrator.py analyse` |
| Phase 2 (Build) | code-architect × 2-3 | — |
| Phase 3 (Review) | code-reviewer × 3 | `code_reviewer.py`, `fix_validator.py` |
| Phase 5 (Fix) | — | `fix_validator.py` |
| Phase 6 (Simplify) | — | `code_simplifier.py` |
| Phase 7 (Validate) | code-reviewer × 3 | `dev_orchestrator.py validate` |
| Phase 8 (Ship) | — | `deployment_readiness.py` |

## Iteration Plan Format

File: `.automate-dev/iteration_plan.md`

```markdown
# Iteration Plan: [Task Description]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Iteration 1
- **Status**: PASS | FAIL | IN_PROGRESS
- **Phase reached**: 7
- **Failures**: [List of failures]
- **Root causes**: [Identified root causes]
- **Fixes applied**: [Description of fixes]
- **Result**: [Outcome]

## Current State
- **Iteration**: N
- **Blocking issues**: [None | List]
- **Quality scores**: Compatibility: XX | Preservation: XX | Quality: XX
```

## Troubleshooting

### Infinite Loop Prevention
- Hard cap at 10 iterations (configurable via `--max-iterations`)
- Each iteration must make measurable progress (at least one new fix or score improvement)
- If two consecutive iterations produce identical scores, escalate to user

### Cannot Achieve 100% Preservation
1. Document what cannot be preserved and why
2. Present alternatives
3. Request explicit approval before proceeding
4. Never silently drop functionality

### Band-Aid Fix Detected
1. Reject the fix immediately
2. Re-analyse the root cause
3. Implement a proper structural fix
4. If stuck after 3 attempts on the same issue, escalate to user with full context

## Installation

### Requirements

- **Claude Code v2.1.111 or later** — required for `claude-opus-4-7` model
  (earlier versions should run `claude update`)
- **Opus 4.7 access** — verify with `/model claude-opus-4-7` in Claude Code
- **Python 3.8+** — for scripts
- **Optional**: Prompt caching enabled for cost reduction on repeated runs

### Claude Code

Copy the package contents to your project:

```bash
# Agents — required for agent-enhanced phases
cp automate-dev/agents/*.md .claude/agents/

# Commands — optional, enables /feature-development slash command
cp automate-dev/commands/*.md .claude/commands/

# Skill — install via Claude Code skill installation
# or copy to your skills directory
```

### Configure Default Model (Optional)

To pin Opus 4.7 globally in Claude Code:

```bash
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-4-7
export ANTHROPIC_DEFAULT_EFFORT=xhigh

# Or set per-session
/model claude-opus-4-7
/effort xhigh
```

### Initialise Token Budget Monitor

At the start of each workflow run:

```bash
python scripts/token_budget_monitor.py init <project_root> --difficulty medium
```

Choose difficulty based on task complexity: `low`, `medium`, `high`, `xhigh`,
or `max` (see `references/model-deployment.md` for classification).

### Claude.ai Projects

Upload the `.skill` or `.zip` file to the project knowledge. The agents
and commands directories are not used in Claude.ai — the skill degrades
gracefully to script-only operation.

### Directory Structure

```
automate-dev/
├── SKILL.md                              Main skill definition (8-phase core loop)
├── LICENSE.txt                           Apache 2.0
├── agents/                               Agent definitions for Claude Code
│   ├── code-explorer.md                  Codebase tracing (sonnet, yellow)
│   ├── code-architect.md                 Architecture design (claude-opus-4-7 xhigh, green)
│   └── code-reviewer.md                  Deep quality review (claude-opus-4-7 xhigh, red)
├── commands/                             Slash commands for Claude Code
│   └── feature-development.md            Guided 7-phase feature development workflow
├── references/                           On-demand reference documentation
│   ├── agents.md                         Agent definitions, prompts, orchestration patterns
│   ├── feature-development.md            Feature development workflow detail (FD-1 to FD-7)
│   ├── workflow-phases.md                Detailed phase instructions with examples
│   ├── iteration-protocols.md            Loop management, stall detection, escalation
│   ├── quality-gates.md                  Thresholds, scoring, pass/fail criteria
│   ├── code-simplification.md            Simplification rules and patterns
│   ├── model-deployment.md               Opus 4.7 routing strategy, difficulty classification
│   └── token-budgeting.md                Phase budgets, prompt caching, cost patterns
└── scripts/                              Automated analysis and enforcement scripts
    ├── dev_orchestrator.py               Main workflow engine (analyse/test/validate/status)
    ├── code_reviewer.py                  Review with band-aid detection (10 patterns)
    ├── code_simplifier.py                Nesting, duplication, naming analysis
    ├── fix_validator.py                  Validates fixes are permanent, not workarounds
    ├── iteration_planner.py              Creates/updates plans, stall detection, escalation
    ├── deployment_readiness.py           Security, error handling, dependency checks
    └── token_budget_monitor.py           Token usage tracking, budget enforcement, cost reports
```


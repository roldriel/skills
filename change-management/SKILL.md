---
name: change-management
description: Define how software changes are recorded, separated, reviewed, integrated, versioned, and released. Use when deciding how work becomes Issues, branches, commits, Pull Requests, releases, or hotfixes. This skill does not define SDD, TDD, architecture, implementation strategy, coding style, testing strategy, or deployment implementation.
---

# Change Management

## Mission

Define the repository rules for representing and recording software changes.

This skill governs:

- work representation;
- branch selection and lifecycle;
- commit structure;
- Pull Request boundaries;
- integration flow;
- Semantic Versioning;
- releases;
- maintenance branches;
- hotfixes;
- rollback-oriented change design.

It does not govern software design or implementation.

## Core Flow

```text
Work
  ↓
Issue when appropriate
  ↓
Temporary branch
  ↓
Atomic incremental commits
  ↓
Pull Request
  ↓
development
  ↓
master
  ↓
vX.Y.Z
```

Maintenance:

```text
stable/X.Y.x
  ↓
hotfix/X.Y/<name>
  ↓
stable/X.Y.x
  ↓
vX.Y.Z
  ↓
functional forward-port
  ↓
development
```

## Mandatory Invariants

1. `development` is the integration branch.
2. `master` is the release-ready branch.
3. `stable/X.Y.x` exists only when independent maintenance is required.
4. Temporary branches are deleted after merge.
5. Releases use standard Semantic Versioning.
6. Commits use Conventional Commits in English.
7. Commit titles have no body.
8. A commit represents one coherent functional, technical, or documentary intention.
9. More than 5 changed files or 400 changed lines is a review warning, not an automatic failure.
10. Every commit must preserve an incremental, functional repository state.
11. Breaking changes use `!` in the Conventional Commit title.
12. Breaking-change explanation and migration guidance belong in the PR and release notes.
13. Planned work is tracked in GitHub Projects and Issues instead of `ROADMAP.md`.
14. Small direct requests do not require artificial Issues.
15. Broad work must be decomposed into independently manageable units.
16. Release tags are immutable.
17. Hotfixes must be functionally forward-ported to `development`.
18. This skill does not decide product priority, roadmap direction, or implementation methodology.

## Optional Companion Skills

Use these when available and relevant:

- `roldriel/skills:github-projects` — Projects operations.
- `roldriel/skills:github-issues` — Issue operations.
- `roldriel/skills:github-pull-requests` — Pull Request operations.
- `roldriel/skills:github-releases` — Release operations.
- `roldriel/skills:suggest-commits` — commit-history analysis.

They are optional capabilities, not dependencies.

If unavailable, continue with available capabilities. Recommend installation only when the missing skill materially improves the current task, using the compact Skill Family recommendation format.

## Workflow

1. Identify the work.
2. Find existing Issue/Project work when applicable.
3. Decompose broad work into coherent units.
4. Select branch type and base.
5. Implement using the project's implementation methodology.
6. Organize changes into atomic incremental commits.
7. Validate commit policy and functional state.
8. Open or update the PR against the correct target.
9. Integrate according to repository policy.
10. Delete the temporary branch after merge.
11. Release according to SemVer when intended.
12. For hotfixes, create the patch release and forward-port the fix to `development`.

## Issue Decision

Use an existing Issue when it already represents the request.

Use an Issue for planned features, known bugs, substantial refactors, technical tasks, multi-step work, or backlog-tracked work.

Do not create an artificial Issue for a small direct request such as:

```text
"Fix this typo."
"Correct this validation condition."
```

A broad request must be decomposed before implementation.

## Branch Policy

Long-lived:

```text
development
master
stable/X.Y.x
```

Temporary:

```text
feature/<name>
fix/<name>
hotfix/X.Y/<name>
refactor/<name>
docs/<name>
chore/<name>
```

Default bases:

```text
feature/*   → development
fix/*       → development
refactor/*  → development
docs/*      → development
chore/*     → development
hotfix/*    → stable/X.Y.x
```

If no stable branch exists, a one-off hotfix may start from the exact affected release tag.

## Commit Policy

A commit represents the smallest meaningful coherent intention.

Atomicity is not one line, one variable, or one file per commit. Multiple files are correct when they form one functional unit.

Requirements:

- Conventional Commits;
- English;
- imperative intent;
- no body.

Breaking change:

```text
feat(api)!: replace payment contract
```

Never use a commit body containing `BREAKING CHANGE:`.

Preferred size:

- 5 or fewer changed files;
- 400 or fewer changed lines.

Exceeding either is a review warning. Do not create artificial micro-commits to satisfy a number.

Every commit must leave the repository functional and internally consistent.

## Pull Request Policy

A PR is the unit of review and integration.

Ordinary work:

```text
temporary branch → development
```

Hotfix:

```text
hotfix/* → stable/X.Y.x
```

A PR should have one coherent purpose and communicate:

- what changed;
- why;
- validation performed;
- material risks;
- breaking-change impact and migration guidance when applicable.

Do not combine unrelated work.

The exact merge mechanism is governed by repository configuration; this skill must not invent one.

## Versioning

Use standard SemVer:

```text
MAJOR.MINOR.PATCH
```

- MAJOR: incompatible external/public contract change.
- MINOR: one or more backward-compatible features.
- PATCH: backward-compatible bug fixes.

A MINOR release may contain multiple features.

Examples:

```text
1.2.0 → 1.3.0   ranking + monetization
1.3.0 → 1.3.1   bug fix
1.3.1 → 1.4.0   new features
1.4.0 → 2.0.0   breaking change
```

Starting versions may be `0.1.0` or `1.0.0`; PATCH starts at zero.

## Release Policy

```text
development → master → vX.Y.Z
```

The tag identifies the exact release commit and is immutable.

Release notes communicate features, bug fixes, breaking changes, and migrations.

## Stable Branch Policy

Create `stable/X.Y.x` only when a released `X.Y` line must be maintained independently.

```text
v1.4.0
  ↓
stable/1.4.x
  ├── v1.4.1
  ├── v1.4.2
  └── v1.4.3
```

Do not create stable branches automatically for every release.

## Hotfix Policy

With a stable branch:

```text
stable/X.Y.x
      ↓
hotfix/X.Y/<name>
      ↓
stable/X.Y.x
      ↓
vX.Y.Z
      ↓
functional forward-port
      ↓
development
```

Without one, a one-off hotfix may start from the exact affected release tag.

Hotfixes normally increment PATCH. Do not force a feature or breaking change into PATCH.

Forward-port the behavior correction, not necessarily the exact historical implementation.

## Temporary Branch Lifecycle

```text
create → work → PR → merge → delete
```

Do not retain or reuse merged temporary branches.

## Rollback-Oriented Design

A commit should be reasonably reversible without removing unrelated work.

For persistent external state, use incremental compatibility-preserving transitions so code rollback does not leave the system inconsistent.

## Non-Goals

This skill does not:

- implement code;
- define architecture;
- define SDD or TDD;
- define test strategy;
- manage GitHub resources as its primary responsibility;
- decide roadmap or priority;
- require companion skills;
- install skills without explicit approval.

## References

- `references/issues.md` — Issue decisions and decomposition.
- `references/branches.md` — branch semantics and lifecycle.
- `references/commits.md` — commit policy, atomicity, and incrementality.
- `references/releases.md` — SemVer, releases, stable branches, and hotfixes.
- `references/examples.md` — explicit agent workflows and worked cases.

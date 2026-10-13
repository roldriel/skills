---
name: github-issues
description: Operate safely on GitHub Issues by discovering and identifying issues, reading issue state and metadata, and performing explicitly authorized issue mutations with post-mutation verification. Use when a consumer needs to inspect or change Issue state; do not use it to decide roadmap, priority, strategy, acceptance, or project workflow.
---

# GitHub Issues

## Purpose

Provide an independent operational capability for working with GitHub Issues.

This skill follows the GitHub Skill Family methodology:

```text
DISCOVER
  ↓
IDENTIFY
  ↓
READ
  ↓
UNDERSTAND
  ↓
PLAN
  ↓
MUTATE
  ↓
VERIFY
  ↓
REPORT
```

The skill operates on observed GitHub state. It does not determine what work should exist, whether work is strategically accepted, or how Issues should be used as a project-management system.

## Family Contract

This skill conforms to ../FAMILY.md and the repository-level FAMILY.md.

Family membership establishes shared methodology, terminology, conventions, invariants, and verification expectations. It does not create runtime or installation dependencies on other family members.

## Supported Scope

### Issue discovery and identification

- Search Issues using GitHub search qualifiers.
- Scope searches to a repository when required.
- Identify an exact Issue by repository owner/name and Issue number.
- Distinguish an Issue from a Pull Request even though GitHub exposes Pull Requests through the Issues API surface.

Issue titles are not stable identifiers. Repository + Issue number is the primary human-operational identity.

### Issue reads

Read enough state to support a requested operation, including when available:

- title;
- body;
- state;
- state reason;
- labels;
- assignees;
- milestone;
- author;
- timestamps;
- URL;
- Pull Request association when relevant;
- comments when the requested operation depends on conversation state.

Do not infer strategic meaning from Issue metadata.

### Issue mutations

Initial mutation scope:

1. create an Issue;
2. update Issue title or body;
3. open or close an Issue;
4. set a state reason when changing lifecycle state;
5. add labels;
6. add assignees;
7. set a milestone;
8. replace labels or assignees only when explicit removal/replacement is requested and the complete current set has first been observed.

Closing or reopening is a lifecycle mutation and requires explicit authorization.

## Current-State Invariant

Before mutating an existing Issue, read its relevant current state.

Never assume:

- the Issue exists;
- it is still open;
- a label is absent or present;
- an assignee is absent or present;
- the milestone is unset;
- the resource is an Issue rather than a Pull Request.

A mutation must be based on observed state, not on a stale or imagined snapshot.

## Minimum-Mutation Invariant

Prefer additive operations when they satisfy the requested outcome.

For labels and assignees:

- use additive operations when adding;
- do not use full-set replacement merely to add one value;
- when removal or replacement requires full-set replacement, read the complete current set first;
- calculate the smallest resulting set that satisfies the request;
- preserve unrelated labels and assignees.

Never overwrite metadata blindly.

## Issue vs Pull Request

GitHub can expose Pull Requests through Issue endpoints. This does not make Pull Request-specific operations part of this skill.

If an identified resource is a Pull Request:

- Issue-level metadata operations may be performed only when they are within this skill's contract;
- Pull Request review, merge, branch, reviewer, diff, and review-thread operations belong to github-pull-requests;
- do not infer authority to perform those operations from the Issue representation.

## Creation

Creating an Issue requires an explicit requested outcome and enough information to create it safely.

Supported creation inputs may include:

- repository;
- title;
- body;
- labels;
- assignees;
- milestone.

Creation must not be used to silently convert an idea into a strategic commitment.

If the consumer has not established that an Issue should exist, stop rather than inventing acceptance or priority.

## Lifecycle

For close/reopen operations:

1. identify the exact Issue;
2. read current state;
3. determine whether the requested transition is already satisfied;
4. if already satisfied, return `NO_CHANGE_REQUIRED`;
5. otherwise perform only the requested transition;
6. reread the Issue;
7. verify state and state reason when applicable.

Do not close an Issue merely because work appears complete. Do not reopen an Issue merely because new activity exists.

## Labels, Assignees, and Milestones

These are Issue metadata operations, not strategic decisions.

A label mutation must not silently redefine the repository's label taxonomy.

An assignee mutation must not infer ownership from context.

A milestone mutation must not be interpreted as roadmap acceptance or prioritization.

If the requested label, assignee, or milestone cannot be identified or validated, report the insufficiency instead of guessing.

## Error and Uncertainty Handling

Distinguish at least:

- `NOT_FOUND`: target does not exist or is inaccessible;
- `AMBIGUOUS`: target cannot be uniquely identified;
- `UNSUPPORTED_STATE`: observed resource/state is outside this skill's contract;
- `MUTATION_REJECTED`: GitHub rejected the requested mutation;
- `VERIFICATION_FAILED`: mutation response exists but resulting state cannot be verified;
- insufficient target information;
- API failure;
- permission failure.

An API error is not evidence of successful mutation.

When material ambiguity remains, stop.

## Verification Invariant

Every successful mutation must be followed by a read or equivalent returned state sufficient to verify the requested outcome.

Verification must check the affected property, not merely that the API returned without an exception.

Examples:

- Issue creation → verify repository/number and intended metadata;
- title/body update → verify exact affected fields;
- close/reopen → verify state and applicable state reason;
- add label → verify label membership;
- add assignee → verify assignee membership;
- set milestone → verify milestone identity;
- full-set replacement → verify the resulting complete set.

## Consumer Boundary

This skill does not decide:

- whether an Issue should exist strategically;
- roadmap placement;
- priority;
- acceptance;
- product scope;
- whether an Issue is the source of truth;
- project-management methodology;
- GitHub Project state;
- Pull Request review or merge strategy.

A consumer may compose this skill with other independent skills, but this skill must remain usable by itself.

## Expected Result States

Normal outcomes should use:

- `VERIFIED`
- `NO_CHANGE_REQUIRED`
- `NOT_FOUND`
- `AMBIGUOUS`
- `UNSUPPORTED_STATE`
- `MUTATION_REJECTED`
- `VERIFICATION_FAILED`

Reports should identify the repository, Issue number, requested operation, observed pre-state when material, and verified post-state.

## Non-Goals

This skill does not:

- manage Pull Request reviews or merges;
- manage GitHub Projects;
- define roadmap or priority;
- decide strategic acceptance;
- administer repository settings;
- create branches;
- silently repair unexpected metadata;
- invent missing labels, milestones, assignees, or Issues.

## Core Principle

**Operate on observed Issue state, make the smallest authorized mutation, and verify the resulting state.**

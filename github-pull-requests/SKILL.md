---
name: github-pull-requests
description: Operate safely on GitHub Pull Requests by discovering and identifying PRs, reading branch, review, merge, and lifecycle state, and performing explicitly authorized PR mutations with post-mutation verification. Use for Pull Request operations; do not use it to decide roadmap, priority, strategy, or acceptance.
---

# GitHub Pull Requests

## Purpose

Provide an independent operational capability for working with GitHub Pull Requests.

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

The skill operates on observed Pull Request state. It does not determine whether a change should be proposed, accepted, merged, or prioritized strategically.

## Family Contract

This skill conforms to ../FAMILY.md and the repository-level FAMILY.md.

Family membership establishes shared methodology, terminology, conventions, invariants, and verification expectations. It does not create runtime or installation dependencies on other family members.

## Supported Scope

### Pull Request discovery and identification

- Search Pull Requests by repository, organization, or supported GitHub qualifiers.
- Identify an exact Pull Request by repository owner/name and PR number.
- Read enough state to distinguish a Pull Request from an Issue represented through GitHub's shared issue surface.

Repository + PR number is the primary operational identity. Titles and branch names are not unique identifiers.

### Pull Request reads

Read relevant state as required, including:

- title;
- body;
- state;
- draft status;
- merged status;
- base branch;
- head branch;
- commit SHAs;
- changed-file/addition/deletion metadata when available;
- mergeability when available;
- requested reviewers;
- reviews;
- review comments/threads when required;
- timestamps;
- URL.

Do not infer approval, readiness, or strategic acceptance from one field alone.

### Pull Request mutations

Initial mutation scope:

1. create a Pull Request;
2. update title or body;
3. update the base branch;
4. open or close a Pull Request;
5. convert an open Pull Request to draft;
6. mark a draft Pull Request ready when the operation is supported;
7. request reviewers;
8. submit a review;
9. resolve or unresolve review threads;
10. enable auto-merge only when explicitly requested and the resulting repository/PR conditions are observable.

Merge itself is a consequential lifecycle mutation and is not part of the initial mutation scope unless a future revision explicitly adds it with its own verification contract.

## Current-State Invariant

Before mutating an existing Pull Request, read the relevant current state.

Never assume:

- the PR exists;
- it is open;
- it is a draft;
- the base branch is unchanged;
- reviewers are not already requested;
- a review thread is unresolved;
- auto-merge is disabled;
- the PR is mergeable.

Use observed state to determine whether a mutation is necessary and safe.

## Minimum-Mutation Invariant

Perform only the mutation required by the requested outcome.

Examples:

- adding a reviewer must not replace unrelated reviewers;
- changing the base branch must not modify title/body;
- changing title must not rewrite the body;
- converting to draft must not close the PR;
- requesting review must not imply approval.

Preserve unrelated PR state.

## Review Boundary

Reviews are operational review actions, not strategic acceptance decisions.

This skill may:

- read review state;
- submit an explicitly requested review action;
- inspect review comments;
- resolve/unresolve review threads when explicitly requested.

It must not decide that a PR should be approved, rejected, or merged merely because the observed state appears favorable.

A review action is consequential and requires explicit authorization or a higher-level consumer decision already in force.

## Draft and Ready State

Draft transitions are lifecycle mutations.

Before changing draft state:

1. identify the PR;
2. read current draft/state;
3. determine whether the requested state is already satisfied;
4. perform only the requested transition;
5. reread;
6. verify the resulting draft/state fields.

Do not infer readiness from passing checks, reviewer activity, or title conventions.

## Reviewer Requests

Before requesting reviewers:

1. read current requested reviewers;
2. determine which requested reviewers are missing;
3. add only the requested reviewers;
4. verify the resulting reviewer set.

Do not infer reviewer identity from ownership or CODEOWNERS unless the consumer explicitly supplies that as the decision basis.

## Base Branch Changes

Changing the base branch is a structural PR mutation.

Require an explicit target branch. Read the current base first and return `NO_CHANGE_REQUIRED` if it already matches.

After mutation, verify the exact resulting base branch.

Do not change branches merely to make a PR mergeable.

## Merge and Auto-Merge

Merge and auto-merge have different risk profiles.

This skill initially treats direct merge as out of scope.

Auto-merge may be enabled only when explicitly requested. Before enabling it, inspect the PR state and relevant repository conditions exposed by the available operation. Verify that auto-merge was actually enabled.

Never interpret enabling auto-merge as evidence that the PR is approved, mergeable, or strategically accepted.

## Error and Uncertainty Handling

Distinguish:

- `NOT_FOUND`;
- `AMBIGUOUS`;
- `UNSUPPORTED_STATE`;
- `MUTATION_REJECTED`;
- `VERIFICATION_FAILED`;
- insufficient target information;
- permission failure;
- API failure.

An API response without verified resulting state is not sufficient evidence of success.

Stop on material ambiguity.

## Verification Invariant

Every successful mutation must be followed by a read or returned state sufficient to verify the requested outcome.

Examples:

- create PR → verify repository, number, title, base, head, and state;
- title/body update → verify affected fields;
- base change → verify base branch;
- close/reopen → verify state;
- draft transition → verify draft state;
- reviewer request → verify requested reviewers;
- review submission → verify resulting review state when available;
- thread resolution → verify thread state;
- auto-merge → verify enabled state when exposed.

## Consumer Boundary

This skill does not decide:

- roadmap placement;
- priority;
- strategic acceptance;
- whether a PR should exist;
- whether a PR should merge;
- whether a review should be approved;
- Project state;
- Issue strategy;
- repository administration.

A consumer may compose this skill with independent Issue or Project skills without creating a dependency between those skills.

## Expected Result States

Normal outcomes should use:

- `VERIFIED`
- `NO_CHANGE_REQUIRED`
- `NOT_FOUND`
- `AMBIGUOUS`
- `UNSUPPORTED_STATE`
- `MUTATION_REJECTED`
- `VERIFICATION_FAILED`

Reports should identify the repository, PR number, requested operation, material pre-state, and verified post-state.

## Non-Goals

This skill does not:

- merge Pull Requests;
- decide approval or acceptance;
- manage GitHub Projects;
- manage repository settings;
- create branches;
- define CI policy;
- define review methodology;
- silently repair branch or review state.

## Core Principle

**Operate on observed Pull Request state, make the smallest authorized mutation, and verify the resulting state.**

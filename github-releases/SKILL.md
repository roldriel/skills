---
name: github-releases
description: Operate safely on GitHub Releases by discovering and identifying releases and tags, reading release metadata, and performing explicitly authorized release mutations with post-mutation verification. Use for release operations; do not use it to decide versioning policy, release readiness, or strategic publication.
---

# GitHub Releases

## Purpose

Provide an independent operational capability for working with GitHub Releases.

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

The skill operates on observed GitHub release state. It does not determine whether a version should be released, whether a release is ready, or what versioning policy the repository should follow.

## Family Contract

This skill conforms to ../FAMILY.md and the repository-level FAMILY.md.

Family membership establishes shared methodology, terminology, conventions, invariants, and verification expectations. It does not create runtime or installation dependencies on other family members.

## Supported Scope

### Release discovery and identification

- Identify releases by repository and stable release ID when available.
- Identify a release by tag when tag identity is sufficient and unambiguous.
- Read the repository's release collection when discovery is required.
- Distinguish a Git tag from a GitHub Release: a tag can exist without a Release.

Do not use a release title as a stable identifier.

### Release reads

Read relevant metadata as required, including:

- release ID;
- tag name;
- release name;
- body/notes;
- draft status;
- prerelease status;
- published timestamp;
- target commitish when available;
- URL;
- associated tag information when exposed.

When a release is identified by tag, verify that the intended release and tag correspond.

### Release mutations

Initial mutation scope:

1. create a Release for an explicitly identified tag;
2. update release name or notes;
3. change draft state;
4. change prerelease state;
5. publish a draft Release when explicitly requested.

Deleting Releases, deleting tags, moving tags, and rewriting published release history are out of initial scope.

## Release vs Tag

A GitHub Release is associated with a Git tag, but the two are distinct resources.

This skill must not assume:

- creating a Release creates a new tag in every circumstance;
- a tag implies a Release exists;
- deleting a Release should delete its tag;
- changing release metadata should change the tag;
- publishing a Release should alter repository history.

Tag creation or mutation is a separate operation and must not be performed implicitly.

## Current-State Invariant

Before mutating an existing Release, read its current state.

Never assume:

- the Release exists;
- it is draft;
- it is prerelease;
- the tag exists;
- the tag points to the intended commit;
- the Release has not already been published.

For publication-sensitive operations, tag identity and target state are material and must be observed when the available API exposes them.

## Minimum-Mutation Invariant

Perform only the requested release mutation.

Examples:

- changing release notes must not change prerelease state;
- changing prerelease state must not rewrite notes;
- publishing a draft must not change unrelated metadata;
- creating a Release must not silently create or modify unrelated tags.

Preserve repository history and unrelated release state.

## Publication Boundary

Publishing a Release is a consequential mutation.

Before publishing:

1. identify the exact Release;
2. read current draft/published state;
3. confirm the requested tag identity;
4. verify that the target is already a Release in the expected repository;
5. perform only the publication mutation;
6. reread;
7. verify that the Release is published.

This skill does not decide whether publication is strategically authorized. That decision belongs to the consumer or governance layer.

## Versioning Boundary

This skill does not define or infer:

- semantic versioning policy;
- next version;
- release cadence;
- changelog policy;
- whether a release is ready;
- whether a tag should be created;
- whether a version is compatible with a roadmap.

If the consumer has not supplied the intended version/tag, stop rather than inventing one.

## Error and Uncertainty Handling

Distinguish:

- `NOT_FOUND`;
- `AMBIGUOUS`;
- `UNSUPPORTED_STATE`;
- `MUTATION_REJECTED`;
- `VERIFICATION_FAILED`;
- tag/release mismatch;
- insufficient target information;
- permission failure;
- API failure.

An API error is not evidence that a Release was created or published.

When a tag/release relationship cannot be verified for a publication-sensitive operation, stop.

## Verification Invariant

Every successful mutation must be followed by a read or returned state sufficient to verify the requested outcome.

Examples:

- create Release → verify repository, release identity, tag, and intended metadata;
- update notes/name → verify affected fields;
- draft/prerelease transition → verify resulting flags;
- publish → verify published state and publication timestamp when exposed.

## Consumer Boundary

This skill does not decide:

- whether a release should exist;
- next version;
- release readiness;
- versioning policy;
- roadmap placement;
- strategic publication;
- tag creation/deletion policy;
- repository administration.

A consumer may compose this skill with Issues, Pull Requests, or Projects without creating dependencies between those skills.

## Expected Result States

Normal outcomes should use:

- `VERIFIED`
- `NO_CHANGE_REQUIRED`
- `NOT_FOUND`
- `AMBIGUOUS`
- `UNSUPPORTED_STATE`
- `MUTATION_REJECTED`
- `VERIFICATION_FAILED`

Reports should identify the repository, Release/tag identity, requested operation, material pre-state, and verified post-state.

## Non-Goals

This skill does not:

- delete releases;
- delete or move tags;
- rewrite repository history;
- decide version numbers;
- define release methodology;
- decide release readiness;
- manage Projects, Issues, or Pull Request review;
- silently repair tag/release inconsistencies.

## Core Principle

**Operate on observed Release state, make the smallest authorized mutation, and verify the resulting state.**

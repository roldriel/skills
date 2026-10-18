# suggest-commits Conformance Cases

These cases define expected agent behavior for the `suggest-commits` skill.
They are evaluation fixtures, not claims that Git mutations were executed.

Each case specifies:

- observed repository state;
- expected commit boundaries;
- expected classification;
- expected warnings or confidence;
- forbidden behavior.

## Case 01 — No Changes

### Input
`git status` shows a clean working tree and no staged changes.

### Expected
Report that there are no repository changes to organize.
Do not invent commits.

### Forbidden
- proposing empty commits;
- inferring work from file names or previous context only.

## Case 02 — Small Bug Fix

### Input
`src/balance.py` and `tests/test_balance.py` contain only the correction for duplicate transactions.

### Expected
One commit:

```text
fix(balance): prevent duplicate transactions
```

Confidence may be High when the intent is unambiguous.

## Case 03 — One Feature Across Multiple Files

### Input
Changes to model, service, API route, and feature tests all implement player ranking.

### Expected
Prefer one coherent feature commit or a small sequence of feature commits only when the changes have meaningful incremental boundaries.

Valid example:

```text
feat(ranking): add ranking model
feat(ranking): calculate player scores
test(ranking): cover ranking calculation
```

Do not create one commit per file.

## Case 04 — Multiple Intentions in One File

### Input
`src/auth/service.py` contains both a refresh-token feature and an unrelated validation refactor.

### Expected
Propose separate commits and recommend partial staging when safe.

### Forbidden
```text
feat(auth): add refresh tokens and refactor validation
```

## Case 05 — Feature Plus CI

### Input
Application changes implement a new feature while `.github/workflows/test.yml` changes CI behavior for an unrelated reason.

### Expected
Separate the feature and CI intentions.

Example:

```text
feat(api): add audit endpoint
ci: update test workflow
```

## Case 06 — Large but Cohesive Change

### Input
A single authentication flow changes 12 files and 700 lines. All changes are necessary for the same functional unit.

### Expected
Flag the size warning.
Do not split merely to satisfy the thresholds.
The commit can remain atomic if the intention is cohesive.

## Case 07 — Size Threshold Exceeded with Real Boundaries

### Input
A working tree contains a feature affecting 4 files and 220 lines and an unrelated refactor affecting 3 files and 210 lines.

### Expected
Split into two commits.
The warning is not about total working-tree size; it is about each candidate commit.

## Case 08 — Breaking Change

### Input
Public API contract changes incompatibly.

### Expected
Use the `!` marker:

```text
feat(api)!: replace payment contract
```

Explain impact and migration in the Pull Request or release communication.

### Forbidden
Generating a commit body containing `BREAKING CHANGE:`.

## Case 09 — Non-Breaking Internal Refactor

### Input
Private implementation is reorganized without changing an external contract.

### Expected
```text
refactor(auth): extract token validator
```

Do not mark the commit as breaking.

## Case 10 — Incremental State Violation

### Input
A proposed sequence requires the first commit to break the application and a later commit to restore functionality.

### Expected
Reject or qualify the sequence.
Do not present the sequence as incrementally valid.
Prefer a sequence where every commit leaves a functional, internally consistent state.

## Case 11 — Incrementality Cannot Be Established

### Input
A diff contains a migration and application changes, but available evidence is insufficient to establish whether the intermediate states are compatible.

### Expected
Do not claim verified incrementality.
Lower confidence and state the limitation.
Recommend compatibility-preserving sequencing when appropriate.

## Case 12 — Merge Conflict

### Input
`git status` reports unresolved conflict state for one or more files.

### Expected
Report the conflicts.
Stop normal proposal for conflicted paths.

### Forbidden
Designing a normal commit history that includes unresolved conflict state.

## Case 13 — Ambiguous Classification

### Input
A change could reasonably be interpreted as either a bug fix or an internal refactor.

### Expected
Use the evidence to select the most accurate type.
If ambiguity remains, lower confidence and explain why.
Do not invent a definitive classification without evidence.

## Case 14 — Partial Staging

### Input
One file contains two independently reviewable intentions.

### Expected
Recommend:

```bash
git add -p path/to/file
```

Explain which hunks belong to each proposed commit.

### Forbidden
Assuming the staging command has already been executed.

## Case 15 — Optional Change-Management Companion Available

### Input
`roldriel/skills:change-management` is available while commit analysis is requested.

### Expected
Use it as an optional repository policy reference when relevant.
The current skill remains responsible for commit analysis.

### Forbidden
Treating the companion as a hard dependency.

## Case 16 — Optional Companion Unavailable

### Input
`roldriel/skills:change-management` is unavailable. The current task is still analyzable from Git evidence.

### Expected
Continue using the built-in fallback rules.
If the missing companion would materially improve the current task, emit only the compact recommendation:

```text
> Optional skill: `roldriel/skills:change-management` can improve this task by providing repository change-policy interpretation. It is not required. Install it?
```

Do not fail solely because the companion is unavailable.

## Case 17 — Optional Skill Source Must Be Explicit

### Input
A recommendation is needed for GitHub Pull Request operations.

### Expected
Name the distributor and repository:

```text
roldriel/skills:github-pull-requests
```

### Forbidden
```text
github-pull-requests
```
when another provider could expose the same skill name.

## Case 18 — Commit Body Must Never Be Proposed

### Input
The agent is preparing a Conventional Commit for a normal feature.

### Expected
```text
feat(ranking): add player ranking
```

### Forbidden
Any proposal containing a commit body.

## Case 19 — Commit Size Warning

### Input
A candidate commit changes 6 files and 350 lines, all for one cohesive feature.

### Expected
Keep the candidate potentially atomic.
Flag the file-count threshold warning.
Do not automatically split it.

## Case 20 — Commit Size Warning by Lines

### Input
A candidate commit changes 4 files and 500 lines, all for one cohesive feature.

### Expected
Keep the candidate potentially atomic.
Flag the line-count threshold warning.
Do not automatically split it.

## Case 21 — Commit Order Dependency

### Input
An internal refactor creates an interface required by a later feature implementation.

### Expected
Recommend the prerequisite refactor before the feature commit when both remain independently meaningful.
Do not apply a fixed global type ordering when repository evidence shows a dependency.

## Case 22 — Tests Coupled to a Feature

### Input
Production changes and tests exist solely to validate the same new feature.

### Expected
Keep them in the same atomic change when that produces a clearer history.
Do not create a meaningless test-only commit solely because tests are in a separate directory.

## Case 23 — Independent Test Coverage

### Input
No production behavior changes. New tests increase coverage for an existing stable component.

### Expected
Use a tests-only commit:

```text
test(auth): cover token edge cases
```

## Case 24 — Standalone Documentation

### Input
README restructuring is unrelated to the current code change.

### Expected
Separate documentation from the functional change:

```text
docs(readme): reorganize installation guide
```

## Global Conformance Rule

A proposal is conforming only when it satisfies all applicable rules:

1. evidence-based;
2. one coherent intention per commit;
3. no artificial micro-commits;
4. preferred size thresholds evaluated;
5. incremental state evaluated;
6. Conventional Commit title in English;
7. no commit body;
8. `!` for breaking changes;
9. no unverified claims;
10. optional skills identified by distributor and repository;
11. missing optional skills do not block the task;
12. compact installation recommendation only when materially useful.
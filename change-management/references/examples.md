# Worked Examples

## Feature

Request:

```text
Implement player ranking.
```

Issue:

```text
Add player ranking
```

Branch:

```text
feature/player-ranking
```

Commits:

```text
feat(ranking): add ranking model
feat(ranking): calculate player scores
test(ranking): cover ranking calculation
```

PR:

```text
feature/player-ranking → development
```

## Small Bug

Request:

```text
Fix duplicated balance transactions.
```

No existing Issue and the request is narrow.

Branch:

```text
fix/duplicate-balance-transaction
```

Commit:

```text
fix(balance): prevent duplicate transactions
```

No artificial Issue is required.

## Mixed Changes

One file contains:

```text
payment bug fix
unrelated authentication refactor
```

Do not produce:

```text
fix: update payment and authentication
```

Use partial staging and separate commits when safe.

## Large Cohesive Change

A single authentication flow changes 12 files and 700 lines.

The thresholds are exceeded, but the change may still be cohesive.

Do not split artificially. Flag the size for review in the PR.

## Breaking Change

Commit:

```text
feat(api)!: replace payment contract
```

PR explains impact and migration.

Release:

```text
1.8.4 → 2.0.0
```

No commit body is used.

## Hotfix

Current release:

```text
v1.4.2
```

Stable branch exists:

```text
stable/1.4.x
```

Flow:

```text
hotfix/1.4/duplicate-payment
        ↓
stable/1.4.x
        ↓
v1.4.3
        ↓
development
```

## Optional Skill

If GitHub Project operations are required and the companion is unavailable:

```text
> Optional skill: `roldriel/skills:github-projects` can improve this task
> by providing direct GitHub Projects operations and verification.
> It is not required. Install it?
```

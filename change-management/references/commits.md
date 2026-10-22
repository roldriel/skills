# Commits

All commits use Conventional Commits in English and have no body.

Examples:

```text
feat(ranking): add player ranking
fix(balance): prevent duplicate transactions
refactor(auth): extract token validation
docs(api): document pagination
chore: remove obsolete script
```

Breaking change:

```text
feat(api)!: replace payment contract
```

Do not put `BREAKING CHANGE:` in a commit body. Explain impact and migration in the PR and release notes.

## Atomicity

A commit represents one coherent intention.

Do not confuse atomicity with one line, variable, or file per commit.

Multiple files are valid when they form one functional unit.

Use partial staging when one file contains independent intentions and the split is safe.

## Size

Preferred thresholds:

- <= 5 changed files;
- <= 400 changed lines.

Crossing either is a review warning, not an automatic failure.

Do not create meaningless micro-commits to satisfy a number.

## Incrementality

Each commit must leave the repository functional and internally consistent.

Avoid intentionally committing broken intermediate states.

For persistent external state, use incremental compatibility-preserving transitions.

## Revertability

A commit should be reasonably reversible without removing unrelated work.

Tests and documentation tightly coupled to a feature or fix normally belong to the same atomic change.

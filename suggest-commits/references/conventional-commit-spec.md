# Conventional Commit Specification

This document defines commit classification rules.

It does not define workflow.

It does not define commit boundaries.

It only defines how a commit should be classified once its intention is known.

---

# Commit Types

Choose the narrowest accurate type.

## feat

Use for new functionality.

Examples:

* new API endpoint
* new user capability
* new service
* new command
* new feature flag

Examples:

```text
feat(auth): add refresh token support
feat(api): expose user search endpoint
```

---

## fix

Use for bug fixes.

Examples:

* defect correction
* incorrect behavior
* edge case handling
* regression fixes

Examples:

```text
fix(auth): prevent expired token reuse
fix(users): handle empty email addresses
```

---

## refactor

Use for structural improvements without behavior changes.

Examples:

* extract services
* split modules
* improve architecture
* simplify implementation

Do not use when observable behavior changes.

Examples:

```text
refactor(auth): extract token validator
refactor(api): isolate request parsing
```

---

## perf

Use only when the primary intention is performance improvement.

Examples:

* reduce allocations
* optimize queries
* cache expensive operations

Examples:

```text
perf(users): reduce database round trips
perf(cache): avoid redundant serialization
```

---

## test

Use when changes affect tests only.

Examples:

* new tests
* test refactors
* fixture updates
* helper updates

Examples:

```text
test(auth): cover refresh token flow
test(api): add validation edge cases
```

---

## docs

Use when changes affect documentation only.

Examples:

* README updates
* API documentation
* architecture documentation
* comments intended as documentation

Examples:

```text
docs(readme): document authentication flow
docs(api): describe pagination behavior
```

---

## style

Use for formatting-only changes.

Examples:

* whitespace
* formatting
* lint fixes without behavioral impact

Examples:

```text
style(api): format request handlers
```

---

## build

Use for build system changes.

Examples:

* package manager configuration
* build tooling
* compilation pipeline
* bundling configuration

Examples:

```text
build(web): update vite configuration
build(api): migrate packaging workflow
```

---

## ci

Use for CI/CD changes.

Examples:

* GitHub Actions
* GitLab CI
* Jenkins
* deployment pipelines

Examples:

```text
ci: add test workflow
ci: enable release automation
```

---

## chore

Use for maintenance work that does not fit another type.

Examples:

* housekeeping
* repository cleanup
* maintenance tasks
* non-functional administrative work

Do not use chore when a more specific type exists.

Examples:

```text
chore: remove obsolete scripts
chore: reorganize repository metadata
```

---

# Scope Rules

Scopes should describe real business or technical domains.

Prefer:

* service names
* package names
* application names
* domain concepts
* bounded contexts

Good examples:

```text
auth
payments
users
billing
api
sdk
mobile
web
notifications
```

Examples:

```text
feat(auth): add refresh token support
fix(payments): prevent duplicate charges
```

---

Avoid generic scopes.

Avoid:

```text
core
common
shared
helpers
utils
base
misc
general
```

Use them only when they genuinely represent a project domain.

Prefer no scope over a misleading scope.

Good:

```text
fix: prevent duplicate user creation
```

Better than:

```text
fix(utils): prevent duplicate user creation
```

when "utils" is not a meaningful domain.

---

# Monorepo Rules

For monorepositories, prefer package or application ownership.

Examples:

```text
packages/api
packages/sdk
packages/web

apps/mobile
apps/admin
```

Recommended scopes:

```text
api
sdk
web
mobile
admin
```

Examples:

```text
feat(api): add audit endpoint
fix(web): handle session expiration
refactor(sdk): simplify client initialization
```

---

# Breaking Changes

A breaking change exists only when an external contract becomes incompatible.

Breaking changes affect consumers.

Internal implementation details do not qualify.

---

## Typical Breaking Changes

Examples:

* public API changes
* public function signature changes
* CLI argument changes
* event payload changes
* schema changes requiring migration
* removal of supported configuration keys
* public SDK changes

Examples:

```text
feat(auth)!: replace legacy token format
```

---

## Non-Breaking Changes

Do not mark as breaking:

* internal refactors
* private function changes
* file moves
* code organization
* test updates
* documentation updates

Examples:

```text
refactor(auth): extract token validation
```

This is not breaking.

---

## Breaking Change Format

Use the `!` marker in the commit title:

```text
feat(auth)!: replace legacy token format
```

Commit bodies are prohibited by the repository change policy.

Do not generate:

```text
BREAKING CHANGE: Legacy JWT payloads are no longer accepted.
```

inside a commit body.

Breaking-change impact and migration guidance belong in the Pull Request and release communication.

---

# Commit Title Rules

All titles must:

* be written in English
* use imperative mood
* describe intent
* stay under 72 characters

---

Good:

```text
feat(auth): add refresh token support
fix(api): prevent duplicate user creation
refactor(users): extract validation service
```

---

Bad:

```text
feat(auth): modified auth files
fix(users): update code
refactor(core): cleanup
```

These describe implementation details rather than intent.

---

# Title Principles

Prefer:

```text
add
remove
prevent
support
extract
introduce
simplify
improve
optimize
document
```

Avoid vague verbs:

```text
update
change
modify
adjust
fix stuff
cleanup
misc
```

unless they accurately describe the intent.

---

# Classification Principles

Choose the most specific valid type.

Prefer:

```text
fix
```

over:

```text
chore
```

when fixing a bug.

Prefer:

```text
docs
```

over:

```text
chore
```

for documentation work.

Prefer:

```text
refactor
```

over:

```text
chore
```

for structural improvements.

`chore` is the fallback classification when no specific category applies.

# Commit Boundary Rules

This document defines commit boundary concepts.

It does not define workflow.

It does not define output formatting.

It only defines how repository changes should be grouped into logical commits.

---

# Core Principle

A commit represents a single intention.

A commit does not represent:

* a file
* a directory
* a package
* a pull request
* a work session

Files are implementation details.

Intentions define commit boundaries.

---

# Primary Grouping Rule

Always group changes by intention first.

Only use repository structure as a supporting signal.

Never use repository structure as the primary grouping mechanism.

---

# Valid Commit

A valid commit answers a single question:

> Why was this change made?

The answer should be short and unambiguous.

Examples:

```text
Add refresh token support

Prevent duplicate user creation

Extract validation service

Document authentication flow
```

Each answer represents a single intention.

---

# Invalid Commit

An invalid commit contains multiple unrelated answers.

Examples:

```text
Add refresh token support
+
Update CI pipeline
```

```text
Fix payment bug
+
Update README
```

```text
Refactor API
+
Upgrade dependencies
```

These should normally be separated.

---

# Intentions

Typical intentions include:

* feature implementation
* bug fix
* refactor
* performance optimization
* test coverage
* documentation
* dependency update
* build change
* CI/CD change
* migration
* cleanup

Intentions are conceptual.

They are not tied to file types.

---

# Files Do Not Define Commits

Do not assume:

```text
one file = one commit
```

Do not assume:

```text
one directory = one commit
```

Do not assume:

```text
one package = one commit
```

These may be true.

They are not automatically true.

---

# Single Intention Across Multiple Files

A single intention may span many files.

Example:

```text
src/auth/service.py
src/auth/models.py
src/auth/routes.py
tests/test_auth.py
```

If all changes contribute to refresh token support:

```text
One commit
```

is appropriate.

---

# Multiple Intentions Inside One File

A single file may contain multiple intentions.

Example:

```text
src/auth/service.py
```

contains:

```text
refresh token feature
```

and

```text
validation refactor
```

These should not automatically share a commit.

Partial staging may be appropriate.

---

# Mixed Commits

A mixed commit contains unrelated intentions.

Mixed commits reduce:

* review quality
* blame quality
* history clarity
* revert safety

Prefer separating mixed commits.

---

# Common Mixed Commit Patterns

## Feature + Documentation

Example:

```text
New API endpoint
+
README update
```

Usually separate.

Documentation may follow the feature.

---

## Feature + Refactor

Example:

```text
Add refresh token support
+
Extract validation layer
```

If the refactor is not required for the feature:

Separate.

---

## Fix + Dependency Update

Example:

```text
Prevent race condition
+
Upgrade framework version
```

Usually separate.

---

## Application Code + CI

Example:

```text
Feature implementation
+
GitHub Actions update
```

Usually separate.

---

## Application Code + Build System

Example:

```text
Business logic change
+
Bundler configuration update
```

Usually separate.

---

# Refactor Dependencies

Sometimes a refactor exists only to enable another change.

Example:

```text
Extract token validator
↓
Required for refresh token support
```

Possible outcomes:

```text
One commit
```

or

```text
Refactor commit
↓
Feature commit
```

Choose the option that produces the clearest history.

---

# Tests

Tests require special handling.

Tests that validate a feature are usually part of the feature.

Example:

```text
Implementation
+
Feature tests
```

Usually:

```text
One commit
```

is appropriate.

---

Tests that introduce independent coverage may deserve separation.

Example:

```text
No production code changes
+
Additional coverage
```

Usually:

```text
Separate test commit
```

is appropriate.

---

# Documentation

Documentation requires special handling.

Documentation tightly coupled to a change may remain with the change.

Example:

```text
New endpoint
+
OpenAPI documentation
```

may belong together.

---

Standalone documentation improvements should be separated.

Example:

```text
README restructuring
Architecture documentation
Tutorial updates
```

Usually separate.

---

# Dependency Updates

Dependency updates should be treated as independent intentions unless they are required for another change.

Example:

```text
Upgrade Flask
```

is a separate intention.

Example:

```text
Upgrade Flask because new feature requires it
```

may be grouped.

Use judgment.

Prefer separation when uncertain.

---

# Migrations

Schema migrations require careful treatment.

Example:

```text
Database schema
+
Application code
+
Migration scripts
```

may belong to a single intention.

Do not separate artificially when all changes represent one logical evolution.

---

# Cleanup

Cleanup is often overused.

Do not classify work as cleanup simply because it is small.

Examples of legitimate cleanup:

```text
Remove dead code
Delete unused assets
Remove obsolete scripts
```

Cleanup should remain isolated from unrelated work.

---

# Partial Staging

Partial staging is appropriate when:

* one file contains multiple intentions
* changes can be separated safely
* separation improves history clarity

Partial staging is not required when:

* all changes support the same intention

---

# Splitting Principle

When uncertain:

Prefer splitting.

A slightly verbose history is acceptable.

A misleading history is not.

---

# Cohesion Principle

Every proposed commit should have strong internal cohesion.

All changes inside a commit should contribute to the same goal.

A reviewer should be able to understand:

```text
What changed?
Why did it change?
```

without needing unrelated context.

---

# Reviewability Principle

A reviewer should be able to review each proposed commit independently.

If a commit requires understanding multiple unrelated concerns:

it is probably too broad.

---

# Revertability Principle

A commit should ideally be reversible without affecting unrelated work.

If reverting a commit would unexpectedly remove multiple unrelated intentions:

the commit boundary is likely incorrect.

---

# Final Boundary Rule

The best commit history is not the shortest history.

The best commit history is the history that most accurately represents the evolution of the codebase.

Intentions define commits.

Files do not.


---

# Commit Size

Preferred thresholds:

- 5 or fewer changed files;
- 400 or fewer changed lines.

These thresholds measure reviewability, not atomicity.

A large commit can be atomic when all changes serve one cohesive intention.

A small commit can still be non-atomic when it mixes unrelated intentions.

Exceeding a threshold should trigger a split analysis, not automatic rejection.

---

# Incremental State

A proposed sequence should advance through functional and internally consistent repository states.

Do not intentionally create:

```text
commit A → broken
commit B → broken
commit C → functional
```

when the history can be designed incrementally.

If functionality cannot be established from available evidence, report the uncertainty rather than presenting the sequence as verified.

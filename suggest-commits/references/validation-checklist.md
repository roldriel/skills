# Validation Checklist

This document defines validation questions.

It does not define workflow.

It does not define commit classification.

It does not define output formatting.

Its purpose is to challenge commit proposals before they are presented.

The goal is not to defend a proposal.

The goal is to find reasons why a proposal may be incorrect.

---

# Validation Principle

Never assume the first grouping is correct.

Every proposed commit should be treated as a hypothesis.

Validation attempts to falsify that hypothesis.

Only proposals that survive validation should be presented.

---

# Commit Boundary Validation

For every proposed commit ask:

## Single Intention

Does this commit represent exactly one intention?

Questions:

* Can the commit be summarized with a single reason?
* Does every change contribute to that reason?
* Would a reviewer describe the commit with one sentence?

If not:

consider splitting.

---

## Mixed Concerns

Does the commit contain unrelated concerns?

Examples:

```text
feature
+
documentation
```

```text
feature
+
dependency update
```

```text
fix
+
CI change
```

```text
refactor
+
build tooling
```

If unrelated concerns exist:

consider splitting.

---

## Hidden Intentions

Could a second intention be hidden inside the same changes?

Common indicators:

* unrelated code paths
* unrelated modules
* unrelated business concepts
* unrelated motivations

If yes:

consider splitting.

---

# Partial Staging Validation

When a file participates in multiple candidate commits ask:

* Are the intentions separable?
* Would git add -p improve history quality?
* Can the changes be reviewed independently?

If yes:

recommend partial staging.

---

# Scope Validation

For every scope ask:

* Is this a real project domain?
* Would another developer recognize this boundary?
* Does the scope help understanding?

Reject weak scopes.

Examples of suspicious scopes:

```text
core
common
shared
base
helpers
utils
misc
```

Prefer no scope over a misleading scope.

---

# Type Validation

For every type ask:

* Is this the most specific valid type?
* Is a more precise type available?

Examples:

Reject:

```text
chore
```

when:

```text
fix
```

is more accurate.

Reject:

```text
chore
```

when:

```text
docs
```

is more accurate.

Use the narrowest accurate classification.

---

# Breaking Change Validation

For every breaking change ask:

* Does this affect consumers?
* Does this affect public contracts?
* Does this require migration?
* Would existing integrations fail?

If all answers are no:

it is not a breaking change.

---

Reject breaking classification for:

* internal refactors
* private methods
* implementation details
* file moves
* test updates
* documentation updates

---

# Dependency Validation

For dependency updates ask:

* Is the update a separate intention?
* Is the update required for another change?
* Can it be reviewed independently?

If yes:

consider separate commits.

---

# Test Validation

For test changes ask:

* Do tests exist only to support the feature?
* Do tests introduce independent coverage?

Feature-supporting tests often belong with the feature.

Independent coverage often deserves separation.

---

# Documentation Validation

For documentation ask:

* Does it exist solely to explain the change?
* Is it independently valuable?

If independently valuable:

consider separation.

---

# Refactor Validation

For refactors ask:

* Does the refactor change behavior?
* Is the refactor required for another intention?
* Can it be reviewed independently?

Independent refactors often deserve separation.

---

# Commit Size Validation

Large commits require extra scrutiny.

Ask:

* Can the commit be divided into smaller logical units?
* Would the resulting history become clearer?
* Would review become easier?

If yes:

consider splitting.

---

# Over-Splitting Validation

Do not split mechanically.

Ask:

* Are the resulting commits meaningful?
* Does each commit still represent a coherent intention?
* Does the split improve history quality?

Avoid:

```text
one commit per file
```

Avoid:

```text
one commit per tiny edit
```

Splitting must improve understanding.

---

# Reviewability Validation

For every proposed commit ask:

Can a reviewer understand:

```text
What changed?
Why did it change?
```

without reading unrelated commits?

If not:

the boundary may be incorrect.

---

# Revertability Validation

Ask:

Would reverting this commit remove unrelated work?

If yes:

the boundary may be incorrect.

Well-formed commits should be reasonably reversible.

---

# Ordering Validation

When multiple commits are proposed ask:

* Is the proposed order logical?
* Do later commits depend on earlier commits?
* Would cherry-picking remain reasonable?

Adjust ordering when dependencies exist.

---

# Confidence Validation

Confidence must reflect uncertainty.

Never use confidence to reward effort.

Never use confidence to reward code quality.

Never use confidence to reward commit size.

Confidence only measures confidence in:

* intention detection
* boundary correctness
* classification correctness

---

# Confidence Reduction Signals

Reduce confidence when:

* multiple interpretations are possible
* one file contains several intentions
* partial staging is required
* commit boundaries are ambiguous
* scope selection is uncertain
* classification is uncertain
* missing context affects analysis

---

# Confidence Inflation Rule

Never increase confidence merely because:

* many files support the proposal
* naming appears obvious
* directory structure appears obvious

Confidence must be earned through clarity.

---

# Final Validation Question

Before presenting the result ask:

> If another experienced developer reviewed these changes, would they likely produce substantially the same commit structure?

If the answer is uncertain:

reduce confidence.

If the answer is likely yes:

confidence may remain high.


---

# Incremental State Validation

For every proposed sequence ask:

- Does each commit move the repository to a coherent state?
- Does a later commit merely repair a known-broken earlier commit?
- Can the sequence be structured so each commit remains functional?
- Is the available evidence sufficient to assess this?

If incremental validity cannot be established, lower confidence and state the limitation.

Do not claim verified incrementality solely because the final result works.

---

# Commit Size Validation

Use these reviewability thresholds:

- 5 or fewer changed files;
- 400 or fewer changed lines.

If exceeded:

- inspect for multiple intentions;
- consider a meaningful split;
- keep cohesive changes together when splitting would be artificial;
- report the warning when the large cohesive commit remains.

---

# Commit Message Validation

Every proposed commit title must:

- use Conventional Commits;
- be in English;
- have no body;
- use `!` for breaking changes.

Do not produce `BREAKING CHANGE:` commit-body text.

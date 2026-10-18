# Confidence Model

This document defines confidence assignment rules.

It does not define workflow.

It does not define commit boundaries.

It does not define commit classification.

Its purpose is to communicate how certain the proposed commit structure is.

---

# Confidence Purpose

Confidence measures confidence in analysis.

Confidence does not measure:

* code quality
* implementation quality
* architectural quality
* test quality
* developer skill

Confidence only measures confidence in:

* intention detection
* commit boundaries
* commit classification

---

# Available Levels

Use exactly one value:

```text
High
Medium
Low
```

Do not invent additional levels.

Do not use percentages.

Do not use numeric scores.

Do not use ranges.

---

# High Confidence

Use High when the proposed commit structure is clear and unambiguous.

Characteristics:

* intentions are obvious
* boundaries are obvious
* classification is obvious
* no competing interpretations exist
* no partial staging is required
* scope is clear
* breaking change status is clear

Examples:

```text
New authentication endpoint
+
Associated tests
+
Associated documentation
```

All changes support the same intention.

Confidence:

```text
High
```

---

Example:

```text
Single bug fix
Clearly isolated files
No unrelated changes
```

Confidence:

```text
High
```

---

# Medium Confidence

Use Medium when the proposal is reasonable but uncertainty exists.

Characteristics:

* multiple interpretations are possible
* boundaries require judgment
* partial staging may be needed
* scope selection is uncertain
* classification is plausible but not obvious

Examples:

```text
Feature implementation
+
Refactor in the same module
```

The relationship is unclear.

Confidence:

```text
Medium
```

---

Example:

```text
One file contains several conceptual changes
```

Possible separation exists.

Confidence:

```text
Medium
```

---

Example:

```text
Potential feature
Potential fix
```

Classification uncertainty exists.

Confidence:

```text
Medium
```

---

# Low Confidence

Use Low when major ambiguity exists.

Characteristics:

* intentions cannot be determined reliably
* boundaries are highly uncertain
* repository state is incomplete
* large mixed changes exist
* staging state obscures intent
* missing context prevents reliable analysis

Examples:

```text
Massive mixed commit
Many unrelated modules
No clear intention boundaries
```

Confidence:

```text
Low
```

---

Example:

```text
Generated code
Large formatting changes
Business logic changes
Refactors
Documentation
```

all mixed together.

Confidence:

```text
Low
```

---

Example:

```text
Repository state appears partially staged
Intentions cannot be reconstructed safely
```

Confidence:

```text
Low
```

---

# Confidence Reduction Rules

Reduce confidence when any of the following are true.

---

## Multiple Plausible Interpretations

Example:

```text
Could be one feature
Could be one refactor
Could be two commits
```

Reduce confidence.

---

## Partial Staging Required

Example:

```text
One file contains multiple intentions
```

Reduce confidence.

---

## Ambiguous Classification

Example:

```text
fix
or
refactor
```

Reduce confidence.

---

## Ambiguous Scope

Example:

```text
auth
or
api
```

Reduce confidence.

---

## Ambiguous Boundaries

Example:

```text
One commit
or
Two commits
```

Both appear reasonable.

Reduce confidence.

---

## Incomplete Evidence

Example:

```text
Diff does not provide enough context
```

Reduce confidence.

---

# Confidence Preservation Rules

Do not reduce confidence merely because:

* many files changed
* many lines changed
* many commits are proposed

Large changes can still have clear intentions.

Confidence depends on clarity.

Not size.

---

# Confidence Inflation Prohibition

Never increase confidence because:

* naming appears good
* directory structure appears clean
* commit messages look professional
* code quality appears high

Confidence must be based on evidence.

Not impressions.

---

# Reason Requirement

When confidence is:

```text
Medium
```

or

```text
Low
```

provide a reason.

Examples:

```text
Confidence: Medium

Reason:
Multiple intentions detected inside src/auth/service.py.
```

---

```text
Confidence: Low

Reason:
Repository contains heavily mixed changes with unclear boundaries.
```

---

# Consistency Rule

Two developers may disagree on the ideal commit structure.

That alone does not require lower confidence.

Lower confidence only when the available evidence genuinely supports multiple plausible interpretations.

---

# Final Confidence Test

Before assigning confidence ask:

> Would another experienced developer likely propose a substantially similar commit structure using the same diff?

If:

```text
Likely yes
```

Confidence may be:

```text
High
```

If:

```text
Possibly
```

Confidence should be:

```text
Medium
```

If:

```text
Unclear
```

Confidence should be:

```text
Low
```


---

# Incrementality

Incremental-state assessment is part of confidence.

Reduce confidence when:

- the sequence may require known-broken intermediate states;
- functionality cannot be established from available evidence;
- persistent external-state transitions are involved and compatibility is unclear.

Do not claim verified incrementality when the analysis cannot establish it.

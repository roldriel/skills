---
name: github-projects
description: Operate safely on GitHub Projects v2 by discovering and identifying Projects, reading items, fields, and views, and performing explicitly authorized item and field mutations with post-mutation verification. Use when a consumer needs to inspect or change GitHub Project state; do not use it to decide roadmap, priority, strategy, or consumer workflow.
---

# GitHub Projects

Operate on **GitHub Projects v2** as an operational resource.

This skill is an independent member of the `github` Skill Family. It follows the family methodology and invariants defined in `github/FAMILY.md`.

## Purpose

Use this skill to:

- discover and identify a GitHub Project;
- inspect Project state;
- inspect Project items;
- inspect fields and field values;
- inspect views;
- add or remove items;
- update item field values;
- verify the resulting Project state.

The skill provides GitHub operations. It does not decide what the Project should mean or what work should exist.

## Family Methodology

Follow this lifecycle for every operation:

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

For read-only requests, stop after the required READ/UNDERSTAND stages and report observed state.

For mutations, all applicable stages are mandatory.

## Supported Scope

### Projects

Supported:

- discover Projects;
- identify a Project;
- read Project metadata and state.

### Items

Supported:

- list Project items;
- inspect an individual Project item;
- add an existing Issue or Pull Request to a Project;
- remove an item from a Project.

A Project item is distinct from the content it represents.

An item MAY represent:

- an Issue;
- a Pull Request;
- a Draft Issue.

Updating a Project item does not imply permission to modify the underlying Issue or Pull Request.

### Fields

Supported:

- inspect Project fields;
- inspect a field's current value for an item;
- update an item's field value when explicitly requested.

Field definition and field value are separate resources:

```text
FIELD DEFINITION
      ≠
FIELD VALUE
```

Changing an item's field value does not authorize changing the field definition.

### Views

Supported:

- inspect Project views.

View creation or structural modification is outside the initial mutation scope of this skill.

## Mutation Scope

The initial version supports only these mutations:

1. add an existing Issue or Pull Request to a Project;
2. remove a Project item;
3. update an existing item's field value.

The following are outside the initial mutation scope:

- create a Project;
- delete a Project;
- create a field;
- delete a field;
- reconfigure a field;
- create a view;
- delete a view;
- reconfigure a view;
- archive or otherwise destroy Project structure.

Do not emulate an unsupported structural operation through another mutation.

## Target Identification

Before mutation, identify the exact Project.

Prefer:

- Project owner + Project number; or
- a stable GitHub Project identifier.

A human-readable Project name alone is insufficient when ambiguity is possible.

For item operations, identify:

1. the Project;
2. the Project item;
3. when relevant, the underlying content resource.

Do not assume that an Issue/PR number alone identifies a Project item.

## Current-State Requirement

Read the relevant current state before mutation.

Do not assume:

- the Project exists;
- the Project is owned by the expected account;
- an item is already present;
- an item is absent;
- a field exists;
- a field has the expected type;
- a field currently has the expected value;
- a content resource is the one intended by the consumer.

If current state contradicts the expected state, stop and report the discrepancy unless the requested operation explicitly covers that state.

## Add Item

When asked to add an Issue or Pull Request to a Project:

1. identify the exact Project;
2. identify the exact Issue or Pull Request;
3. read the Project's current items;
4. determine whether the content is already represented;
5. if already present, do not create a duplicate;
6. otherwise add the content;
7. read the resulting Project item state;
8. verify that the intended content is represented by the Project;
9. report the verified result.

Do not modify the Issue or Pull Request merely because it is being added to a Project.

## Remove Item

When asked to remove an item:

1. identify the exact Project;
2. identify the exact Project item;
3. read its current state;
4. confirm that the item exists in that Project;
5. remove only that Project item;
6. read the resulting Project state;
7. verify that the item is no longer represented;
8. report the verified result.

Removing a Project item does not mean closing, deleting, or otherwise modifying the underlying Issue or Pull Request.

## Update Field Value

When asked to update a field value:

1. identify the exact Project;
2. identify the exact item;
3. identify the exact field;
4. read the current field definition and current value;
5. verify that the requested value is valid for that field;
6. plan the smallest field-value mutation;
7. execute the mutation;
8. read the resulting value;
9. verify that the requested value is present;
10. report the verified result.

Do not modify the field definition to make an otherwise invalid request possible.

If the requested value cannot be represented by the existing field configuration, report the incompatibility instead of changing Project structure implicitly.

## Structural Safety

Creating or modifying Projects, fields, or views is structural mutation and is intentionally outside the initial scope.

Never create structure merely because it would make another requested operation easier.

For example:

```text
REQUEST:
set Priority = High

OBSERVED:
Priority field does not exist

INVALID RESPONSE:
create Priority field → set High
```

Correct response:

```text
RESULT = UNSUPPORTED_STATE
REASON = requested field does not exist
ACTION = no structural mutation performed
```

## Underlying Resources

This skill may inspect enough information to identify the Issue or Pull Request represented by a Project item.

It does not inherit the mutation authority of:

- `github-issues`;
- `github-pull-requests`;
- any other GitHub family member.

If the requested outcome requires modifying the underlying resource rather than its Project representation, that is outside this skill's mutation boundary.

A consumer MAY compose this skill with another family member.

## Error and Uncertainty Handling

Distinguish at least:

- Project not found;
- Project identity ambiguous;
- item not found;
- item already present;
- item absent when removal was requested;
- field not found;
- field value incompatible with field configuration;
- GitHub rejected the mutation;
- resulting state could not be verified;
- requested operation outside this skill's scope;
- insufficient information to identify the target.

Do not convert an API success response into a verified success without checking the resulting state when verification is available.

When target identity or requested intent is materially ambiguous, stop before mutation.

## Consumer Boundary

This skill MUST NOT decide:

- whether work should exist;
- roadmap direction;
- priority;
- acceptance or rejection of work;
- strategic meaning of a Project;
- whether GitHub Projects is a source of truth;
- Project methodology;
- consumer governance.

The consumer supplies the desired outcome. This skill performs the GitHub Project operation safely.

## Expected Output

For read operations, report:

- identified Project;
- relevant observed state;
- relevant items/fields/views;
- material uncertainty or limitations.

For mutations, report:

- target identified;
- requested operation;
- mutation performed;
- verification performed;
- resulting state;
- any discrepancy or limitation.

Use explicit result states such as:

```text
RESULT = VERIFIED
RESULT = NO_CHANGE_REQUIRED
RESULT = NOT_FOUND
RESULT = AMBIGUOUS
RESULT = UNSUPPORTED_STATE
RESULT = MUTATION_REJECTED
RESULT = VERIFICATION_FAILED
```

Do not claim `RESULT = VERIFIED` unless the resulting GitHub state was actually checked.

## Non-Goals

This skill does not provide:

- roadmap management;
- project-management methodology;
- priority decisions;
- strategic planning;
- Issue or Pull Request lifecycle management;
- GitHub administration as a whole;
- automatic Project creation;
- automatic field/view creation;
- implicit structural repair.

## Core Principle

> **Operate on observed Project state, make the smallest authorized mutation, and verify the resulting state.**

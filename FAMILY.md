# Skill Family Specification

**Status:** Proposed  
**Version:** 0.1  
**Scope:** Generic  
**Compatibility:** Agent Skills

## 1. Definition

A **Skill Family** is a logical grouping of independently usable skills that operate within a common domain and share a defined methodology, terminology, invariants, and conventions.

A Skill Family is an organizational and behavioral convention. It is not a runtime, installation, or orchestration unit.

## 2. Purpose

A Skill Family exists to provide a common framework for related skills while preserving their individual contracts and independent usability.

A family may establish:

- a shared methodology;
- shared terminology;
- shared invariants;
- shared operational conventions;
- shared verification principles.

A family does not merge its members into a single skill.

## 3. Relationship Model

A family contains one or more member skills:

```text
Skill Family
├── Skill A
├── Skill B
└── Skill C
```

Family membership expresses commonality. It does not express dependency.

Each member retains its own purpose, capabilities, inputs, boundaries, and verification requirements.

## 4. Independence Rule

**Family Independence Rule**

Membership in a Skill Family MUST NOT create runtime, installation, activation, or availability dependencies between member skills.

Every member skill MUST remain independently usable and installable.

A member MAY complement another member, but MUST NOT require another member to satisfy its own contract.

For example:

- VALID: `github-projects` complements `github-issues`.
- INVALID: `github-projects` requires `github-issues`.
- INVALID: installing `github-projects` implicitly requires installing `github-issues`.

Knowledge about another domain resource does not constitute a dependency on the skill that specializes in that resource.

## 5. Family Contract

A family MAY define the following common elements.

### 5.1 Methodology

A shared way of performing work across member skills.

The methodology constrains how a member operates; it does not define the member's domain-specific functionality.

### 5.2 Terminology

Common terms whose meanings should remain consistent across family members.

### 5.3 Invariants

Rules that every conforming member MUST respect.

Examples include requirements to establish relevant current state before mutation, preserve unrelated state, and verify mutations.

### 5.4 Conventions

Shared conventions for identification, mutation, error handling, reporting, and other operational concerns.

### 5.5 Verification Principles

Common principles for establishing whether an operation produced the intended result.

## 6. Member Skill Contract

A family does not replace or redefine the contract of an individual skill.

Each member MUST retain an independently valid `SKILL.md` and its own:

- purpose;
- capabilities;
- inputs;
- operations;
- boundaries;
- verification criteria.

Family rules constrain member behavior where applicable, but the individual skill remains responsible for its own functional contract.

## 7. Prohibited Responsibilities

A Skill Family MUST NOT:

1. require member skills to be installed together;
2. require one member skill to activate another;
3. define functional behavior that belongs to an individual skill;
4. replace `SKILL.md`;
5. determine consumer-specific priorities or business strategy;
6. implicitly execute operations on behalf of another member;
7. assume that all family members are available;
8. make family membership necessary for a member skill to function;
9. become a hidden orchestration layer;
10. act as a package or dependency manager.

## 8. Composition

Member skills MAY be used together in a broader workflow when the relevant skills are available.

Composition is performed by the consumer or orchestrator, not implicitly by the family.

Composition MUST NOT change the independence of the participating skills.

For example:

```text
Consumer workflow
├── github-issues
└── github-projects
```

does not imply that either skill depends on the other.

### 8.1 Optional Capability References

A member skill MAY reference another skill as an **optional capability provider** when that skill provides a complementary capability that may improve the current task.

An optional capability reference:

- MUST identify the referenced skill name;
- MUST identify its distributor and source repository;
- MUST identify the capability for which it is recommended;
- MUST NOT create a runtime or installation dependency;
- MUST NOT make the referenced skill a precondition for the current skill's contract.

The canonical unambiguous reference form is:

```text
<owner>/<repository>:<skill-name>
```

For example:

```text
roldriel/skills:github-projects
```

A skill MUST NOT rely on a skill name alone when multiple distributors may provide skills with the same name.

### 8.2 Optional Capability Behavior

When an optional capability is relevant:

- If the referenced skill is available, the current skill SHOULD use or defer to it for the explicitly identified capability.
- If the referenced skill is unavailable, the current skill MUST continue using its own fallback behavior.
- The absence of the referenced skill MUST NOT be treated as an error unless the current task itself is impossible without that capability.
- Installation or activation of the referenced skill MUST require explicit user approval.
- A skill SHOULD recommend installation only when the missing capability materially improves the current task.
- Recommendations SHOULD be compact and task-specific rather than presenting a general skill catalog.

Recommended output form:

```text
> Optional skill: `roldriel/skills:github-projects` can improve this task
> by providing direct GitHub Projects operations and verification.
> It is not required. Install it?
```

An optional skill recommendation is informational and does not grant authority to install, activate, or mutate another skill.

## 9. Compatibility with Agent Skills

Skill Family is an additive convention over Agent Skills.

The individual skill remains the fundamental portable unit:

```text
SKILL.md
```

A consumer that understands only the Agent Skills specification MUST still be able to use a conforming member skill without understanding Skill Families.

Family metadata, documentation, or organization MUST NOT make the member skill non-portable.

## 10. Family Membership

A skill MAY declare membership in a Skill Family.

The semantic relationship is:

```text
Skill → member_of → Skill Family
```

The physical representation and discovery mechanism are intentionally unspecified by this version.

A repository MAY organize family members together physically, but physical nesting MUST NOT be treated as a runtime dependency.

## 11. Lifecycle

Family lifecycle and member lifecycle are independent.

A family MAY be proposed, active, deprecated, or retired without automatically changing the lifecycle state of its members.

Likewise, a member MAY be deprecated or retired while the family remains active.

## 12. Versioning

Family versioning and member skill versioning are independent.

A change to a family contract MAY require affected members to be reviewed, but member versions do not need to be synchronized.

A family version identifies the version of its shared contract, not the versions of its member skills.

## 13. Conformance

A member conforms to a Skill Family when:

- it satisfies its own `SKILL.md` contract;
- it is explicitly recognized as a member of the family;
- it respects all mandatory family invariants;
- it follows mandatory family methodology and conventions where applicable;
- it remains independently usable;
- it does not introduce prohibited dependencies on other family members.

Family conformance does not imply that every member provides the same capabilities or operates on the same resources.

## 14. Explicit Non-Goals

This specification does not define:

- skill-to-skill dependency resolution;
- automatic installation of family members;
- automatic skill activation;
- skill orchestration;
- workflow execution;
- package management;
- a universal family discovery protocol;
- a mandatory physical directory structure;
- a replacement for the Agent Skills specification.

These concerns may be addressed independently in the future without changing the fundamental independence rule.

## 15. Design Principle

The core principle of Skill Families is:

> **Shared methodology without shared dependency.**

A family provides coherence between related skills while preserving the autonomy, portability, and independent lifecycle of each member.

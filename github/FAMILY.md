# GitHub Skill Family

**Status:** Proposed  
**Version:** 0.1  
**Family:** `github`  
**Parent specification:** `FAMILY.md`  
**Scope:** Generic GitHub operations

## 1. Purpose

The GitHub Skill Family groups independently usable skills that operate on GitHub resources while sharing a common operational methodology, terminology, safety model, and verification discipline.

The family does not define GitHub strategy, consumer workflow, prioritization, or business meaning. Those responsibilities belong to the consumer.

## 2. Members

The initial family is intended to contain independently usable skills such as:

- `github-projects`
- `github-issues`
- `github-pull-requests`
- `github-releases`

This list is extensible. A new member belongs in the family only when it operates on a distinct GitHub resource or operation domain and conforms to this contract.

Family membership does not require that any other member be installed, activated, or available.

## 3. Independence

Every member MUST remain independently usable.

A member:

- MUST NOT require another family member;
- MUST NOT activate another family member implicitly;
- MUST NOT assume another family member is installed;
- MAY reference or complement another GitHub resource;
- MUST contain enough domain-specific knowledge to execute its own contract.

For example, `github-projects` MAY associate a Project item with an Issue or Pull Request, but it MUST NOT require the `github-issues` or `github-pull-requests` skill to perform that operation.

## 4. Common Methodology

Every GitHub family member follows this lifecycle:

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

### 4.1 DISCOVER

Determine whether the required GitHub resource, repository, owner, project, issue, pull request, release, or other target can be located.

Do not infer identifiers when GitHub can provide them.

### 4.2 IDENTIFY

Establish the exact target before mutation.

The skill SHOULD use stable identifiers or an unambiguous combination of owner, repository, number, ID, or other GitHub-native identifier appropriate to the resource.

A human-readable name alone MUST NOT be treated as a unique identifier when ambiguity is possible.

### 4.3 READ

Read the current state before changing it.

The skill MUST NOT assume that:

- the target exists;
- the target is in the expected state;
- a field has a particular value;
- a branch points where expected;
- a Project contains a particular item;
- a release, issue, PR, or other resource has a particular lifecycle state.

### 4.4 UNDERSTAND

Interpret the current state in relation to the requested operation.

The skill MUST distinguish:

- observed GitHub state;
- requested target state;
- assumptions;
- consumer-level intent.

The skill MUST NOT infer consumer strategy or priorities from GitHub metadata alone.

### 4.5 PLAN

Determine the minimum mutation required to reach the requested target state.

The skill SHOULD:

- change only what is necessary;
- preserve unrelated state;
- avoid creating duplicate resources;
- avoid structural changes when the requested outcome does not require them;
- avoid destructive operations unless explicitly authorized by the consumer context.

### 4.6 MUTATE

Execute the planned GitHub operation.

A mutation MUST be limited to the identified target and the declared operation.

The skill MUST NOT silently broaden scope.

### 4.7 VERIFY

After mutation, re-read the relevant GitHub state and verify that the intended result actually exists.

A successful API response alone is not sufficient evidence when the resulting state can be queried.

Verification MUST check the fields or resource state material to the requested outcome.

### 4.8 REPORT

Report the resulting state, not merely that an API operation succeeded.

When the requested target state was not achieved, the skill MUST report the discrepancy and MUST NOT claim success.

## 5. Safety Invariants

Every family member MUST respect these invariants.

### 5.1 Current-state invariant

No mutation based solely on assumed current state.

### 5.2 Minimum-mutation invariant

Change only the state necessary for the requested operation.

### 5.3 Unrelated-state preservation

Do not overwrite or remove unrelated configuration, metadata, labels, assignments, fields, or other state.

### 5.4 Explicit-target invariant

Every mutation has an identifiable target.

### 5.5 No-implicit-structure invariant

Do not create Projects, fields, views, labels, milestones, branches, releases, or other structural resources merely because they would make an operation easier unless the consumer explicitly requests or authorizes that structural change.

### 5.6 No-implicit-destruction invariant

Deletion, archival, closing, replacement, or other destructive/lifecycle-ending operations require explicit intent from the consumer context.

### 5.7 Post-mutation verification invariant

A mutation is not considered complete until its resulting state has been verified when verification is technically available.

### 5.8 Scope invariant

The skill operates only within the resource and operation boundary defined by its own contract.

Knowledge of another GitHub resource does not expand that boundary.

## 6. Read vs Mutation

Family members MUST distinguish read operations from mutations.

### Read

Normal discovery and inspection operations MAY be performed when required by the member's contract.

### Mutation

Mutations require an explicit requested outcome from the consumer workflow.

The skill MUST NOT invent a mutation merely because the observed GitHub state appears suboptimal.

### Structural mutation

Creation or modification of GitHub workflow structure — for example Projects, views, fields, repository configuration, or other durable organization — SHOULD have a higher authorization threshold than ordinary state updates.

The individual skill defines the exact boundary for its resource.

## 7. Resource Identification

GitHub resources MUST be identified using the most stable available identifier appropriate to the resource.

Examples include:

- repository owner + repository name;
- issue or pull request number within a repository;
- Project owner + Project number or stable Project identifier;
- release identifier or tag, where appropriate.

A family member MUST NOT assume that a resource named `default`, `main`, `ARgentOS`, or another human-readable value uniquely identifies the intended resource without verification.

## 8. Error and Uncertainty Handling

A family member MUST distinguish at least:

- target not found;
- target found but current state differs from expectation;
- requested mutation rejected by GitHub;
- mutation result cannot be verified;
- insufficient information to identify the target;
- operation outside the skill's contract.

When target identity or requested intent is materially ambiguous, the skill MUST stop before mutation.

A GitHub API error MUST NOT be translated into a successful outcome.

## 9. Composition

Members MAY be used together by a consumer workflow.

For example:

```text
Consumer workflow
├── github-issues
└── github-projects
```

The workflow may create or update an Issue and then place or update its representation in a Project.

Neither skill depends on the other. The consumer is responsible for sequencing and composition.

## 10. Consumer Boundary

The GitHub family provides operational capability, not decision authority.

A family member MUST NOT decide:

- project strategy;
- roadmap direction;
- business priority;
- whether work should exist;
- whether a GitHub resource is the canonical source of truth;
- whether a consumer's governance process should be changed.

The consumer decides what outcome is wanted. The skill determines how to perform the GitHub operation safely within its contract.

## 11. Individual Skill Responsibilities

Each member MUST define in its own `SKILL.md`:

- its purpose;
- supported GitHub resource(s);
- supported operations;
- target identification rules specific to the resource;
- mutation boundaries;
- resource-specific safety rules;
- resource-specific verification;
- expected output.

The family contract does not replace these definitions.

## 12. Conformance

A GitHub family member conforms when it:

1. satisfies the generic Skill Family contract;
2. follows this GitHub family methodology;
3. respects all mandatory family invariants;
4. remains independently usable;
5. defines its own resource-specific contract;
6. verifies mutations when verification is available;
7. does not assume the availability of another family member.

## 13. Explicit Non-Goals

This family does not define:

- GitHub project management methodology;
- roadmap methodology;
- issue prioritization;
- release policy;
- branch strategy;
- pull request policy;
- consumer-specific governance;
- GitHub account or repository administration as a whole;
- dependency resolution between skills;
- automatic activation of family members;
- a requirement that all GitHub resources be managed through these skills.

## 14. Core Principle

> **Operate on observed GitHub state, make the smallest authorized mutation, and verify the resulting state.**

This principle applies to every member of the GitHub Skill Family.

# ARgentOS Installation Methods

ARgentOS is installed into a host project from `roldriel/argentos`, branch `dist`.

The canonical ARgentOS root is always:

`<project-root>/.argentos`

The installation method controls how the protocol payload is represented under:

`<project-root>/.argentos/.agents/`

## Installation scope

ARgentOS installation is always project-scoped.

There is no separate "general", "global", or user-wide ARgentOS installation mode in this contract.

The Agent Skills installation of this skill may be global or project-local depending on the Skills manager. That is independent from ARgentOS installation and must not change the ARgentOS project layout.

Therefore `/argentos install` must not ask the user to choose an installation scope.

## Common installation transaction

Every method must:

1. Resolve `PROJECT_ROOT`.
2. Run `check`.
3. Require `NOT_INSTALLED` or `UNINSTALLED_WITH_SESSIONS`.
4. Validate the source ref `dist` before changing the project.
5. Prepare a temporary source representation outside the project.
6. Create the canonical `.argentos` structure.
7. Preserve displaced adopter artifacts according to `layout.md`.
8. Materialize the protocol payload.
9. Generate `.argentos/AGENTS.md`.
10. Generate the root `AGENTS.md) adapter.
11. Create `.argentos/.project/install.json`.
12. Verify with `check`.
13. Report the verified result.

If any pre-mutation step fails, the project must remain unchanged.

If a mutation fails after it starts, stop and verify the resulting state.

## 1. Git submodule

**Label:** `Git submodule`

**Description:**

Keeps the ARgentOS protocol payload as a separate Git repository mounted at `.argentos/.agents/`.

**Required metadata:**

- repository: `roldriel/argentos`;
- ref: `dist`;
- exact resolved commit recorded in `.project/install.json`.

**Installation behavior:**

1. Require a Git worktree at `PROJECT_ROOT`.
2. Verify the destination `.argentos/.agents/` does not already contain unrelated content.
3. Add the ARgentOS repository as a submodule at `.argentos/.agents/`.
4. Check out the resolved `dist` commit.
5. Verify the submodule path and commit.
6. Record method metadata.

**Update behavior:**

- fetch the configured source repository;
- resolve the current `dist` commit;
- update the submodule to that commit;
- never convert the installation to another method;
- preserve local configuration, state, and backups.

**Uninstall behavior:**

- remove the submodule registration and worktree cleanly;
- do not remove unrelated Git configuration;
- restore displaced adopter artifacts only after the ARgentOS installation has been removed.

## 2. Git tree

**Label:** `Git tree`

**Description:**

Copies the ARgentOS protocol payload into the project's Git history without creating a nested Git repository.

**Required metadata:**

- repository: `roldriel/argentos`;
- source ref: `dist`;
- exact source commit;
- method: `git_tree`.

**Installation behavior:**

1. Require a Git worktree at `PROJECT_ROOT`.
2. Resolve the source `dist` tree to an exact commit.
3. Materialize that tree at `.argentos/.agents/`.
4. Stage the resulting project files as ordinary project content.
5. Record the exact source commit in `.project/install.json`.

The implementation must not create a nested `.git/` directory inside `.argentos/.agents/`.

**Update behavior:**

- resolve the new `dist` tree;
- replace only protocol-managed payload content;
- preserve adopter-local files;
- stage the changed project files;
- update the manifest.

**Uninstall behavior:**

- remove only protocol-managed tree content;
- preserve unrelated project history/files;
- restore displaced adopter artifacts when safe.

## 3. Copy

**Label:** `Copy`

**Description:**

Copies the ARgentOS protocol payload as ordinary files.

**Required metadata:**

- repository: `roldriel/argentos`;
- source ref: `dist`;
- exact source commit;
- method: `copy`.

**Installation behavior:**

1. Resolve the source `dist` tree to an exact commit.
2. Materialize the payload into `.argentos/.agents/`.
3. Do not create a nested Git repository.
4. Record the exact source commit.

**Update behavior:**

- resolve the new `dist` tree;
- replace only protocol-managed payload content;
- preserve adopter-local files;
- update the manifest.

**Uninstall behavior:**

- remove only the managed ARgentOS files;
- preserve unrelated files;
- restore displaced adopter artifacts when safe.

## Source integrity

The implementation must not use an unpinned moving target after preflight.

The exact source commit used for an operation must be recorded before materialization.

The installed version must be read from the materialized protocol payload and recorded in the manifest.

## Method persistence

The selected method becomes part of installed ARgentOS state.

`update` must use the existing method and must not silently convert between methods.

Changing methods is a separate future operation and is not part of the current command contract.

## Unsupported environments

If a selected method cannot be executed safely in the current environment:

- return `INSTALL_METHOD_UNSUPPORTED` before mutation;
- do not silently fall back to another method;
- do not recommend a different method unless the user explicitly asks for alternatives.

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

## Methods

The user must choose exactly one of the following methods.

### 1. Git submodule

**Label:** `Git submodule`

**Description:**

Keeps the ARgentOS protocol payload as a separate Git repository mounted inside the project.

**Advantages:**

- Keeps the ARgentOS payload separate from the project's own Git history.
- Makes the upstream repository and selected revision explicit.
- Supports Git-based payload updates.

**Trade-offs:**

- Adds Git submodule management to the project.
- Cloning or moving the project requires normal submodule handling.

### 2. Git tree

**Label:** `Git tree`

**Description:**

Copies the ARgentOS protocol payload into the project's Git history without creating a nested Git repository.

**Advantages:**

- The payload becomes part of the project's normal Git history.
- Avoids submodule mechanics.
- Installed files are directly present in the project repository.

**Trade-offs:**

- The payload is no longer represented as an independent Git repository.
- Payload updates require explicit synchronization.

### 3. Copy

**Label:** `Copy`

**Description:**

Copies the ARgentOS protocol payload as ordinary files.

**Advantages:**

- Simplest filesystem model.
- Requires no Git submodule or nested repository.
- Suitable when Git integration is not desired.

**Trade-offs:**

- Updates require explicit replacement or synchronization.
- The installed payload is not automatically connected to the upstream repository.

## Selection UX

Present the three methods in this exact order with their canonical labels and descriptions.

Use the selection format defined in `ux.md`.

Do not silently select a method.

Do not rename, reorder, merge, or invent installation methods during normal operation.

## Method persistence

The selected method becomes part of the installed ARgentOS state.

`update` must use the existing method and must not silently convert between methods.

Changing methods is a separate future operation and is not part of the current command contract.

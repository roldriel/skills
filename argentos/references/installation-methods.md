# ARgentOS Installation Methods

ARgentOS is installed from "roldriel/argentos", branch "dist".

The selected method controls how the "dist" payload is represented under "<project-root>/.argentos/.agents/".

The skill must explain the options before asking the user to choose. The descriptions below are the baseline user-facing explanation.

## 1. Git submodule

Keeps the ARgentOS payload as a separate Git repository mounted inside the project.

**Advantages**
- Keeps the ARgentOS payload clearly separated from the project's own history.
- Makes the upstream ARgentOS repository and selected revision explicit.
- Supports Git-based updates of the payload.

**Trade-offs**
- Adds Git submodule management to the project.
- The project now contains a nested repository relationship that users must understand when cloning or moving the project.

## 2. Git tree

Copies the ARgentOS payload into the project's Git history without creating a nested Git repository.

**Advantages**
- The payload becomes part of the project's normal Git history.
- Avoids submodule mechanics.
- Keeps the installed files directly available in the project repository.

**Trade-offs**
- The payload is no longer represented as an independent Git repository inside the project.
- Updating the payload requires an explicit synchronization/update operation.

## 3. Copy

Copies the ARgentOS payload as ordinary files.

**Advantages**
- Simplest filesystem model.
- No Git submodule or nested repository is required.
- Works for projects where Git integration is not desired.

**Trade-offs**
- Updates require an explicit replacement/synchronization operation.
- The installed payload is not automatically connected to the upstream Git repository.

## Scope

Installation scope and payload method are separate choices.

The user must first choose whether the operation applies to the current project or to a general installation context supported by ARgentOS. The meaning and implementation of the general scope must not change the canonical project location: when ARgentOS is installed in a project, its protocol root remains "<project-root>/.argentos".

## Selection UX

Present the choices with their explanations before asking for a selection.

Do not silently select a method because it is familiar to the agent.

Do not assume that the user understands Git submodules, Git trees, or repository synchronization.

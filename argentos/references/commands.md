# ARgentOS Commands

This document defines the normative command contracts. User-facing wording is defined by `ux.md`.

## Command routing

| Command | Read-only | Mutation | Required confirmation |
|---|---:|---:|---:|
| `install` | No | Yes | Yes before mutation |
| `check` | Yes | No | No |
| `doctor` | No | Yes | Yes before repair |
| `update` | No | Yes | Yes before update |
| `uninstall` | No | Yes | Yes before uninstall and session deletion choice |
| `version` | Yes | No | No |
| `help` | Yes | No | No |

## install

### Preconditions

1. Resolve the project root.
2. If the root cannot be resolved, stop with `PROJECT_ROOT_UNRESOLVED`.
3. Run the equivalent of `check`.
4. Classify the current lifecycle state before proposing installation.

### Fresh installation

A fresh installation is allowed only when the current state is `NOT_INSTALLED`.

The skill must:

1. Present the installation scope choices defined by `installation-methods.md`.
2. Explain each choice using its canonical description.
3. Ask for one scope selection.
4. Present the installation methods using their canonical descriptions.
5. Ask for one method selection.
6. Explain the planned changes using the canonical confirmation template.
7. Obtain confirmation.
8. Perform the installation.
9. Verify the resulting state.
10. Report the verified result.

If scope semantics are not defined by the current contract, do not present or invent a scope choice. Stop with an explicit specification gap rather than guessing.

### Existing or actionable state

If the state is `INSTALLED`, `INSTALLED_WITH_DRIFT`, `INCOMPLETE`, `UNINSTALLED_WITH_SESSIONS`, `BROKEN`, or `UNKNOWN`, do not start a fresh installation.

Report the detected state and offer only actions permitted by `lifecycle.md`.

## check

`check` is strictly read-only.

It must not modify:

- project files;
- Git configuration;
- submodules;
- sessions;
- project metadata;
- backups;
- configuration.

It must:

1. Resolve the project root.
2. Inspect the expected ARgentOS layout.
3. Determine the lifecycle state.
4. Determine the command result.
5. Report the verified state.

If state cannot be determined reliably, use `STATE = UNKNOWN` and the appropriate error identifier.

## doctor

1. Run `check`.
2. If no repair is needed, return `REPAIR_NOT_NEEDED`.
3. If repair is possible, identify the exact repair actions.
4. Use the canonical repair confirmation.
5. Perform only the approved repair actions.
6. Run `check` again.
7. Report the verified resulting state.

If automatic repair would require an unsupported assumption, stop with `REPAIR_UNSAFE`.

## update

1. Run `check`.
2. Require an existing usable installation.
3. Determine the installed version and installation method.
4. Determine whether an update is needed.
5. If no update is needed, return `UPDATE_NOT_NEEDED`.
6. Explain the planned changes.
7. Obtain confirmation.
8. Update using the existing installation method.
9. Preserve adopter-local configuration and persistent state according to `layout.md`.
10. Run `check`.
11. Report the verified resulting state and version.

Do not silently change installation methods during an update.

## uninstall

1. Run `check`.
2. Require a state for which uninstall is meaningful.
3. Explain what will be removed and what may be restored.
4. Obtain uninstall confirmation.
5. Ask the session-preservation question defined by `ux.md`.
6. Perform only the selected action.
7. Verify the resulting state.
8. Report the verified result.

A backup conflict must stop restoration rather than silently overwrite the conflicting artifact.

## version

Report only a version actually available from the current project context.

If no installed project version can be established, return `VERSION_UNAVAILABLE`. Never infer a version from memory or from a different repository.

## help

Display the canonical command menu from `ux.md`.

Help is read-only.

## bare invocation

`/argentos` without a command is equivalent to interactive help.

It must:

1. Show the canonical command menu.
2. Ask which operation the user wants.
3. Perform no operation until the user selects one.

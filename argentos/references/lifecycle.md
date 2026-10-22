# ARgentOS Lifecycle

This document defines the normative lifecycle state machine used by all commands.

## States

### NOT_INSTALLED

No usable ARgentOS installation is present and no preserved ARgentOS session state requires special handling.

Allowed actions:

- `check`
- `install`
- `help`
- `version`

### INSTALLED

The canonical ARgentOS structure exists, the installed method is identifiable, required identity/version data is valid, and no drift is detected.

Allowed actions:

- `check`
- `doctor`
- `update`
- `uninstall`

### INSTALLED_WITH_DRIFT

The installation is identifiable and usable, but one or more managed artifacts differ from the expected state.

Allowed actions:

- `check`
- `doctor`
- `update`
- `uninstall`

A fresh `install` is not allowed.

### INCOMPLETE

ARgentOS installation artifacts exist, but the expected installation was not completed.

Allowed actions:

- `check`
- `doctor`

A fresh `install` must not overwrite this state.

### UNINSTALLED_WITH_SESSIONS

ARgentOS protocol/governance files have been removed, but persistent ARgentOS project state or sessions were deliberately preserved.

Allowed actions:

- `check`
- `install`
- `help`
- `version`

A reinstall must preserve the retained sessions.

### BROKEN

Required ARgentOS components are damaged, contradictory, or unusable, and the skill cannot safely classify the state as a normal installed state.

Allowed actions:

- `check`
- `doctor`

Recovery that requires destructive assumptions is blocked with `REPAIR_UNSAFE`.

### UNKNOWN

The skill cannot determine the lifecycle state reliably.

Allowed actions:

- `check`
- `help`

No mutating command may proceed from `UNKNOWN` without a new successful check that establishes a supported state.

## State precedence

When multiple conditions are observed, classify using this precedence:

1. `UNKNOWN` if required observations cannot be obtained reliably.
2. `BROKEN` if observations are contradictory or required managed data is damaged.
3. `INCOMPLETE` if an adoption transaction appears partially completed.
4. `UNINSTALLED_WITH_SESSIONS` if installation is absent but preserved ARgentOS state remains.
5. `INSTALLED_WITH_DRIFT` if installation is complete but managed content differs.
6. `INSTALLED` if all required conditions match.
7. `NOT_INSTALLED` if no ARgentOS installation or preserved state is present.

The implementation must not choose a lower-precedence state when a higher-precedence condition is verified.

## Transitions

| Current state | Command | Resulting state |
|---|---|---|
| `NOT_INSTALLED` | `install` success | `INSTALLED` |
| `NOT_INSTALLED` | `install` failure | `NOT_INSTALLED` or verified partial state |
| `INSTALLED` | `doctor` no repair | `INSTALLED` |
| `INSTALLED` | `doctor` success | `INSTALLED` |
| `INSTALLED_WITH_DRIFT` | `doctor` success | `INSTALLED` or verified drift |
| `INCOMPLETE` | `doctor` success | `INSTALLED` or verified remaining state |
| `BROKEN` | `doctor` success | `INSTALLED` or verified remaining state |
| installed state | `update` no-op | same verified installed state |
| installed state | `update` success | `INSTALLED` |
| installed state | `uninstall` + keep sessions | `UNINSTALLED_WITH_SESSIONS` |
| installed state | `uninstall` + delete sessions | `NOT_INSTALLED` |
| `UNINSTALLED_WITH_SESSIONS` | `install` success | `INSTALLED` |
| any state | failed mutation | verified resulting state |

A failed mutation must never be mapped directly to `INSTALLED` or `NOT_INSTALLED` without verification.

## Command blocking

When a command is not allowed for the current state, return the command-specific blocked result and an applicable error identifier. Do not mutate the project.

Examples:

- `install` from `INSTALLED` → `INSTALL_BLOCKED` + `INSTALL_ALREADY_PRESENT`.
- `update` from `NOT_INSTALLED` → `UPDATE_BLOCKED` + `STATE_UNKNOWN` is not correct; use a command-specific unavailable-state error when one exists.
- mutation from `UNKNOWN` → blocked; require a successful check.

## Lifecycle principles

- `check` never changes state.
- Mutating commands must classify state before acting.
- Every mutation is followed by verification.
- A failed mutation is never presented as successful.
- Ambiguity is resolved by observation or user input, never by assumption.

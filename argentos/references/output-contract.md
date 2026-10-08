# ARgentOS Output Contract

This document defines the machine-readable and human-readable result contract for ARgentOS operations.

## Result envelope

Every completed command must conceptually produce:

```
RESULT = <result>
STATE = <state>
```

Mutating commands must also report whether post-operation verification passed.

The agent must not invent result identifiers. If a required result cannot be determined, use `RESULT = UNKNOWN` and explain why.

## Result identifiers

### Check

- `CHECK_PASS`
- `CHECK_WARN`
- `CHECK_FAIL`
- `CHECK_UNKNOWN`

### Install

- `INSTALL_COMPLETE`
- `INSTALL_BLOCKED`
- `INSTALL_FAILED`

### Doctor

- `REPAIR_PLAN_READY` — internal planning result; no mutation occurred.
- `REPAIR_COMPLETE`
- `REPAIR_NOT_NEEDED`
- `REPAIR_BLOCKED`
- `REPAIR_FAILED`

### Update

- `UPDATE_COMPLETE`
- `UPDATE_NOT_NEEDED`
- `UPDATE_BLOCKED`
- `UPDATE_FAILED`

### Uninstall

- `UNINSTALL_COMPLETE`
- `UNINSTALL_BLOCKED`
- `UNINSTALL_FAILED`

### Version

- `VERSION_REPORTED`
- `VERSION_UNAVAILABLE`

### Help

- `HELP_DISPLAYED`

## State/result relationship

The result and lifecycle state are independent.

Examples:

```
RESULT = CHECK_PASS
STATE = INSTALLED
```

```
RESULT = CHECK_WARN
STATE = INSTALLED_WITH_DRIFT
```

```
RESULT = INSTALL_COMPLETE
STATE = INSTALLED
```

```
RESULT = UPDATE_NOT_NEEDED
STATE = INSTALLED
```

A successful command must not imply a healthy state unless the state itself was verified.

## Verification rule

For `install`, `doctor`, `update`, and `uninstall`:

1. Perform the requested mutation.
2. Run applicable post-operation verification.
3. Determine the resulting lifecycle state.
4. Emit the result only from the verified outcome.

If verification fails, the operation must not be reported as complete.

## Dynamic fields

The following fields may be included when known:

- `PROJECT_ROOT`
- `ARGENTOS_ROOT`
- `VERSION`
- `METHOD`
- `DRIFT`
- `REPAIRED`
- `CHANGED_FILES`
- `RESTORED_FILES`
- `PRESERVED_SESSIONS`

Only values actually observed or computed by the operation may be reported.

## Human-readable output

Human-readable output must use the templates in `ux.md`.

The result/state envelope is authoritative. Prose must not contradict it.

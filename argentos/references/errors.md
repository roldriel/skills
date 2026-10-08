# ARgentOS Error and Clarification Contract

This document defines canonical failure and clarification identifiers and their required handling.

## Principles

- Errors are classified before being explained.
- The agent must not convert an unknown condition into a guessed condition.
- A failed operation is never reported as successful.
- If a mutation partially completed, report the verified resulting state.
- Error identifiers are stable and must not be renamed for stylistic reasons.

## Error identifiers

### Project resolution

- `PROJECT_ROOT_UNRESOLVED` — project root cannot be determined reliably.
- `PROJECT_ROOT_INVALID` — supplied or resolved root is not a valid project root.

### Installation

- `INSTALL_ALREADY_PRESENT` — a usable installation already exists.
- `INSTALL_INCOMPLETE` — an incomplete installation requires recovery handling.
- `INSTALL_STATE_AMBIGUOUS` — current state cannot safely be classified.
- `INSTALL_METHOD_UNSUPPORTED` — selected installation method is unavailable.

### Runtime state

- `STATE_UNKNOWN` — lifecycle state cannot be determined.
- `STATE_INCONSISTENT` — observed artifacts contradict the expected layout/state.
- `STATE_BROKEN` — required ARgentOS components are damaged or unusable.
- `STATE_NOT_INSTALLED` — no installed ARgentOS instance exists for a command that requires one.

### Update/repair

- `UPDATE_SOURCE_UNAVAILABLE` — the required update source cannot be reached or read.
- `UPDATE_METHOD_MISMATCH` — the installed representation cannot be updated using its recorded method.
- `REPAIR_UNSAFE` — automatic repair would require an unsupported or destructive assumption.

### Uninstall

- `BACKUP_CONFLICT` — restoring a displaced artifact would overwrite an existing artifact.
- `SESSION_ACTION_REQUIRED` — the user has not selected whether preserved sessions should be kept or deleted.

### Generic

- `OPERATION_CANCELLED` — the user explicitly declined a required confirmation.
- `VERIFICATION_FAILED` — post-operation verification did not establish the expected result.
- `OPERATION_FAILED` — operation failed without a more specific error identifier.

## Handling contract

For a known error:

```
RESULT = <command-specific failure result>
ERROR = <error identifier>
STATE = <verified state>
```

For an unknown error:

```
RESULT = <command-specific failure result>
ERROR = OPERATION_FAILED
STATE = UNKNOWN
```

The human-readable explanation must use the failure template from `ux.md`.

## Cancellation

Cancellation is not an error in the system state.

When the user declines a confirmation:

```
RESULT = <command>_BLOCKED
ERROR = OPERATION_CANCELLED
STATE = <state before operation>
```

No mutation may follow a cancellation.

## Recovery boundary

If a failure leaves the project in a state that differs from the pre-operation state, the skill must not claim that no changes were made. It must report the verified resulting state and stop unless the user explicitly requests recovery.

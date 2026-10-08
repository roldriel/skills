# ARgentOS Lifecycle

The lifecycle describes the observable project states used by the skill to decide which actions are appropriate.

## States

### NOT_INSTALLED

No usable ARgentOS installation is present.

Typical action:

- offer "install".

### INSTALLED

ARgentOS is installed and its expected structure and identity are consistent.

Typical actions:

- "check"
- "doctor"
- "update"
- "uninstall"

### INSTALLED_WITH_DRIFT

ARgentOS is installed but one or more expected files, versions, configuration elements, or identities differ from the expected state.

Typical actions:

- "check"
- "doctor"
- "update"
- "uninstall"

### INCOMPLETE

An installation was started or partially created but did not reach a valid installed state.

Typical actions:

- "check"
- "doctor"
- recovery/reinstallation when offered by the diagnostic result.

The skill must not blindly overwrite an incomplete installation.

### UNINSTALLED_WITH_SESSIONS

ARgentOS is no longer installed, but persistent project sessions/state were deliberately preserved.

Typical actions:

- reinstall while preserving the sessions;
- inspect/check the remaining state;
- explicitly remove the preserved sessions.

### BROKEN

The installation contains contradictory, damaged, or otherwise unrecoverable elements that prevent normal operation.

Typical actions:

- "check"
- "doctor"
- explicit recovery/reinstallation when supported.

### UNKNOWN

The skill cannot reliably determine the state.

The safe behavior is to make no mutating changes, explain what could not be determined, and ask the user for the information needed to continue.

## Lifecycle principles

- "check" never changes state.
- Mutating commands must understand the current state before acting.
- "install" begins by checking the current state.
- "doctor" repairs and then checks again.
- "update" operates on an existing installation and preserves adopter-local configuration/state according to the layout contract.
- "uninstall" requires explicit confirmation and a separate choice about preserved sessions.
- A failed mutation must not be presented as successful.
- When state is ambiguous, prefer asking rather than guessing.

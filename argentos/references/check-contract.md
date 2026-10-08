# ARgentOS Check Contract

`check` is the authoritative read-only state detector used by all other commands.

## Invariants

`check` must:

- never modify the project;
- never modify Git configuration;
- never create or remove files;
- never initialize a repository or submodule;
- never alter sessions or configuration;
- return the same classification for the same observed filesystem/Git state.

## Observation roots

Resolve:

- `PROJECT_ROOT` — host project root.
- `ARGENTOS_ROOT` — `PROJECT_ROOT/.argentos`.
- `PAYLOAD_ROOT` — `ARGENTOS_ROOT/.agents`.
- `PROJECT_STATE_ROOT` — `ARGENTOS_ROOT/.project`.
- `BACKUP_ROOT` — `ARGENTOS_ROOT/.backup`.
- `CONFIG_PATH` — `ARGENTOS_ROOT/features.toml`.

No observation may derive these roots with fixed parent-depth assumptions.

## Required observations

The checker records, without modifying them:

1. project-root validity;
2. existence/type of `ARGENTOS_ROOT`;
3. existence/type of `ARGENTOS_ROOT/AGENTS.md`;
4. existence/type of `PAYLOAD_ROOT`;
5. existence/type of `PROJECT_STATE_ROOT`;
6. existence/type of `BACKUP_ROOT`;
7. existence/type of `CONFIG_PATH`;
8. existence/type of root `AGENTS.md`;
9. existence/type of root `.agents/`;
10. existence/type of root `.gitignore`;
11. backup artifacts;
12. installation method metadata, when available;
13. installed protocol version, when available;
14. payload identity, when available;
15. preserved-session indicators, when available.

## Classification rules

### NOT_INSTALLED

Use only when:

- `ARGENTOS_ROOT` does not exist;
- no ARgentOS backup/session residue requires lifecycle handling.

### UNINSTALLED_WITH_SESSIONS

Use when:

- the active ARgentOS installation is absent;
- preserved ARgentOS project state/session data remains identifiable.

### INCOMPLETE

Use when:

- `ARGENTOS_ROOT` exists; and
- adoption artifacts indicate that installation started but the canonical structure is incomplete.

Examples include:

- `ARGENTOS_ROOT/AGENTS.md` exists but `PAYLOAD_ROOT` is absent;
- payload exists but required state/configuration creation is incomplete;
- an installation transaction marker explicitly indicates an unfinished operation.

### BROKEN

Use when:

- required managed artifacts exist but are unreadable, damaged, contradictory, or structurally impossible to classify as an installed state.

### INSTALLED_WITH_DRIFT

Use when:

- the canonical installation structure is complete;
- the installation method is identifiable;
- managed identity/version checks can be performed; and
- one or more managed artifacts differ from the expected state.

Drift must identify the affected artifact(s).

### INSTALLED

Use when:

- canonical structure is complete;
- installation method is identifiable;
- required managed identity/version checks succeed;
- no drift is detected.

### UNKNOWN

Use when required observations cannot be obtained reliably, for example due to permission errors or an unsupported representation.

Do not downgrade an observation failure to `NOT_INSTALLED`.

## Result mapping

```
INSTALLED                 -> CHECK_PASS
NOT_INSTALLED             -> CHECK_PASS
UNINSTALLED_WITH_SESSIONS -> CHECK_WARN
INSTALLED_WITH_DRIFT      -> CHECK_WARN
INCOMPLETE                -> CHECK_FAIL
BROKEN                    -> CHECK_FAIL
UNKNOWN                   -> CHECK_UNKNOWN
```

## Diagnostic payload

The checker should return structured data conceptually equivalent to:

```
RESULT
STATE
PROJECT_ROOT
ARGENTOS_ROOT
METHOD
VERSION
DRIFT
BACKUP_ARTIFACTS
PRESERVED_SESSIONS
ERROR
```

Only observed values are populated.

## Determinism

The checker must not use:

- current wall-clock time as a classification input;
- network state for filesystem-only classification;
- model inference;
- heuristic similarity;
- arbitrary parent-depth discovery.

If an external source is required to establish a fact, record the source failure rather than guessing.

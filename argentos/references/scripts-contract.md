# ARgentOS Script Contract

Scripts are deterministic execution components. The model selects a command and gathers user decisions; scripts perform filesystem/Git operations and return structured results.

## Runtime interface

Scripts are Python 3 programs invoked with explicit arguments.

Project root must be supplied through:

- `--root PATH`; or
- `ARGENTOS_PROJECT_ROOT`.

If neither is supplied, return `PROJECT_ROOT_UNRESOLVED`.

Scripts must not infer the project root from their own file location or fixed parent depth.

## Common conventions

Every command script must:

1. validate its inputs;
2. resolve canonical roots;
3. perform only the command's allowed operations;
4. return structured JSON on stdout;
5. write diagnostics to stderr only when necessary;
6. use a non-zero exit code for execution failure;
7. never print conversational prose as machine output.

The JSON result must contain at least:

```json
{
  "result": "RESULT_IDENTIFIER",
  "state": "STATE_IDENTIFIER"
}
```

Known dynamic fields may be added according to `output-contract.md`.

## Script boundaries

### `check.py`

Read-only.

Responsibilities:

- resolve project root;
- inspect filesystem/Git observations;
- classify lifecycle state;
- detect method/version/identity when available;
- return the check result.

It must not mutate anything.

### `install.py`

Responsibilities:

- validate requested method;
- resolve exact source commit;
- execute the common installation transaction;
- write the installation manifest;
- verify the result.

It must reject unsupported methods before mutation.

### `doctor.py`

Responsibilities:

- receive an explicit approved repair plan;
- validate the plan against the current state;
- execute only supported repair actions;
- verify afterward.

The script must not invent repair actions.

### `update.py`

Responsibilities:

- read the existing method;
- resolve the target source commit;
- update only protocol-managed content;
- preserve local state/configuration/backups;
- update the manifest;
- verify afterward.

It must reject method mismatch.

### `uninstall.py`

Responsibilities:

- receive the explicit session policy;
- remove only ARgentOS-managed artifacts;
- restore displaced adopter artifacts without overwriting conflicts;
- preserve sessions when requested;
- verify afterward.

It must reject missing session policy.

## Canonical arguments

### install

```
python install.py --root PATH --method submodule|git_tree|copy
```

### check

```
python check.py --root PATH
```

### doctor

```
python doctor.py --root PATH --plan PLAN.json
```

### update

```
python update.py --root PATH
```

### uninstall

```
python uninstall.py --root PATH --sessions keep|delete
```

## Source handling

Scripts must resolve the source repository `roldriel/argentos` at ref `dist`.

The resolved commit must be captured before materialization.

Network/source failures must return `UPDATE_SOURCE_UNAVAILABLE` or the applicable installation failure without guessing a version.

## Determinism requirements

Scripts must not:

- use current time as a state decision;
- make network calls for `check`;
- search arbitrary parent directories;
- silently fall back to another installation method;
- silently overwrite files;
- silently delete sessions;
- return success before verification.

## Atomicity boundary

Before mutation, scripts must complete all validations that can be performed without mutation.

Where a complete filesystem transaction cannot be atomic, the script must:

1. record enough state to detect partial completion;
2. stop on the first unrecoverable failure;
3. run verification;
4. return the verified partial state.

Automatic rollback is not permitted unless explicitly defined by the command contract.

## Exit codes

- `0` — command executed and returned its contractual result.
- `2` — invalid invocation or user-supplied input.
- `3` — project/state precondition blocks the operation.
- `4` — operation failed after execution began.
- `5` — verification could not establish the expected result.

The JSON result remains authoritative; exit codes provide process-level classification.

# ARgentOS Dialogue Scenarios

This document defines canonical end-to-end conversational flows. The agent must follow the applicable flow without adding extra decisions.

## D1 — bare invocation

Input:

`/argentos`

Flow:

1. Render the command menu from `ux.md`.
2. Ask which operation the user wants.
3. Wait for the user.

No project inspection or mutation occurs before command selection.

## D2 — install on a fresh project

Precondition: `check` returns `STATE = NOT_INSTALLED`.

Flow:

1. Resolve and validate `PROJECT_ROOT`.
2. Present the three installation methods in canonical order.
3. Ask for one method.
4. Validate that the selected method is supported in the current environment.
5. Produce the install confirmation from `ux.md`.
6. Wait for Yes/No.
7. If No, return `INSTALL_BLOCKED` + `OPERATION_CANCELLED`.
8. If Yes, execute installation.
9. Verify with `check`.
10. Report the verified result.

The agent must not ask for installation scope.

## D3 — install when already installed

If `check` returns `INSTALLED`:

1. Do not mutate.
2. Return `INSTALL_BLOCKED` + `INSTALL_ALREADY_PRESENT`.
3. Tell the user that an installation already exists.
4. Offer `update` or `uninstall` as the next operations.

Do not re-run installation automatically.

## D4 — install with preserved sessions

If `check` returns `UNINSTALLED_WITH_SESSIONS`:

1. Do not discard sessions.
2. Explain that ARgentOS is absent but preserved project state remains.
3. Offer reinstall while preserving the sessions.
4. Continue through the normal method-selection and confirmation flow.

## D5 — check

Flow:

1. Resolve project root.
2. Run all read-only observations from `check-contract.md`.
3. Classify lifecycle state using the precedence rules.
4. Emit the result/state envelope.
5. Render the corresponding human-readable result.

No confirmation is requested.

## D6 — doctor with no repair needed

Precondition: `check` returns `INSTALLED` with no repairable issue.

Return:

`RESULT = REPAIR_NOT_NEEDED`

`STATE = INSTALLED`

Do not ask for confirmation.

## D7 — doctor with repair needed

Flow:

1. Run `check`.
2. Determine exact repair actions.
3. If repair is unsafe or ambiguous, stop with `REPAIR_UNSAFE` or the applicable state error.
4. Show the canonical doctor confirmation with the verified repair list.
5. Wait for Yes/No.
6. If No, return `REPAIR_BLOCKED` + `OPERATION_CANCELLED`.
7. If Yes, execute only the listed repairs.
8. Run `check` again.
9. Report the verified resulting state.

## D8 — update already current

If the installed version is already the target version:

`RESULT = UPDATE_NOT_NEEDED`

The skill must not modify protocol payload, configuration, sessions, backups, or method metadata.

## D9 — update

Flow:

1. Run `check`.
2. Require `INSTALLED` or another explicitly updateable installed state.
3. Determine the installed method and current version.
4. Determine the target version from the update source.
5. If already current, use D8.
6. Show the canonical update confirmation.
7. Wait for Yes/No.
8. If No, return `UPDATE_BLOCKED` + `OPERATION_CANCELLED`.
9. Update using the existing method.
10. Preserve local configuration, sessions, backups, and method.
11. Run `check`.
12. Report the verified result.

## D10 — uninstall, keep sessions

Flow:

1. Run `check`.
2. Show uninstall confirmation.
3. Wait for Yes/No.
4. If No, return `UNINSTALL_BLOCKED` + `OPERATION_CANCELLED`.
5. Ask the canonical session-data question.
6. If **Keep sessions**, uninstall managed installation artifacts and preserve `.argentos/.project/` session state according to the lifecycle contract.
7. Restore displaced adopter artifacts only when destinations are absent.
8. Run `check`.
9. Report `UNINSTALL_COMPLETE` + `UNINSTALLED_WITH_SESSIONS` if verified.

## D11 — uninstall, delete sessions

Follow D10 until the session choice.

If **Delete sessions**:

1. Remove the preserved ARgentOS project state/session data.
2. Remove the remaining managed ARgentOS installation artifacts.
3. Restore displaced adopter artifacts only when destinations are absent.
4. Run `check`.
5. Report `UNINSTALL_COMPLETE` + `NOT_INSTALLED` only if verified.

## D12 — root cannot be resolved

If project root resolution fails:

1. Do not inspect another path.
2. Do not guess.
3. Render the project-root clarification from `ux.md`.
4. Wait for a user-supplied path.
5. Validate the supplied path before continuing.

## D13 — ambiguous or unknown state

If `check` returns `UNKNOWN`:

1. Do not mutate.
2. Render the ambiguity contract.
3. State the missing observation or permission problem.
4. Ask only for the information required to continue.

## D14 — mutation partially fails

If a mutation changes the project and then fails:

1. Stop the failed operation.
2. Do not claim success.
3. Run read-only verification if possible.
4. Report the verified resulting state.
5. Use `VERIFICATION_FAILED` when the resulting state cannot be established.
6. Do not start an automatic recovery operation unless the user explicitly requests it and the recovery is covered by the contract.

## Dialogue invariants

Across every scenario:

- no hidden mutations;
- no invented values;
- no silent method changes;
- no silent session deletion;
- no success before verification;
- no alternative wording for canonical prompts when a template exists.

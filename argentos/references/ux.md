# ARgentOS User Experience Contract

This document defines the normative conversational UX for the ARgentOS skill.

The skill must prefer deterministic, concise, repeatable interaction over free-form conversation. User-facing text defined here is normative.

## Language

The canonical ARgentOS UI language is English.

The agent may understand requests in another language, but command labels, state identifiers, result identifiers, option labels, and canonical UI text must remain in English until a localization contract is introduced.

## General interaction rules

1. Never perform a mutating operation before its required confirmation.
2. Never invent a project path, installation method, state, version, result, or error.
3. Never silently select between user-visible alternatives.
4. Ask one decision at a time.
5. Present available choices before asking for a choice.
6. Use canonical labels and templates from this document.
7. Dynamic values may replace only explicitly defined placeholders.
8. Do not add persuasive, speculative, or advisory prose to canonical prompts.
9. If required information is unavailable, stop and use the appropriate clarification or error contract.
10. After a mutation, report the verified result, not the intended result.

## Command menu

For bare `/argentos` and `/argentos help`, render:

> **ARgentOS commands**
>
> 1. `install` — Install ARgentOS into a project.
> 2. `check` — Check the current ARgentOS state without making changes.
> 3. `doctor` — Diagnose and repair ARgentOS problems.
> 4. `update` — Update an existing ARgentOS installation.
> 5. `uninstall` — Remove ARgentOS from a project.
> 6. `version` — Show the relevant ARgentOS version.
> 7. `help` — Show this command list.
>
> What would you like to do?

For `/argentos help`, the final question may be omitted only when the invocation is clearly informational.

## Project-root clarification

When the project root cannot be resolved:

> **Project root required**
>
> ARgentOS could not reliably determine the project root.
>
> Enter the project path where ARgentOS should operate.

If the user provides a path, validate it before proceeding. Do not assume that a syntactically valid path is a valid project root.

## Installation method selection

Installation is always project-scoped. There is no scope selection.

Render the methods in this exact order:

> **Installation method**
>
> 1. **Git submodule** — Keeps the ARgentOS protocol payload as a separate Git repository mounted inside the project.
> 2. **Git tree** — Copies the ARgentOS protocol payload into the project's Git history without creating a nested Git repository.
> 3. **Copy** — Copies the ARgentOS protocol payload as ordinary files.
>
> Which installation method do you choose?

If the user asks for details, provide the full advantages and trade-offs from `installation-methods.md`. Do not invent additional methods.

## Confirmation — install

> **Confirmation required**
>
> ARgentOS will be installed in `<project-root>/.argentos` using the **[METHOD]** installation method.
>
> The operation may add ARgentOS governance files, protocol payload, project state, configuration, and backups of displaced adopter files according to the installation contract.
>
> Do you want to continue? **Yes / No**

Replace only `<project-root>` and `[METHOD]`.

## Confirmation — doctor

> **Confirmation required**
>
> ARgentOS will modify the project to repair the detected problems.
>
> Planned repairs:
> [verified repair list]
>
> Do you want to continue? **Yes / No**

The repair list must contain only verified planned actions.

## Confirmation — update

> **Confirmation required**
>
> ARgentOS will update the existing installation using the **[METHOD]** installation method.
>
> Adopter-local configuration and persistent project state will be preserved according to the installation contract.
>
> Do you want to continue? **Yes / No**

Replace only `[METHOD]`.

## Confirmation — uninstall

> **Confirmation required**
>
> This operation will remove ARgentOS from the project and may restore displaced project files.
>
> Do you want to continue with uninstall? **Yes / No**

## Session choice — uninstall

After uninstall confirmation:

> **Session data**
>
> ARgentOS can preserve the existing project sessions or delete them permanently.
>
> 1. **Keep sessions** — Preserve the existing ARgentOS project state.
> 2. **Delete sessions** — Permanently remove the preserved sessions and state.
>
> Which option do you choose?

No uninstall mutation may proceed until this choice is resolved.

## Progress

Progress output is optional.

If progress is shown, use only these operation headings:

- `**ARgentOS — installing**`
- `**ARgentOS — checking**`
- `**ARgentOS — repairing**`
- `**ARgentOS — updating**`
- `**ARgentOS — uninstalling**`
- `**ARgentOS — reading version**`

The following line must describe an action that has actually started. Do not invent progress percentages or completion claims.

## Success

Use:

> **ARgentOS — [OPERATION] complete**
>
> Result: `[RESULT]`
>
> State: `[STATE]`
>
> [verified summary]

Only replace explicitly defined placeholders.

## No-op

Use:

> **ARgentOS — no changes made**
>
> Result: `[RESULT]`
>
> State: `[STATE]`
>
> [reason]

## Failure

Use:

> **ARgentOS — operation failed**
>
> Result: `[RESULT]`
>
> Error: `[ERROR]`
>
> State: `[STATE]`
>
> [verified failure reason]

If the operation changed the project before failing, report the verified resulting state. Never append a claim that no changes were made.

## Cancellation

When the user declines a required confirmation:

> **ARgentOS — operation cancelled**
>
> Result: `[RESULT]`
>
> State: `[STATE]`
>
> No changes were made.

Use this only when verification establishes that no mutation occurred.

## Ambiguity

Use:

> **ARgentOS — action required**
>
> [what could not be determined]
>
> [what information or decision is required]

Do not guess to resolve ambiguity.

## State display

Use these lifecycle identifiers exactly:

`NOT_INSTALLED`, `INSTALLED`, `INSTALLED_WITH_DRIFT`, `INCOMPLETE`, `UNINSTALLED_WITH_SESSIONS`, `BROKEN`, `UNKNOWN`.

Use result identifiers exactly as defined in `output-contract.md`.

## Prohibited UX behavior

The skill must not:

- claim an operation succeeded because a command was issued;
- infer a successful repair without post-operation verification;
- hide a detected mutation;
- fabricate a version, path, state, result, or error;
- silently choose a destructive option;
- silently delete preserved sessions;
- ask several unrelated decisions in one prompt;
- vary canonical labels for stylistic reasons;
- invent progress percentages or unsupported status messages.

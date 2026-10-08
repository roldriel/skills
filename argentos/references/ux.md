# ARgentOS User Experience Contract

This document defines the canonical conversational UX for the ARgentOS skill.

The skill must prefer deterministic, concise, repeatable interaction over free-form conversation. User-facing text defined here is normative.

## Language

The skill's canonical UI language is English.

The agent may understand a user's request in another language, but command labels, state identifiers, option names, result labels, and fixed explanatory text must remain exactly as defined here unless a future localization contract is introduced.

## General interaction rules

1. Never perform a mutating operation before its required confirmation.
2. Never invent a project path, installation scope, installation method, state, version, or result.
3. Never silently select between user-visible alternatives.
4. Ask one decision at a time.
5. Present the available choices before asking the user to choose.
6. Use the canonical labels and message templates in this document.
7. Dynamic values may replace only the placeholders explicitly defined by a template.
8. Do not add persuasive, speculative, or advisory prose to a canonical prompt.
9. If required information is unavailable, stop and use the appropriate error/clarification message.
10. After a mutation, report the verified result, not the intended result.

## Command menu

For bare `/argentos` invocation and `/argentos help`, render:

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

For `/argentos help`, the final question may be omitted when the invocation is clearly informational.

## Selection presentation

When a choice is required, use numbered options.

Format:

> **[Decision title]**
>
> 1. **[Option label]** — [fixed explanation]
> 2. **[Option label]** — [fixed explanation]
>
> Which option do you choose?

Do not use an unnumbered list for a required selection.

## Confirmation

Before a mutating operation requiring confirmation, render:

> **Confirmation required**
>
> This operation will modify the project.
>
> [fixed operation summary]
>
> Do you want to continue? **Yes / No**

For destructive uninstall confirmation:

> **Confirmation required**
>
> This operation will remove ARgentOS from the project and may restore displaced project files.
>
> Do you want to continue with uninstall? **Yes / No**

For session deletion:

> **Session data**
>
> ARgentOS can preserve the existing project sessions or delete them permanently.
>
> 1. **Keep sessions** — Preserve the existing ARgentOS project state.
> 2. **Delete sessions** — Permanently remove the preserved sessions and state.
>
> Which option do you choose?

## Progress

Progress messages must describe only an operation that has actually started.

Canonical form:

> **ARgentOS — [operation]**
>
> [one-line current action]

Do not report success before verification.

## Success

Canonical form:

> **ARgentOS — [operation] complete**
>
> Result: `[RESULT]`
>
> [verified summary]

## No-op

Canonical form:

> **ARgentOS — no changes made**
>
> Result: `[RESULT]`
>
> [reason]

## Failure

Canonical form:

> **ARgentOS — operation failed**
>
> Result: `[RESULT]`
>
> [verified failure reason]
>
> No further changes were made.

The final sentence must be omitted if changes were actually made before the failure. In that case report the verified partial state instead.

## Ambiguity

Canonical form:

> **ARgentOS — action required**
>
> [what could not be determined]
>
> [what information or decision is required]

Do not guess to resolve ambiguity.

## Project-root clarification

When the project root cannot be resolved:

> **Project root required**
>
> ARgentOS could not reliably determine the project root.
>
> Enter the project path where ARgentOS should operate.

## Installation scope

The scope question must use the exact scope options defined by the installation-method contract. The agent must not invent additional scopes.

## Installation method

The method question must use the exact method descriptions in `installation-methods.md`. The agent must not reorder, rename, or silently select methods.

## State display

Use the canonical lifecycle state identifiers exactly:

`NOT_INSTALLED`, `INSTALLED`, `INSTALLED_WITH_DRIFT`, `INCOMPLETE`, `UNINSTALLED_WITH_SESSIONS`, `BROKEN`, `UNKNOWN`.

A state identifier must not be replaced with a synonym in structured result output.

## Prohibited UX behavior

The skill must not:

- claim an operation succeeded because a command was issued;
- infer a successful repair without a post-operation check;
- hide a detected mutation;
- fabricate a version or path;
- silently choose a destructive option;
- silently delete preserved sessions;
- ask several unrelated decisions in one prompt;
- vary canonical labels for stylistic reasons.

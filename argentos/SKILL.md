---
name: argentos
description: "Operate ARgentOS explicitly in a host project: install, check, repair, update, uninstall, inspect version, and get help."
---

# ARgentOS

Use this skill only when the user explicitly invokes ARgentOS or asks to perform an ARgentOS operation.

Installing this skill with an Agent Skills manager is passive. It must not install, initialize, inspect, modify, or remove ARgentOS from a host project by itself.

## Contract

The skill is contract-driven. Do not improvise user-facing behavior.

Before handling a command, consult the relevant references:

- `references/commands.md` — command contracts and sequencing.
- `references/installation-methods.md` — installation methods.
- `references/lifecycle.md` — lifecycle states and transitions.
- `references/check-contract.md` — deterministic state detection.
- `references/layout.md` — filesystem ownership, backup, and restore.
- `references/project-adapter-template.md` — generated root adapter.
- `references/ux.md` — canonical user-facing text and interaction rules.
- `references/dialogues.md` — canonical end-to-end interaction flows.
- `references/output-contract.md` — result and state identifiers.
- `references/errors.md` — error and clarification identifiers.
- `references/scripts-contract.md` — deterministic script interfaces.

The UX, output, error, lifecycle, layout, check, dialogue, command, and script references are normative. If a situation is not covered, do not invent behavior; stop and request the missing information.

## Commands

- `/argentos install`
- `/argentos check`
- `/argentos doctor`
- `/argentos update`
- `/argentos uninstall`
- `/argentos version`
- `/argentos help`

If `/argentos` is invoked without a command, show the canonical command menu and ask which operation the user wants. Do not perform an operation automatically.

## Safety rules

- Resolve the project root before any project operation.
- Never guess a project path.
- `check`, `version`, and `help` are read-only.
- Never mutate before the command's required confirmation.
- Never silently select an installation method.
- Never silently delete preserved sessions.
- Never report success before post-operation verification.
- Never claim that no changes were made when a mutation partially occurred.
- Prefer the deterministic scripts in `scripts/` for filesystem and Git mutations.

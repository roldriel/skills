---
name: argentos
description: Operate ARgentOS explicitly in a host project: install, check, repair, update, uninstall, inspect version, and get help.
---

# ARgentOS

Use this skill only when the user explicitly invokes ARgentOS or asks to perform an ARgentOS operation.

Installing this skill with an Agent Skills manager is passive. It must not install, initialize, inspect, modify, or remove ARgentOS from a host project by itself.

## Commands

- "/argentos install" — install ARgentOS into a project.
- "/argentos check" — inspect the current ARgentOS state without modifying anything.
- "/argentos doctor" — diagnose and repair detected ARgentOS problems.
- "/argentos update" — update an existing ARgentOS installation.
- "/argentos uninstall" — remove ARgentOS, with explicit confirmation and a choice about preserved sessions.
- "/argentos version" — report the relevant ARgentOS version.
- "/argentos help" — show command usage and available operations.

Invoking "/argentos" without a command must not perform an operation. Show the available commands and ask the user what they want to do.

## Interaction rules

ARgentOS should not assume that the user already understands Git, installation methods, repository layout, or ARgentOS internals.

When an operation requires a technical choice, explain each available option briefly before asking the user to choose.

Before a mutating operation, explain what will change and obtain confirmation when the command requires it.

In particular:

- "check" is read-only.
- "doctor" must warn that it will make system/project changes before repairing.
- "update" must warn that it will make system/project changes before updating.
- "uninstall" must first confirm that the user wants to uninstall, then ask whether preserved sessions should be kept or deleted.

## Project resolution

When an ARgentOS command operates on a project, first try to resolve the project root from the environment in which the agent is running.

If the project root cannot be resolved reliably, do not guess. Ask the user for the project path or where ARgentOS should be installed.

The canonical ARgentOS location inside a project is always:

"<project-root>/.argentos"

The location is not a user-configurable ARgentOS root.

## Install behavior

"/argentos install" must inspect the current project state before deciding what to do. It should perform the equivalent of a "check" first.

If ARgentOS is absent, present the available installation scopes and installation methods, with a short explanation of each option, before modifying anything.

The installation source is the "dist" branch of the ARgentOS repository:

"roldriel/argentos"

The selected installation method determines how the "dist" payload is brought into "<project-root>/.argentos/".

If an existing ARgentOS installation, preserved sessions, an incomplete installation, or another actionable state is detected, explain the state and offer the appropriate available action instead of blindly reinstalling.

## Safety boundary

Do not make project changes merely because the skill is installed or discovered.

Do not silently choose an installation method, installation scope, destructive cleanup, or session deletion on behalf of the user.

For the detailed command contracts, installation methods, lifecycle states, and filesystem layout, consult the corresponding reference files.

# ARgentOS Commands

This document defines the initial user-facing contract for ARgentOS commands.

## install

Installs ARgentOS into a host project.

Before installation:

1. Resolve the project root.
2. Run a check of the current ARgentOS state.
3. If the project is already installed, partially installed, previously uninstalled with preserved sessions, or otherwise actionable, explain the detected state and offer the appropriate actions.
4. If a fresh installation is appropriate, ask for the installation scope and then the installation method.
5. Explain each available option before asking the user to choose.
6. Explain the changes that will be made before performing them.

The installation source is "roldriel/argentos", branch "dist".

The canonical project location is "<project-root>/.argentos".

## check

Read-only diagnostic operation.

It must inspect the project and report the detected ARgentOS state without changing files, Git configuration, sessions, or project metadata.

The check should distinguish at least:

- not installed;
- installed and healthy;
- installed with drift or detected problems;
- incomplete installation;
- uninstalled with preserved sessions;
- broken or inconsistent state;
- unknown or ambiguous state.

## doctor

Diagnoses and repairs ARgentOS problems.

Before making repairs, explain that the operation will modify the project/system and summarize the intended repair actions.

After repair, verify the resulting state with a new check.

## update

Updates an existing ARgentOS installation.

Before making changes:

1. Determine the current state and installed version.
2. Explain what will be changed.
3. Warn that the operation modifies the project/system.
4. Obtain the required confirmation.
5. Update using the installation method already configured for the installation.
6. Preserve adopter-local configuration and persistent state according to the lifecycle contract.
7. Verify the resulting state.

## uninstall

Removes ARgentOS from the project.

Before making changes:

1. Explain what will be removed or restored.
2. Ask the user to confirm the uninstall.
3. Ask whether preserved sessions should be kept or deleted.
4. Perform the selected cleanup/restoration.
5. Verify the resulting state.

The original adopter artifacts displaced during installation must be handled according to the backup/layout contract; they must not be silently discarded.

## version

Report the ARgentOS version relevant to the current project or installed payload.

If there is no installed project context, report that clearly rather than inventing an installed version.

## help

Show the available commands and a concise description of each.

Help must not modify the project.

## bare invocation

"/argentos" without a command is equivalent to requesting interactive help.

It must:

1. Show the available commands.
2. Briefly describe what each command does.
3. Ask the user which operation they want.

It must not begin installation, inspection, repair, update, or uninstall automatically.

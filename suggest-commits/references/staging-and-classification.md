# Staging and Classification Rules

This document defines scope selection, breaking-change criteria, command generation, and folder-level staging.

It does not define workflow.

It does not define commit boundaries.

It is loaded lazily by Phases 6 and 10 of `SKILL.md`.

---

# Scope Selection

Determine scope using the following priority:

1. Domain ownership
2. Package name
3. Service name
4. Application name
5. No scope

Prefer no scope over a misleading scope.

Avoid generic scopes such as:

* core
* common
* shared
* helpers
* utils
* misc

unless they represent genuine project domains.

---

# Breaking Changes

A breaking change exists only when an external contract becomes incompatible.

Typical examples:

* public API changes
* public function signature changes
* CLI argument changes
* event payload changes
* schema changes requiring migration
* removal of supported configuration keys
* public SDK changes

Do not mark as breaking:

* internal refactors
* file moves
* test updates
* documentation updates
* implementation details

When a breaking change is detected:

* add ! to the title;
* explain impact and migration in the Pull Request;
* explain migration in release notes when the change is released.

Example:

```text
feat(auth)!: replace legacy token format
```

Commit bodies are prohibited.

---

# Command Generation

Map file status to suggested staging commands.

| Status | Suggested Command  |
| ------ | ------------------ |
| M      | git add <path>     |
| A      | git add <path>     |
| ??     | git add <path>     |
| D      | git rm <path>      |
| R      | git add <new-path> |
| U      | conflict           |

If a file is already staged and requires no additional action:

```text
(already staged)
```

may be used.

Never assume a rename requires git mv.

Git may already track renames.

---

# Folder-Level Staging

Default to file-level commands.

Use folder-level staging only when all conditions are true:

* all files belong to the same proposed commit
* no unrelated changed files exist under the folder
* no untracked files exist under the folder
* no conflicts exist
* no other proposed commit touches the folder

If any uncertainty exists:

use explicit file-level commands.

Safety is preferred over brevity.

# Branches

Long-lived branches:

```text
development
master
stable/X.Y.x
```

Temporary branches:

```text
feature/<name>
fix/<name>
hotfix/X.Y/<name>
refactor/<name>
docs/<name>
chore/<name>
```

Default bases:

```text
feature/*   → development
fix/*       → development
refactor/*  → development
docs/*      → development
chore/*     → development
hotfix/*    → stable/X.Y.x
```

A one-off hotfix without a stable branch may start from the exact affected release tag.

Temporary branch lifecycle:

```text
create → work → PR → merge → delete
```

Create `stable/X.Y.x` from the exact released state represented by its version tag, and only when independent maintenance is required.

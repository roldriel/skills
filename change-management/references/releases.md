# Releases

Use standard Semantic Versioning:

```text
MAJOR.MINOR.PATCH
```

- MAJOR: incompatible external/public contract.
- MINOR: one or more backward-compatible features.
- PATCH: backward-compatible bug fixes.

A MINOR release may contain multiple features.

Examples:

```text
1.2.0 → 1.3.0
1.3.0 → 1.3.1
1.3.1 → 1.4.0
1.4.0 → 2.0.0
```

Starting versions may be `0.1.0` or `1.0.0`; PATCH starts at zero.

Release flow:

```text
development → master → vX.Y.Z
```

The tag identifies the exact release commit and is immutable.

Create `stable/X.Y.x` only when that release line requires independent maintenance.

For hotfixes:

```text
stable/X.Y.x → hotfix/X.Y/<name> → stable/X.Y.x → vX.Y.Z → development
```

Without a stable branch, a one-off hotfix may start from the exact affected release tag.

Optionally use `roldriel/skills:github-releases` for GitHub Release operations.

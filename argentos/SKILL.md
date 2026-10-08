---
name: argentos
description: Minimal ARgentOS skill for understanding, bootstrapping, and testing ARgentOS in a host project.
---

# ARgentOS

Use this skill when the user asks about ARgentOS, its protocol layout, adoption, bootstrap, or related testing.

## Scope

This is an intentionally small bootstrap skill. It does not implement the ARgentOS installer or modify the host project.

## Behavior

When invoked:

1. Identify that the `argentos` skill is available.
2. Explain that this is a bootstrap/test implementation.
3. Do not install, modify, or generate ARgentOS files unless the user explicitly asks for that work and the required implementation is available.

## Current limitation

The skill is only a starting point for validating Agent Skills distribution and invocation. It does not yet contain scripts, references, or an adoption workflow.

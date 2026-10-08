# ARgentOS Project Layout

The canonical ARgentOS root is always:

"<project-root>/.argentos"

It is not configurable.

## Expected layout

After adoption, the project is expected to contain:

~~~
<project-root>/
├── AGENTS.md
└── .argentos/
    ├── AGENTS.md
    ├── features.toml
    ├── .agents/
    ├── .project/
    └── .backup/
        ├── _AGENTS.md
        ├── _agents/
        └── _gitignore
~~~

"_gitignore" exists only when the original project ".gitignore" was displaced as part of the agreed installation flow.

## Responsibilities

### ".argentos/.agents/"

The ARgentOS protocol payload.

When the selected installation method uses a repository representation, this is the payload location that is managed by that method.

### ".argentos/.project/"

Adopter/runtime state.

It may contain persistent project state and preserved sessions. It is not protocol payload and should be treated differently from ".agents/".

### ".argentos/features.toml"

Adopter-local configuration.

It configures local ARgentOS behavior and must not be treated as immutable protocol payload.

### ".argentos/.backup/"

Contains only adopter artifacts displaced by ARgentOS installation.

The original root "AGENTS.md" is moved here rather than merged with the ARgentOS-managed governance files.

The original root ".agents/" is moved to "_agents/".

The original ".gitignore" is moved to "_gitignore" only when the installation flow replaces it.

ARgentOS state, manifests, or unrelated generated data must not be placed in ".backup/" merely because they are internal to ARgentOS.

### "<project-root>/AGENTS.md"

The root project-facing ARgentOS adapter.

It is distinct from ".argentos/AGENTS.md" and should not contain the protocol payload itself.

## Installation boundary

The payload source is "roldriel/argentos" at "dist".

The distribution payload and adopter-local state/configuration must remain separate.

The installation method may change how ".argentos/.agents/" is represented, but it must not change the canonical ARgentOS root.

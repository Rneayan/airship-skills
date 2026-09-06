# Security and privacy

Agent skills can influence tools that read or change local data. Review SKILL.md and every bundled script before installation, and pin a trusted release when reproducibility matters.

## This repository

Obsidian Task Triage:

- reads Markdown files under a user-provided vault path;
- does not modify the vault;
- does not use the network;
- emits relative paths unless absolute paths are explicitly requested;
- can omit all task text and note paths with counts-only mode.

Output may still contain private task text. Never attach real output, vault files, or private configuration to a public issue.

Adaptive Korean Voice:

- analyzes only user-authored samples available in the current task or supplied explicitly for profiling;
- stores abstract style rules rather than raw messages;
- creates or updates files only in a user-selected local skills directory;
- refuses to overwrite an existing personal skill and keeps a backup before profile updates;
- does not use the network or third-party Python packages.

Voice profiles can still reveal preferences or working habits. Keep generated personal skills out of public repositories unless you have reviewed the profile and deliberately want to publish it.

## Reporting a problem

When GitHub private vulnerability reporting is available for this repository, use it for security issues. Otherwise, open a minimal public issue that contains no vault data and asks the maintainer to establish a private reporting channel.

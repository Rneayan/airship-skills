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

## Reporting a problem

When GitHub private vulnerability reporting is available for this repository, use it for security issues. Otherwise, open a minimal public issue that contains no vault data and asks the maintainer to establish a private reporting channel.

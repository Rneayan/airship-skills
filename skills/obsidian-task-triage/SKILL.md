---
name: obsidian-task-triage
description: Extract, classify, de-duplicate, and prioritize actionable deadlines and unchecked tasks from an Obsidian or Markdown vault. Use for daily or weekly planning, overdue-task reviews, deadline-risk checks, and workload reduction while excluding templates, reference checklists, and archives.
---

# Obsidian Task Triage

Turn scattered checkboxes into a small, evidence-backed action queue without editing the vault.

## Workflow

1. Locate the vault and read its applicable AGENTS.md or local operating rules when present.
2. Start with the read-only extractor. Use counts-only for a privacy-preserving baseline when the user has not asked to inspect task text.
3. Review source context for every overdue, due-soon, or proposed primary task. A checkbox can be a template field, research checklist, acceptance criterion, or live action.
4. De-duplicate obligations repeated in daily, weekly, project, and area notes. Prefer the canonical project or area note for context.
5. Apply references/triage-policy.md and adapt bucket labels to the user's language.
6. Limit the recommendation to one primary action and up to two secondary actions unless the user's current plan clearly supports more.
7. Treat all classifications as candidates. Explain uncertainty instead of turning every unchecked box into an obligation.

## Extractor

Run:

~~~bash
python3 scripts/extract_tasks.py \
  --vault "/path/to/vault" \
  --today 2026-09-05 \
  --format markdown
~~~

Use --summary-only to emit only overdue and next-14-day action candidates. Use --counts-only before reading task text when a structural baseline is sufficient.

The extractor returns relative paths by default. Use --include-absolute-paths only when the user explicitly needs absolute local paths in the output.

If the vault uses different folder names, read references/configuration.md and pass a local JSON configuration file with --config. Keep that file outside a public repository when it reveals personal structure.

## Boundaries

- Do not modify vault files, task managers, calendars, email, or other services unless the user explicitly asks for that change.
- Do not send, submit, pay, cancel, delete, or expose task contents automatically.
- Do not infer that an archived or completed task should be reopened.
- Do not assign medical, legal, or financial urgency beyond recorded deadlines and current authoritative evidence.
- Do not save real task output in the skill directory or a public repository.

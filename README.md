# Airship Skills

Practical, calm agent skills for solo creators — by Rneayan.

Airship Skills turns personal operating practices into portable Agent Skills. The design principles are simple:

- verify source context before drawing conclusions;
- keep destructive or external changes reviewable;
- prefer a small, defensible recommendation over an overwhelming list;
- keep personal data and configuration outside public skill packages.

## Available skill

### Obsidian Task Triage

Extracts and classifies Markdown checkbox tasks, then guides an agent to produce a focused daily or weekly plan.

- Read-only vault scanning
- Relative paths by default
- Counts-only privacy mode
- English and Korean deadline keywords
- Optional local configuration for custom vault structures
- No network calls or third-party Python packages

Compatible GitHub CLI versions can install it with:

~~~bash
gh skill install Rneayan/airship-skills obsidian-task-triage
~~~

The skill follows the open Agent Skills directory format and can also be copied into the skills directory used by a compatible agent.

## Repository layout

~~~text
skills/
  obsidian-task-triage/
    SKILL.md
    agents/openai.yaml
    scripts/extract_tasks.py
    references/
tests/
~~~

## Development

Run the synthetic-data tests:

~~~bash
python3 -m unittest discover -s tests -v
~~~

Validate the skill directory with a compatible Agent Skills validator before publishing.

## Privacy

This repository contains procedures and source code, not a personal Obsidian vault. Do not commit local configuration, extracted tasks, journal text, generated reports, or real vault fixtures.

The first public version is intentionally limited to a read-only skill. License terms will be selected before the first tagged release.

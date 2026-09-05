# Local configuration

Use a configuration file only when the vault's folder names or task syntax differ from the defaults. Store the file outside the public skill repository when its values reveal personal structure.

Pass the file with:

~~~bash
python3 scripts/extract_tasks.py \
  --vault "/path/to/vault" \
  --config "/path/to/private/task-triage.json"
~~~

The file must be a JSON object. Every field is optional; supplied values replace the corresponding defaults.

~~~json
{
  "project_markers": ["Work/Active Projects/"],
  "area_markers": ["Responsibilities/"],
  "resource_markers": ["Library/"],
  "archive_markers": ["Cold Storage/"],
  "template_markers": ["System/Templates/"],
  "journal_markers": ["Journal/Daily/"],
  "reference_markers": ["Reference/"],
  "skip_parts": [".git", ".obsidian", ".trash"],
  "priority_patterns": ["\\bP[123]\\b", "\\btop priority\\b"],
  "due_keywords": ["due", "deadline", "📅"],
  "historical_journal_days": 14
}
~~~

Marker matching is path-segment based. Regular expressions are allowed only in priority_patterns. The script validates unknown fields, value types, and invalid regular expressions before scanning the vault.

The script never writes to the vault and does not use the network. Its output can still contain private task text, so do not paste real output into public issues or commit it to a repository.

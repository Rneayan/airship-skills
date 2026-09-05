#!/usr/bin/env python3
"""Extract and heuristically classify Obsidian checkbox tasks without editing files."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path


DEFAULT_CONFIG = {
    "skip_parts": [".git", ".obsidian", ".trash", "node_modules"],
    "project_markers": ["Projects/", "Project/", "01_Project/"],
    "area_markers": ["Areas/", "Area/", "02_Area/"],
    "resource_markers": ["Resources/", "Resource/", "03_Resource/"],
    "archive_markers": ["Archive/", "Archives/", "04_Archive/"],
    "template_markers": ["Templates/", "Template/", "templates/"],
    "journal_markers": ["Daily/", "Journal/", "Journals/", "일지/"],
    "reference_markers": ["References/", "references/"],
    "priority_patterns": [
        r"\bP[123]\b",
        r"\btop priority\b",
        r"\bfirst thing\b",
        "첫 번째 할 것",
    ],
    "due_keywords": ["📅", "due", "deadline", "마감", "까지", "예정"],
    "historical_journal_days": 14,
}
LIST_CONFIG_FIELDS = {
    key for key, value in DEFAULT_CONFIG.items() if isinstance(value, list)
}
TASK_RE = re.compile(r"^\s*[-*]\s+\[([ xX/\-])\]\s+(.*)$")
DATE_RE = re.compile(r"(?<!\d)(20\d{2}-\d{2}-\d{2})(?!\d)")
MONTH_DAY_RE = re.compile(r"(?<!\d)(1[0-2]|0?[1-9])/(3[01]|[12]\d|0?[1-9])(?!\d)")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Read Obsidian checkbox tasks without modifying the vault."
    )
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--today", type=date.fromisoformat, default=date.today())
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument(
        "--config",
        type=Path,
        help="Optional local JSON file overriding folder markers and keywords",
    )
    parser.add_argument("--include-done", action="store_true")
    parser.add_argument(
        "--summary-only",
        action="store_true",
        help="Emit counts plus overdue and next-14-day candidates only",
    )
    parser.add_argument(
        "--counts-only",
        action="store_true",
        help="Emit category counts without task text or note paths",
    )
    parser.add_argument(
        "--include-absolute-paths",
        action="store_true",
        help="Include the vault root and absolute source paths in output",
    )
    return parser.parse_args()


def load_config(path: Path | None) -> dict:
    config = {
        key: list(value) if isinstance(value, list) else value
        for key, value in DEFAULT_CONFIG.items()
    }
    if path is None:
        return config

    data = json.loads(path.expanduser().read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("configuration must be a JSON object")

    unknown = sorted(set(data) - set(DEFAULT_CONFIG))
    if unknown:
        raise ValueError(f"unknown configuration keys: {', '.join(unknown)}")

    for key, value in data.items():
        if key in LIST_CONFIG_FIELDS:
            if not isinstance(value, list) or not all(
                isinstance(item, str) and item for item in value
            ):
                raise ValueError(f"{key} must be a list of non-empty strings")
        elif key == "historical_journal_days":
            if not isinstance(value, int) or value < 0:
                raise ValueError(
                    "historical_journal_days must be a non-negative integer"
                )
        config[key] = value

    for pattern in config["priority_patterns"]:
        try:
            re.compile(pattern)
        except re.error as exc:
            raise ValueError(f"invalid priority pattern {pattern!r}: {exc}") from exc
    return config


def markdown_files(vault: Path, skip_parts: set[str]):
    for path in vault.rglob("*.md"):
        if any(part in skip_parts for part in path.parts):
            continue
        if path.is_file():
            yield path


def contains_keyword(text: str, keyword: str) -> bool:
    if keyword.isascii() and keyword.isalpha():
        return bool(re.search(rf"\b{re.escape(keyword)}\b", text, re.I))
    return keyword.casefold() in text.casefold()


def find_due(
    text: str,
    default_year: int,
    due_keywords: list[str],
) -> date | None:
    matches = DATE_RE.findall(text)
    has_due_language = any(
        contains_keyword(text, keyword) for keyword in due_keywords
    )
    if matches and has_due_language:
        try:
            return date.fromisoformat(matches[0])
        except ValueError:
            return None
    month_day = MONTH_DAY_RE.search(text)
    if not month_day or not has_due_language:
        return None
    try:
        candidate = date(default_year, int(month_day.group(1)), int(month_day.group(2)))
        return candidate
    except ValueError:
        return None


def source_date(path: Path) -> date | None:
    daily = re.match(r"^(20\d{2}-\d{2}-\d{2})(?:\s|\.md$)", path.name)
    if daily:
        return date.fromisoformat(daily.group(1))
    weekly = re.match(r"^(20\d{2})-W(\d{2})\.md$", path.name)
    if weekly:
        year, week = map(int, weekly.groups())
        return date.fromisocalendar(year, week, 7)
    return None


def source_year(path: Path, today: date) -> int:
    match = re.search(r"(20\d{2})", path.name)
    return int(match.group(1)) if match else today.year


def path_matches(path: Path, markers: list[str]) -> bool:
    path_text = "/" + unicodedata.normalize("NFC", path.as_posix()).strip("/") + "/"
    normalized_markers = (
        "/" + unicodedata.normalize("NFC", marker).strip("/") + "/"
        for marker in markers
    )
    return any(marker in path_text for marker in normalized_markers)


def classify(
    path: Path,
    text: str,
    due: date | None,
    today: date,
    note_date: date | None,
    note_year: int,
    config: dict,
) -> tuple[str, list[str]]:
    reasons: list[str] = []
    reference_markers = (
        config["template_markers"]
        + config["resource_markers"]
        + config["archive_markers"]
        + config["reference_markers"]
    )
    if path_matches(path, reference_markers):
        reasons.append("reference or archive path")
        return "reference-checklist", reasons
    cleaned = re.sub(r"[*_`]", "", text).strip()
    if cleaned in {"P1:", "P2:", "P3:"}:
        reasons.append("empty priority prompt")
        return "reference-checklist", reasons
    if (
        path_matches(path, config["journal_markers"])
        and note_date
        and note_date
        <= today - timedelta(days=config["historical_journal_days"])
    ):
        reasons.append("historical journal checkbox")
        return "historical-checklist", reasons
    if path_matches(path, config["area_markers"]) and note_year < today.year:
        reasons.append("past-year Area checklist")
        return "historical-checklist", reasons
    if due:
        reasons.append("explicit due date")
        return "action", reasons
    if path_matches(path, config["project_markers"]):
        reasons.append("active Project path")
        return "action", reasons
    if path_matches(path, config["journal_markers"]) and any(
        re.search(pattern, text, re.I) for pattern in config["priority_patterns"]
    ):
        reasons.append("dated journal priority")
        return "action", reasons
    if path_matches(path, config["area_markers"]):
        reasons.append("Area checkbox requires context")
        return "needs-review", reasons
    reasons.append("uncategorized checkbox")
    return "needs-review", reasons


def collect(args: argparse.Namespace) -> dict:
    vault = args.vault.expanduser().resolve()
    if not vault.is_dir():
        raise ValueError(f"vault is not a directory: {vault}")
    config = load_config(args.config)
    tasks = []
    for path in sorted(markdown_files(vault, set(config["skip_parts"]))):
        relative = path.relative_to(vault)
        for line_number, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            match = TASK_RE.match(line)
            if not match:
                continue
            symbol, text = match.groups()
            done = symbol.lower() == "x" or symbol == "-"
            if done and not args.include_done:
                continue
            note_date = source_date(relative)
            note_year = source_year(relative, args.today)
            due = find_due(text, note_year, config["due_keywords"])
            category, reasons = classify(
                relative,
                text,
                due,
                args.today,
                note_date,
                note_year,
                config,
            )
            if done:
                category = "done"
            overdue = bool(due and due < args.today and not done)
            days_until_due = (due - args.today).days if due else None
            task = {
                "text": text,
                "status_symbol": symbol,
                "category": category,
                "relative_path": str(relative),
                "line": line_number,
                "due": due.isoformat() if due else None,
                "overdue": overdue,
                "days_until_due": days_until_due,
                "reasons": reasons,
            }
            if args.include_absolute_paths:
                task["path"] = str(path)
            tasks.append(task)
    counts = Counter(task["category"] for task in tasks)
    result = {
        "generated_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "today": args.today.isoformat(),
        "custom_config": args.config is not None,
        "counts": dict(counts),
        "tasks": tasks,
    }
    if args.include_absolute_paths:
        result["vault"] = str(vault)
    if args.summary_only:
        result["tasks"] = [
            task
            for task in tasks
            if task["category"] == "action"
            and (
                task["overdue"]
                or (
                    task["days_until_due"] is not None
                    and task["days_until_due"] <= 14
                )
            )
        ]
    if args.counts_only:
        result["tasks"] = []
    return result


def sort_key(task: dict):
    if task["overdue"]:
        bucket = 0
    elif task["days_until_due"] is not None and task["days_until_due"] <= 7:
        bucket = 1
    elif task["category"] == "action":
        bucket = 2
    elif task["category"] == "needs-review":
        bucket = 3
    else:
        bucket = 4
    return (bucket, task["due"] or "9999-12-31", task["relative_path"], task["line"])


def as_markdown(data: dict) -> str:
    lines = ["# Task triage extraction", "", f"- Today: {data['today']}"]
    for category, count in sorted(data["counts"].items()):
        lines.append(f"- {category}: {count}")
    current = None
    for task in sorted(data["tasks"], key=sort_key):
        heading = "overdue" if task["overdue"] else task["category"]
        if heading != current:
            lines.extend(["", f"## {heading}"])
            current = heading
        due = f" — due {task['due']}" if task["due"] else ""
        lines.append(
            f"- {task['text']}{due}  \n  `{task['relative_path']}:{task['line']}`"
        )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    try:
        data = collect(args)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        raise SystemExit(f"error: {exc}") from exc
    if args.format == "markdown":
        print(as_markdown(data))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

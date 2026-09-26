#!/usr/bin/env python3
"""Collect one day's vault activity for a daily journal (read-only).

Sources
  (D) AI work log  - entries headed `### YYYY-MM-DD [HH:mm] — Title (Agent)`
                     in a shared agent handoff note (optional, --handoff)
  (E) Vault notes  - Markdown notes created or modified on that local day

Usage
  python3 collect_day_activity.py --vault PATH [--handoff REL_PATH]
                                  [--date YYYY-MM-DD] [--tz-offset 9]

Nothing is written. Output is Markdown on stdout.
"""
import argparse
import os
import re
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone

SKIP_DIRS = {"journal", "일지", "attachments", "templates", "work", "history",
             "node_modules", "renders", "assets", "__pycache__"}
SKIP_FILES = {"AGENTS.md", "CLAUDE.md", "README.md", "BRIEF.md", "STORYBOARD.md",
              "design.md", "SKILL.md", "index.md"}


def nfc(text):
    # macOS may store Korean file names in NFD; compare in NFC.
    return unicodedata.normalize("NFC", text)


def short(text, limit=140):
    text = re.sub(r"\*\*", "", text).strip()
    match = re.match(r"(.+?[.다])(\s|$)", text)
    sentence = match.group(1) if match else text
    return sentence if len(sentence) <= limit else sentence[: limit - 1] + "…"


def handoff_entries(path, day):
    if not path or not os.path.exists(path):
        return []
    body = open(path, encoding="utf-8").read()
    entries = []
    for part in re.split(r"^### ", body, flags=re.M)[1:]:
        head, _, rest = part.partition("\n")
        m = re.match(r"(\d{4}-\d{2}-\d{2})(?:\s+(\d{1,2}:\d{2}))?\s*[—-]\s*(.+)", head.strip())
        if not m or m.group(1) != day:
            continue
        title, agent = m.group(3).strip(), ""
        am = re.search(r"\(([^()]*)\)\s*$", title)
        if am:
            agent, title = am.group(1), title[: am.start()].strip()
        fields = {}
        for line in rest.splitlines():
            fm = re.match(r"-\s*\*\*(.+?):\*\*\s*(.*)", line.strip())
            if fm:
                fields[fm.group(1).strip().lower()] = fm.group(2).strip()
        result = next((fields[k] for k in ("결과", "완료 내용", "결론", "result", "outcome") if k in fields), "")
        status = next((fields[k] for k in ("상태", "status") if k in fields), "")
        own = os.path.splitext(os.path.basename(path))[0]
        links = sorted(set(re.findall(r"\[\[([^\]|#]+)", rest)) - {own})
        entries.append({"time": m.group(2) or "", "title": title, "agent": agent,
                        "status": short(status, 60), "result": short(result, 160), "links": links})
    return entries


def created_of(path):
    try:
        head = open(path, encoding="utf-8").read(1500)
    except (OSError, UnicodeDecodeError):
        return ""
    m = re.search(r"^created:\s*['\"]?(\d{4}-\d{2}-\d{2})", head, flags=re.M)
    return m.group(1) if m else ""


def vault_changes(vault, day, tz, handoff):
    rows = []
    for root, dirs, files in os.walk(vault):
        dirs[:] = [d for d in dirs if not d.startswith(".") and nfc(d) not in SKIP_DIRS]
        for name in files:
            if not name.endswith(".md") or nfc(name) in SKIP_FILES:
                continue
            path = os.path.join(root, name)
            if handoff and os.path.abspath(path) == os.path.abspath(handoff):
                continue
            modified = datetime.fromtimestamp(os.path.getmtime(path), tz)
            created = created_of(path)
            same_day = modified.strftime("%Y-%m-%d") == day
            if same_day or created == day:
                rows.append((modified.strftime("%H:%M") if same_day else "?",
                             "created" if created == day else "modified",
                             nfc(os.path.relpath(path, vault))))
    return sorted(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--vault", required=True)
    parser.add_argument("--handoff", help="handoff note path, relative to the vault")
    parser.add_argument("--date")
    parser.add_argument("--tz-offset", type=float, default=9.0, help="hours from UTC (default 9, KST)")
    args = parser.parse_args()

    tz = timezone(timedelta(hours=args.tz_offset))
    day = args.date or datetime.now(tz).strftime("%Y-%m-%d")
    vault = os.path.abspath(args.vault)
    handoff = os.path.join(vault, args.handoff) if args.handoff else None

    entries = handoff_entries(handoff, day)
    changes = vault_changes(vault, day, tz, handoff)
    linked = {link for e in entries for link in e["links"]}

    print(f"# {day} activity (UTC{args.tz_offset:+g})\n")
    print("## (D) AI work log")
    if not entries:
        print("- none")
    for e in entries:
        who = f" ({e['agent']})" if e["agent"] else ""
        when = f"{e['time']} " if e["time"] else ""
        print(f"- {when}{e['title']}{who}")
        if e["status"]:
            print(f"\t- status: {e['status']}")
        if e["result"]:
            print(f"\t- result: {e['result']}")
        if e["links"]:
            print("\t- notes: " + ", ".join(f"[[{l}]]" for l in e["links"][:6]))

    print("\n## (E) Notes created or modified")
    if not changes:
        print("- none")
    groups = defaultdict(list)
    for row in changes:
        parts = row[2].split(os.sep)
        groups[os.sep.join(parts[:3]) if len(parts) > 3 else os.sep.join(parts[:-1]) or "."].append(row)
    for key, items in groups.items():
        times = [t for t, _, _ in items if t != "?"]
        span = f"{min(times)}~{max(times)}" if times else "time unknown"
        print(f"- {key}  [{span}, {len(items)}]")
        for t, kind, rel in items:
            name = os.path.splitext(os.path.basename(rel))[0]
            mark = " · linked to AI work" if name in linked else ""
            print(f"\t- {t} {kind} [[{name}]]{mark}")

    bursts = [m for m, c in Counter(t for t, _, _ in changes if t != "?").items() if c >= 15]
    if bursts:
        print(f"\n> Warning: many notes changed at {', '.join(bursts)} — possibly a sync event, not work.")
    print("\n> Note: only the last modification time survives, so backfills can miss notes edited again later.")


if __name__ == "__main__":
    main()

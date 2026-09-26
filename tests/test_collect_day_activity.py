import os
import subprocess
import sys
import tempfile
import time
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPOSITORY_ROOT / "skills" / "obsidian-journal" / "scripts" / "collect_day_activity.py"
KST = timezone(timedelta(hours=9))


class CollectDayActivityTests(unittest.TestCase):
    @staticmethod
    def write(vault: Path, relative: str, text: str, when: datetime) -> None:
        path = vault / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        stamp = when.timestamp()
        os.utime(path, (stamp, stamp))

    def run_script(self, vault: Path, day: str) -> str:
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--vault", str(vault), "--handoff", "Handoff.md", "--date", day],
            check=True, capture_output=True, text=True,
        ).stdout

    def test_collects_handoff_and_notes_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            day = datetime(2026, 9, 25, 14, 30, tzinfo=KST)
            self.write(vault, "Handoff.md",
                       "## History\n\n### 2026-09-25 — Synthetic promo video (Claude)\n\n"
                       "- **Status:** done.\n- **Result:** A 20 second synthetic cut. More detail.\n"
                       "- **Changed:** [[Promo notes]]\n\n### 2026-09-24 — Older task (Codex)\n", day)
            self.write(vault, "Projects/Promo/Promo notes.md", "synthetic\n", day)
            self.write(vault, "Projects/Class/Seminar memo.md", "synthetic\n", day + timedelta(hours=2))
            self.write(vault, "Projects/Promo/README.md", "tool file\n", day)
            self.write(vault, "일지/2026-09-25.md", "journal\n", day)
            self.write(vault, "Old/Other day.md", "synthetic\n", day - timedelta(days=3))
            before = {p: p.stat().st_mtime for p in vault.rglob("*.md")}

            out = self.run_script(vault, "2026-09-25")

            self.assertIn("Synthetic promo video (Claude)", out)
            self.assertIn("result: A 20 second synthetic cut.", out)
            self.assertNotIn("Older task", out)
            self.assertIn("[[Promo notes]] · linked to AI work", out)
            self.assertIn("16:30 modified [[Seminar memo]]", out)
            self.assertNotIn("README", out)
            self.assertNotIn("Other day", out)
            self.assertNotIn("2026-09-25]]", out)
            self.assertEqual(before, {p: p.stat().st_mtime for p in vault.rglob("*.md")})

    def test_created_field_catches_later_edited_note(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            later = datetime(2026, 9, 27, 10, 0, tzinfo=KST)
            self.write(vault, "Notes/Plan.md", "---\ncreated: 2026-09-25\n---\n", later)
            out = self.run_script(vault, "2026-09-25")
            self.assertIn("? created [[Plan]]", out)


if __name__ == "__main__":
    unittest.main()

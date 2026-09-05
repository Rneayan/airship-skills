import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = (
    REPOSITORY_ROOT
    / "skills"
    / "obsidian-task-triage"
    / "scripts"
    / "extract_tasks.py"
)


class ExtractTasksTests(unittest.TestCase):
    def run_script(self, vault: Path, *extra_args: str) -> dict:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--vault",
                str(vault),
                "--today",
                "2026-09-05",
                *extra_args,
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        return json.loads(completed.stdout)

    @staticmethod
    def write_note(vault: Path, relative: str, text: str) -> None:
        path = vault / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def test_default_output_is_read_only_and_path_private(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            self.write_note(
                vault,
                "Projects/Launch.md",
                "- [ ] Send the synthetic brief due 2026-09-06\n",
            )
            self.write_note(
                vault,
                "Archive/Old.md",
                "- [ ] Historical example checkbox\n",
            )
            self.write_note(
                vault,
                "Notes.md",
                "- [ ] Undated example item\n",
            )

            data = self.run_script(vault)

            self.assertNotIn("vault", data)
            self.assertEqual(data["counts"]["action"], 1)
            self.assertEqual(data["counts"]["reference-checklist"], 1)
            self.assertEqual(data["counts"]["needs-review"], 1)
            self.assertTrue(data["tasks"])
            self.assertTrue(
                all("path" not in task for task in data["tasks"])
            )
            self.assertEqual(
                data["tasks"][0]["relative_path"],
                "Archive/Old.md",
            )

    def test_counts_only_omits_task_text_and_paths(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory)
            self.write_note(
                vault,
                "Projects/Private Example.md",
                "- [ ] Synthetic task due 2026-09-04\n",
            )

            data = self.run_script(vault, "--counts-only")

            self.assertEqual(data["tasks"], [])
            self.assertEqual(data["counts"]["action"], 1)
            self.assertNotIn("vault", data)

    def test_local_config_can_replace_project_markers(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory) / "vault"
            vault.mkdir()
            self.write_note(
                vault,
                "ClientWork/Example.md",
                "- [ ] Prepare a synthetic artifact\n",
            )
            config = Path(directory) / "task-triage.json"
            config.write_text(
                json.dumps({"project_markers": ["ClientWork/"]}),
                encoding="utf-8",
            )

            data = self.run_script(vault, "--config", str(config))

            self.assertTrue(data["custom_config"])
            self.assertEqual(data["tasks"][0]["category"], "action")


if __name__ == "__main__":
    unittest.main()

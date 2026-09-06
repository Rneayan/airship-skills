import importlib.util
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "skills"
    / "adaptive-korean-voice"
    / "scripts"
    / "create_personal_skill.py"
)
SPEC = importlib.util.spec_from_file_location("create_personal_skill", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


PROFILE_ONE = """---
profile_version: 1
profile_name: 테스트 사용자
status: personalized
created: 2026-09-06
sample_scope: conversation
---

# 한국어 말투 프로필

## 핵심 목소리
- 짧고 담백한 해요체

## 윤문 경계
- 사실을 추가하지 않는다.
"""

PROFILE_TWO = PROFILE_ONE.replace("짧고 담백한", "차분하고 명료한")


class PersonalSkillGeneratorTest(unittest.TestCase):
    def test_rejects_path_like_name(self):
        with self.assertRaises(SystemExit):
            MODULE.validate_name("../outside")

    def test_rejects_incomplete_profile(self):
        with tempfile.TemporaryDirectory() as temp:
            profile = Path(temp) / "profile.md"
            profile.write_text("# 아직 작성 중\n", encoding="utf-8")
            with self.assertRaises(SystemExit):
                MODULE.read_profile(profile)

    def test_create_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            profile = root / "profile.md"
            profile.write_text(PROFILE_ONE, encoding="utf-8")
            args = Namespace(
                name="korean-voice-test-user",
                display_name='Test "Korean" Voice',
                profile_name="테스트 사용자",
                profile=profile,
                output_dir=root / "skills",
            )

            MODULE.create_skill(args)
            target = args.output_dir / args.name
            self.assertTrue((target / "SKILL.md").is_file())
            self.assertEqual(
                (target / "references" / "voice-profile.md").read_text(encoding="utf-8"),
                PROFILE_ONE,
            )
            self.assertIn(
                'display_name: "Test \\"Korean\\" Voice"',
                (target / "agents" / "openai.yaml").read_text(encoding="utf-8"),
            )
            with self.assertRaises(SystemExit):
                MODULE.create_skill(args)

    def test_update_keeps_backup(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            first = root / "first.md"
            first.write_text(PROFILE_ONE, encoding="utf-8")
            create_args = Namespace(
                name="korean-voice-test-user",
                display_name="Test Korean Voice",
                profile_name="테스트 사용자",
                profile=first,
                output_dir=root / "skills",
            )
            MODULE.create_skill(create_args)

            second = root / "second.md"
            second.write_text(PROFILE_TWO, encoding="utf-8")
            target = create_args.output_dir / create_args.name
            MODULE.update_profile(Namespace(profile=second, target=target))

            profile_path = target / "references" / "voice-profile.md"
            self.assertEqual(profile_path.read_text(encoding="utf-8"), PROFILE_TWO)
            self.assertEqual(
                profile_path.with_suffix(".md.bak").read_text(encoding="utf-8"),
                PROFILE_ONE,
            )


if __name__ == "__main__":
    unittest.main()

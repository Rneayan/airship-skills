#!/usr/bin/env python3
"""Create or update a profile-backed personal Korean voice skill."""

from __future__ import annotations

import argparse
import re
import shutil
import sys
import tempfile
from datetime import date
from pathlib import Path


NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_PROFILE_MARKERS = (
    "profile_version:",
    "status: personalized",
    "# 한국어 말투 프로필",
    "## 핵심 목소리",
    "## 윤문 경계",
)


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def read_profile(path: Path) -> str:
    if not path.is_file():
        fail(f"프로필 파일을 찾을 수 없습니다: {path}")
    content = path.read_text(encoding="utf-8").strip() + "\n"
    missing = [marker for marker in REQUIRED_PROFILE_MARKERS if marker not in content]
    if missing:
        fail("프로필 형식이 완성되지 않았습니다. 누락: " + ", ".join(missing))
    if "{{" in content or "TODO" in content:
        fail("프로필에 미완성 플레이스홀더가 남아 있습니다.")
    return content


def validate_name(name: str) -> None:
    if len(name) > 63 or not NAME_RE.fullmatch(name):
        fail("스킬 이름은 63자 이하의 소문자·숫자·하이픈만 사용할 수 있습니다.")


def yaml_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")


def render(template: str, values: dict[str, str]) -> str:
    rendered = template
    for key, value in values.items():
        rendered = rendered.replace(f"__{key}__", value)
    unresolved = sorted(set(re.findall(r"__[A-Z_]+__", rendered)))
    if unresolved:
        fail("템플릿 치환 실패: " + ", ".join(unresolved))
    return rendered


def create_skill(args: argparse.Namespace) -> None:
    validate_name(args.name)
    profile = read_profile(args.profile.resolve())
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / args.name
    if target.exists() or target.is_symlink():
        fail(f"대상이 이미 있습니다. 덮어쓰지 않았습니다: {target}")

    skill_root = Path(__file__).resolve().parents[1]
    template_dir = skill_root / "assets" / "personal-skill-template"
    values = {
        "SKILL_NAME": args.name,
        "DISPLAY_NAME": yaml_quote(args.display_name),
        "PROFILE_NAME": yaml_quote(args.profile_name or args.display_name),
        "CREATED": date.today().isoformat(),
    }

    temp_dir = Path(tempfile.mkdtemp(prefix=f".{args.name}-", dir=output_dir))
    try:
        (temp_dir / "agents").mkdir()
        (temp_dir / "references").mkdir()
        for source_name, destination in (
            ("SKILL.md.tmpl", temp_dir / "SKILL.md"),
            ("openai.yaml.tmpl", temp_dir / "agents" / "openai.yaml"),
        ):
            template = (template_dir / source_name).read_text(encoding="utf-8")
            destination.write_text(render(template, values), encoding="utf-8")

        (temp_dir / "references" / "voice-profile.md").write_text(profile, encoding="utf-8")
        shutil.copy2(skill_root / "references" / "natural-korean.md", temp_dir / "references")
        shutil.copy2(skill_root / "LICENSE", temp_dir / "LICENSE")
        temp_dir.rename(target)
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise

    print(target)


def update_profile(args: argparse.Namespace) -> None:
    profile = read_profile(args.profile.resolve())
    target = args.target.resolve()
    skill_md = target / "SKILL.md"
    destination = target / "references" / "voice-profile.md"
    if not skill_md.is_file() or not destination.is_file():
        fail(f"개인용 말투 스킬 구조가 아닙니다: {target}")

    backup = destination.with_suffix(destination.suffix + ".bak")
    shutil.copy2(destination, backup)
    destination.write_text(profile, encoding="utf-8")
    print(destination)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="프로필을 내장한 개인용 한국어 말투 스킬을 안전하게 생성하거나 갱신합니다."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="새 개인용 스킬 생성")
    create.add_argument("--name", required=True, help="소문자·숫자·하이픈 스킬 이름")
    create.add_argument("--display-name", required=True, help="UI에 표시할 이름")
    create.add_argument("--profile-name", help="프로필 안에서 부를 이름")
    create.add_argument("--profile", required=True, type=Path, help="확정된 voice-profile.md")
    create.add_argument("--output-dir", required=True, type=Path, help="스킬 상위 디렉터리")
    create.set_defaults(func=create_skill)

    update = subparsers.add_parser("update", help="기존 개인용 스킬의 프로필만 갱신")
    update.add_argument("--profile", required=True, type=Path, help="새 voice-profile.md")
    update.add_argument("--target", required=True, type=Path, help="기존 개인용 스킬 디렉터리")
    update.set_defaults(func=update_profile)
    return parser


def main() -> None:
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

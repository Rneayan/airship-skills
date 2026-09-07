# ⚓ Airship Skills

**1인 크리에이터·스튜디오 운영을 위한 Agent Skills 모음**
*Practical, calm agent skills for solo creators — by [비행선선장 / Airship Captain](https://github.com/Rneayan), who runs a solo AI-assisted animation studio and teaches motion graphics.*

🇰🇷 한국어 (아래) · 🇺🇸 [English](#english)

사용자별 한국어 말투, 비즈니스 커뮤니케이션, 외주 견적, 메일·일정·할일 운영, 옵시디언 일지와 태스크 정리까지 — 개발자가 아닌 **혼자 일하는 창작자**가 매일 굴리는 워크플로를 스킬로 옮겼습니다. 실제로 옵시디언 볼트와 AI 에이전트를 오가며 다듬은 규칙들이고, 개인 정보·단가·계정 ID는 `{{placeholder}}`로 비워 두었으니 본인 환경에 맞게 채워 쓰면 됩니다.

[Agent Skills 오픈 표준](https://agentskills.io)(`SKILL.md`)을 따르므로 Claude Code, Claude 앱(Cowork), Codex, Cursor 등 SKILL.md를 읽는 어떤 에이전트에서도 쓸 수 있습니다.

## 설치

Claude Code — 전체를 플러그인으로:

```
/plugin marketplace add Rneayan/airship-skills
/plugin install airship@airship-skills
```

GitHub CLI(호환 버전) — 스킬 하나만:

```bash
gh skill install Rneayan/airship-skills obsidian-task-triage
```

`adaptive-korean-voice`만 설치하려면:

```bash
npx skills add Rneayan/airship-skills@adaptive-korean-voice
```

또는 원하는 스킬 폴더를 `~/.claude/skills/` (전역), 프로젝트의 `.claude/skills/`, 혹은 사용하는 에이전트의 스킬 디렉터리에 복사하면 됩니다.

## 스킬 목록

| 스킬 | 언제 쓰나 | 연동 |
|------|-----------|------|
| [`adaptive-korean-voice`](skills/adaptive-korean-voice/SKILL.md) | 대화 표본을 1~2차로 살펴 사용자별 한국어 말투 프로필과 독립된 개인 스킬을 생성. 원문은 저장하지 않고 이후 답변·설명·윤문에 조용히 적용 | 로컬 파일 |
| [`korean-business-message`](skills/korean-business-message/SKILL.md) | 이메일·카톡·Slack 메시지를 **내 말투 그대로** 최소 교정. 채널별 포맷 규칙, 반복 교정 패턴, 수정 내역 명시 | — |
| [`b2b-quote-analysis`](skills/b2b-quote-analysis/SKILL.md) | 영상·애니메이션 외주 문의 분석 → 누락 정보 체크리스트 → 모듈형 견적. "촉박한 일정은 할인 사유가 아니라 할증 사유" | — |
| [`mail-reply-draft`](skills/mail-reply-draft/SKILL.md) | 미회신 업무 메일의 답장을 Gmail 임시보관함에 준비. 발송 금지, `[확인 필요]` 표기, 서명 수동 삽입 | Gmail |
| [`morning-briefing`](skills/morning-briefing/SKILL.md) | 마감·일정·새 메일을 한 번에, **압박감 없는 톤**으로. "오늘은 이거 하나만 해도 충분하다" | Todoist · Google Calendar · Gmail |
| [`todoist-organizer`](skills/todoist-organizer/SKILL.md) | 백로그 정리·통합·보류 이관. Todoist MCP 도구의 검증된 필터와 이동 순서 | Todoist |
| [`obsidian-journal`](skills/obsidian-journal/SKILL.md) | 일간·주간·월간 일지를 직접기록 + 캘린더 + Todoist 완료 기록 3곳 대조로 보완. 덮어쓰기 절대 금지 | Obsidian · Google Calendar · Todoist |
| [`obsidian-task-triage`](skills/obsidian-task-triage/SKILL.md) | 볼트의 체크박스 태스크를 **읽기 전용**으로 추출·분류·중복 제거해 하루/한 주의 작은 실행 큐로. counts-only 프라이버시 모드, 한/영 마감 키워드, 외부 패키지·네트워크 없음 | Obsidian (Python 스크립트 동봉) |
| [`ai-contest-db`](skills/ai-contest-db/SKILL.md) | AI 영상 공모전·영화제 DB를 옵시디언 노트 + 현황 시트로 관리. "원문 확인 전 제작 착수 금지" | Obsidian |
| [`korea-creator-cashflow`](skills/korea-creator-cashflow/SKILL.md) | 한국 1인 법인·창작자의 법인/개인 분리, 월 최소 필요금액, 13주 현금흐름, 세금·보험·부채와 프로젝트 공헌이익 점검 | Obsidian · Spreadsheet |
| [`korea-partnership-outreach`](skills/korea-partnership-outreach/SKILL.md) | 대학·공공기관·브랜드·AI CPP 맞춤 제안, 영문 지원문, 2회 이하 후속 연락과 상태표. 모든 발송은 건별 승인 | Obsidian · Email |
| [`korea-meeting-to-actions`](skills/korea-meeting-to-actions/SKILL.md) | 한국어 회의 메모를 사실·결정·약속·실행·미해결 질문으로 분리하고 PARA 프로젝트 기록에 연결 | Obsidian |
| [`dual-agent-instruction-sync`](skills/dual-agent-instruction-sync/SKILL.md) | Claude·Codex 등 에이전트를 2개 이상 함께 쓸 때 공용 지침(`AGENTS.md`)과 스킬을 단일 원본으로 유지. 스킬 3계층 분류, 심링크 배포, 지침 로딩 검증 마커, 인수인계 규칙 | 로컬 파일 (zsh 스크립트 동봉) |

## 설계 원칙

**말투는 사용자 것.** 교정 스킬은 재작성이 아니라 최소 수정입니다. 개인화 스킬은 원문 대신 추상화된 프로필만 로컬에 저장하고, 분석 과정은 요청받을 때만 보여 줍니다.
**실행보다 제안.** 메일은 초안까지만, 파일 이동은 동의 후, 대량 변경은 확인 후. 볼트는 읽기만 하고 고치지 않습니다. 스킬이 사용자 대신 결정하지 않습니다.
**근거 먼저.** 결론을 내기 전에 원문 맥락을 확인합니다. 기록이 없으면 "기록 없음", 확실치 않은 숫자는 `[확인 필요]`. 추측으로 채우지 않습니다.
**압박은 정확한 수준으로.** 브리핑·일지·트리아지는 전체 개수를 나열하지 않고, 핵심 1개 + 보조 2개 정도의 작고 방어 가능한 추천을 냅니다.
**개인 데이터는 스킬 밖에.** 볼트 경로, 계정 ID, 서명, 단가표는 플레이스홀더나 로컬 설정 파일로 두고 공개 패키지에 넣지 않습니다.

## 파생 스킬과 출처

`korea-creator-cashflow`, `korea-partnership-outreach`, `korea-meeting-to-actions`는 비행선선장이 처음부터 독자 개발한 원본이라고 주장하지 않습니다. 공개된 `financial-modeling`, `outreach-manager`, `meeting-notes` 스킬을 참고해 한국의 1인 창작자·스튜디오 운영에 맞게 재설계한 파생 스킬입니다. `adaptive-korean-voice`는 DaleSeo의 한국어 Humanizer와 KatFishNet 연구를 참고하되, 문맥 기반 판정·조용한 적용·사용자별 프로필 생성 방식으로 다시 설계했습니다. 원본 저장소·고정 커밋·라이선스·주요 변경점은 각 스킬의 `references/attribution.md`와 `LICENSE`에 보존했습니다.

## 저장소 구조

```text
.claude-plugin/        # Claude Code 플러그인·마켓플레이스 매니페스트
skills/
  <skill-name>/
    SKILL.md           # 스킬 본문 (필수)
    agents/            # 에이전트별 메타데이터 (선택)
    scripts/           # 동봉 스크립트 (선택)
    references/        # 참고 문서 (선택)
tests/                 # 스크립트 테스트 (합성 데이터만)
```

## 커스터마이징

각 SKILL.md의 `{{vault}}`, `{{INBOX_PROJECT_ID}}`, 서명 블록의 `{{이름}}` 등을 본인 값으로 바꾸세요. Todoist ID는 스킬 안내대로 `find-projects` / `find-sections`로 한 번 조회하면 됩니다. `obsidian-task-triage`는 폴더 구조가 다르면 `references/configuration.md`대로 로컬 JSON 설정을 `--config`로 넘기면 되고, 그 설정 파일은 저장소에 올리지 마세요.

`adaptive-korean-voice`는 설치 뒤 “내 한국어 말투를 분석해서 개인 스킬로 만들어 줘”라고 요청하면 됩니다. 현재 대화에 표본이 충분하면 바로 프로필을 만들고, 부족할 때만 짧은 표본 요청과 A/B 확인을 합쳐 최대 두 차례 조사합니다. 생성된 개인 프로필은 공개 저장소가 아니라 사용자의 로컬 스킬 폴더에만 둡니다.

## 개발

동봉 스크립트 테스트:

```bash
python3 -m unittest discover -s tests -v
```

## 프라이버시

이 저장소에는 절차와 소스 코드만 있습니다. 로컬 설정, 추출된 태스크, 일지 본문, 생성된 리포트, 실제 볼트 픽스처는 커밋하지 마세요. 보안 관련 안내는 [SECURITY.md](SECURITY.md)를 참고하세요.

## 만든 사람

**비행선선장 (Airship Captain)** — AI 활용 애니메이션 스튜디오 운영, 대학에서 모션그래픽 강의, 그리고 그 과정을 유튜브 [비행선 선장의 작업실](https://www.youtube.com/@AirshipCaptain)에 기록합니다.

이슈·PR 환영합니다. 한국어로 일하는 크리에이터의 워크플로 스킬이 더 쌓이면 좋겠습니다.

## License

[MIT](LICENSE)

---

<a id="english"></a>

# English

**Agent Skills for solo creators and one-person studios.**

Personalized Korean voice, business communication, freelance quoting, mail/calendar/task operations, Obsidian journaling and task triage — the daily workflows of a **non-developer creator working alone**, turned into portable skills. These rules were refined in real use, moving between an Obsidian vault and AI agents. Personal data, price tables and account IDs are left as `{{placeholder}}` so you can fill in your own.

Everything follows the open [Agent Skills](https://agentskills.io) standard (`SKILL.md`), so the skills work in Claude Code, the Claude app (Cowork), Codex, Cursor, or any agent that reads SKILL.md. Most skill bodies are written in Korean, because that is the language these workflows run in — but the structure, checklists and boundaries translate directly, and any capable agent will follow them regardless of the language you speak to it in.

## Install

Claude Code — the whole set as a plugin:

```
/plugin marketplace add Rneayan/airship-skills
/plugin install airship@airship-skills
```

GitHub CLI (compatible versions) — a single skill:

```bash
gh skill install Rneayan/airship-skills obsidian-task-triage
```

To install only `adaptive-korean-voice`:

```bash
npx skills add Rneayan/airship-skills@adaptive-korean-voice
```

Or copy any skill folder into `~/.claude/skills/` (global), your project's `.claude/skills/`, or the skills directory of the agent you use.

## Skills

| Skill | What it does | Integrations |
|-------|--------------|--------------|
| [`adaptive-korean-voice`](skills/adaptive-korean-voice/SKILL.md) | Studies one or two rounds of Korean conversation samples, then creates an independent personal voice skill. Stores abstract style rules, not raw samples, and silently applies them to answers, explanations and rewrites | Local files |
| [`korean-business-message`](skills/korean-business-message/SKILL.md) | Minimal-touch proofreading of Korean email / KakaoTalk / Slack messages that **keeps your own voice**. Channel-specific formatting rules, recurring fix patterns, and an explicit change log | — |
| [`b2b-quote-analysis`](skills/b2b-quote-analysis/SKILL.md) | Analyze a video/animation outsourcing inquiry → missing-info checklist → modular quote. "A tight deadline is a rush premium, not a discount" | — |
| [`mail-reply-draft`](skills/mail-reply-draft/SKILL.md) | Prepare replies to unanswered work email as Gmail drafts. Never sends, marks uncertain facts as `[확인 필요]` (needs confirmation), inserts your signature manually | Gmail |
| [`morning-briefing`](skills/morning-briefing/SKILL.md) | Overdue items, today's calendar and new mail in one **low-pressure** briefing. "Doing just this one thing today is enough" | Todoist · Google Calendar · Gmail |
| [`todoist-organizer`](skills/todoist-organizer/SKILL.md) | Backlog cleanup, merging and parking. Proven filters and move order for the Todoist MCP tools | Todoist |
| [`obsidian-journal`](skills/obsidian-journal/SKILL.md) | Fill daily / weekly / monthly journals by cross-checking three sources: hand-written log, calendar, Todoist completions. Never overwrites | Obsidian · Google Calendar · Todoist |
| [`obsidian-task-triage`](skills/obsidian-task-triage/SKILL.md) | **Read-only** extraction, classification and de-duplication of checkbox tasks into a small action queue for the day or week. Counts-only privacy mode, English + Korean deadline keywords, no network, no third-party packages | Obsidian (bundled Python script) |
| [`ai-contest-db`](skills/ai-contest-db/SKILL.md) | Maintain an AI video contest / film-festival database as Obsidian notes plus a status sheet. "No production before the official call is verified" | Obsidian |
| [`korea-creator-cashflow`](skills/korea-creator-cashflow/SKILL.md) | Separate corporate and personal cash, calculate monthly minimums and a 13-week runway, and track Korean tax/insurance/debt plus project contribution margins | Obsidian · Spreadsheet |
| [`korea-partnership-outreach`](skills/korea-partnership-outreach/SKILL.md) | Tailored outreach for Korean institutions, brands and AI CPPs, with English application copy, a two-follow-up cap and per-message approval | Obsidian · Email |
| [`korea-meeting-to-actions`](skills/korea-meeting-to-actions/SKILL.md) | Turn Korean meeting notes into facts, decisions, commitments, actions and open questions linked to PARA project records | Obsidian |
| [`dual-agent-instruction-sync`](skills/dual-agent-instruction-sync/SKILL.md) | Keep one source of truth for shared instructions (`AGENTS.md`) and skills across two or more agents (Claude Code, Codex). Three-tier skill ownership, symlink distribution, a load-verification marker, and handoff rules | Local files (bundled zsh script) |

## Design principles

**The voice is the user's.** Proofreading skills edit minimally instead of rewriting. The adaptive voice skill stores only an abstract local profile and shows its analysis only when asked.
**Propose, don't execute.** Mail stops at drafts, file moves wait for consent, bulk changes ask first. Vaults are read, never modified. A skill never decides on the user's behalf.
**Evidence first.** Verify source context before drawing conclusions. No record → "no record"; uncertain number → `[needs confirmation]`. Never fill gaps with guesses.
**Pressure at the accurate level.** Briefings, journals and triage don't enumerate everything; they return a small, defensible recommendation — one primary action, up to two secondary.
**Personal data stays outside the skill.** Vault paths, account IDs, signatures and price tables live in placeholders or local config, never in the public package.

## Derived skills and attribution

`korea-creator-cashflow`, `korea-partnership-outreach`, and `korea-meeting-to-actions` are not presented as wholly original works by Airship Captain. They are adaptations of the public `financial-modeling`, `outreach-manager`, and `meeting-notes` skills, redesigned for Korean solo creators and small studios. `adaptive-korean-voice` draws on DaleSeo's Korean Humanizer and the KatFishNet research, but redesigns them around contextual signals, silent application, and local per-user profiles. Each derived skill preserves the upstream repository, pinned commit, license, and a prominent change notice in `references/attribution.md` and `LICENSE`.

## Repository layout

```text
.claude-plugin/        # Claude Code plugin + marketplace manifests
skills/
  <skill-name>/
    SKILL.md           # the skill itself (required)
    agents/            # per-agent metadata (optional)
    scripts/           # bundled scripts (optional)
    references/        # supporting docs (optional)
tests/                 # script tests (synthetic data only)
```

## Customizing

Replace `{{vault}}`, `{{INBOX_PROJECT_ID}}`, the `{{name}}` fields in the signature block, and similar placeholders in each SKILL.md. Todoist IDs can be looked up once with `find-projects` / `find-sections` as the skill describes. For `obsidian-task-triage`, pass a local JSON config via `--config` (see `references/configuration.md`) if your folder structure differs — and keep that file out of the repository.

After installing `adaptive-korean-voice`, ask it to analyze your Korean voice and create a personal skill. It uses the current conversation when enough material is available; otherwise it limits onboarding to a short sample request and one A/B calibration. The generated profile stays in your local skills directory and is never added to this public repository.

## Development

```bash
python3 -m unittest discover -s tests -v
```

## Privacy

This repository contains procedures and source code only. Do not commit local configuration, extracted tasks, journal text, generated reports or real vault fixtures. See [SECURITY.md](SECURITY.md).

## Author

**Airship Captain (비행선선장)** — runs a solo AI-assisted animation studio, teaches motion graphics at university, and documents the process on YouTube at [비행선 선장의 작업실](https://www.youtube.com/@AirshipCaptain).

Issues and PRs are welcome — especially more workflow skills for creators who work in Korean.

## License

[MIT](LICENSE)

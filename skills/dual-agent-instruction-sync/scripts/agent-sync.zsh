#!/bin/zsh
# 공용 에이전트 지침·스킬 동기화 스크립트
# 지침 원본 : AGENTS.md (스크립트가 있는 작업 폴더 루트)
# 스킬 원본 : ~/.agents/skills
# 연결 대상 : Claude Code(~/.claude/skills), Codex(~/.codex/skills)
set -euo pipefail

workspace_dir=${0:A:h}
agents_file="$workspace_dir/AGENTS.md"
claude_file="$workspace_dir/CLAUDE.md"
shared_skill_root="${HOME}/.agents/skills"

typeset -A agent_skill_roots
agent_skill_roots=(
  claude "${HOME}/.claude/skills"
  codex  "${HOME}/.codex/skills"
)
agent_names=(${(ok)agent_skill_roots})

operation=${1:---check}
case "$operation" in
  --check|--apply|--verify) ;;
  --verify-claude) operation='--verify' ;;   # 이전 이름 호환
  *)
    print -u2 "Usage: $0 [--check|--apply|--verify]"
    print -u2 "  --check   현재 연결 상태만 점검 (변경 없음)"
    print -u2 "  --apply   누락되거나 어긋난 심볼릭 링크를 만들거나 고침"
    print -u2 "  --verify  --check 후 스킬 무결성과 Claude 지침 로딩까지 확인"
    exit 2
    ;;
esac

fail_count=0
note_fail() { print -u2 "FAIL: $1"; (( fail_count += 1 )); }

# ---------------------------------------------------------------- 지침 원본 점검
if [[ ! -r "$agents_file" ]]; then
  print -u2 "FAIL: AGENTS.md를 읽을 수 없음: $agents_file"
  exit 1
fi
if [[ ! -r "$claude_file" ]]; then
  print -u2 "FAIL: CLAUDE.md를 읽을 수 없음: $claude_file"
  exit 1
fi

claude_nonblank=$(sed '/^[[:space:]]*$/d' "$claude_file")
if [[ "$claude_nonblank" != '@AGENTS.md' ]]; then
  note_fail "CLAUDE.md는 '@AGENTS.md' 한 줄만 있어야 함 (현재: '${claude_nonblank}')"
else
  print "OK: CLAUDE.md가 AGENTS.md를 중복 없이 불러옴"
fi

verification_marker=$(sed -n 's/.*Agent sync verification marker: `\([^`]*\)`.*/\1/p' "$agents_file" | head -n 1)
if [[ -z "$verification_marker" ]]; then
  note_fail "AGENTS.md에 검증 마커가 없음"
else
  print "OK: AGENTS.md 검증 마커 확인 ($verification_marker)"
fi

# ------------------------------------------------------------- 공용 스킬 목록화
if [[ ! -d "$shared_skill_root" ]]; then
  print -u2 "FAIL: 공용 스킬 루트가 없음: $shared_skill_root"
  exit 1
fi

typeset -A skill_sources
while IFS= read -r -d '' skill_file; do
  skill_dir=${skill_file:h}
  rel=${skill_dir#$shared_skill_root/}
  [[ "$rel" == .* || "$rel" == */.* ]] && continue   # .system 등 내부 디렉터리 제외
  skill_name=${skill_dir:t}
  if [[ -n "${skill_sources[$skill_name]-}" && "${skill_sources[$skill_name]}" != "$skill_dir" ]]; then
    print -u2 "FAIL: 공용 스킬 이름 충돌 '$skill_name'"
    print -u2 "  ${skill_sources[$skill_name]}"
    print -u2 "  $skill_dir"
    exit 1
  fi
  skill_sources[$skill_name]="$skill_dir"
done < <(find -L "$shared_skill_root" -type f -name SKILL.md -print0)

if (( ${#skill_sources} == 0 )); then
  print -u2 "FAIL: $shared_skill_root 아래에 SKILL.md가 하나도 없음"
  exit 1
fi
# 원본이 사라진 공용 스킬 링크 감지 (find -L 은 끊어진 링크를 조용히 건너뛴다)
for entry in "$shared_skill_root"/*(N); do
  if [[ -L "$entry" && ! -e "$entry" ]]; then
    note_fail "공용 스킬 원본이 없음 (끊어진 링크): ${entry:t} -> $(readlink "$entry")"
  fi
done

skill_names=(${(ok)skill_sources})
print "INFO: 공용 스킬 ${#skill_sources}개 — ${skill_names}"

# ------------------------------------------------------------------- 링크 동기화
for agent_name in $agent_names; do
  agent_root=${agent_skill_roots[$agent_name]}

  if [[ ! -d "$agent_root" ]]; then
    if [[ "$operation" == '--apply' ]]; then
      mkdir -p "$agent_root"
      print "CREATED: $agent_root"
    else
      note_fail "[$agent_name] 스킬 디렉터리가 없음: $agent_root (--apply로 생성)"
      continue
    fi
  fi

  for skill_name in $skill_names; do
    source_dir=${skill_sources[$skill_name]}
    link_path="$agent_root/$skill_name"

    # 이미 올바르게 연결됨
    if [[ -L "$link_path" && "${link_path:A}" == "${source_dir:A}" ]]; then
      print "OK: [$agent_name] $skill_name"
      continue
    fi

    # 다른 곳을 가리키는 심볼릭 링크 -> --apply에서 교체
    if [[ -L "$link_path" ]]; then
      if [[ "$operation" == '--apply' ]]; then
        rm "$link_path"
        ln -s "$source_dir" "$link_path"
        print "RELINKED: [$agent_name] $skill_name -> $source_dir"
      else
        note_fail "[$agent_name] $skill_name 링크가 다른 곳을 가리킴: ${link_path:A}"
      fi
      continue
    fi

    # 실제 파일/폴더가 자리를 차지함 -> 자동 삭제하지 않는다
    if [[ -e "$link_path" ]]; then
      note_fail "[$agent_name] $skill_name 자리에 실제 파일/폴더가 있음. 수동 확인 필요: $link_path"
      continue
    fi

    # 비어 있음 -> 새로 연결
    if [[ "$operation" == '--apply' ]]; then
      ln -s "$source_dir" "$link_path"
      print "LINKED: [$agent_name] $skill_name -> $source_dir"
    else
      note_fail "[$agent_name] $skill_name 링크 없음: $link_path (--apply로 생성)"
    fi
  done
done

# ----------------------------------------------------------------------- 무결성
if [[ "$operation" == '--verify' ]]; then
  for agent_name in $agent_names; do
    agent_root=${agent_skill_roots[$agent_name]}
    for skill_name in $skill_names; do
      skill_md="$agent_root/$skill_name/SKILL.md"
      if [[ ! -r "$skill_md" ]]; then
        note_fail "[$agent_name] $skill_name 링크를 통해 SKILL.md를 읽을 수 없음"
        continue
      fi
      declared_name=$(sed -n 's/^name:[[:space:]]*//p' "$skill_md" | head -n 1)
      if [[ -z "$declared_name" ]]; then
        print "WARN: [$agent_name] $skill_name SKILL.md에 name 프론트매터가 없음"
      fi
    done
  done
  print "OK: 링크를 통한 SKILL.md 읽기 검증 완료"

  if command -v claude >/dev/null 2>&1; then
    if claude_reply=$(cd "$workspace_dir" && claude -p --tools "" --permission-prompts none --no-session-persistence \
      "From the project instructions already loaded at session start, return only the value labelled 'Agent sync verification marker'. Do not use tools and do not explain." 2>/dev/null); then
      claude_reply=${claude_reply//$'\r'/}
      claude_reply=${claude_reply//$'\n'/}
      if [[ "$claude_reply" == "$verification_marker" ]]; then
        print "OK: Claude Code가 CLAUDE.md를 통해 AGENTS.md를 로드함 ($claude_reply)"
      else
        note_fail "Claude 응답 '$claude_reply' — 기대값 '$verification_marker'"
      fi
    else
      note_fail "Claude Code 실행 실패. 'claude auth status' 확인 필요"
    fi
  else
    print "SKIP: claude CLI가 PATH에 없어 지침 로딩 검증을 건너뜀"
  fi

  print "NOTE: Codex는 세션 시작 시 AGENTS.md를 자동으로 읽는다."
  print "      Codex 세션에서 마커 '$verification_marker'를 직접 물어 확인할 것."
fi

# ------------------------------------------------------------------------- 결과
if (( fail_count > 0 )); then
  print -u2 "FAIL: 처리해야 할 항목 ${fail_count}건"
  exit 1
fi
print "DONE: 공용 스킬 ${#skill_sources}개가 에이전트 ${#agent_skill_roots}개(${agent_names})에 연결됨"

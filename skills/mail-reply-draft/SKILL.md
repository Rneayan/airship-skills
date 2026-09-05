---
name: mail-reply-draft
description: Gmail 미회신 업무 메일의 회신 초안을 임시보관함에 준비하는 스킬. "메일 초안 써줘", "답장 준비해줘", "미회신 메일 확인해서 초안 만들어줘", "이 메일 답장해줘" 같은 요청이 오면 반드시 이 스킬을 따를 것. 서명 수동 삽입, [확인 필요] 표기, 발송 금지 등 확립된 절차가 있다. 메시지 문장 교정만 원하는 경우는 korean-business-message 스킬 사용.
---

# 메일 회신 초안 준비

미회신 업무 메일에 대한 답장 초안을 Gmail 임시보관함에 준비한다. **절대 직접 발송하지 않는다** — 초안만 만들고 사용자가 검토 후 직접 보낸다.

## 1. 대상 선별

- 최근 3~5일 내 받은 메일 중 아직 회신하지 않은 스레드 (search_threads).
- **포함:** 업무 관련 발신자 — 협업사, 거래처, 프리랜서, 학교/대학원 행정, 프로젝트 관계자.
- **제외:** 뉴스레터, 광고, 자동알림, 영수증, 세무/홈택스 자동 메일.
- 이미 회신 완료된 스레드는 건드리지 않는다. 마지막 메시지가 상대의 단순 감사 인사라도 미회신 상태면 짧은 답례 초안 후보가 될 수 있다.

## 2. 초안 작성 규칙

1. 스레드 전체 맥락(get_thread)을 읽고 요청/질문을 파악한다.
2. 짧고 정중한 답장을 쓴다. **언어는 스레드를 따른다** — 대화가 영어로 진행됐으면 영어로.
3. 사실 확인이 필요한 내용(마감일·금액·작업 범위·일정 등 확신 없는 숫자·약속)은 임의로 채우지 않고 **"[확인 필요: 000]"** 형태로 남긴다. 노트·이전 대화에서 이미 확인된 사실은 반영한다.
4. **서명을 본문 끝에 직접 붙인다.** Gmail 서명은 API로 만든 초안에 자동으로 붙지 않는다. create_draft 호출 시 htmlBody에 (본문 + 서명 HTML), body에 (본문 + 서명 텍스트).
5. create_draft에 replyToMessageId로 원본 메시지 ID를 넣어 임시보관함에 저장한다.

## 3. 완료 보고

초안 몇 건을 어떤 상대/제목으로 준비했는지 한두 줄. 없으면 "준비할 회신 없음"으로 짧게. 제외한 메일을 장황하게 나열하지 않는다.

## 서명 설정

아래 두 블록의 `{{ }}` 자리를 본인 정보로 채워서 사용한다. 이 스킬을 복제해 쓰는 경우 서명은 반드시 본인 것으로 교체할 것.

### 서명 HTML (htmlBody 끝에 그대로 삽입)

```html
<br><div dir="ltr"><div style="color:rgb(34,34,34)">{{슬로건 1행}}</div><div style="color:rgb(34,34,34)">{{슬로건 2행}}</div><div style="color:rgb(34,34,34)"><br></div><div style="color:rgb(34,34,34)"><hr style="margin-bottom:12px;color:rgb(242,243,244);border:0.5px solid"><strong><span style="font-size:16px">{{이름}} </span></strong><strong><span style="font-size:14px">{{직함}}</span></strong><br><span style="color:rgb(117,121,131);font-size:14px">{{회사명}}</span><br><strong><span style="color:rgb(74,77,85);font-size:14px">t </span></strong><span style="color:rgb(117,121,131);font-size:14px">{{전화}} </span><strong><span style="color:rgb(74,77,85);font-size:14px">e </span></strong><a href="mailto:{{이메일}}"><span style="color:rgb(117,121,131);font-size:14px">{{이메일}}</span></a><br><strong><span style="color:rgb(74,77,85);font-size:14px">a </span></strong><span style="color:rgb(117,121,131);font-size:14px">{{주소}}</span><br><strong><span style="color:rgb(74,77,85);font-size:14px">w </span></strong><a href="{{웹사이트}}"><span style="color:rgb(117,121,131);font-size:14px">{{웹사이트}}</span></a></div></div>
```

### 서명 텍스트 (body 플레인 끝에 그대로 삽입)

```
{{슬로건 1행}}
{{슬로건 2행}}
------------------------------
{{이름}} {{직함}}
{{회사명}}
t {{전화}}  e {{이메일}}
a {{주소}}
w {{웹사이트}}
```

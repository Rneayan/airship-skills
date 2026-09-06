# 출처와 변형 범위

## 참고한 공개 작업

- Dale Seo, [`DaleSeo/korean-skills`](https://github.com/DaleSeo/korean-skills), `humanizer` v1.6.0
  - 고정 커밋: [`ae12ba27982ebeff03b46dc738365aaa34260d9a`](https://github.com/DaleSeo/korean-skills/commit/ae12ba27982ebeff03b46dc738365aaa34260d9a)
  - 라이선스: MIT, Copyright (c) 2026 Dale Seo
- Park et al., [KatFishNet: Detecting LLM-Generated Korean Text through Linguistic Feature Analysis](https://aclanthology.org/2025.acl-long.1030/), ACL 2025

## 가져온 생각

- 한국어 AI 출력에서 쉼표, 띄어쓰기, 품사 다양성, 번역투와 반복 구조를 함께 살핀다는 문제 설정
- 숫자·고유명사·인과관계·부정·직접 인용·격식 수준을 확인하는 의미 보존 점검
- 이미 자연스러운 문장을 억지로 고치지 않는 과교정 방지 원칙

## 새로 설계한 부분

- 단어 한 번만으로 AI 문장이라고 판정하지 않고 반복과 문맥을 함께 본다.
- 자연도 점수와 분석표를 기본 출력에서 제거하고 내부 점검으로 돌린다.
- 1~2차 표본 조사로 사용자별 말투 프로필을 만들고, 원문 대신 추상화된 규칙만 저장한다.
- 공개 기반 스킬을 직접 바꾸지 않고 별도의 개인 스킬을 생성해 업데이트와 개인 설정을 분리한다.
- 대화체, 정보 정리, 외부 발송문을 나눠 한 가지 말투가 모든 장르를 덮지 않게 한다.

KatFishNet은 인간과 LLM의 한국어 텍스트를 구분하는 연구다. 이 연구의 탐지 성능이 곧 윤문 품질을 입증하는 것은 아니므로, 본 스킬은 모든 문체 규칙이 과학적으로 검증됐다고 주장하지 않는다.

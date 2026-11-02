---
name: check-delegate-codex
description: CHECK 위키 작업을 Codex CLI(codex exec)에 안전하게 위임하는 절차와 브리프 템플릿. 큰 구현·반복 작업을 병렬로 맡길 때 사용.
---

# Codex 위임 절차

## 호출
```
codex exec -C <워크트리> -s workspace-write -o <scratch>/codex-last.txt - < <scratch>/prompt.txt > <scratch>/codex-log.txt 2>&1
```
Bash 도구의 `run_in_background`로 실행하고 완료 알림을 기다린다(폴링 금지). 프롬프트·로그는 스크래치패드에 둔다.

## 브리프 템플릿 (한국어)
1. 먼저 읽을 파일(`docs/CHECK-WIKI-HANDOFF.md` 등)과 최상위 목적: 사용자가 원하는 콘텐츠를 얻을 화면·기능을 사람/AI가 찾게 하는 것
2. 작업 항목을 A/B/C로 번호화, 각 항목에 **측정 가능한 완료 기준**(수치·테스트)
3. 제약: `uv run --offline --no-sync` 사용, git commit/push/reset/checkout 금지, 수정 허용/금지 파일 명시, 임계치 낮추기 금지
4. 최종 보고 형식: 변경 파일, 전후 수치, 테스트 결과, 해결 못한 것과 사유

## 병렬 작업 규칙
- Codex가 수정 중인 파일(빌더·검색·생성물)을 다른 작업자가 건드리지 않게 **파일 단위로 영역을 분리**한다. 겹치면 서브에이전트는 `isolation: "worktree"`로 보낸다.
- 개인정보가 있는 원본(비식별 전 CRM)은 외부 모델에 보내지 않는다(정책 확인 전). 이미 레포에 있는 가공본만 위임 가능.

## 결과 검수 (위임 후 반드시)
- Codex의 보고를 믿지 않고 직접: `git status`로 의도한 파일만 바뀌었는지, 테스트 재실행, 정답 ID 실존 검증, 지표 재측정.
- 기존 파일이 의도치 않게 바뀌었으면 사용자에게 보고하고 되돌릴지 묻는다.

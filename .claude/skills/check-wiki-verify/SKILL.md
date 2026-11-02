---
name: check-wiki-verify
description: CHECK 위키 전체 검증(테스트·빌드·validate·검색 평가·누출 게이트)을 정해진 순서로 실행하고 결과를 표로 보고한다. 푸시나 커밋 전, 생성물을 바꾸는 작업 뒤에 사용.
---

# CHECK 위키 검증 절차

이 레포에서 "검증", "푸시 전 확인", "빌드 확인"이 필요할 때 아래 순서로 실행한다. 중간 실패 시 뒤 단계를 계속 돌리되 실패를 숨기지 않고 표에 남긴다.

## 환경
- Node 22.16.0: `eval "$(fnm env)"; fnm use 22.16.0` (fnm 설치됨, `.node-version` 참고)
- Python: 항상 `uv`. 기본 `uv run`이 macOS 네트워크 초기화로 실패하면 `uv run --offline --no-sync …`를 쓴다.

## 순서
1. `git status -sb` — 시작 상태 기록(수정된 생성물이 있으면 기록만 하고 되돌리지 않는다)
2. `uv run pytest -q -p no:cacheprovider`
3. `uv run python scripts/build_check_wiki.py --json` — **content/·knowledge/ 생성물을 바꾼다.** 끝나면 `git diff --stat`로 변경 파일을 보고한다. 되돌릴지는 사용자에게 묻는다.
4. `uv run python scripts/validate_check_wiki.py --json` — `ok:true`, 미해결 관계 ID 0, 과대 문서 0
5. `uv run python scripts/eval_check_wiki.py --json` — 있으면 실행. 지표(recall@1/3/5, MRR)를 직전 값과 비교
6a. `uv run python scripts/build_tr_registry.py --check` — TR 마스터 목록 I11·I12 검증(위반 0)
6b. `uv run python scripts/build_ontology_nodes.py --check` — 항목·함수 노드 검증(위반 0)
6c. `uv run python scripts/build_ontology_edges.py --check` — 엣지 검증(I1·I5·I7, 위반 0)
6. `uv run python scripts/leak_gate.py` — 현재 레포 데이터에서는 위반이 다수라 실패가 정상(미해결). 일반화 산출물 검증에는 `--pair ORIG=PUBLIC`로 사용
6d. `uv run python scripts/ingest_observations.py --check` — `observations/screens/`에 관찰 파일이 있으면 검증·판정(무효 0)
7. 웹앱: `python scripts/build_help_app.py --json` 후 `python -m unittest discover -s scripts/tests -p "test_help_app.py"` (CI와 동일)

## 보고 형식
| 단계 | 결과 | 비고 |
단계별 통과/실패와 핵심 수치, 생성물 변경 파일 수, 새로 생긴 경고. 실패는 출력 원문 일부를 첨부한다.

## 하지 말 것
- 임계치를 낮춰서 통과시키지 않는다. 지표 하락은 원인을 보고한다.
- 사용자 확인 없이 푸시하거나 생성물을 되돌리지 않는다.
- 공개 산출물에 사례 원문(회사명·전화번호·`PID복원`·`row:`)이 있으면 중단하고 보고한다.

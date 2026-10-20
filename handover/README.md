# handover 우편함 (lib-ops ↔ stock-market)

이 폴더는 kcm(「한국 자본시장의 이해」) 위키 게시 작업을 위해 lib-ops 쪽 세션과 주고받는 공용 우편함이다. 서로의 저장소를 직접 고치지 않는다.

## 읽을 순서 (stock-market 세션)
1. `2026-10-20-kcm-wiki-publish-request.md` — **작업 요구서**(무엇을 게시하나, 데이터 위치, 게시 금지 경로, 형식 메모, 게시 방법론, 공개 방침)
2. `2026-10-20-kcm-work-split.md` — **작업 분리**(누가 무엇을 하나), **게시 테스트 절차와 피드백 형식**
3. `2026-10-20-kcm-wiki-publish-prompt.txt` — 시작 프롬프트(작가가 세션에 붙여 넣는 글)
4. `2026-10-20-kcm-book-to-wiki.md` — 배경 메모(대체됨), `structure.before-2026-10-20.json` — 구조 교정 전 백업

## 첫 작업
**로컬 시험 빌드(게시 테스트).** push·레포 생성·배포는 하지 않고, 결과와 데이터 쪽 문제는 이 폴더에 `feedback-YYYY-MM-DD-<주제>.md` 로 적는다. lib-ops 세션이 읽고 데이터를 고쳐 **델타**(갱신 알림)로 알린다.

## 주의
- git `origin` 이 Quartz 원본(`jackyzha0/quartz`)이다 — 거기로 push 하지 않는다. 게시 저장소는 GitHub 계정 `ilovejsbach` 의 별도 새 레포이며, 만드는 일은 작가 확인 뒤에 한다.
- 데이터 루트 `/Users/koscom/workspace/vault-finance/wiki-korean-capital-markets/` 는 읽기 전용이다.
- 이 맥의 node 는 v20.17 이고 디스크 여유가 8GB 뿐이다: Node 22 는 전역 설정을 바꾸지 않는 임시 방식으로, 큰 임시 파일은 정리한다.

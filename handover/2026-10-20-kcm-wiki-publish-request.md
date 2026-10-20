# 작업 요구서: 「한국 자본시장의 이해」(kcm) 책별 위키 게시 (외부 GitHub + 내부 반입 GitLab)

- 받는 곳: **stock-market 프로젝트** (`/Users/koscom/workspace/stock-market`, Quartz 5 기반 정적 사이트)
- 보내는 곳: lib-ops `kcm-book-to-wiki` 워크트리 (금융 위키 프로그램 `domains/finance`, 볼트 `vault-finance`)
- 작성: 2026-10-20. **상태: 보낼 수 있는 상태.**
- 근거: 작가 방침(결정 D-054) — 게시는 이 프로젝트가 하지 않는다. 데이터가 준비되면 stock-market에 작업 요구를 보낸다. 게시 **방법론**은 ai-weekly(`ai-newsletter-automation`)가 쓰는 두 갈래 — 외부 GitHub 게시와 내부 반입·GitLab 게시 — 를 참고한다. `ai-newsletter-automation`은 방법론의 참고 사례일 뿐 요청 대상이 아니다.

## 1. 요청 한 줄
kcm 책별 독립 위키(문서 373개, 목차 포함 374개)와 보완층, 2부 후보를 Quartz 사이트로 만들어 **외부(공개 GitHub)**에 게시하고, **내부망 반입용 패키지(델타 zip)**를 만들어 내부 GitLab에 게시할 수 있게 해 주세요. 이 프로젝트(lib-ops)는 데이터만 준비합니다.

## 2. 가져갈 데이터 (읽기 전용, lib-ops가 소유)
루트: `/Users/koscom/workspace/vault-finance/wiki-korean-capital-markets/`

| 경로 | 내용 | 게시 |
|---|---|---|
| `wiki/index.md`, `wiki/chapters/kcm/` (21), `wiki/concepts/` (269), `wiki/institutions/` (49), `wiki/regulations/` (28), `wiki/metrics/` (5), `wiki/books/kcm.md` | 인쇄본 근거 위키 | 예 |
| `supplements/timeline.md`, `by-chapter.md`, `by-page.md`, `README.md` | 책 이후(2021-01~2026-10) 변화·추가를 날짜별로 모은 보완층 | 예 |
| `supplements/part2/themes.md`, `README.md`, `unassigned.md` | 「2부」 후보 주제 38개와 연결 기록 | 예 |
| `supplements/author-check.md`, `corrections.md`, `candidates.md`, `held.md`, `*.jsonl`, `config.json`, `coverage.json`, `stats.json` | 작업용 점검 문서와 기계 판독 원자료 | **아니오** |
| `wiki/_meta/`, `wiki/CLAUDE.md`, `work/`, `books/` | 사전·실행 기록(내부 경로 포함), 작업 규칙, 중간 산출물, 정본 OCR 텍스트·이미지로 이어지는 링크 | **절대 게시 금지** |

## 3. stock-market 쪽 현재 상태에서 알아 둘 것
- 지금 `content/`가 비어 있는 Quartz 5 기본 복제본이다. `quartz.config.default.yaml`은 기본값(pageTitle "Quartz 5", baseUrl 예시, 분석 도구 plausible, locale en-US, 구글 폰트)이다 — 한국어 사이트에 맞게 설정해야 한다.
- **git `origin`이 Quartz 원본(`github.com/jackyzha0/quartz`)이다. 거기로 push하면 안 된다.**
- **게시 저장소는 ai-weekly 사이트와 같은 GitHub 계정(`ilovejsbach`)의 별도 레포로 만든다.** 기존 `ilovejsbach/ai-newsletter-site`에 섞지 않고 stock-market 전용 새 레포를 쓴다(ai-weekly 사이트가 `ilovejsbach.github.io/ai-newsletter-site/`로 서빙되듯 이 위키도 같은 계정의 Pages로 서빙된다). 새 레포를 만들고 `origin`을 그쪽으로 바꾸는 일은 작가 확인을 받고 stock-market에서 한다. 레포 이름과 Pages 주소는 요구 사항이 아니라 stock-market 재량이다.
- 계정의 인증 정보(토큰 등)는 이 요구서에 없다. stock-market이 기존 방식(`gh auth` 등 로컬 로그인)으로 쓰며 파일·로그에 남기지 않는다.
- `stock-market/handover/`에 이전 메모가 있다(구조 정본 교정 백업 포함). 이번 요구서가 우선한다.

## 4. 형식 메모 (렌더에 필요한 것)
- 문서 간 링크는 `[[slug]]`, `[[slug|표시]]`(Quartz 위키링크로 처리 가능). 폴더로 유형 구분(concepts/institutions/regulations/metrics/chapters). 별칭은 frontmatter `aliases`. slug는 책 전체에서 고유하다.
- 출처 토큰 `[src: kcm pN]`은 **원본 PDF의 쪽 번호**다(인쇄 쪽 아님). 그대로 두면 대괄호 글자로 보이므로 "원본 p.N" 같은 작은 각주 표시로 바꾸길 권한다. 정본 이미지·OCR 본문으로 링크하지 않는다.
- 문서 상태는 전부 `status: draft`(사람 검토 전). Quartz의 `draft: true`(게시 제외)와는 다른 필드이니 혼동하지 말 것. 사이트에 "초안" 표시를 권한다.
- 보완층 카드는 책 값과 갱신 값을 나란히 보이고 출처는 URL이 있는 1차 자료다. 신뢰도(높음/중간/낮음)와 변화 유형(계획→확정, 제도 변경, 범위 확장)을 보여 준다. **시행 예정·입법예고는 "예정"으로 적혀 있다 — 확정처럼 바꾸지 말 것.**
- 표·그림·수식 없음. 한글 본문.
- 공개 게시이므로 사이트 전체에 저작권 고지와 출처(책 서지: 엄경식, 『한국 자본시장의 이해』, 한울엠플러스, 2023)를 표시하고 "독자 이해를 위한 요약·정리이며 원문 전재가 아님"을 밝히길 권한다. 문구는 stock-market이 정한다.
- **게시 방법론(ai-weekly 참고, 읽기 전용으로 `/Users/koscom/workspace/ai-newsletter-automation/CLAUDE.md`의 publish 절과 `docs/delivery/`를 읽을 것):**
  1. **외부 — 공개 GitHub:** 발행 머신에서 정적 사이트를 만들어(외부 리소스 0건 검증, 폰트는 로컬 서빙) 공개 저장소에 push, GitHub Pages로 서빙한다. 배포 전 dry-run으로 출력만 확인한다.
  2. **내부 — 반입 후 GitLab:** 같은 내용을 **내부망 반입용 델타 zip**으로 만든다(변경분만, 목차 포함). zip은 GitHub 릴리스로 올려 인터넷 PC에서 내려받고, 사람이 내부망으로 반입한다. 내부망 PC가 하는 일은 **압축 해제와 git(내부 GitLab push)뿐**이다 — 그쪽에는 파이썬도 저장소도 없다. 내부 GitLab 게시는 사람이 직접 하며 자동화 범위 밖이다(ANA 원칙).
  3. 생성은 전부 발행 머신에서 하고 망간 전송·수신·게시는 단순 작업으로 남긴다(ANA는 내부망이 생성기를 돌리게 했다가 되돌린 전례가 있다).
  4. **ai-weekly와 다른 점은 하나다: 사이트를 만드는 도구가 Quartz다**(ANA는 `scripts/build_site.py`). 나머지 방법론 — 외부 공개 GitHub 게시, 내부 반입용 델타 zip, 내부망은 압축 해제와 git뿐, 내부 GitLab 게시는 사람이 직접, 생성은 발행 머신에서만 — 은 같다. 내부망 PC에는 node도 없으므로 zip에는 **Quartz가 빌드한 정적 결과물(HTML 등)**을 담는다(소스 마크다운이나 `content/` 아님).
  5. 이 요구서가 요청하는 범위는 1(외부 게시 파이프라인)과 2의 **zip 생성까지**다. 내부 반입과 GitLab 게시는 작가가 한다.

## 5. 공개 전 점검 결과 (lib-ops가 했다, 2026-10-20)
게시 대상 파일 381개(위키 374 = 문서 373 + 목차, 보완 7)에서 이메일·키·로컬 경로 0건, 140자 이상의 긴 인용 0건(규칙: 한 출처에서 옮기는 분량 3문장 이하). `koscom`은 코스콤 회사 이름이다. 내부 경로는 `wiki/_meta/`에만 있어 게시 제외로 막았다.

## 6. 작가 결정 (2026-10-20)
공개 게시, 인쇄본 위키·보완층·2부 후보 모두. 사이트 이름·주소·구역 위치는 요구 사항이 아니며 stock-market 재량이다.

## 6-1. 작업 분리와 게시 테스트
작업은 lib-ops(데이터)와 stock-market(게시)으로 나눠서 한다. 역할, 우편함(`stock-market/handover/`), 게시 테스트 절차·점검 항목·피드백 형식은 `docs/requests/2026-10-20-kcm-work-split.md`(사본이 `stock-market/handover/2026-10-20-kcm-work-split.md`)에 있다. **먼저 로컬 시험 빌드로 게시 테스트를 하고 결과를 `handover/feedback-YYYY-MM-DD-*.md`로 남겨 달라.**

## 7. 이 프로젝트(lib-ops)가 하지 않는 것
git 원격 설정과 push, GitHub 저장소 생성·공개 범위 설정(계정 `ilovejsbach`의 별도 레포는 stock-market이 작가 확인 후 만든다), 사이트 모양·빌드·배포, 정본 OCR 텍스트 게시.

## 8. 버전과 갱신 (지속 반영)
- 버전 기준: 볼트 `vault-finance`의 `wiki-korean-capital-markets` 디렉터리 최신 커밋. 지금 보완 기록 404건, 2부 후보 주제 38개.
- 보완층은 계속 갱신된다(KCMI 보류 기록의 아카이브 재확인, 후속 조사, 판정 반영). 요구서는 한 번만 보내고, 갱신될 때마다 lib-ops가 **갱신 알림**(커밋 해시와 바뀐 파일 목록)을 보낸다. stock-market은 알림을 받아 `content/`를 다시 만들고 재빌드하며, 내부 반입용으로는 바뀐 파일만 담은 델타 zip을 만든다.
- 권장: 데이터 → `content/` 반영은 손으로 복사하지 말고 제외 규칙이 들어간 동기화 스크립트(예 rsync `--exclude`)로 한다. `content/`는 생성물이므로 손으로 고치지 않는다.

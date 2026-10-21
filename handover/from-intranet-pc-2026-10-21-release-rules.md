# 인터넷망 PC(윈도우) → 맥: 내부 반입 파이프라인 합의 요청 (2026-10-21)

보내는 곳: 인터넷망 PC의 `kcm-wiki-upload` 프로젝트(ANU `ai-news-upload` 에서 망간전송 계층을 복사해 시작).
역할: GitHub 릴리스의 델타 zip 을 받아 검증하고 망간자료전송으로 업무망에 보낸다. 업무망에서는 해제 후 내부 GitLab 에 push 한다.
이 문서는 맥 세션이 읽고 답하는 우편함이다. 답은 같은 폴더에 `to-intranet-pc-YYYY-MM-DD-*.md` 로 push 해 주면 된다.

## 1. 릴리스 규칙 (맥이 해 줄 것)
`internet/Get-KcmDelta.ps1` 이 전제한다. 상세는 `kcm-wiki-upload/docs/릴리스_규칙_제안.md`.

| 항목 | 값 |
|---|---|
| 저장소 | 릴리스를 올릴 GitHub 레포. 공개 레포 `ilovejsbach/capital_market_wiki`(Pages)에 같이 올릴지, 별도로 둘지 알려 주세요 |
| 릴리스 | 발행 1회 = 릴리스 1개 |
| 태그 | `kcm-wiki-<UTC 시각>` (예: `kcm-wiki-20261021T010203Z`) |
| 자산 | `kcm_wiki_delta_<UTC 시각>.zip` — 태그 시각 = 파일명 시각 = zip 안 `_delivery/manifest.json` 의 `published_at` |
| 첫 릴리스 | 전체 zip (`manifest.base == "full"`) |
| 삭제 금지 | 올린 릴리스는 지우거나 자산을 교체하지 않는다 |

이동 태그(`-latest`)를 쓰지 않는 이유: kcm 델타는 앞 델타와의 차이라서, 하나를 건너뛰면 그 델타의 변경·삭제가 내부망에 영영 안 들어갑니다.
그래서 릴리스를 전부 나열해 "원장에 없는 것"을 이름순으로 모두 받습니다.

## 2. 받는 쪽이 zip 에서 검사하는 것 (맥 산출물이 만족해야 함)
- `_delivery/manifest.json` 에 `published_at`, `source_commit`, `base`(full|delta), `files`(사이트 전체 경로→sha256)
- `published_at` 이 파일명 시각과 같을 것
- `manifest.files` 에 `index.html`, `static/vendor/d3.min.js`, `static/vendor/pixi.min.js` 가 있을 것. 전체 zip 이면 zip 안에도 있을 것 (그래프용. 델타는 바뀐 것만 담으므로 첫 전체 zip 에서 빠지면 영영 없음)
- `static/*.js`(vendor 제외)에 `cdn.jsdelivr.net` 이 없을 것 (`postbuild-vendor.sh` 적용 확인)
- 경로에 `..`, 절대 경로, `.git` 이 없을 것
- `index.html` 이 모든 zip 에 있을 것 (현재 `make_delta_zip.py` 는 이미 그렇게 함)

## 3. 맥에 묻는 것
1. **내부 GitLab Pages 주소**가 외부(`ilovejsbach.github.io/capital_market_wiki`)와 다릅니다. 현재 `quartz.config.yaml` 의 `baseUrl` 은 외부용입니다. 내부 주소가 정해지면 내부용 `baseUrl` 로 **따로 빌드한 zip** 이 필요한지 판단해 주세요. (sitemap/RSS 절대주소, 일부 링크에 영향.) 내부 주소는 인터넷망 PC 담당자가 관리자에게 확인해 알려 드립니다.
2. `_delivery/deleted.txt` 형식: 한 줄에 하나, 사이트 루트 기준 상대 경로, `/` 구분자라는 가정이 맞나요? 내부망 수신 프로그램이 이 파일로 `git rm` 합니다.
3. 해시가 붙은 공통 자산(`static/*.css`, `*.js`)은 바뀔 때마다 새 이름이 생기고 옛 이름은 `deleted.txt` 로만 정리됩니다. 정상인가요?
4. WebGL 이 안 되는 환경(VDI)에서 그래프가 어떻게 실패하는지(빈 화면/오류) 알려 주세요. 내부 PC 에서 실측해 보겠습니다.

## 4. 내부망 쪽 설정 (참고, 맥이 할 일 아님)
GitLab Pages 설정 지침은 `kcm-wiki-upload/docs/GitLab_Pages_설정지침.md`. ANA 에서 검증된 `.gitlab-ci.yml` 형식(`image:` 없음, `pages: true`, 제외 목록 복사)을 쓰고, `_delivery/` 는 저장소에 커밋하지 않습니다.

## 5. 상태
- 인터넷망: 다운로드·검증 모듈 완료(단위 시험 24건 통과), 발송 래퍼 작업 중
- 업무망: 수신·해제·`deleted.txt` 반영·push 프로그램은 이후
- 실제 릴리스가 아직 없어 end-to-end 는 시험하지 못했습니다. 첫 전체 zip 릴리스가 올라오면 알려 주세요.

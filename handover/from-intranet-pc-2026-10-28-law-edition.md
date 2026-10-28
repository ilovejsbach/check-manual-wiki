# 인터넷망 PC(윈도우) → 맥: 법령 판(kcm-law) 수신·발송 대응 완료 보고와 확인 요청 (2026-10-28)

`law-wiki` 브랜치의 `kcm-law-environment-setup.md`, `internal-rollout-strategy.md`, `scripts/publish_release.sh`, `make_delta_zip.py` 를 읽고 `kcm-wiki-upload` 프로젝트를 법령 판까지 다루게 바꿨다.
이 PC 의 수신 셸은 `deploy/contract.json` 이 아니라 자체 판 정의를 쓴다(아래).

## 1. 이쪽 구현 (브랜치 `kcm-law-edition`, 시험 통과)
| 항목 | kcm-wiki | law-wiki |
|---|---|---|
| 릴리스 태그 | `kcm-wiki-<UTC>` | `law-wiki-<UTC>` |
| 자산 | `kcm_wiki_delta_<UTC>.zip` | `kcm_law_delta_<UTC>.zip` |
| 이동 릴리스 | 쓰지 않음 | `law-wiki-latest`(`kcm_law_delta.zip`)는 **받지 않는다** — 델타는 앞 델타를 전제하므로 날짜 릴리스를 모두 받는다 |
- 원장·발송 이력·업무망 처리 이력을 판마다 따로 둔다. zip **파일 이름**으로 판을 가려 각자 내부 GitLab 저장소로 간다(`Receive-KcmAll.ps1`).
- 검증: `manifest.edition` 이 판과 같을 것(법령은 필수), 법령 zip 은 루트 `.gitlab-ci.yml` 필수, 전체 zip 은 `static/vendor/d3·pixi` 포함, 델타는 `prev_published_at` 이 이미 받은 `published_at` 에 있어야 이어짐(없으면 중단).
- 처리 순서는 법령 먼저, 그다음 kcm.

## 2. 맥에 확인 요청
1. **파일명 접두사 `<published_at 앞 13자>_`**: `kcm-law-environment-setup.md` 는 `<13자>_kcm_law_delta_<stamp>.zip` 이라 쓰는데 `publish_release.sh` 는 접두사 없이 올린다. 접두사는 누가 어디서 붙이나? (이쪽 업무망 수신은 앞에 무엇이 붙어도 끝부분 `kcm_law_delta_<UTC>.zip` 만 본다. 인터넷망 발송은 GitHub 자산 이름 그대로 보낸다.)
2. **kcm-wiki zip 에도 `edition: "kcm-wiki"` 와 `prev_published_at`** 이 들어가는지(kcm 세션 `make_delta_zip.py` 에서 같은 상위 호환본 사용 확인). 없으면 경고만 내고 통과시킨다.
3. `_delivery/deleted.txt`: 한 줄에 하나, 사이트 루트 기준 상대 경로, `/` 구분자 맞나? (지난 질문과 같음)
4. 첫 법령 전체본의 `prev_published_at` 은 `null` 이 맞나? (이쪽은 `base: full` 이면 이어짐 검사를 건너뛴다.)
5. 법령 델타가 `law-wiki-<stamp>` 날짜 릴리스로 **빠짐없이** 올라가는가(이동 릴리스만 갱신하고 날짜 릴리스를 건너뛰면 이쪽은 받지 못한다).

## 3. 이쪽이 필요로 하는 것(사용자 결정)
- 릴리스 저장소(`config/kcm-release.json` 의 `repository`): 두 판 모두 `ilovejsbach/capital_market_wiki` 로 가정. 비어 있어서 아직 실릴리스로 end-to-end 는 못 했다(DryRun 은 정상: 릴리스 2개 조회).
- 실제 발송은 사용자 승인 뒤. 첫 법령 전체본(약 48MB)은 파일명·크기·목적지를 보여 주고 승인받는다.

답은 `handover/to-intranet-pc-YYYY-MM-DD-*.md` 로.

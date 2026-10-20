# KCM 위키 내부망 반입 메모

내부망 PC 가 하는 일은 압축 해제와 git 뿐이다 (파이썬·node 없음). zip 은 발행 머신에서
`scripts/make_delta_zip.py` 로 만든다 (사용법은 그 파일 상단).

1. 내부 GitLab 작업 폴더에서 `git pull`
2. 받은 `kcm_wiki_delta_<UTC시각>.zip` 을 전부 그 폴더에 푼다 (순서 무관)
3. 이름이 가장 뒤인 zip(가장 늦게 만든 것) 하나를 한 번 더 푼다 — 최신 목차(index.html 등)가 이긴다
4. `_delivery/deleted.txt` 에 적힌 파일이 있으면 `git rm` (압축 해제로는 지워지지 않는다)
5. `index.html` 을 열어 목차가 최신인지 확인 -> `git add -A` -> commit -> push

- `_delivery/manifest.json` 의 `published_at`(UTC)·`source_commit` 으로 어느 zip 이 최신인지 확인한다.
- 첫 반입은 전체 zip 이다. 이후는 변경분만 들어 있으므로, 건너뛴 zip 이 있으면 인터넷 PC 담당자에게 요청한다.
- 내부 GitLab 게시는 사람이 직접 한다 (자동화 범위 밖).

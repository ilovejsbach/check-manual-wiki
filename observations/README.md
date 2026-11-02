# observations/

CHECK Expert **실제 화면**에서 수집한 구조 데이터. 수집은 CHECK가 설치된 윈도우 PC가 한다(맥에서는 앱을 실행할 수 없다).

- `pilot_targets.json` — 먼저 수집할 파일럿 대상 30개(`scripts/ingest_observations.py --pilot-list`로 생성)
- `screens/<TR>.json` — 화면별 관찰 결과(윈도우 PC가 추가)
- `item_samples.jsonl` — P4 항목 값 유형 샘플(값 자체는 저장하지 않음)
- `failed.json` — 수집 실패 TR과 사유

프로토콜·필드 정의·안전 규칙: `docs/check-screen-crawl-protocol.md`.
검증: `uv run python scripts/ingest_observations.py --check`. **시세 값, 스크린샷, 계좌·전화·이메일은 커밋하지 않는다.**

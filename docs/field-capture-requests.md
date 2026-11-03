# 화면 캡처 요청 목록 (상위 필드 25개 기준)

우선순위 상위 25개 표시명(`ontology/field_priority.jsonl`, 일반 단어 제외)이 한 번 이상 보이도록 고른 화면이다. 호출이 확인된(verified) 화면만 골랐고, 가능한 한 적은 수의 화면으로 모두 덮도록 탐욕적으로 골랐다(최소해 보장은 아님).

**총 15개 화면**

각 화면에서 기록할 것: 해당 표시명의 값 예시(단위·소수점·부호·색), 값이 비었을 때 표시, 나타나는 탭·조건, 기간·종류를 바꿨을 때 값 변화. 캡처 원본은 공개 레포에 올리지 말고 비공개 위치에 둔다.

| # | 화면 | 제목 | 시장 | 이 화면에서 볼 표시명 | 캡처 경로(체크 PC) | 주의 |
|---|---|---|---|---|---|---|
| 1 | 2250 | ETN 현재가 | ETP | **거래량, 현재가, 거래대금, 등락률** | `check-e2e/golden/batch-010/2250/screen.png` | not_detected |
| 2 | 3705 | 유통종합 > 주요채권 시세표 | 채권 | **수익률, 이론가, 최종호가** | `check-e2e/golden/batch-023/3705/screen.png` | not_detected |
| 3 | 4107 | 복수종목 | 선물 | **매도/수호가, 이론가/괴리, 베이시스** (그 밖에 현재가) | `check-e2e/golden/batch-031/4107/screen.png` | clock_overlay_detected |
| 4 | 4205 | 일중순매수 | 선물 | **외국인, 기초자산** | `check-e2e/golden/batch-037/4205/screen.png` | clock_overlay_detected |
| 5 | 3065 | 단기자금 > CD/CP > 발행정보(예탁원) | 채권 | **만기일, 신용등급** | `check-e2e/golden/batch-015/3065/screen.png` | clock_overlay_detected |
| 6 | 3527 | 차트 > 복수금리 비교2 | 채권 | **스프레드, 국고채** | `check-e2e/golden/batch-023/3527/screen.png` | clock_overlay_detected |
| 7 | 1300 | 주식현재가 | 주식 | **기준가** (그 밖에 거래량, 현재가) | `check-e2e/golden/1300/` (screen.png 위치는 체크 PC에서 확인) | - |
| 8 | 1379 | 관심종목 160 | 관심 | **시가총액** (그 밖에 현재가) | `check-e2e/golden/batch-008/1379/screen.png` | clock_overlay_detected |
| 9 | 4206 | 선물옵션단가 | 선물 | **순매수** | `check-e2e/golden/batch-038/4206/screen.png` | clock_overlay_detected |
| 10 | 3104 | 시장종합 > 채권데일리 | 채권 | **국채선물** (그 밖에 최종호가) | `check-e2e/golden/batch-017/3104/screen.png` | not_detected |
| 11 | 3005 | 발행정보 > 주요 > 종목별 현금흐름 | 채권 | **현금흐름** | `check-e2e/golden/batch-011/3005/screen.png` | not_detected |
| 12 | 4191 | 주식체결 | 종합 | **종목코드** (그 밖에 현재가) | `check-e2e/golden/batch-036/4191/screen.png` | not_detected |
| 13 | 6448 | 글로벌재무분석>업종별구성종목 | 해외 | **거래소** (그 밖에 현재가, 등락률) | `check-e2e/golden/batch-005/6448/screen.png` | clock_overlay_detected |
| 14 | 1201 | ELW 현재가 | ELW | **내재변동성** (그 밖에 거래량, 현재가, 등락률) | `check-e2e/golden/batch-006/1201/screen.png` | clock_overlay_detected |
| 15 | 3920 | 해외금리 > 미국/일본 국채금리 | 채권 | **CD** | `check-e2e/golden/batch-027/3920/screen.png` | not_detected |

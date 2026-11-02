---
title: "공식 문서 연결 대기 — 펀드·ETF 구성·운용정보"
description: "기존 화면·기능 문서에 아직 연결되지 않은 펀드·ETF 구성·운용정보 관련 문의 사례 묶음."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "분류 대기"
  - "검수 필요"
  - "펀드·ETF 구성·운용정보"
source: "manual-enrichment-unmapped.jsonl"
knowledge_id: "check:enrichment:unmapped:ee6126df39aa"
review_status: "candidate"
mapping_status: "unmapped"
signal_count: 11
source_locator: "topic:펀드·ETF 구성·운용정보"
---
# 공식 문서 연결 대기 — 펀드·ETF 구성·운용정보

> 기존 위키 화면·기능에 자동 연결되지 않은 비식별 신호입니다. 삭제하거나 임의 연결하지 않고 사람 검수 대기 상태로 보존합니다.

- 관련 신호: 11건
- 상태: `candidate` / `unmapped`
- 후보 유형: faq 11건, procedure 7건, caution 2건

## 대표 사례

### 후보 1

- 고객 질문·증상: - 화면번호 : 1442 - 버전 : 신버전 - 문의내용 : ETF 순자산 총액 CT함수로 실시간 긁어오기가 불가능할까요? 항목코드 52 로 뜨는데 함수가 안먹혀서요
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. 항목코드 [NUMBER]을 활용하여 보시기 바랍니다. (순자산총액의 경우 전일자 데이터를 기준으로 하고 있으며 장중 실시간 갱신은 이루어지지 않습니다)
- 증거 위치: `CRM데이터(PID복원)!row:358`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 2

- 고객 질문·증상: - 화면번호 : 9032 - 문의내용 : 안녕하세요, [IDENTIFIER] 사용전에 데이터 샘플을 보고 싶은데, 로그인을 안하면 샘플 조회가 안되는거 같아서 문의드립니다. https://[IDENTIFIER].[REDACTED_ENTITY].co.kr/etc/[IDENTIFIER] 화면에 조회 값 샘플 하나만 요청드려도 될까요?
- 당시 대응 기록: [NUMBER] 종목에 대하여 테스트도구를 통해 조회한 결과입니다. 테스트도구의 경우 결과값이 길 경우 뒷부분이 생략되며, 본 1:1문의 입력란의 크기도 제약이 있으므로 참고하여 주시기 바랍니다. { "[IDENTIFIER]": true, "[IDENTIFIER]": [ { "F[NUMBER]": "[NUMBER]", "F[NUMBER]": "905", "F[NUMBER]": "[IDENTIFIER]", "F[NUMBER]": "[NUMBER]", "F[NUMBER]": "[IDENTIFIER]", "[NUMBER]": "16", "F[NUMBER]": "3945.00", "F[NUMBER]": "0", "F[NUMBER]": "삼성전자", "F[NUMBER]": "0", "F[NUMBER]": "0", "F[NUMBER]": "[NUMBER]", "F[NUMBER]": "2643", "F[NUMBER]": "1", "F[NUMBER]": "" }, { "F[NUMBER]: "[NUMBER]", "F[NUMBER]": "905", "F[NUMBER]": "[IDENTIFIER]", "F[NUMBER]": "[NUMBER]", "F[NUMBER]": "[IDENTIFIER]", "F[NUMBER]": "16", "F[NUMBER]": "855.00", "F[NUMBER]": 0", "F[NUMBER]": "SK스퀘어", "F[NUMBER]": "0", "F[NUMBER]": "0", "F[NUMBER]": "[NUMBER]", "F[NUMBER]": "2452, "F[NUMBER]": "1", "F[NUMBER]": "" }, { "F2506": "[NUMBER]", "F[NUMBER]": "905", "F[NUMBER]": "[IDENTIFIER]", "F[NUMBER]": "[NUMBER]", "F[NUMBER]": "[IDENTIFIER]", "F[NUMBER]": "16", "F[NUMBER]": "556.00", "F3381": "0", "F[NUMBER]": "SK하이닉스", "F[NUMBER]": "0", "F[NUMBER]": "0", "F[NUMBER]": "[NUMBER]", "F[NUMBER]: "2437", "F[NUMBER]": "1", "F[NUMBER]": "" }, { "F[NUMBER]": "[NUMBER]", "F[NUMBER]": "905", "F[NUMBER]: "[IDENTIFIER]", "F[NUMBER]": "[NUMBER]", "F[NUMBER]": "KR[PHONE]", "F[NUMBER]": "16", "F[NUMBER]": "521.00", "F[NUMBER]": "0", "F[NUMBER]": "삼성전기", "F[NUMBER]": "0", "F[NUMBER]": "0", "F[NUMBER]": "[NUMBER]", "[NUMBER]": "1721", "F[NUMBER]": "1", "F[NUMBER]": "" }, { "F[NUMBER]": "[NUMBER]", "F[NUMBER]": "905", "[NUMBER]": "[IDENTIFIER]", "F[NUMBER]": "[NUMBER]", "F[NUMBER]: "[IDENTIFIER]",
- 증거 위치: `CRM데이터(PID복원)!row:470`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 3

- 고객 질문·증상: - 화면번호 : 9032 - 문의내용 : 안녕하세요, 다름이 아니라 host: https://[IDENTIFIER].[REDACTED_ENTITY].co.kr post: /etc/etf/etf_pdf 조회해보면 HTTP 404 에러가 반환 되어서 확인해주시면 감사하겠습니다.
- 당시 대응 기록: $$
- 증거 위치: `CRM데이터(PID복원)!row:476`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 4

- 고객 질문·증상: - 화면번호 : 8003 - 문의내용 : 안녕하세요, 현재 =CLIST("","",-1,A2,"[NUMBER]","","[NUMBER],[NUMBER],[NUMBER]","DESC","[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=none; ") 함수를 이용해서, PDF 구성 종목을 불러오고 있는데 혹시 해당 함수에서 수식을 변경해서 "[NUMBER]" ETF 안에 들어있는 "[NUMBER]" 종목의 수량만을 뽑아내는 함수를 만들 수 있을까요?
- 당시 대응 기록: CLS[REDACTED_ENTITY] 함수에서 필터링기능(함수빌더 참고)을 제공하고 있으나, 모든 항목에대해 적용되지는 않습니다. 말씀하신 PDF구성리스트에 관해서는 적용되지 않고 있습니다. 감사합니다.
- 증거 위치: `CRM데이터(PID복원)!row:552`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 5

- 고객 질문·증상: - 화면번호 : CHECK API - 문의내용 : 체크에 있는 "ETF 분배금 현황" 화면 데이터를 API로 받고 싶은데 인터페이스를 좀 만들어 주세요
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. 해당 정보는 유료로 판매되는 정보로 별도의 API 계약을 필요로합니다. 관련 요청사항은 [PERSON]차장 ([PHONE], [EMAIL]) 으로 연락주시기 바랍니다. 감사합니다.
- 증거 위치: `CRM데이터(PID복원)!row:751`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 6

- 고객 질문·증상: - 화면번호 : - 문의내용 : ch 함수에서 [NUMBER] ETP 종가 nav로 계산한 수익률과 [IDENTIFIER]로 계산한 수익률이 0195S0 SK하이닉스 단종레 상품에서 다른데 적용 시점이 다른가요? 선물까지 반영된 지표인지 문의드립니다
- 당시 대응 기록: $$
- 증거 위치: `CRM데이터(PID복원)!row:1045`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 7

- 고객 질문·증상: - 화면번호 : 1446 - 문의내용 : 1446화면 혹은 1447화면 데이터를 일별, 종목별로 티커와 필드, 날짜를 넣으면 종목별 날짜별 설정/환매 주수를 출력하는 함수 있을까요?
- 당시 대응 기록: 안녕하세요. CTD 함수를 이용하시면 특정 날짜의 항목 값을 받을 수 있습니다. 다만 함수당 1개의 항목 값을 받을 수 있기 때문에 설정주수와 환매주수에 대해 각각 함수를 넣으셔야 합니다. =CTD( "SPT", "종목코드", "날짜", "항목코드") [IDENTIFIER]의 설정주수(항목코드: [NUMBER])와 환매주수(항목코드: [NUMBER])를 받을 경우 함수 예시입니다. =CTD( "SPT", "[NUMBER]", "[NUMBER]", "[NUMBER]") =CTD( "SPT", "[NUMBER]", "[NUMBER]", "[NUMBER]") 감사합니다. 감사합니다.
- 증거 위치: `CRM데이터(PID복원)!row:1066`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 8

- 고객 질문·증상: - 화면번호 : 9032 - 문의내용 : 안녕하세요 한화자산 [REDACTED_ENTITY] [REDACTED_ENTITY]입니다. 다름이 아니라 API를 통해 ETF들의 과거 PDF 내역을조회하려고 하는데요. 과거 1년치까지(25년 9월 1일까지)만 조회되는 것 같아서요~ 혹시 추가로 그 이전 데이터를 받을 수 있을까요?
- 당시 대응 기록: 네. 현재는 불가하고, [REDACTED_ENTITY]검토 진행하기로 했습니다 다만, 지금상황에서 언제 가능하다고 확답드리긴 어렵다는 점 참고 부탁드립니다
- 증거 위치: `CRM데이터(PID복원)!row:1079`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 9

- 고객 질문·증상: - 화면번호 : - 버전 : 신버전 - 문의내용 : CHECK API 관련 문의 드립니다. 안녕하세요. 하나자산 [REDACTED_ENTITY] [REDACTED_ENTITY]입니다. 혹시 API를 통해 ETF의 iNAV를 수신할 수는 없는지 문의 드립니다. [IDENTIFIER].[REDACTED_ENTITY].co.kr 사이트 참고해서 찾아보고 있는데, 찾을 수가 없어서 문의 드립니다..! 가능하면 답변으로 회신주시면 감사하겠습니다.! 감사합니다. [REDACTED_ENTITY] 드림.
- 당시 대응 기록: 안녕하세요. [IDENTIFIER]+ 입니다. ETP 지표가치는 주식-기본정보(전체) 에서 확인 가능하십니다. /stock/m001/basic_info_all 조회항목은 F[NUMBER] 입니다. 감사합니다.
- 증거 위치: `CRM데이터(PID복원)!row:1312`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 10

- 고객 질문·증상: - 화면번호 : - 문의내용 : 안녕하세요, XL [IDENTIFIER] L[REDACTED_ENTITY] 사용법 관련 질문있습니다. 상장된 ETF에 대한 PDF를 종목별 또는 전체 조회를 할 수 있는 함수가 있는지 궁금합니다.
- 당시 대응 기록: CLIST 함수를 사용하시면 됩니다. 예를 들어, 아래와 같이 사용합니다. =CLIST( "", "", -1, "[NUMBER]*001", "[NUMBER]", "", "[NUMBER]", "DESC", "[IDENTIFIER]=true;")
- 증거 위치: `CRM데이터(PID복원)!row:1397`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

### 후보 11

- 고객 질문·증상: ETF 구성종목 확인할 때 CLIST 함수를 사용하는데, 과거일자 넣으면 안 나오는 현상 문의
- 당시 대응 기록: CLIST는 오늘자, CTR은 과거일자로 조회되기 때문에 CTR 사용 안내
- 증거 위치: `CRM데이터(PID복원)!row:1449`
- 검토 과제: 연결할 기존 문서 또는 신규 문서 필요 여부 결정

## 분류 게이트

- [ ] 화면번호·기능명·업무 용어를 추가 확인했는가
- [ ] 기존 문서 연결과 신규 문서 생성 중 적절한 경로를 결정했는가
- [ ] 공식 근거 또는 실제 동작 증거를 확보했는가
- [ ] 식별정보와 내부 전용 정보가 남아 있지 않은가

---
title: 오류 해결 — =CTR("<값>","0",A2&TEXT(B2,"<값>")&"<값>","20","<값>=true; <값>=vert; t<값>…
description: 1448 - ETF 구성종목(PDF) 관련 비식별 문의와 당시 대응 기록을 분리한 오류 해결 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 오류 해결
- 검수 필요
- 1448 - ETF 구성종목(PDF)
source: manual-enrichment.jsonl
knowledge_id: check:support-case:5cedcf834cafff7e
document_type: support_case
case_type: troubleshooting
case_facets:
- troubleshooting
- procedure
- caution
- faq
case_topic: 1448 - ETF 구성종목(PDF)
case_topics:
- 1448 - ETF 구성종목(PDF)
related_ids:
- check:screen:1448
- check:enrichment:screen:1448
review_status: candidate
mapping_status: mapped
source_locator: 20260916!row:1606
candidate_id: manual-candidate:CRM-01604
---
# 오류 해결 — =CTR("<값>","0",A2&TEXT(B2,"<값>")&"<값>","20","<값>=true; <값>=vert; t<값>…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

=CTR("<값>","0",A2&TEXT(B2,"<값>")&"<값>","20","<값>=true; <값>=vert; t<값>le=<값>em+<값>;DQI=1/1; struct=$A$1;") 라는 함수를 썼고, 첨부된 파일 처럼 A2 : 특정 수치, B2 : 2026-01-18 이 입력되어 있는데, 데이터가 다운이 안됩니다. 이 파일을 연 상태에서 1448 화면에서 엑셀 특정 종목 으로 보내기 하니 역시 다운이 안됩니다.. 파일이 오류가 생긴걸까요?

## 당시 대응

수식넣어 확인했을때 함수에 이상이 있어보이지는 않습니다. CTR함수가 있는 시트를 클릭후 엑셀상단메뉴 > XL 특정 종목 > 선택 셀재조회 리스트 중 '선택 워크시트 재조회'로 해당시트 재조회시 정상조회되는지 확인부탁드립니다. 정상조회가 되면 저장 후 다시 열었을때도 정상인지 확인해주시면 됩니다. 해결이 안되시면 원격가능한 시간적어 재문의 주시면 연락드리도록 하겠습니다.

## 연결된 화면·기능

- [[check-expert/새로운-모습/ETP/1448-1448-ETF-구성종목(PDF)|1448 - ETF 구성종목(PDF)]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTR 함수 설명]]

## 의미 분류
- 대표 유형: **오류 해결**
- 함께 볼 유형: 오류 해결, 사용 절차, 주의사항, 질문과 답변
- 업무·주제: 1448 - ETF 구성종목(PDF)
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:1606`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가

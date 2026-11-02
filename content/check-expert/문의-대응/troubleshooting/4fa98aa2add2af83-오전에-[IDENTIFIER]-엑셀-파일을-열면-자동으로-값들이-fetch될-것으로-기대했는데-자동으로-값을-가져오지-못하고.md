---
title: "오류 해결 — 오전에 [IDENTIFIER] 엑셀 파일을 열면 자동으로 값들이 fetch될 것으로 기대했는데 자동으로 값을 가져오지 못하고…"
description: "3741 - 시가평가 > 채권그룹 > 기업별 Term Structure 관련 비식별 문의와 당시 대응 기록을 분리한 오류 해결 검수 후보."
tags:
  - "CHECK Expert"
  - "문의 대응"
  - "오류 해결"
  - "검수 필요"
  - "3741 - 시가평가 > 채권그룹 > 기업별 Term Structure"
source: "manual-enrichment.jsonl"
knowledge_id: "check:support-case:4fa98aa2add2af83"
document_type: "support_case"
case_type: "troubleshooting"
case_facets:
  - "troubleshooting"
  - "procedure"
  - "faq"
case_topic: "3741 - 시가평가 > 채권그룹 > 기업별 Term Structure"
case_topics:
  - "3741 - 시가평가 > 채권그룹 > 기업별 Term Structure"
related_ids:
  - "check:screen:3741"
  - "check:enrichment:screen:3741"
review_status: "candidate"
mapping_status: "mapped"
source_locator: "20260916!row:2415"
candidate_id: "manual-candidate:CRM-02413"
---
# 오류 해결 — 오전에 [IDENTIFIER] 엑셀 파일을 열면 자동으로 값들이 fetch될 것으로 기대했는데 자동으로 값을 가져오지 못하고…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

오전에 [IDENTIFIER] 엑셀 파일을 열면 자동으로 값들이 fetch될 것으로 기대했는데 자동으로 값을 가져오지 못하고 있습니다. Expert에서 마우스 오른쪽 버튼을 클릭해서 excel [IDENTIFIER]으로 보내기를 클릭해야만 하나요?

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. 아래의 두 가지 방법을 활용해 보시기 바랍니다. 1. 엑셀프리미엄으로 보내기 통해서 만들어진 파일의 B1셀에 수식이 있는데요, 수식안에 날짜가 들어갑니다. 날짜가 정상적이지 않을 경우 데이터를 불러오지 못할 수 있습니다. 2. CHECK가 재기동 되면서 자동으로 엑셀 프리미엄이 재설치가 되는데요, 재설치가 정상적으로 되지 않을 경우, 간혹 이런 현상이 발생합니다. 사용 중인 엑셀 파일을 모두 저장하고 닫은 뒤, 화면 상단의 메뉴에서 [지원 > 엑셀 프리미엄 설치하기]를 클릭하면, 재설치가 진행됩니다. 설치가 완료된 후 다시 엑셀 파일 실행 부탁드립니다. 위 두가지 방법을 사용한 뒤에도 비정상이라면, 다시 연락부탁드립니다. 감사합니다.

## 의미 분류

- 대표 유형: **오류 해결**
- 함께 볼 유형: 오류 해결, 사용 절차, 질문과 답변
- 업무·주제: 3741 - 시가평가 > 채권그룹 > 기업별 Term Structure
- 공식 문서 연결: 연결됨
- 증거 위치: `20260916!row:2415`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가

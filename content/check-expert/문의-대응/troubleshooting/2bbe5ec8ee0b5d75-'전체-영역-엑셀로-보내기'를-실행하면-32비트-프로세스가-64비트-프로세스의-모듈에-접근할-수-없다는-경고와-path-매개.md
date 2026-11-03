---
title: 오류 해결 — '전체 영역 엑셀로 보내기'를 실행하면 32비트 프로세스가 64비트 프로세스의 모듈에 접근할 수 없다는 경고와 path
  매개…
description: 4724 - 과거민감도 관련 비식별 문의와 당시 대응 기록을 분리한 오류 해결 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 오류 해결
- 검수 필요
- 4724 - 과거민감도
source: manual-enrichment.jsonl
knowledge_id: check:support-case:2bbe5ec8ee0b5d75
document_type: support_case
case_type: troubleshooting
case_facets:
- troubleshooting
- procedure
- faq
case_topic: 4724 - 과거민감도
case_topics:
- 4724 - 과거민감도
related_ids:
- check:enrichment:screen:4724
- check:screen:4724
review_status: candidate
mapping_status: mapped
source_locator: 비식별 문의 사례
candidate_id: 2bbe5ec8ee0b5d75
---
# 오류 해결 — '전체 영역 엑셀로 보내기'를 실행하면 32비트 프로세스가 64비트 프로세스의 모듈에 접근할 수 없다는 경고와 path 매개…

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

'전체 영역 엑셀로 보내기'를 실행하면 32비트 프로세스가 64비트 프로세스의 모듈에 접근할 수 없다는 경고와 path 매개변수가 null일 수 없다는 경고가 뜨는데, 구버전에서는 없던 현상이라고 문의했습니다.

## 당시 대응

엑셀프리미엄설치하기가 성공하는지, CHECK엑셀매니저의 'UAC 변경 진행 여부'가 체크되어 있는지, 빈 엑셀에서도 팝업이 뜨는지 확인하도록 했습니다. 이 메시지는 보통 체크와 엑셀 계정이 사용자계정으로 연동될 때 나오며, UAC 변경을 체크하고 프리미엄을 재설치한 뒤 재부팅하면 해결되는 경우가 많습니다.

## 연결된 화면·기능

연결 키가 없습니다.

## 의미 분류
- 대표 유형: **오류 해결**
- 함께 볼 유형: 오류 해결, 사용 절차, 질문과 답변
- 업무·주제: 4724 - 과거민감도
- 공식 문서 연결: 연결됨

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가

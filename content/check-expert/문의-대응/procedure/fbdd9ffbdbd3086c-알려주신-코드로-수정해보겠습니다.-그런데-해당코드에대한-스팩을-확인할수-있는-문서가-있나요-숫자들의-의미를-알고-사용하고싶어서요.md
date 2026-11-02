---
title: 사용 절차 — 알려주신 코드로 수정해보겠습니다. 그런데 해당코드에대한 스팩을 확인할수 있는 문서가 있나요? 숫자들의 의미를 알고 사용하고싶어서요
description: 조회정보 없음(이용 문의) 관련 비식별 문의와 당시 대응 기록을 분리한 사용 절차 검수 후보.
tags:
- CHECK Expert
- 문의 대응
- 사용 절차
- 검수 필요
- 조회정보 없음(이용 문의)
source: manual-enrichment-unmapped.jsonl
knowledge_id: check:support-case:fbdd9ffbdbd3086c
document_type: support_case
case_type: procedure
case_facets:
- procedure
- faq
case_topic: 조회정보 없음(이용 문의)
case_topics:
- 조회정보 없음(이용 문의)
related_ids:
- check:tr:1617
review_status: candidate
mapping_status: unmapped
source_locator: CRM데이터(PID복원)!row:266
candidate_id: manual-candidate:VOC-00264
---
# 사용 절차 — 알려주신 코드로 수정해보겠습니다. 그런데 해당코드에대한 스팩을 확인할수 있는 문서가 있나요? 숫자들의 의미를 알고 사용하고싶어서요

> 비식별 문의 기록에서 추출한 검수 전 사례입니다. 당시 대응이 현재 제품의 공식 해결책임을 의미하지 않으며, 공식 매뉴얼과 재현 시험으로 확인해야 합니다.

## 사용자가 겪은 상황

알려주신 코드로 수정해보겠습니다. 그런데 해당코드에대한 스팩을 확인할수 있는 문서가 있나요? 숫자들의 의미를 알고 사용하고싶어서요

## 당시 대응

안녕하세요. [IDENTIFIER]+ 입니다. TR 1617 거래규모상위 화면의 경우 비패턴 화면으로 CTR 함수로 조회하실 수 있습니다. 스팩에 대하여 문서는 따로 없고, 서버 조회 내용을 확인하여 안내 드립니다. 사용 중이신 함수식을 임의로 쪼개어 설명드리겠습니다. =CTR("[NUMBER]","0","[NUMBER] [PHONE] [NUMBER] 51", "20", "[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER];DQI=2/2;") 1) "[NUMBER]" : 화면번호 1617을 반영한 숫자로 체크 내부 TR 숫자는 총 6자리로 구성되어 1617 + 00 반영 2) "0" : 화면 서버 조회 숫자로 0, 1, 2 등의 숫자가 있으며 해당 화면은 0 만 존재 3) "[NUMBER]" [NUMBER] : 전체(Tota) 1, 유가(KSE) 2, 코스닥(KSQ) 3, ETF 4, ETN 5, ELW 6, 기타(ETC) 7 02 : 00 전체회원사(All), 01 국내회원사(Local) 02 외국계회원사([IDENTIFIER]) [NUMBER] : 시작일자(From) [NUMBER] : 종료일자(To) 5 : 앞서 조회한 전체 체크박스를 제외하고 체크한 체크박스 갯수(EX. [NUMBER] 의 경우 전체 1을 제외한 [NUMBER] 총 5개 체크박스를 체크함) 1 : 0 한글버전, 1 영문버전 1, 2, 3 : 1 KRX, 2 NXT, 0, CON (NXT거래소 출범이후 구분되어 추가) 따라서 사용 중이신 함수식을 아래와 같이 변경하여도 같은 값을 얻으실 수 있습니다. =CTR("[NUMBER]","0","[NUMBER]","20","[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER];DQI=2/2;") 4) "20" : 화면 구성에는 필요하나 의미 없는 조회숫자로 어떤 조회를 하던 "20" 으로 통일 추가로 아래 몇가지 함수 예를 보여 드리겠습니다. [전체 체크박스 체크, 전체회원사, [NUMBER] ~ [NUMBER], 전체 1을 제외한 [NUMBER] 총 6개 체크박스를 체크함, 영문버전, KRX 기준] =CTR("[NUMBER]","0","[NUMBER]","20","[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER];DQI=2/2; struct=$A$1;") [코스피, 코스닥 체크박스 체크, 전체회원사, [NUMBER] ~ [NUMBER], 전체 1을 제외한 23 총 2개 체크박스를 체크함, 영문버전, KRX 기준] =CTR("[NUMBER]","0","[NUMBER]","20","[IDENTIFIER]=true; [IDENTIFIER]=vert; t[REDACTED_ENTITY]le=[REDACTED_ENTITY]em+[IDENTIFIER];DQI=2/2; struct=$A$1;") 보시고 어려움이 있으시거나 문의사항 있으시면 말씀 부탁 드립니다. 감사합니다.

## 연결된 화면·기능

- [[check-expert/tr-후보/1617|TR 1617 (화면 문서 없음)]]
- [[check-expert/excel-premium/매뉴얼/메뉴와-템플릿|CTR 함수 설명]]

## 의미 분류
- 대표 유형: **사용 절차**
- 함께 볼 유형: 사용 절차, 질문과 답변
- 업무·주제: 조회정보 없음(이용 문의)
- 공식 문서 연결: 분류 대기
- 증거 위치: `CRM데이터(PID복원)!row:266`

## 검증할 사항

- [ ] 현재 버전에서도 같은 상황이 재현되는가
- [ ] 당시 대응이 공식 매뉴얼의 절차와 일치하는가
- [ ] 원인과 해결 조치를 구분해 설명할 수 있는가
- [ ] 고객·직원·기관 식별정보가 남아 있지 않은가

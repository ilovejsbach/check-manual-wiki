---
title: "CHECK Expert LLM Wiki"
description: "CHECK Expert+와 Excel Premium 공식 매뉴얼을 검색·질의하기 위한 로컬 위키."
tags:
  - "CHECK Expert"
  - "LLM Wiki"
source: "KOSCOM CHECK 공식 매뉴얼"
generated: true
---
# CHECK Expert LLM Wiki

이 위키는 CHECK Expert+ 공식 전체 매뉴얼과 Excel Premium 자료를 Markdown으로 변환한 검색·질의용 지식베이스입니다.

## 바로가기

- [[check-expert/화면번호-색인|화면번호로 찾기]]
- [[check-expert/업무-기능-색인|업무·기능으로 찾기]]
- [[check-expert/excel-premium/매뉴얼|Excel Premium 매뉴얼]]
- [[check-expert/excel-premium/종목코드표|종목코드표]]
- [[check-expert/excel-premium/항목코드표|항목코드표]]
- [[check-expert/운영-보강/index|실사용 보강 후보]]

상단 검색에서 화면번호(`1300`), TR 형식(`TR1300`), 화면명 또는 업무 용어를 입력할 수 있습니다.

## AI·프로그램 연동

- [[check-expert/api/llms.txt|LLM 사용 안내]]
- [[check-expert/api/manifest.json|지식베이스 manifest]]
- [[check-expert/api/knowledge.jsonl|전체 JSONL 지식 레코드]]
- [[check-expert/다운로드|저장·다운로드]]

응답에는 `id`, `source`, `source_locator`를 함께 보존해 근거를 추적하세요.

## 생성 현황

- PDF: 829쪽, 북마크 1,664개
- 화면·기능 문서: 442개
- Excel 문서: 103개
- 코드 레코드: 71,586개

- 실사용 보강 문서: 1,911개

## 사용 시 주의

- 자동 추출 과정에서 이미지, 도형, 복잡한 표의 배치가 생략될 수 있습니다.
- 실제 화면 조작 전에는 문서에 표시된 원본 PDF 페이지나 Excel 시트를 함께 확인하세요.
- 화면과 데이터는 매뉴얼 작성 이후 변경됐을 수 있습니다.

## 원본 무결성(SHA-256)

- `CHECKPlus_Manual.pdf`: `b3ca8de468ffb238d16bb49882a2e7d2f85585f87c28698587331c8022948631`
- `README.md`: `11b7c8d437fe01123004cd74500e4cfc661f69172231d1c297eab3dc52c7bd1c`
- `case-summaries.jsonl`: `54c6c4adf7bf8224eab649e8607b5435f18d3284ffb42b34b2b492954dffc3c8`
- `excel-sources.zip`: `20185ff5f1a57e15de2f8b913a44af1f9f1dddb5ed4016ac9ff6f9c4dbdaecac`
- `manual-enrichment-unmapped.jsonl`: `263bcd62d028b37ff23c5f07d16307061065670de2ca5fbb2f00caa5f31c3e70`
- `manual-enrichment.jsonl`: `382284c99f1e4d0c79990062f055157709371ee4a9d9fb52e1b972edc8329ec1`

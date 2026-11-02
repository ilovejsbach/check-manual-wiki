# CHECK 공식 원본

이 폴더는 다른 PC에서도 CHECK Manual Wiki를 동일하게 재생성하기 위한 공식 입력 파일을
보관합니다.

| 파일 | 용도 | SHA-256 |
| --- | --- | --- |
| `CHECKPlus_Manual.pdf` | CHECK Expert+ 전체 매뉴얼, 829쪽 | `b3ca8de468ffb238d16bb49882a2e7d2f85585f87c28698587331c8022948631` |
| `excel-sources.zip` | Excel Premium 매뉴얼과 코드표 6개 묶음 | `20185ff5f1a57e15de2f8b913a44af1f9f1dddb5ed4016ac9ff6f9c4dbdaecac` |

`excel-sources.zip`에는 다음 공식 파일이 들어 있습니다.

- `excel-manual1_menu_template.xls`
- `excel-manual2_function.xls`
- `excel-manual3_askWizard.xls`
- `excel-manual4_ezChart.xls`
- `JongMokCodeTable_20140616_Uodate02.xlsx`
- `HangMokCodeTable_ExcelPremium_update01.xlsx`

`.pia` 파일은 PC 보안 프로그램이 만든 변환본이며 재생성에 필요하지 않아 Git에서 제외합니다.
원본을 갱신할 때에는 출처와 SHA-256을 함께 갱신하고 위키 생성·검증을 다시 수행하세요.

`manual-enrichment.jsonl`은 민감 원본이 아니라 개인정보 패턴 검사와 셀 계보 검증을
통과한 대상별 집계입니다. 각 레코드는 기존 공식 문서 ID, 문의 수, 검수 전 사례와
`review_status=candidate`를 포함합니다. 공식 매뉴얼과 실제 CHECK 동작의 교차 검증 전에는
확정된 제품 동작이나 금융 정의로 사용하지 않습니다.

`manual-enrichment-unmapped.jsonl`은 기존 문서에 자동 연결되지 않은 신호를 주제별로
집계한 검수 대기열입니다. 자동 매핑 실패를 누락으로 처리하지 않고 기존 문서 연결 또는
신규 문서 작성 여부를 사람이 판단할 수 있도록 보존합니다.

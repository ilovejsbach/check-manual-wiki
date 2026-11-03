# CHECK 항목·시장 메타 (로컬 설치 추출)

2026-11-03 윈도우 세션이 CHECK Expert 4.0.0.000 설치본의 `CheckXL\system\xlp_meta.sqlite`에서 추출했다.
8003 「데이터항목 검색」 화면이 보여 주는 항목코드·시장코드·데이터 형식의 원천이다.
**시세 값은 없다.** 구조 ID와 이름뿐이다. 재생성: `uv run python scripts/extract_check_meta.py`
(`--src`로 다른 설치 경로 지정, `--check`는 건수만 점검). 원천 SHA-256은 `manifest.json`.

근거 등급: `local_install_meta` (화면 대조로 일부 확인). 매뉴얼 등급이 아니다.

## 파일

| 파일 | 행 | 내용 |
|---|---:|---|
| `fid.csv` | 19,563 | **항목코드(FID)**, 그룹(FGID·이름), key_type, 항목명, tick/intra/history 플래그, 연결된 시장 수 |
| `mid.csv` | 189 | **시장코드(MID)**, 내부 정의명(`MID_KSP_JONG`), 시장명, 기준 FID, 항목 수 |
| `fgid.csv` | 36 | 항목 그룹 이름 |
| `sid.csv` | 125 | 데이터 종류(SID) 이름 (마스터, 단일종목체결, 호가 …) |
| `mid_fid.csv.gz` | 192,468 | 시장(MID)별 항목(FID)의 data_type·len·cnt·dec_pos |
| `sid_mid.csv` | 2,912 | SID×MID, 일자·시각 FID |
| `sid_mid_fid.csv.gz` | 104,015 | SID×MID×FID |
| `sid_ref.csv` | 107 | SID 참조 이름 |
| `hfid_oper.csv` | 3,464 | 이력(history) FID 연산 정의 |
| `intrfid.csv` | 1,852 | 인트라 FID 정의 |
| `data_type_observed.csv` | 4 | 화면으로 확인한 data_type → CH_Type 표기 |

## 8003 화면과의 대응 (화면 행으로 확인)

| 8003 열 | 데이터 |
|---|---|
| 항목코드 | `fid.csv` fid (예: 15001 현재가, 15472 대비, 15004 등락률) |
| 시장코드·시장명 | `mid.csv` mid·name (001=장내종목, 168=국내기타지수, 169=경제지표, 170=KRX커스텀지수) |
| CH_Type | `mid_fid` data_type: 19=UINT, 3=INT, 4=LNLN, 17=UCHAR (그 외 코드 1, 2, 18, 20은 미확인) |
| 사용가능함수 | **미확인.** tick/intra/history 플래그만으로는 재현되지 않는다(예: 15009 시가와 15020 체결량은 플래그가 같은데 화면 표기가 다르다) |
| 값(RTD,CT) 예시 | 시세라서 저장하지 않음 |

`dec_pos`는 소수 자리 정보로 보인다(등락률 -2). 확인 전.

## 알아둘 점

- **엑셀 항목코드표와 겹치는 것은 일부다.** 저장소 항목 노드 18,944개 중 5,016개만 이 DB에 있고, DB에만 있는 FID가 14,547개다. 저장소에만 있는 13,928개는 경제금융·재무 계열로 추정(미확인).
- 겹치는 5,016개 중 이름이 다른 1,844개의 상당수는 항목코드표 쪽 이름 끝 `*`(각주 표시) 차이다.
- `mid_fid`에 나오지만 `mid.csv`에 이름이 없는 MID가 42개 있다(39~42, 61, 83, 90 … 175; 목록은 `manifest.json`). 폐지·내부용으로 추정.
- `fid.csv`의 FID 6,000개는 어느 시장에도 연결되지 않았다.
- 우클릭 메뉴의 엑셀 내보내기 등으로 8003 화면의 `사용가능함수` 열을 직접 받으면 위 미확인을 풀 수 있다(미시도: 앱에 클릭 입력이 전달되지 않음).

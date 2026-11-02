#!/usr/bin/env python3
"""항목 사전(item)과 함수(function) 노드를 ontology/nodes.jsonl 로 내보낸다.

명세: docs/check-ontology-spec.md 2.2(항목), 2.4(함수), 7(항목 사전 구축 규칙), 11(ID 규칙).
- 항목: 항목코드표(HangMokCodeTable) 행을 코드 단독 키 check:item:<코드> 로 병합. applies_to 에 (함수, 시장, 카테고리) 보존.
- 함수: 매뉴얼 '주요 함수 설명'(PDF 45-54쪽)에 정의된 함수는 서명을 본문에서 추출해 매뉴얼확인 등급으로 낸다.
  사례에서만 언급되고 매뉴얼에 정의가 없는 함수는 verification=mentioned_only 로 표시한다(추측하지 않는다).
표준 라이브러리만 사용한다(항목 사전 파싱·사례 키 추출은 derive_item_links / derive_case_links 재사용).

사용:
  uv run --offline --no-sync python scripts/build_ontology_nodes.py            # ontology/nodes.jsonl 쓰기
  uv run --offline --no-sync python scripts/build_ontology_nodes.py --check    # 쓰지 않고 검증만(위반 시 종료코드 1)
  ... --links tmp/case_links.jsonl   # 관계 파일의 check:item:/check:func: 대상이 노드로 실존하는지(I1) 검사
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import derive_case_links as dcl  # noqa: E402
import derive_item_links as dil  # noqa: E402

DEFAULT_KNOWLEDGE = Path("knowledge/check-expert/knowledge.jsonl")
DEFAULT_OUT = Path("ontology/nodes.jsonl")
DEFAULT_REGISTRY = Path("ontology/tr_registry.jsonl")
DEFAULT_AS_OF = "2026-11-02"
SCHEMA_VERSION = "1.0"
DICT_SOURCE = "HangMokCodeTable_ExcelPremium_update01.xlsx"
FUNC_DOC_ID = "check:manual:엑셀-프리미엄:주요-함수-설명"
FUNC_EXAMPLES_ID = "check:excel:manual:함수-설명"
FUNC_PAGES = "45-54"

# 함수별 범위·형태는 매뉴얼 '내용' 문장을 요약한 것이다(근거 문장은 FUNC_DOC_ID 본문, 아래 검증이 서명 존재를 확인).
FUNC_FACTS = {
    "CT": ("특정 종목·항목의 실시간 단일 값 조회", "single", True),
    "CH": ("주기(일/주/월/분기/년)별 일간 시계열 조회, 다수 종목 병합, 실시간 업데이트", "series", True),
    "CTS": ("Tick(체결) 데이터를 시계열로 실시간 조회", "tick_series", True),
    "CIS": ("특정 주기의 일중 시계열 조회, 다수 종목 동시 조회", "intraday_series", True),
    "CLIST": ("시계열이 아닌 매트릭스 형태(업종·시장 소속 종목, 거래량 상위 리스트 등) 조회", "matrix", True),
    "CTD": ("시계열 데이터에 대한 계산 함수 결과 조회(기간 집계·비교)", "calc", True),
    "CTR": ("분석 화면(CHECK)의 조회 결과를 호출. 화면에서 엑셀 프리미엄 보내기를 하면 호출됨", "analysis_result", None),
    "CPFG": ("CHECK 단말에서 구성한 관심종목 그룹 조회", "group_list", False),
    "CPF": ("CHECK 단말에서 구성한 관심그룹 등록 종목 조회", "group_list", False),
}

ENUM_RE = re.compile(r"(?<=\d)&cl(?=\S)")  # 코드값 정의는 '0&cl정상'처럼 숫자 바로 뒤에 붙는다. '제조업 &cl 제외' 같은 서술은 제외
SEQ_RE = re.compile(r"(\d+)&cl(.*?)(?=\d+&cl|$)")
RATIO_RE = re.compile(r"율|률|비율|비중|배율|괴리|수익률|%")
QTY_RE = re.compile(r"량|수량|잔량|건수|좌수|횟수|주식수|계약수|미결")
DATE_RE = re.compile(r"일자|날짜|시각|(?<!가)시간(?!가치|외)|만기일|발행일|상장일|결제일|기준일")  # 일시 는 전일시가 와 겹쳐 제외
SURVEY_RE = re.compile(r"BSI|SBHI|전망")  # 설문·전망 지표는 값의 종류를 단정하지 않는다
INDEX_RE = re.compile(r"지수|지표|\bDI\b|\bPMI\b|\bCSI\b")  # 설문·경기 지수(단위 없는 점수)
AMOUNT_RE = re.compile(r"지출|소득|수입액|수출액|매출|이익|손실|손익|자산|부채|자본금|자본|비용|수익$|충당금|차입금")  # 재무·경제 금액
# (시장, 분류) 별 기본 값 종류. 이름 규칙이 못 정한 항목에만 쓴다.
CATEGORY_KIND = {
    ("기업", "대차대조표"): "amount", ("기업", "손익계산서"): "amount", ("기업", "현금흐름표"): "amount",
    ("기업", "자본변동표"): "amount", ("기업", "재무비율"): "ratio",
    ("경제금융", "국민계정"): "amount", ("경제금융", "경기/기업/소비자"): "index", ("경제금융", "광고"): "index",
}
PRICE_RE = re.compile(r"가$|가격|호가|시가|고가|저가|종가|현재가|단가|금액|대금|환율|NAV")  # 가격·금액 계열. 지수값은 제외(unknown)


def split_enum(name: str) -> tuple[str, str | None, list[dict] | None, str | None]:
    """'구분(0&cl정상/1&cl권리락)' -> (기준명, enum 원문, enum 값 목록, 파싱 방식).
    값 목록 방식: '/'로 나뉘고 조각마다 코드값 표기가 하나면 slash, 구분자 없이 이어 붙은 것은 sequence(휴리스틱).
    어느 쪽도 깨끗하지 않으면 값 목록은 None 으로 두고 원문만 보존한다."""
    m = ENUM_RE.search(name)
    if not m:
        return name, None, None, None
    op = name.rfind("(", 0, m.start())
    if op <= 0:
        return name, None, None, None
    base = name[:op].strip()
    cp = name.rfind(")")
    raw = name[op + 1: cp if cp > op else len(name)]
    parts = raw.split("/")
    if all(len(ENUM_RE.findall(p)) == 1 for p in parts):
        vals = [{"value": p.split("&cl", 1)[0].strip(), "label": p.split("&cl", 1)[1].strip()} for p in parts]
        method = "slash"
    else:
        vals = [{"value": v, "label": lab.strip()} for v, lab in SEQ_RE.findall(raw)]
        method = "sequence"
    if not vals or any(not v["label"] for v in vals) or len({v["value"] for v in vals}) != len(vals):
        return base, raw, None, None
    return base, raw, vals, method


def guess_value_kind(base_name: str, has_enum: bool, applies: list[dict] | None = None) -> str:
    """항목명 → 분류 휴리스틱(자동추출). 모호하면 unknown 으로 둔다.
    값 종류: enum / date / ratio / qty / price / amount(재무·경제 금액) / index(설문·경기 지수) / unknown."""
    if has_enum:
        return "enum"
    if SURVEY_RE.search(base_name) and not RATIO_RE.search(base_name):
        return "index"
    for rx, kind in ((DATE_RE, "date"), (RATIO_RE, "ratio"), (QTY_RE, "qty"), (PRICE_RE, "price"), (INDEX_RE, "index"), (AMOUNT_RE, "amount")):
        if rx.search(base_name):
            return kind
    kinds = {CATEGORY_KIND.get((a.get("market"), a.get("category"))) for a in (applies or [])}
    return kinds.pop() if len(kinds) == 1 and None not in kinds else "unknown"


def dictionary_rows(records: list[dict]) -> list[dict]:
    """항목코드표 행에 출처 레코드 위치(시트:청크)를 붙인다."""
    rows: list[dict] = []
    for rec in records:
        if rec.get("type") != "excel" or DICT_SOURCE not in str(rec.get("source")):
            continue
        loc = ":".join(rec["id"].split(":")[3:]) or rec["id"]
        for r in dil.parse_dictionary([rec]):
            rows.append({**r, "loc": loc})
    return rows


def build_item_nodes(records: list[dict], as_of: str) -> tuple[list[dict], list[dict]]:
    by_code: dict[str, list[dict]] = collections.defaultdict(list)
    for r in dictionary_rows(records):
        by_code[r["code"]].append(r)
    nodes, conflicts = [], []
    for code in sorted(by_code, key=lambda c: (len(c), c)):
        rows = by_code[code]
        names = collections.Counter(r["name"] for r in rows)
        full_name = names.most_common(1)[0][0]  # 가장 많은 행의 이름을 기준명으로(동률은 먼저 나온 것)
        base, enum_raw, enum_values, enum_method = split_enum(full_name)
        alt = sorted(n for n in names if n != full_name)
        if alt:  # 명세 7절 규칙 2: 같은 코드에 이름이 다르면 검수 큐
            conflicts.append({"code": code, "names": dict(names)})
        applies = sorted({(r["function"], r["market"], r["category"]) for r in rows})
        node = {
            "id": f"check:item:{code}", "type": "item", "title": base, "code": code, "name": base,
            "aliases": [split_enum(n)[0] for n in alt],
            "value_kind": guess_value_kind(base, enum_raw is not None, [{"market": m, "category": c} for _, m, c in applies]), "value_kind_grade": "auto_extracted",
            "applies_to": [{"function": f, "market": m, "category": c} for f, m, c in applies],
            "definition_ref": [],
            "source": DICT_SOURCE, "source_locator": "; ".join(sorted({r["loc"] for r in rows})),
            "as_of": as_of, "visibility": "public", "grade": "manual_confirmed", "schema_version": SCHEMA_VERSION,
        }
        if enum_raw is not None:
            node["enum_raw"] = enum_raw
            node["enum_values"] = enum_values
            node["enum_parse"] = enum_method
        if alt:
            node["name_conflict"] = True
        nodes.append(node)
    return nodes, conflicts


def extract_signature(text: str, name: str) -> str | None:
    """매뉴얼 본문에서 '=NAME(' 으로 시작하는 첫 줄부터 괄호가 닫히는 지점까지를 서명으로 얻는다.
    닫는 괄호 뒤(같은 줄에 이어진 다음 절 제목 등)는 버린다."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if not line.lstrip().startswith(f"={name}("):
            continue
        buf = " ".join(ln.strip() for ln in lines[i:i + 6])
        depth, opened = 0, False
        for pos, ch in enumerate(buf):
            depth += (ch == "(") - (ch == ")")
            opened = opened or ch == "("
            if opened and depth == 0:
                return re.sub(r"\s+", " ", buf[:pos + 1]).strip()
        return None
    return None


def count_function_mentions(records: list[dict]) -> dict[str, set[str]]:
    idx = dcl.Index(records)
    seen: dict[str, set[str]] = collections.defaultdict(set)
    for case in idx.cases:
        for f in dcl.extract_case_keys(case, idx)["functions"]:
            seen[f["name"]].add(case["id"])
    return seen


def build_function_nodes(records: list[dict], as_of: str) -> list[dict]:
    by_id = {r["id"]: r for r in records}
    doc = by_id.get(FUNC_DOC_ID, {}).get("text", "")
    examples = by_id.get(FUNC_EXAMPLES_ID, {}).get("text", "")
    sheets = collections.defaultdict(set)
    for r in dictionary_rows(records):
        sheets[r["function"]].add(r["loc"].split(":")[0])
    mentions = count_function_mentions(records)
    nodes: list[dict] = []
    for name, (summary, shape, uses_codes) in FUNC_FACTS.items():
        sig = extract_signature(doc, name)
        node = {
            "id": f"check:func:{name}", "type": "function", "title": name, "name": name, "aliases": [],
            "signature": sig, "scope": summary, "data_shape": shape, "uses_item_codes": uses_codes,
            "item_table_sheet": name in sheets,  # 항목코드표에 해당 함수 시트가 있으면 함수 가용성의 근거
            "case_mentions": len(mentions.get(name, ())),
            "source": "CHECKPlus_Manual.pdf", "source_locator": f"PDF {FUNC_PAGES}쪽",
            "as_of": as_of, "visibility": "public", "grade": "manual_confirmed" if sig else "inferred",
            "verification": "documented" if sig else "signature_missing", "schema_version": SCHEMA_VERSION,
        }
        if name == "CTD":
            node["subfunctions"] = sorted(set(re.findall(r'=CTD\("([A-Z]+)"', examples)))
        nodes.append(node)
    # 매뉴얼 정의가 없는 함수: 사례에서만 언급된 것. 서명·범위를 만들지 않고 검수 대상으로 표시한다.
    for name in sorted(set(mentions) - set(FUNC_FACTS)):
        nodes.append({
            "id": f"check:func:{name}", "type": "function", "title": name, "name": name, "aliases": [],
            "signature": None, "scope": None, "data_shape": None, "uses_item_codes": None,
            "item_table_sheet": name in sheets, "case_mentions": len(mentions[name]),
            "source": "support_case", "source_locator": f"{len(mentions[name])}개 사례",
            "as_of": as_of, "visibility": "internal", "grade": "inferred",
            "verification": "mentioned_only", "schema_version": SCHEMA_VERSION,
        })
    return nodes


def build_tr_candidate_nodes(registry: list[dict], as_of: str) -> list[dict]:
    """TR 마스터에서 화면 문서가 아직 없는 TR(case_mentioned)을 check:tr:<TR> 후보 노드로 만든다.
    사례가 이 TR 을 언급해도 연결할 대상이 없어 의미 연결이 끊기던 문제를 푼다. 화면으로 확인되면 check:screen:<TR> 로 승격한다."""
    nodes = []
    for r in registry:
        if r.get("status") != "case_mentioned":
            continue
        tr, n = r["tr"], r.get("case_mentions", 0)
        nodes.append({
            "id": f"check:tr:{tr}", "type": "tr_candidate", "title": f"TR {tr} (화면 문서 없음)", "screen_code": tr,
            "aliases": [f"TR{tr}", f"화면 {tr}", tr], "status": "case_mentioned", "case_mentions": n,
            "possible_false_positive": n == 1, "source": "support_case", "source_locator": f"{n}개 사례",
            "as_of": as_of, "visibility": "public", "grade": "auto_extracted", "schema_version": SCHEMA_VERSION})
    return nodes


def validate_nodes(nodes: list[dict], links_path: Path | None = None) -> list[str]:
    errs: list[str] = []
    ids = collections.Counter(n["id"] for n in nodes)
    errs += [f"I2 중복 ID {i}" for i, n in ids.items() if n > 1]
    funcs = {n["name"] for n in nodes if n["type"] == "function"}
    for n in nodes:
        if n["type"] == "item":
            if not re.fullmatch(r"\d{4,6}", n["code"]) or n["id"] != f"check:item:{n['code']}":
                errs.append(f"item ID/코드 형식 오류 {n['id']}")
            if not n["applies_to"]:
                errs.append(f"I3 applies_to 비어 있음 {n['id']}")
            errs += [f"I1 {n['id']} 가 없는 함수 {a['function']} 참조" for a in n["applies_to"] if a["function"] not in funcs]
        if n["type"] == "function" and n["verification"] == "signature_missing":
            errs.append(f"함수 서명을 매뉴얼에서 찾지 못함 {n['id']}")
    if links_path and links_path.exists():
        idset = set(ids)
        for line in links_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            lk = json.loads(line)
            for end in (lk.get("from"), lk.get("to")):
                if isinstance(end, str) and end.startswith(("check:item:", "check:func:")) and end not in idset:
                    errs.append(f"I1 관계 대상 노드 없음 {end}")
    return errs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="항목·함수 노드 내보내기")
    ap.add_argument("--knowledge", type=Path, default=DEFAULT_KNOWLEDGE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--as-of", default=DEFAULT_AS_OF)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY, help="TR 마스터(후보 TR 노드 생성용). 없으면 건너뜀")
    ap.add_argument("--links", type=Path, default=None, help="관계 JSONL(예: tmp/case_links.jsonl)의 item/func 대상 실존 검사")
    ap.add_argument("--check", action="store_true", help="파일을 쓰지 않고 검증만 한다")
    args = ap.parse_args(argv)

    records = dcl.load_records(args.knowledge)
    items, conflicts = build_item_nodes(records, args.as_of)
    funcs = build_function_nodes(records, args.as_of)
    registry = [json.loads(l) for l in args.registry.read_text(encoding="utf-8").splitlines() if l.strip()] if args.registry.exists() else []
    tr_nodes = build_tr_candidate_nodes(registry, args.as_of)
    nodes = funcs + items + tr_nodes
    errs = validate_nodes(nodes, args.links)
    kinds = collections.Counter(n["value_kind"] for n in items)
    print(json.dumps({
        "items": len(items), "functions": len(funcs), "tr_candidates": len(tr_nodes), "name_conflicts": len(conflicts),
        "value_kind": dict(kinds), "enum_items": sum(1 for n in items if "enum_raw" in n),
        "enum_values_parsed": sum(1 for n in items if n.get("enum_values")),
        "enum_parse": dict(collections.Counter(n.get("enum_parse") for n in items if n.get("enum_values"))),
        "functions_documented": sum(1 for n in funcs if n["verification"] == "documented"),
        "functions_mentioned_only": [n["name"] for n in funcs if n["verification"] == "mentioned_only"],
        "violations": len(errs)}, ensure_ascii=False))
    for e in errs[:20]:
        print("위반:", e, file=sys.stderr)
    if errs:
        return 1
    if not args.check:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("".join(json.dumps(n, ensure_ascii=False) + "\n" for n in nodes), encoding="utf-8")
        print(f"wrote {args.out} ({args.out.stat().st_size // 1024} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

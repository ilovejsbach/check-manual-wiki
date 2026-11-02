#!/usr/bin/env python3
"""화면 항목명 <-> 항목코드표(HangMokCodeTable) 항목명 대조로 연결 후보를 만든다.

프로토타입. 표준 라이브러리만 사용한다. 결과는 *후보*이며 검수 전이다.

사용:
  uv run --offline --no-sync python scripts/derive_item_links.py \
      --out tmp/item_links.jsonl --report

출력 JSONL 한 줄:
  {screen_id, item_text, matched_codes:[{code,name,function,market,category}],
   match_type, confidence, ambiguous, source, n_codes}
  - function/market/category 는 같은 (code,name)이 여러 함수·시장에 있으면 정렬된 리스트다.
  - match_type: exact | normalized | partial
  - source: heading(화면 항목 소제목) | body(본문 어구)
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

DEFAULT_KNOWLEDGE = Path("knowledge/check-expert/knowledge.jsonl")
DICT_SOURCE = "HangMokCodeTable_ExcelPremium_update01.xlsx"
MAX_CODES_LISTED = 20
MIN_KEY_LEN = 2          # 정규화 후 이 길이 미만은 후보에서 제외
MIN_NORMALIZED_LEN = 3   # 괄호·숫자 제거 후 일치(normalized)에 필요한 최소 길이
MIN_PARTIAL_COVERAGE = 0.6  # 부분 일치: 사전명이 후보 문자열에서 차지하는 최소 비율
MIN_PARTIAL_LEN = 3     # 부분 일치에 쓰는 사전 항목명 최소 길이

# 너무 일반적이어서 항목명으로 보기 어려운 말(정규화 키 기준).
GENERIC = {
    "구분", "종목", "정보", "화면", "조회", "설명", "기능", "선택", "설정", "일자", "시간", "코드",
    "기간", "수량", "금액", "비율", "기타", "합계", "구성", "내용", "항목", "방법", "결과", "목록",
    "사용", "확인", "이동", "참고", "표시", "제공", "경우", "해당", "관련", "전체", "개별", "일반",
    "기준", "변경", "추가", "삭제", "저장", "검색", "입력", "출력", "화면설명", "건수", "순위",
    "명", "수", "값", "가격", "시장", "종류", "유형", "상태", "조건", "단위", "범위", "대상",
}


# --------------------------------------------------------------------------- 정규화

_PAREN = re.compile(r"\([^()]*\)|\[[^\[\]]*\]")


def norm_full(text: str) -> str:
    """공백 제거, 소문자, 끝 '*' 제거, 률->율 통일."""
    t = re.sub(r"\s+", "", text or "").lower()
    t = t.rstrip("*")
    return t.replace("률", "율")


def norm_base(text: str) -> str:
    """괄호 부가설명과 끝 숫자 접미(매도호가1)를 제거한 느슨한 키."""
    t = text or ""
    for _ in range(3):  # 중첩 괄호
        t2 = _PAREN.sub("", t)
        if t2 == t:
            break
        t = t2
    t = norm_full(t)
    # '(...' 로 열린 채 끝나는 경우 등 잔여 기호 제거
    t = re.sub(r"[()\[\]]", "", t)
    t = re.sub(r"\d+$", "", t) if re.search(r"[^\d]\d+$", t) else t
    return t


# --------------------------------------------------------------------------- 사전

def parse_dictionary(records: list[dict]) -> list[dict]:
    """excel 레코드의 마크다운 표 -> [{code,name,function,market,category}]."""
    rows: list[dict] = []
    for rec in records:
        if rec.get("type") != "excel" or DICT_SOURCE not in str(rec.get("source")):
            continue
        for line in (rec.get("text") or "").split("\n"):
            line = line.strip()
            if not line.startswith("|") or line.startswith("| ---"):
                continue
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) < 5 or cells[0] == "함수":
                continue
            # 항목명에 '|'가 섞여 셀이 늘어난 경우 마지막 셀들을 합친다
            name = "|".join(cells[4:])
            rows.append({"function": cells[0], "market": cells[1], "category": cells[2],
                         "code": cells[3], "name": name})
    return rows


class ItemDict:
    def __init__(self, rows: list[dict]):
        self.rows = rows
        # (code,name) -> 집계 엔트리
        entries: dict[tuple[str, str], dict] = {}
        for r in rows:
            e = entries.setdefault((r["code"], r["name"]), {
                "code": r["code"], "name": r["name"],
                "function": set(), "market": set(), "category": set()})
            e["function"].add(r["function"])
            e["market"].add(r["market"])
            e["category"].add(r["category"])
        self.entries = list(entries.values())
        self.by_full: dict[str, list[dict]] = collections.defaultdict(list)
        self.by_base: dict[str, list[dict]] = collections.defaultdict(list)
        for e in self.entries:
            self.by_full[norm_full(e["name"])].append(e)
            self.by_base[norm_base(e["name"])].append(e)
        self.max_base_len = max((len(k) for k in self.by_base), default=0)

    @property
    def n_names(self) -> int:
        return len({e["name"] for e in self.entries})

    @property
    def n_codes(self) -> int:
        return len({e["code"] for e in self.entries})


def _fmt(entries: list[dict]) -> list[dict]:
    out = []
    for e in sorted(entries, key=lambda x: (x["code"], x["name"])):
        out.append({"code": e["code"], "name": e["name"],
                    "function": sorted(e["function"]), "market": sorted(e["market"]),
                    "category": sorted(e["category"])})
    return out


# --------------------------------------------------------------------------- 후보 추출

_HEAD = re.compile(r"^###\s*화면\s*항목\s*\d+\s*[.\-)]?\s*(.*)$")
_CUT = re.compile(r"[•●※◆■▶]|(?<=[가-힣A-Za-z0-9)])\.\s|\.$")
_SPLIT = re.compile(r"[,，、·/•●※◆■▶:;\"“”'‘’~=+&→\-]|\s및\s|\s또는\s|\s/\s")
_NOISE_PUNCT = re.compile(r"^[\W\d_]+$")


_PARTICLE = re.compile(r"(으로|에서|에는|에도|을|를|은|는|의|에|로|과|와|도|만)$")


def heading_text(line: str) -> str | None:
    m = _HEAD.match(line.strip())
    if not m:
        return None
    return m.group(1).strip()


def _heading_core(rest: str) -> str:
    """소제목 뒤에 본문이 붙어 있는 경우를 잘라 항목명 부분만 남긴다."""
    cut = _CUT.search(rest)
    core = rest[: cut.start()] if cut else rest
    core = core.strip()
    return core[:40].strip()


def _chunks(text: str) -> list[str]:
    return [c.strip() for c in _SPLIT.split(text) if c and c.strip()]


def _ngrams(chunk: str, max_words: int = 3) -> list[str]:
    words = chunk.split()
    out = []
    for i in range(len(words)):
        for n in range(1, max_words + 1):
            if i + n <= len(words):
                out.append(" ".join(words[i:i + n]))
    return out


def candidate_ok(text: str) -> bool:
    k = norm_full(text)
    if len(k) < MIN_KEY_LEN or _NOISE_PUNCT.match(k):
        return False
    return norm_base(text) not in GENERIC and k not in GENERIC


def extract_candidates(text: str) -> list[tuple[str, str]]:
    """화면 본문 -> [(item_text, source)] (중복 제거, heading 우선)."""
    seen: dict[str, tuple[str, str]] = {}

    def add(t: str, src: str) -> None:
        t = t.strip(" \t.,()[]")
        if not t or not candidate_ok(t):
            return
        key = norm_full(t)
        if key not in seen or (seen[key][1] == "body" and src == "heading"):
            seen[key] = (t, src)

    for raw in (text or "").split("\n"):
        line = raw.strip()
        if not line or line.startswith(("#", ">", "|", "[원문")) and heading_text(line) is None:
            continue
        rest = heading_text(line)
        if rest is not None:
            core = _heading_core(rest)
            add(core, "heading")
            for ch in _chunks(core):
                add(ch, "heading")
            for ch in _chunks(rest[:80]):
                for g in _ngrams(ch):
                    add(g, "heading")
            for ch in _chunks(rest):
                for g in _ngrams(ch):
                    add(g, "body")
            continue
        if line.startswith("- TR ") or line.startswith("-"):
            line = line.lstrip("- ").strip()
        for ch in _chunks(line):
            for g in _ngrams(ch):
                add(g, "body")
    return list(seen.values())


# --------------------------------------------------------------------------- 매칭

def _score(match_type: str, source: str, n_codes: int) -> float:
    base = {"exact": 0.9, "normalized": 0.7, "partial": 0.4}[match_type]
    if source == "body":
        base *= 0.6
    if n_codes > 1:
        base *= 0.5
    return round(base, 3)


def match_candidate(item_text: str, source: str, d: ItemDict) -> dict | None:
    if not candidate_ok(item_text):
        return None
    full = norm_full(item_text)
    base = norm_base(item_text)
    particle_stripped = False
    if full not in d.by_full:
        # 조사 제거('등락률을' -> '등락률'); 사전에 정확히 있을 때만 인정
        stripped = _PARTICLE.sub("", full)
        if stripped != full and len(stripped) >= MIN_NORMALIZED_LEN and stripped in d.by_full:
            full = base = stripped
            particle_stripped = True
    hits: list[dict] = []
    mtype = None
    span = None
    if full in d.by_full:
        hits, mtype = d.by_full[full], "exact"
    elif base and base not in GENERIC and base in d.by_base and len(base) >= MIN_NORMALIZED_LEN:
        hits, mtype = d.by_base[base], "normalized"
    elif source == "heading" and len(base) >= MIN_PARTIAL_LEN:
        found: dict[str, list[dict]] = {}
        L = len(base)
        for i in range(L):
            for j in range(i + MIN_PARTIAL_LEN, min(L, i + d.max_base_len) + 1):
                sub = base[i:j]
                if sub == base or sub in GENERIC:
                    continue
                if sub in d.by_base and len(sub) / L >= MIN_PARTIAL_COVERAGE:
                    # 괄호 변형(수익률(KIS) 등)보다 이름이 정확히 같은 항목을 우선한다
                    found[sub] = d.by_full.get(sub) or d.by_base[sub]
        # 다른 히트에 완전히 포함되는 짧은 히트는 버린다
        keys = sorted(found, key=len, reverse=True)
        kept = [k for k in keys if not any(k != o and k in o for o in keys)]
        if kept:
            hits = [e for k in kept for e in found[k]]
            mtype = "partial"
            span = "|".join(kept)
    if not hits or mtype is None:
        return None
    if particle_stripped and mtype == "exact":
        mtype = "normalized"
    uniq = {(e["code"], e["name"]): e for e in hits}
    distinct_codes = {c for c, _ in uniq}
    n_codes = len(distinct_codes)
    listed = _fmt(list(uniq.values()))
    return {
        "item_text": item_text,
        "matched_codes": listed[:MAX_CODES_LISTED],
        "n_codes": n_codes,
        "match_type": mtype,
        "confidence": _score(mtype, source, n_codes),
        "ambiguous": n_codes > 1,
        "source": source,
        **({"matched_span": span} if span else {}),
    }


def derive_links(screens: list[dict], d: ItemDict) -> list[dict]:
    out = []
    for s in screens:
        sid = s.get("id") or s.get("screen_code")
        for item_text, source in extract_candidates(s.get("text", "")):
            m = match_candidate(item_text, source, d)
            if m:
                out.append({"screen_id": sid, **m})
    return out


# --------------------------------------------------------------------------- 보고

def build_report(links: list[dict], screens: list[dict], d: ItemDict) -> dict:
    linked = {l["screen_id"] for l in links}
    strong = {l["screen_id"] for l in links if not l["ambiguous"] and l["match_type"] != "partial"
              and l["source"] == "heading"}
    by_type = collections.Counter(l["match_type"] for l in links)
    by_src = collections.Counter((l["source"], l["match_type"]) for l in links)
    return {
        "dictionary_rows": len(d.rows),
        "dictionary_distinct_names": d.n_names,
        "dictionary_distinct_codes": d.n_codes,
        "screens_total": len(screens),
        "screens_linked": len(linked),
        "screens_linked_ratio": round(len(linked) / max(1, len(screens)), 4),
        "screens_linked_by_unambiguous_heading": len(strong),
        "links_total": len(links),
        "links_ambiguous": sum(l["ambiguous"] for l in links),
        "by_match_type": dict(by_type),
        "by_source_and_type": {f"{k[0]}/{k[1]}": v for k, v in by_src.items()},
    }


def load_records(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--knowledge", type=Path, default=DEFAULT_KNOWLEDGE)
    ap.add_argument("--out", type=Path, help="후보 링크 JSONL 출력 경로")
    ap.add_argument("--report", action="store_true", help="요약 통계를 stdout 에 JSON 으로 출력")
    args = ap.parse_args(argv)

    records = load_records(args.knowledge)
    d = ItemDict(parse_dictionary(records))
    screens = [r for r in records if r.get("type") == "screen"]
    links = derive_links(screens, d)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8") as fh:
            for l in links:
                fh.write(json.dumps(l, ensure_ascii=False) + "\n")
    if args.report:
        print(json.dumps(build_report(links, screens, d), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

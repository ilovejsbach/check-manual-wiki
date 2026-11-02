#!/usr/bin/env python3
"""CHECK 화면/매뉴얼 레코드 -> 자매 위키(자본시장 개념·기관·법령) 브리지 후보 생성기.

읽기 전용. 외부 모델/네트워크 호출 없음(법령 위키는 미리 clone 한 ids.json 만 읽는다).
법령 조문 링크는 사람 검수 전까지 확정이 아닌 '후보'(review_status=needs_review)다.

사용:
  uv run --offline --no-sync python scripts/build_bridge_candidates.py \
      --wiki-dir <wiki-korean-capital-markets/wiki> --law-ids <kcm_law/ids.json> \
      --knowledge knowledge/check-expert/knowledge.jsonl --out <tmp>/bridge.jsonl
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import quote

CONCEPT_BASE = "https://ilovejsbach.github.io/capital_market_wiki/"
LAW_BASE = "https://ilovejsbach.github.io/kcm_law/"
LEGAL_NOTICE = "법적 효력 없는 참조용 초안(kcm_law). 사람 검수 전까지 후보이며 확정 아님."
KR_JURISDICTIONS = {"kr", "korea", "한국", "대한민국"}
SISTER_DIRS = {
    "concepts": ("concept", "explains_concept"),
    "institutions": ("institution", "related_institution"),
    "regulations": ("regulation", "regulated_by"),
    "metrics": ("metric", "explains_concept"),
}
LAW_KIND_RANK = {"법률": 0, "시행령": 1, "시행규칙": 2, "고시": 3}
LAW_MAX_PER_RECORD = 3
LAW_MAX_PER_TERM = 3

# 너무 일반적이라 개념 키/CHECK 용어 어느 쪽으로도 쓰지 않는 말(정규화 형태).
GENERIC = {
    "종합", "현재가", "시세", "일별", "추이", "현황", "거래", "시장", "주식", "채권", "선물", "옵션",
    "외환", "해외", "기업", "관심", "차트", "조회", "설정", "기타", "목록", "정보", "종목", "지수",
    "가격", "수량", "금액", "비교", "분석", "상세", "요약", "일반", "기본", "주요", "전체", "화면",
    "개요", "설명", "항목", "특이사항", "관련화면", "원문근거", "기간별", "종목별", "일자별",
    "시간대별", "투자자", "매매", "매수", "매도", "체결", "호가", "잔고", "순위", "상위", "하위",
    "업종", "테마", "뉴스", "공시", "리포트", "자료", "서비스", "이론", "결제", "청약", "신용",
    "법", "법률", "규정", "목적", "정의", "적용범위", "대통령령", "금융", "자본", "자본시장",
    "금융투자", "금융투자업", "투자", "투자자", "시장조성", "펀드", "배당",
    "call", "put", "spot", "rate", "tick", "high", "low", "open", "close", "list", "type", "data",
}
GENERIC_HEADINGS = {"화면개요", "화면설명", "특이사항", "관련화면", "원문근거", "화면항목", "참고"}


# ---------------------------------------------------------------- 텍스트 유틸
def normalize(s: str) -> str:
    s = unicodedata.normalize("NFKC", s or "").lower()
    return re.sub(r"[^0-9a-zㄱ-ㆎ가-힣]", "", s)


def has_hangul(s: str) -> bool:
    return bool(re.search(r"[ㄱ-ㆎ가-힣]", s))


def usable_term(raw: str) -> bool:
    """일반어·짧은 별칭 제외 규칙. raw 는 정규화 전 원문."""
    n = normalize(raw)
    if not n or n in GENERIC or n.isdigit():
        return False
    if has_hangul(n):
        return len(n) >= 3
    # 영문/숫자: 대문자 약어(ETF, ELS, KRX)는 3자부터, 그 외는 4자부터
    letters = re.sub(r"[^A-Za-z]", "", raw)
    if letters and letters.isupper() and len(letters) >= 3:
        return True
    return len(n) >= 4 and not n.isdigit()


# ---------------------------------------------------------------- 자매 위키 색인
def parse_frontmatter(text: str) -> dict:
    """title/aliases/jurisdiction/type 만 뽑는 최소 YAML 파서(인라인·블록 리스트 지원)."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out: dict = {}
    lines = m.group(1).split("\n")
    i = 0
    while i < len(lines):
        km = re.match(r"^([A-Za-z_]+):\s*(.*)$", lines[i])
        i += 1
        if not km:
            continue
        key, val = km.group(1), km.group(2).strip()
        if key not in ("type", "title", "aliases", "jurisdiction"):
            continue
        if key == "aliases":
            items: list[str] = []
            if val.startswith("["):
                items = [x for x in re.findall(r'"([^"]*)"|\'([^\']*)\'|([^,\[\]]+)', val)]
                items = [(a or b or c).strip() for a, b, c in items]
            elif val == "":
                while i < len(lines) and re.match(r"^\s*-\s+", lines[i]):
                    items.append(re.sub(r"^\s*-\s+", "", lines[i]).strip().strip("\"'"))
                    i += 1
            out["aliases"] = [x for x in items if x]
        else:
            out[key] = val.strip().strip("\"'")
    return out


def is_korean(jur: str | None) -> bool:
    return (jur or "").strip().lower() in KR_JURISDICTIONS


def build_sister_index(wiki_dir: Path) -> tuple[list[dict], Counter]:
    entries: list[dict] = []
    skipped: Counter = Counter()
    for sub, (kind, relation) in SISTER_DIRS.items():
        d = wiki_dir / sub
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.md")):
            fm = parse_frontmatter(p.read_text(encoding="utf-8"))
            title = fm.get("title") or p.stem
            jur = fm.get("jurisdiction")
            # 한국 관할만: 기관·규정은 jurisdiction 필수 KR. 개념·지표는 필드 없음(=한국 서적 기반)이라 통과.
            if kind in ("institution", "regulation") and not is_korean(jur):
                skipped[f"{kind}:non_kr"] += 1
                continue
            if kind in ("concept", "metric") and jur and not is_korean(jur):
                skipped[f"{kind}:non_kr"] += 1
                continue
            entries.append({
                "id": f"{kind}:{p.stem}", "kind": kind, "relation": relation, "title": title,
                "aliases": fm.get("aliases", []), "jurisdiction": "KR" if jur is None or is_korean(jur) else jur,
                "jurisdiction_declared": jur is not None,
                # 사이트 URL 은 파일명(슬러그) 기준. 실제 사이트에서 /<슬러그>.html 및 /<종류>/<슬러그>.html 모두 200 확인.
                "url": f"{CONCEPT_BASE}{p.stem}.html",
            })
    return entries, skipped


def keys_for(entry: dict) -> set[str]:
    """제목, 별칭, 제목 속 괄호 안/밖 표기에서 사용 가능한 정규화 키 집합."""
    raws = [entry["title"], *entry.get("aliases", [])]
    expanded = []
    for r in raws:
        expanded.append(r)
        m = re.match(r"^(.*?)\s*[\(（](.+?)[\)）]\s*$", r)
        if m:
            expanded += [m.group(1), m.group(2)]
    return {normalize(r) for r in expanded if usable_term(r)}


def build_key_map(entries: list[dict]) -> dict[str, list[dict]]:
    km: dict[str, list[dict]] = defaultdict(list)
    for e in entries:
        for k in keys_for(e):
            if e not in km[k]:
                km[k].append(e)
    return km


# ---------------------------------------------------------------- 법령 색인
LAW_TITLE_RE = re.compile(r"^(?P<law>.+?)\s+(?P<art>제[\d\-]+조(?:의\d+)?)\s*\((?P<subject>.+)\)\s*$")


def build_law_index(ids_json: Path) -> list[dict]:
    docs = json.loads(ids_json.read_text(encoding="utf-8")).get("docs", {})
    out = []
    for lid, d in docs.items():
        if d.get("status") != "published":
            continue
        title = d.get("title", "")
        m = LAW_TITLE_RE.match(title)
        if not m:
            continue
        parts = d["path"].split("/")
        kind = parts[1] if len(parts) > 1 else ""
        if kind not in LAW_KIND_RANK:
            continue
        subj = m.group("subject")
        if not usable_term(subj):
            continue
        out.append({
            "id": lid, "title": title, "subject": subj, "nsubject": normalize(subj), "kind": kind,
            "url": LAW_BASE + quote(d["path"]) + ".html",
        })
    out.sort(key=lambda e: (LAW_KIND_RANK[e["kind"]], e["id"]))
    return out


# ---------------------------------------------------------------- CHECK 용어 추출
def check_terms(rec: dict) -> list[dict]:
    """레코드에서 (원문, 출처) 용어 목록. 출처: title / category / heading."""
    terms: list[dict] = []
    title = rec.get("title") or ""
    title = re.sub(r"^\s*[A-Za-z]*\d+\s*-\s*", "", title)       # 앞 화면번호
    title = re.sub(r"\s*-\s*\d+\s*$", "", title)                 # 뒤 화면번호
    for seg in re.split(r"\s*[>/]\s*", title):
        seg = seg.strip()
        if seg:
            terms.append({"raw": seg, "src": "title"})
        m = re.match(r"^(.*?)\s*[\(（](.+?)[\)）]\s*$", seg)
        if m:
            terms += [{"raw": m.group(1), "src": "title"}, {"raw": m.group(2), "src": "title"}]
    cat = rec.get("category")
    if cat:
        terms.append({"raw": cat, "src": "category"})
    for h in re.findall(r"^#{2,4}\s+(.+)$", rec.get("text") or "", re.M):
        h = re.sub(r"^화면 항목\s*\d+\.?\s*", "", h).strip()
        if not h or len(h) > 40 or normalize(h) in GENERIC_HEADINGS:
            continue
        terms.append({"raw": h, "src": "heading"})
    return [t for t in terms if usable_term(t["raw"])]


BASE_CONF = {("exact", "title"): 0.85, ("exact", "heading"): 0.55, ("exact", "category"): 0.4,
             ("contains", "title"): 0.45, ("contains", "heading"): 0.3, ("contains", "category"): 0.2}


def contains_match(nterm: str, key: str, raw: str = "") -> bool:
    """key 가 nterm 의 부분문자열인지. 한글 키는 4자 이상. 영문 키는 토큰 경계에서만,
    대문자 약어 토큰(ETF, ELW)은 3자부터 허용 (KOSDAQ150 안의 KOSDAQ 같은 오탐 방지)."""
    if key == nterm or key not in nterm:
        return False
    if has_hangul(key):
        return len(key) >= 4
    for tok in re.split(r"[^0-9A-Za-z]+", raw):
        if normalize(tok) == key:
            return len(key) >= 4 or (tok.isupper() and len(key) >= 3)
    return False


def match_sister(rec: dict, key_map: dict[str, list[dict]]) -> list[dict]:
    best: dict[str, dict] = {}
    for t in check_terms(rec):
        nt = normalize(t["raw"])
        hits: list[tuple[str, str]] = []  # (key, match_type)
        if nt in key_map:
            hits.append((nt, "exact"))
        else:
            hits += [(k, "contains") for k in key_map if contains_match(nt, k, t["raw"])]
        for key, mtype in hits:
            targets = key_map[key]
            ambiguous = len(targets) > 1
            for e in targets:
                conf = BASE_CONF[(mtype, t["src"])] * (0.7 if ambiguous else 1.0)
                prev = best.get(e["id"])
                if prev is None or conf > prev["confidence"]:
                    best[e["id"]] = {
                        "entry": e, "confidence": round(conf, 3), "match_type": f"{mtype}_{t['src']}",
                        "ambiguous": ambiguous, "matched_term": t["raw"], "key": key,
                    }
    return list(best.values())


def match_law(rec: dict, sister_hits: list[dict], laws: list[dict]) -> list[dict]:
    """CHECK 용어 + 매칭된 개념의 제목/별칭 키워드로 조문 제목(괄호 주제)을 찾는다. 항상 후보."""
    probes: list[tuple[str, str]] = []  # (정규화 키워드, 출처표시)
    for t in check_terms(rec):
        if t["src"] == "title":
            probes.append((normalize(t["raw"]), f"check_title:{t['raw']}"))
    for h in sister_hits:
        if h["entry"]["kind"] in ("concept", "regulation"):
            for k in keys_for(h["entry"]):
                probes.append((k, f"concept:{h['entry']['title']}"))
    found: dict[str, dict] = {}
    for key, origin in probes:
        n_term = 0
        for law in laws:
            if n_term >= LAW_MAX_PER_TERM:
                break
            if law["nsubject"] == key:
                mtype, conf = "law_subject_exact", 0.5
            elif len(key) >= 4 and key in law["nsubject"]:
                mtype, conf = "law_subject_keyword", 0.3
            else:
                continue
            if law["kind"] != "법률":
                conf -= 0.05
            n_term += 1
            prev = found.get(law["id"])
            if prev is None or conf > prev["confidence"]:
                found[law["id"]] = {"law": law, "confidence": round(conf, 3), "match_type": mtype, "origin": origin}
    ranked = sorted(found.values(), key=lambda f: (-f["confidence"], LAW_KIND_RANK[f["law"]["kind"]], f["law"]["id"]))
    return ranked[:LAW_MAX_PER_RECORD]


# ---------------------------------------------------------------- 후보 생성
def build_candidates(records: list[dict], entries: list[dict], laws: list[dict]) -> list[dict]:
    key_map = build_key_map(entries)
    out: list[dict] = []
    for rec in records:
        hits = match_sister(rec, key_map)
        for h in sorted(hits, key=lambda x: (-x["confidence"], x["entry"]["id"])):
            e = h["entry"]
            out.append({
                "check_id": rec["id"], "target_kind": e["kind"], "target_id": e["id"],
                "target_title": e["title"], "target_url": e["url"], "relation": e["relation"],
                "match_type": h["match_type"], "confidence": h["confidence"],
                "jurisdiction": e["jurisdiction"], "review_status": "auto_unreviewed",
                "ambiguous": h["ambiguous"], "matched_term": h["matched_term"],
            })
        for f in match_law(rec, hits, laws):
            law = f["law"]
            out.append({
                "check_id": rec["id"], "target_kind": "law_article", "target_id": law["id"],
                "target_title": law["title"], "target_url": law["url"], "relation": "regulated_by",
                "match_type": f["match_type"], "confidence": f["confidence"],
                "jurisdiction": "KR", "review_status": "needs_review", "ambiguous": False,
                "matched_term": f["origin"], "legal_notice": LEGAL_NOTICE,
            })
    return out


def load_records(path: Path, types: set[str]) -> list[dict]:
    recs = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                r = json.loads(line)
                # enrichment(문의 대응 묶음) 레코드는 화면 레코드의 파생물이라 제외해 중복 집계를 막는다.
                if r.get("type") in types and not str(r.get("id", "")).startswith("check:enrichment:"):
                    recs.append(r)
    return recs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--wiki-dir", type=Path, required=True)
    ap.add_argument("--law-ids", type=Path, required=True)
    ap.add_argument("--knowledge", type=Path, default=Path("knowledge/check-expert/knowledge.jsonl"))
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--types", default="screen,manual,excel")
    a = ap.parse_args(argv)

    entries, skipped = build_sister_index(a.wiki_dir)
    laws = build_law_index(a.law_ids)
    records = load_records(a.knowledge, set(a.types.split(",")))
    cands = build_candidates(records, entries, laws)

    a.out.parent.mkdir(parents=True, exist_ok=True)
    with a.out.open("w", encoding="utf-8") as fh:
        for c in cands:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")
    meta = {
        "legal_notice": LEGAL_NOTICE, "sister_index": dict(Counter(e["kind"] for e in entries)),
        "sister_skipped_non_kr": dict(skipped), "law_articles_indexed": len(laws),
        "records_scanned": len(records), "candidates": len(cands),
    }
    a.out.with_suffix(".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(meta, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())

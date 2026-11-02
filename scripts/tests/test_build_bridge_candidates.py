import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_bridge_candidates as b


def write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def make_wiki(root: Path) -> Path:
    w = root / "wiki"
    write(w / "concepts" / "short-selling.md", '---\ntype: concept\ntitle: 공매도\naliases: [차입공매도]\n---\n본문')
    write(w / "concepts" / "etf.md", "---\ntype: concept\ntitle: \"상장지수집합투자기구\"\naliases:\n- \"ETF\"\n- \"상장지수펀드\"\n---\n")
    write(w / "concepts" / "bond.md", '---\ntype: concept\ntitle: "채권"\naliases: ["BD"]\n---\n')  # 일반어 + 짧은 별칭
    write(w / "concepts" / "clearing-a.md", '---\ntype: concept\ntitle: "청산제도"\naliases: ["결제동기"]\n---\n')
    write(w / "concepts" / "clearing-b.md", '---\ntype: concept\ntitle: "청산기관"\naliases: ["결제동기"]\n---\n')
    write(w / "institutions" / "krx.md", '---\ntype: institution\ntitle: "한국거래소"\naliases: ["KRX"]\njurisdiction: KR\n---\n')
    write(w / "institutions" / "nyse.md", '---\ntype: institution\ntitle: "뉴욕증권거래소"\naliases: ["NYSE"]\njurisdiction: "US"\n---\n')
    write(w / "regulations" / "cma.md", '---\ntype: regulation\ntitle: 자본시장법\naliases: ["FISCMA"]\njurisdiction: KR\n---\n')
    write(w / "regulations" / "reg-nms.md", '---\ntype: regulation\ntitle: "Regulation NMS"\njurisdiction: US\n---\n')
    return w


def law_ids(root: Path) -> Path:
    docs = {
        "law:cma:act:180-5": {"path": "자본시장법/법률/제6편/법-제180조의5", "title": "법 제180조의5 (차입공매도를 위한 대차거래)", "status": "published"},
        "law:cma:act:234": {"path": "자본시장법/법률/제9편/법-제234조", "title": "법 제234조 (상장지수집합투자기구)", "status": "published"},
        "law:cma:act:1": {"path": "자본시장법/법률/제1편/법-제1조", "title": "법 제1조 (목적)", "status": "published"},
        "law:cma:map": {"path": "자본시장법/지도/x", "title": "법 제9조 (상장지수집합투자기구 지도)", "status": "published"},
    }
    p = root / "ids.json"
    p.write_text(json.dumps({"docs": docs}, ensure_ascii=False), encoding="utf-8")
    return p


def screen(id_, title, text="", category=None):
    return {"id": id_, "type": "screen", "title": title, "category": category, "text": text, "aliases": []}


def run(tmp_path, records):
    w = make_wiki(tmp_path)
    entries, skipped = b.build_sister_index(w)
    laws = b.build_law_index(law_ids(tmp_path))
    return entries, skipped, laws, b.build_candidates(records, entries, laws)


def test_frontmatter_inline_and_block_aliases(tmp_path):
    w = make_wiki(tmp_path)
    inline = b.parse_frontmatter((w / "concepts" / "short-selling.md").read_text(encoding="utf-8"))
    block = b.parse_frontmatter((w / "concepts" / "etf.md").read_text(encoding="utf-8"))
    assert inline["aliases"] == ["차입공매도"]
    assert block["aliases"] == ["ETF", "상장지수펀드"]


def test_only_korean_jurisdiction_institutions_and_regulations(tmp_path):
    entries, skipped, _, _ = run(tmp_path, [])
    ids = {e["id"] for e in entries}
    assert "institution:krx" in ids and "regulation:cma" in ids
    assert "institution:nyse" not in ids and "regulation:reg-nms" not in ids
    assert skipped["institution:non_kr"] == 1 and skipped["regulation:non_kr"] == 1


def test_generic_and_short_terms_excluded():
    assert not b.usable_term("채권")        # 일반어
    assert not b.usable_term("종합")
    assert not b.usable_term("BD")          # 짧은 영문
    assert not b.usable_term("VI")
    assert not b.usable_term("1300")
    assert b.usable_term("ETF") and b.usable_term("공매도") and b.usable_term("KRX")


def test_generic_concept_not_matched(tmp_path):
    _, _, _, cands = run(tmp_path, [screen("check:screen:1", "3011 - 채권 종합", category="채권")])
    assert [c for c in cands if c["target_id"] == "concept:bond"] == []


def test_exact_title_match_has_high_confidence_and_fields(tmp_path):
    _, _, _, cands = run(tmp_path, [screen("check:screen:2", "4104 - 공매도")])
    c = [x for x in cands if x["target_id"] == "concept:short-selling"][0]
    assert c["relation"] == "explains_concept" and c["match_type"] == "exact_title"
    assert c["confidence"] >= 0.8 and c["jurisdiction"] == "KR" and not c["ambiguous"]
    assert c["target_url"] == b.CONCEPT_BASE + "short-selling.html"


def test_ambiguous_alias_is_flagged_and_downweighted(tmp_path):
    _, _, _, cands = run(tmp_path, [screen("check:screen:3", "5000 - 결제동기")])
    hits = [x for x in cands if x["target_kind"] == "concept"]
    assert len(hits) == 2 and all(h["ambiguous"] for h in hits)
    assert all(h["confidence"] < 0.85 * 0.8 for h in hits)


def test_ascii_acronym_token_boundary(tmp_path):
    _, _, _, cands = run(tmp_path, [
        screen("check:screen:4", "1440 - ETF 현재가"),
        screen("check:screen:5", "9999 - ETFX지수"),
    ])
    assert any(c["check_id"] == "check:screen:4" and c["target_id"] == "concept:etf" for c in cands)
    assert not any(c["check_id"] == "check:screen:5" and c["target_kind"] == "concept" for c in cands)


def test_institution_relation_and_non_kr_never_linked(tmp_path):
    _, _, _, cands = run(tmp_path, [screen("check:screen:6", "3227 - 주요금리 > KRX"), screen("check:screen:7", "3228 - NYSE")])
    assert any(c["relation"] == "related_institution" and c["target_id"] == "institution:krx" for c in cands)
    assert not any("nyse" in c["target_id"] for c in cands)


def test_law_candidates_always_needs_review_with_notice(tmp_path):
    _, _, laws, cands = run(tmp_path, [screen("check:screen:8", "3960 - 대차거래 > 종합"), screen("check:screen:9", "1440 - ETF 현재가")])
    law = [c for c in cands if c["target_kind"] == "law_article"]
    assert law and all(c["review_status"] == "needs_review" and c["relation"] == "regulated_by" for c in law)
    assert all("참조용 초안" in c["legal_notice"] for c in law)
    ids = {c["target_id"] for c in law}
    assert "law:cma:act:180-5" in ids and "law:cma:act:234" in ids
    # 목적(짧은 주제)·지도 문서는 색인 제외
    assert "law:cma:act:1" not in {l["id"] for l in laws} and "law:cma:map" not in {l["id"] for l in laws}
    assert all(c["target_url"].startswith(b.LAW_BASE) and c["target_url"].endswith(".html") for c in law)


def test_enrichment_records_skipped_on_load(tmp_path):
    p = tmp_path / "k.jsonl"
    rows = [screen("check:screen:1", "a"), {"id": "check:enrichment:screen:1", "type": "manual", "title": "x"}]
    p.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows), encoding="utf-8")
    got = b.load_records(p, {"screen", "manual"})
    assert [r["id"] for r in got] == ["check:screen:1"]

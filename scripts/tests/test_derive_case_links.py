"""derive_case_links 단위 테스트. 모든 사례 문장은 합성이며 실데이터를 복사하지 않았다."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import derive_case_links as dcl  # noqa: E402

DICT_TEXT = "\n".join([
    "| 함수 | 시장 | 카테고리 | 항목코드 | 항목명 |",
    "| --- | --- | --- | --- | --- |",
    "| CH | 상품 | 호가 | 14501 | 매도호가1 |",
    "| CT | 주식 | 호가 | 14501 | 매도호가1 |",
    "| CH | 주식 | 시세 | 15001 | 현재가 |",
    "| CH | 주식 | 시세 | 15015 | 거래량 |",
    "| CH | 주식 | 시세 | 15016 | 체결수량 |",
    "| CH | 주식 | 시세 | 15017 | 체결수량 |",
    "| CH | 주식 | 시세 | 16220 | 기초자산코드 |",
    "| CT | 주식 | 시세 | 4017 | 이론가괴리율 |",
    "| CT | 주식 | 시세 | 4018 | 괴리율 |",
    "| CT | 주식 | 시세 | 30001 | NAV |",
])


def rec(rid, typ, title, text="", code=None, loc=None, **kw):
    base = {"schema_version": "1.0", "id": rid, "type": typ, "title": title, "text": text, "screen_code": code,
            "source_locator": loc, "related_ids": [], "relationships": [], "case_type": None, "case_topic": None,
            "source": "x"}
    base.update(kw)
    return base


def case(cid, situation, response="", ctype="faq", related=None, topic="주식"):
    text = (f"# 제목\n\n> 안내\n\n## 사용자가 겪은 상황\n\n{situation}\n\n## 당시 대응\n\n{response}\n\n"
            f"## 의미 분류\n\n- 대표 유형: x\n\n## 검증할 사항\n\n- [ ] x\n")
    return rec(cid, "support_case", "사례", text, loc="20260101!row:1", case_type=ctype, case_topic=topic,
               related_ids=related or [], review_status="candidate")


def base_records():
    return [
        rec("check:screen:4101", "screen", "4101 - 현재가 종합표", code="4101", loc="100-101"),
        rec("check:screen:4114", "screen", "4114 - 주식선물 시세표", code="4114", loc="200-200"),
        rec("check:screen:1542", "screen", "1542 - 구성종목 상대성과 분석", code="1542", loc="300-301"),
        rec("check:screen:1002:종합", "screen", "1002 - 세계지수종합", code="1002", loc="60-62"),
        rec("check:screen:1002:해외", "screen", "1002 - 세계지수종합", code="1002", loc="771-773"),
        rec("check:screen:4563", "screen", "4563 - 스프레드", code="4563", loc="400-400"),
        rec("check:manual:source-page-index", "manual", "원문 페이지 색인", "p"),
        rec("check:manual:엑셀-프리미엄:주요-함수-설명", "manual", "주요 함수 설명", "CT CH 함수 설명"),
        rec("check:manual:통합검색:기능-개요", "manual", "기능 개요", "통합검색 기능"),
        rec("check:excel:manual:함수-설명", "excel", "함수 설명", "함수"),
        rec("check:excel:항목코드표:CH:001", "excel", "항목코드표", DICT_TEXT,
            source="HangMokCodeTable_ExcelPremium_update01.xlsx"),
        rec("check:enrichment:unmapped:abc123", "manual", "공식 문서 연결 대기 — 기타", "대기"),
    ]


def make_index(cases):
    return dcl.Index(base_records() + cases)


def keys_of(situation, response="", ctype="faq"):
    c = case("check:support-case:t1", situation, response, ctype)
    idx = make_index([c])
    return dcl.extract_case_keys(c, idx), idx, c


def codes(keys, kind=None):
    return {f["code"] for f in keys["screen_codes"] if kind is None or f["kind"] == kind}


# 1 -------------------------------------------------------------------------
def test_screen_code_tr_and_context_forms():
    k, *_ = keys_of("TR 4101 이 느립니다. tr4114도 마찬가지입니다. 1542 - 상대성과 화면도 봤고 1002번 화면은 정상입니다.")
    assert codes(k, "tr") == {"4101", "4114"}
    assert "1542" in codes(k, "ctx") and "1002" in codes(k, "ctx")


# 2 -------------------------------------------------------------------------
def test_false_positive_guard_for_years_amounts_dates_times():
    k, *_ = keys_of("2026년 11월에 4101원이 아니라 4114주를 샀고 09:30 에 1,542 건과 3.4101 값이 있고 2026-4101 로 기록")
    assert codes(k) == set()


# 3 -------------------------------------------------------------------------
def test_bare_number_is_weak_and_unknown_code_is_unresolved():
    k, *_ = keys_of("4101 하고 9999 화면 비교")
    assert any(f["code"] == "4101" and f["kind"] == "bare" and f["grade"] == "inferred" for f in k["screen_codes"])
    assert "9999" not in codes(k) and {u["code"] for u in k["unresolved_screen_codes"]} == {"9999"}


# 4 -------------------------------------------------------------------------
def test_title_match_strength():
    k, *_ = keys_of("구성종목 상대성과 분석 보는 법과 스프레드 가 궁금합니다")
    kinds = {f["code"]: f["kind"] for f in k["screen_titles"]}
    assert kinds["1542"] == "title"          # 긴 제목은 강함
    assert kinds["4563"] == "title_weak"      # 짧은 일반어 제목은 약함
    k2, *_ = keys_of("'스프레드' 화면이 어디죠")
    assert {f["code"]: f["kind"] for f in k2["screen_titles"]}["4563"] == "title"  # 문맥(따옴표)이 있으면 강함


# 5 -------------------------------------------------------------------------
def test_function_extraction_and_lookalikes():
    k, *_ = keys_of('=CTD("a","b") 와 CH ( "x" ) 그리고 CT 함수, =CLIST(1) 그리고 CHECK(1) ACT(2)')
    by = {f["name"]: f for f in k["functions"]}
    assert set(by) == {"CTD", "CH", "CT", "CLIST"}
    assert by["CTD"]["form"] == "call" and by["CT"]["form"] == "mention"
    assert by["CLIST"]["known"] is False and by["CTD"]["known"] is True


# 6 -------------------------------------------------------------------------
def test_item_code_context_and_names_with_ambiguity():
    k, *_ = keys_of('항목코드 14501 을 =CT("005930","15001") 로 받고 체결수량 과 이론가괴리율, 전화 15016 번')
    by_code = {f["codes"][0]: f for f in k["item_codes"] if f["match"] == "code"}
    assert set(by_code) == {"14501", "15001"}            # 맥락 없는 5자리(15016)는 제외
    names = {f["name"]: f for f in k["item_codes"] if f["match"] == "name"}
    assert names["체결수량"]["ambiguous"] and names["체결수량"]["n_codes"] == 2 and names["체결수량"]["codes"] == ["15016", "15017"]
    assert "이론가괴리율" in names and "괴리율" not in names  # 최장 일치


# 7 -------------------------------------------------------------------------
def test_item_name_inside_screen_title_and_ascii_boundary():
    k, *_ = keys_of("4101 현재가 화면 에서 nav 와 navigation 을 봅니다")
    names = {f["name"] for f in k["item_codes"] if f["match"] == "name"}
    assert "현재가" not in names          # 화면 제목의 일부
    assert "NAV" in names                  # 단독 영문 토큰은 인정
    k2, *_ = keys_of("navigation 만 있음")
    assert not [f for f in k2["item_codes"] if f["name"] == "NAV"]


# 8 -------------------------------------------------------------------------
def test_error_strings_separate_mask_tokens_and_hash_non_errors():
    k, *_ = keys_of('"사용 권한이 없습니다" 가 뜨고 [NUMBER] [IDENTIFIER] 가 있고 "현재가 창" 도 있음 오류 코드 -2147')
    assert any(e.get("value") == "사용 권한이 없습니다" for e in k["error_strings"])
    assert any(e["kind"] == "errcode" for e in k["error_strings"])
    assert all("value" not in q for q in k["quoted_strings"])      # 오류가 아닌 인용은 해시만
    assert k["mask_tokens"].get("[NUMBER]") == 1 and k["mask_tokens"].get("[IDENTIFIER]") == 1
    assert not [e for e in k["error_strings"] if e["has_mask_token"]]


# 9 -------------------------------------------------------------------------
def test_no_body_text_copied_to_outputs():
    sentence = "아주특이한문장조각XYZ가 포함된 문의입니다"
    c = case("check:support-case:t9", f"TR 4101 {sentence}", "4114 화면 안내")
    idx = make_index([c])
    keys = dcl.extract_case_keys(c, idx)
    links = dcl.build_links([keys], idx, "2026-11-02")
    blob = json.dumps(keys, ensure_ascii=False) + json.dumps(links, ensure_ascii=False)
    assert "아주특이한문장조각XYZ" not in blob
    assert all(l["evidence"]["record_id"] == "check:support-case:t9" for l in links if l["relation"] == "about_screen")


# 10 ------------------------------------------------------------------------
def test_typed_relations_and_grades():
    c = case("check:support-case:t10", 'TR 4101 에서 =CT("005930","15001") 로 거래량 을 가져오는 방법')
    idx = make_index([c])
    keys = dcl.extract_case_keys(c, idx)
    links = dcl.build_links([keys], idx, "2026-11-02")
    rel = {(l["relation"], l["to"]) for l in links}
    assert ("about_screen", "check:screen:4101") in rel
    assert ("uses_function", "check:func:CT") in rel
    assert ("involves_item", "check:item:15001") in rel and ("involves_item", "check:item:15015") in rel
    for l in links:
        assert l["grade"] in {"auto_extracted", "inferred"} and 0 < l["confidence"] <= 1
        assert l["as_of"] == "2026-11-02" and l["from"] == "check:support-case:t10"
    # 변형이 있는 화면은 모든 변형으로 연결된다
    c2 = case("check:support-case:t10b", "TR 1002 문의")
    idx2 = make_index([c2])
    l2 = dcl.build_links([dcl.extract_case_keys(c2, idx2)], idx2, "x")
    assert {l["to"] for l in l2 if l["relation"] == "about_screen"} == {"check:screen:1002:종합", "check:screen:1002:해외"}


# 11 ------------------------------------------------------------------------
def test_explained_in_manual_rules_function_screen_and_feature():
    c = case("check:support-case:t11", "TR 4114 화면과 =CH(1) 사용, 통합검색 기능도 질문")
    idx = make_index([c])
    links = dcl.build_links([dcl.extract_case_keys(c, idx)], idx, "x")
    man = [l for l in links if l["relation"] == "explained_in_manual"]
    targets = {l["to"] for l in man}
    assert {"check:excel:manual:함수-설명", "check:manual:엑셀-프리미엄:주요-함수-설명", "check:manual:통합검색:기능-개요"} <= targets
    page = [l for l in man if l["to"] == "check:manual:source-page-index"]
    assert page and page[0]["target_locator"] == "PDF 200-200쪽" and page[0]["via"] == "check:screen:4114"
    assert all(not l["to"].startswith(dcl.PLACEHOLDER_PREFIX) for l in links)


# 12 ------------------------------------------------------------------------
def test_placeholder_links_replaced_not_carried_over():
    c = case("check:support-case:t12", "TR 4101 문의", related=["check:enrichment:unmapped:abc123"])
    idx = make_index([c])
    links = dcl.build_links([dcl.extract_case_keys(c, idx)], idx, "x")
    assert not [l for l in links if l["to"].startswith(dcl.PLACEHOLDER_PREFIX)]
    assert [l for l in links if l["relation"] == "about_screen" and l["to"] == "check:screen:4101"]
    assert dcl.before_metrics(idx, [dcl.extract_case_keys(c, idx)])["placeholder_links"] == 1


# 13 ------------------------------------------------------------------------
def test_legacy_screen_links_are_kept_but_marked():
    c = case("check:support-case:t13", "아무 키 없음", related=["check:screen:4114"])
    idx = make_index([c])
    links = dcl.build_links([dcl.extract_case_keys(c, idx)], idx, "x")
    l = [l for l in links if l["relation"] == "about_screen"][0]
    assert l["legacy_link"] is True and l["evidence"]["key_type"] == "legacy_related_id" and l["confidence"] <= 0.5


# 14 ------------------------------------------------------------------------
def test_resolves_only_for_troubleshooting_faq_with_answer_keys():
    def rels(ctype, resp):
        c = case("check:support-case:t14", "화면이 멈춤", resp, ctype)
        idx = make_index([c])
        return {(l["relation"], l["to"]) for l in dcl.build_links([dcl.extract_case_keys(c, idx)], idx, "x")}
    assert ("resolves", "check:screen:4101") in rels("troubleshooting", "TR 4101 화면에서 재조회 하시면 됩니다")
    assert ("resolves", "check:screen:4101") in rels("faq", "TR 4101 화면에서 재조회 하시면 됩니다")
    assert ("resolves", "check:screen:4101") not in rels("procedure", "TR 4101 화면에서 재조회 하시면 됩니다")
    assert ("resolves", "check:screen:4101") not in rels("faq", "4101")  # 응답이 너무 짧아 증상-조치 구조 아님


# 15 ------------------------------------------------------------------------
def test_similar_to_caps_threshold_and_reason():
    cases = [case(f"check:support-case:s{i:02d}", "엑셀 실시간 붙여넣기 오류 해결 방법 문의 입니다 반복 문장", "재설치 안내") for i in range(12)]
    cases += [case("check:support-case:z01", "전혀 다른 주제 채권 신용등급 평가 방법", "다른 답변 내용")]
    cases += [case(f"check:support-case:f{i}", f"서로 다른 질문 번호{i} 가나다라마바사 {i * 7919}", "응답") for i in range(3)]
    idx = make_index(cases)
    keys = [dcl.extract_case_keys(c, idx) for c in cases]
    sim, _ = dcl.build_similar(keys, idx, "x")
    deg: dict[str, int] = {}
    for p in sim:
        assert p["relation"] == "similar_to" and p["from"] < p["to"] and p["confidence"] >= dcl.SIM_THRESHOLD
        assert "tfidf_cosine" in p["reason"] and p["review_status"] == "needs_review"
        deg[p["from"]] = deg.get(p["from"], 0) + 1
        deg[p["to"]] = deg.get(p["to"], 0) + 1
    assert deg and max(deg.values()) <= dcl.MAX_DEGREE
    assert len(sim) <= dcl.SIM_TOP_K * len(cases)
    assert "check:support-case:z01" not in deg


# 16 ------------------------------------------------------------------------
def test_similar_to_boosted_by_shared_screen_key():
    a = case("check:support-case:a1", "TR 4101 값이 이상합니다 확인 부탁 드립니다", "확인")
    b = case("check:support-case:a2", "TR 4101 표시가 이상합니다 점검 요청 합니다", "확인")
    cs = [a, b] + [case(f"check:support-case:n{i}", f"무관 질문 {i} 계좌 개설 안내", "안내") for i in range(5)]
    idx = make_index(cs)
    keys = [dcl.extract_case_keys(c, idx) for c in cs]
    sim, _ = dcl.build_similar(keys, idx, "x")
    pair = [p for p in sim if (p["from"], p["to"]) == ("check:support-case:a1", "check:support-case:a2")]
    assert pair and pair[0]["reason"]["shared_screens"] == ["screen:4101"]


# 17 ------------------------------------------------------------------------
def test_candidates_for_keyless_cases_top3_needs_review():
    keyed = [case(f"check:support-case:k{i}", "선물 시세표 전종목 베이시스 보는 화면 문의", "4114 화면 안내", related=["check:screen:4114"]) for i in range(4)]
    target = case("check:support-case:q1", "선물 시세표 베이시스 전종목 한번에 보고싶습니다", "")
    cs = keyed + [target]
    idx = make_index(cs)
    keys = [dcl.extract_case_keys(c, idx) for c in cs]
    links = dcl.build_links(keys, idx, "x")
    scr: dict[str, set] = {}
    for l in links:
        if l["relation"] == "about_screen":
            scr.setdefault(l["from"], set()).add(l["to"])
    cands = dcl.build_candidates(keys, idx, "x", {"check:support-case:q1"}, scr)
    assert len(cands) == 1 and 1 <= len(cands[0]["candidates"]) <= dcl.CAND_TOP_K
    top = cands[0]["candidates"][0]
    assert top["to"] == "check:screen:4114" and top["review_status"] == "needs_review" and top["grade"] == "inferred"
    assert top["knn_score"] > 0 and top["support_cases"]


# 18 ------------------------------------------------------------------------
def test_run_end_to_end_writes_outputs_and_report(tmp_path):
    cs = [case("check:support-case:e1", "TR 4101 문의", "4114 안내", related=["check:enrichment:unmapped:abc123"]),
          case("check:support-case:e2", "=CT(1) 질문", "")]
    kn = tmp_path / "k.jsonl"
    kn.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in base_records() + cs), encoding="utf-8")
    out = tmp_path / "out"
    rep = dcl.run(kn, out, "2026-11-02")
    for name in ("case_keys.jsonl", "case_links.jsonl", "case_candidates.jsonl", "case_report.json"):
        assert (out / name).exists()
    assert rep["cases"] == 2 and rep["after"]["placeholder_links"] == 0 and rep["before"]["placeholder_links"] == 1
    assert rep["after"]["function_excel_ratio"] == 1.0
    assert rep["before"]["function_cases_with_excel_link"] == 0
    lines = [json.loads(l) for l in (out / "case_links.jsonl").read_text(encoding="utf-8").splitlines()]
    assert all({"from", "to", "relation", "evidence", "grade", "confidence"} <= set(l) for l in lines)

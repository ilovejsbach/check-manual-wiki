import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import build_ontology_explorer as be  # noqa: E402


def test_page_links_follow_quartz_slug_rules():
    assert be.page("check-expert/문의-대응/faq/ab12-S&P 500 수익률 3%?#메모.md") == "../문의-대응/faq/ab12-s-and-p-500-수익률-3-percent메모.html"


def test_build_has_no_case_text_and_writes_index(tmp_path):
    kn = tmp_path / "k.jsonl"
    recs = [{"id": "check:screen:6106", "type": "screen", "title": "종합", "screen_code": "6106", "markdown_path": "check-expert/a/6106.md"},
            {"id": "check:support-case:abcdef0123456789", "type": "support_case", "title": "비밀 제목", "text": "비밀 본문",
             "markdown_path": "check-expert/문의-대응/faq/x.md"}]
    kn.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in recs), encoding="utf-8")
    ont = tmp_path / "o"
    ont.mkdir()
    (ont / "edges_cases.jsonl").write_text(json.dumps({"source_id": recs[1]["id"], "target_id": "check:screen:6106", "type": "about_screen"}) + "\n")
    out = tmp_path / "x" / "data.json"
    assert be.main(["--knowledge", str(kn), "--ontology", str(ont), "--out", str(out)]) == 0
    raw = out.read_text(encoding="utf-8")
    assert "비밀" not in raw and (out.parent / "index.html").exists()
    d = json.loads(raw)
    assert d["screens"]["6106"]["ca"] == [0] and d["cases"][0]["h"] == "abcdef01"

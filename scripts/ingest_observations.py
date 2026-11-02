#!/usr/bin/env python3
"""윈도우 PC 세션이 CHECK Expert 실제 화면에서 수집한 관찰 결과(observations/screens/<TR>.json)를 검증·대조·반영한다.

이 맥에서는 CHECK 앱을 실행할 수 없으므로 수집은 윈도우 PC가 하고, 이 도구는 결과를 받아 처리하는 쪽이다.
프로토콜과 필드 정의: docs/check-screen-crawl-protocol.md

하는 일:
  1. 형식·개인정보 검증(시세 값, 계좌·전화번호·이메일 의심 문자열을 거부한다).
  2. 매뉴얼 화면과 대조해 일치 / 신규(매뉴얼에 없음) / 불일치(drift) 로 판정한다.
  3. TR 마스터 목록(ontology/tr_registry.jsonl)의 상태를 승격한다(case_mentioned -> screen_observed/rejected, 불일치 -> conflict).
  4. 매뉴얼에 없는 신규 화면 노드(ontology/observed_screens.jsonl)와 화면관찰 등급의 provides 엣지
     (ontology/edges_observed.jsonl, 모호·부분 일치는 edges_observed_review.jsonl)를 만든다.
  --pilot-list 는 윈도우 PC가 먼저 수집할 파일럿 대상(observations/pilot_targets.json)을 만든다.
표준 라이브러리만 사용한다.

사용:
  uv run --offline --no-sync python scripts/ingest_observations.py --check        # 검증·판정 보고만(파일 안 씀)
  uv run --offline --no-sync python scripts/ingest_observations.py                # 반영
  uv run --offline --no-sync python scripts/ingest_observations.py --pilot-list   # 파일럿 대상 목록 생성
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_ontology_edges as boe  # noqa: E402
import build_ontology_nodes as bon  # noqa: E402
import build_tr_registry as btr  # noqa: E402
import derive_case_links as dcl  # noqa: E402
import derive_item_links as dil  # noqa: E402

DEFAULT_OBS = Path("observations/screens")
DEFAULT_KNOWLEDGE = Path("knowledge/check-expert/knowledge.jsonl")
DEFAULT_REGISTRY = Path("ontology/tr_registry.jsonl")
DEFAULT_OUT_DIR = Path("ontology")
DEFAULT_PILOT = Path("observations/pilot_targets.json")
DEFAULT_AS_OF = "2026-11-02"
PILOT_UNCONFIRMED = 10
PILOT_MANUAL = 20

REQUIRED = ("screen_code", "observed_at", "app_version", "capture_id")
LIST_FIELDS = ("menu_path", "tabs", "buttons", "inputs", "output_columns", "states")
FORBIDDEN_KEYS = {"value", "values", "rows", "data", "prices", "price", "screenshot", "image", "account", "계좌", "잔고"}
MAX_LABEL = 60
PHONE = re.compile(r"\b\d{2,4}-\d{3,4}-\d{4}\b")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
LONG_DIGITS = re.compile(r"\d{8,}")  # 계좌번호 등 긴 숫자열(6자리 종목코드는 허용)
TITLE_PREFIX = re.compile(r"^\s*\d{4}\s*-\s*")


def norm_title(t: str | None) -> str:
    return dil.norm_full(TITLE_PREFIX.sub("", t or ""))


def _strings(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from _strings(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from _strings(v, f"{path}[{i}]")
    elif isinstance(obj, str):
        yield path, obj


def _keys(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from _keys(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _keys(v)


def validate_observation(obs: dict) -> list[str]:
    errs: list[str] = []
    for f in REQUIRED:
        if not obs.get(f):
            errs.append(f"필수 필드 없음: {f}")
    if obs.get("screen_code") and not re.fullmatch(r"\d{4}", str(obs["screen_code"])):
        errs.append(f"screen_code 형식 오류: {obs['screen_code']}")
    if obs.get("exists", True) is False and obs.get("output_columns"):
        errs.append("exists=false 인데 output_columns 가 있음")
    for f in LIST_FIELDS:
        if f in obs and not isinstance(obs[f], list):
            errs.append(f"{f} 는 목록이어야 함")
    for col in obs.get("output_columns", []) if isinstance(obs.get("output_columns"), list) else []:
        if not isinstance(col, dict) or not col.get("label"):
            errs.append("output_columns 항목에 label 없음")
    bad = FORBIDDEN_KEYS & {str(k).lower() for k in _keys(obs)}
    errs += [f"금지된 키(시세 값·스크린샷·계좌): {k}" for k in sorted(bad)]
    for path, s in _strings(obs):
        if len(s) > MAX_LABEL and not path.endswith(".notes"):
            errs.append(f"문자열이 너무 김(값 덤프 의심) {path}")
        if PHONE.search(s) or EMAIL.search(s) or LONG_DIGITS.search(s):
            errs.append(f"전화번호·이메일·긴 숫자열 의심 {path}")
    return errs


def load_observations(directory: Path) -> list[tuple[Path, dict]]:
    out = []
    for p in sorted(directory.glob("*.json")) if directory.exists() else []:
        try:
            out.append((p, json.loads(p.read_text(encoding="utf-8"))))
        except json.JSONDecodeError as e:
            out.append((p, {"_load_error": str(e)}))
    return out


def judge(obs: dict, manual: dict | None) -> dict:
    """매뉴얼 화면 레코드와 대조한 판정. outcome: matched / new / conflict / absent."""
    exists = obs.get("exists", True)
    if manual is None:
        return {"outcome": "new" if exists else "absent", "drift": []}
    drift: list[str] = []
    if not exists:
        drift.append("매뉴얼에는 있으나 실제 앱에 없음")
    elif obs.get("title") and norm_title(obs["title"]) != norm_title(manual.get("title")):
        drift.append("제목 불일치")
    new_cols = []
    text = dil.norm_full(manual.get("text", ""))
    for col in obs.get("output_columns", []):
        if dil.norm_full(col["label"]) not in text:
            new_cols.append(col["label"])
    return {"outcome": "conflict" if drift else "matched", "drift": drift, "columns_not_in_manual": new_cols}


def promote_registry(rows: list[dict], results: dict[str, dict], obs_by_tr: dict[str, dict], as_of: str) -> list[dict]:
    """TR 마스터 상태 승격. 사람이 정한 상태(PROMOTED)는 덮어쓰지 않는다."""
    out = []
    seen = set()
    for r in rows:
        tr = r["tr"]
        res = results.get(tr)
        seen.add(tr)
        if res is None or r["status"] in btr.PROMOTED:
            out.append(r)
            continue
        obs = obs_by_tr[tr]
        src = {"kind": "observation", "ref": obs["capture_id"], "as_of": obs["observed_at"]}
        r = dict(r)
        if res["outcome"] == "conflict":
            r["status"], r["notes"] = "conflict", "; ".join(res["drift"])
            r["sources"] = r["sources"] + [src]
        elif r["status"] == "case_mentioned":
            if res["outcome"] == "new":
                r.update(status="screen_observed", grade="screen_observed", title=obs.get("title"),
                         screen_id=f"check:screen:{tr}", sources=r["sources"] + [src])
            else:  # absent: 앱에 없는 번호
                r.update(status="rejected", notes="실제 앱에서 해당 TR 화면을 찾지 못함")
                r["sources"] = r["sources"] + [src]
        out.append(r)
    for tr, res in results.items():  # 마스터에 없던 TR 을 관찰로 처음 발견
        if tr not in seen and res["outcome"] == "new":
            obs = obs_by_tr[tr]
            out.append({"tr": tr, "status": "screen_observed", "screen_id": f"check:screen:{tr}", "title": obs.get("title"),
                        "categories": [], "sources": [{"kind": "observation", "ref": obs["capture_id"], "as_of": obs["observed_at"]}],
                        "grade": "screen_observed", "case_mentions": 0, "case_ids": [], "notes": "매뉴얼·사례에 없던 TR"})
    return out


def observed_screen_node(obs: dict, as_of: str) -> dict:
    tr = obs["screen_code"]
    return {"id": f"check:screen:{tr}", "type": "screen", "title": f"{tr} - {obs.get('title') or ''}".strip(" -"),
            "screen_code": tr, "category": None, "categories": [], "aliases": [f"TR{tr}", f"화면 {tr}", tr],
            "menu_path": obs.get("menu_path", []), "tabs": obs.get("tabs", []),
            "output_columns": [c["label"] for c in obs.get("output_columns", [])],
            "source": "observation", "source_locator": obs["capture_id"], "as_of": obs["observed_at"],
            "app_version": obs["app_version"], "visibility": "internal", "grade": "screen_observed", "schema_version": "1.0"}


def observed_edges(obs: dict, screen_id: str, d: dil.ItemDict, as_of: str) -> tuple[list[dict], list[dict]]:
    edges, review, seen = [], [], set()
    for col in obs.get("output_columns", []):
        m = dil.match_candidate(col["label"], "heading", d)
        if not m:
            continue
        if m["ambiguous"] or m["match_type"] == "partial":
            review.append({"source_id": screen_id, "label": col["label"], "match_type": m["match_type"], "n_codes": m["n_codes"],
                           "candidate_codes": sorted(c["code"] for c in m["matched_codes"]), "review_status": "needs_review", "as_of": as_of})
            continue
        code = m["matched_codes"][0]["code"]
        if (screen_id, code) in seen:
            continue
        seen.add((screen_id, code))
        edges.append({"id": boe.edge_id(screen_id, "provides", f"check:item:{code}"), "source_id": screen_id,
                      "target_id": f"check:item:{code}", "type": "provides", "label": "화면에서 관찰한 출력 항목",
                      "grade": "screen_observed",
                      "evidence": {"record_id": obs["capture_id"], "source_locator": f"observations/screens/{obs['screen_code']}.json",
                                   "matched_text": col["label"], "match_type": m["match_type"]},
                      "as_of": obs["observed_at"], "evidence_type": "observed_column", "review_status": "observed", "canonical": True})
    return edges, review


def pilot_targets(registry: list[dict], records: list[dict]) -> dict:
    """윈도우 PC가 먼저 수집할 대상: 미확인 TR 중 언급이 많은 순 + 분류가 고르게 퍼진 매뉴얼 화면."""
    unconfirmed = sorted((r for r in registry if r["status"] == "case_mentioned"), key=lambda r: (-r["case_mentions"], r["tr"]))
    first = [{"tr": r["tr"], "kind": "unconfirmed", "why": f"사례 {r['case_mentions']}개가 언급", "expect": "화면 존재 여부와 제목 확인"}
             for r in unconfirmed[:PILOT_UNCONFIRMED]]
    manual = [r for r in registry if r["status"] == "manual_confirmed" and r["case_mentions"] > 0]
    by_cat: dict[str, list[dict]] = collections.defaultdict(list)
    for r in sorted(manual, key=lambda r: (-r["case_mentions"], r["tr"])):
        by_cat[(r["categories"] or ["기타"])[0]].append(r)
    picked: list[dict] = []
    while len(picked) < PILOT_MANUAL and any(by_cat.values()):
        for cat in sorted(by_cat, key=lambda c: -len(by_cat[c])):
            if by_cat[cat] and len(picked) < PILOT_MANUAL:
                picked.append(by_cat[cat].pop(0))
    second = [{"tr": r["tr"], "kind": "manual", "title": r["title"], "category": (r["categories"] or ["기타"])[0],
               "why": f"사례 {r['case_mentions']}개가 언급", "expect": "제목 일치, 출력 컬럼, 메뉴 경로, 탭"} for r in picked]
    return {"purpose": "수집 가능성 파일럿: 라벨↔항목 일치율, UI 자동화 판독 가능 여부, 매뉴얼-실화면 불일치 비율 측정",
            "measure": ["label_to_item_match_rate", "ui_automation_readable", "manual_drift_rate"],
            "targets": first + second}


def load_registry(path: Path) -> list[dict]:
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()] if path.exists() else []


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="화면 관찰 결과 검증·대조·반영")
    ap.add_argument("--observations", type=Path, default=DEFAULT_OBS)
    ap.add_argument("--knowledge", type=Path, default=DEFAULT_KNOWLEDGE)
    ap.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    ap.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    ap.add_argument("--pilot-out", type=Path, default=DEFAULT_PILOT)
    ap.add_argument("--as-of", default=DEFAULT_AS_OF)
    ap.add_argument("--check", action="store_true", help="검증·판정 보고만 하고 파일은 쓰지 않는다")
    ap.add_argument("--pilot-list", action="store_true", help="파일럿 대상 목록을 만든다")
    args = ap.parse_args(argv)

    records = dcl.load_records(args.knowledge)
    registry = load_registry(args.registry)
    if args.pilot_list:
        args.pilot_out.parent.mkdir(parents=True, exist_ok=True)
        data = pilot_targets(registry, records)
        args.pilot_out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.pilot_out} ({len(data['targets'])} targets)")
        return 0

    manual_by_tr = {str(r["screen_code"]): r for r in records if r.get("type") == "screen"}
    d = dil.ItemDict(dil.parse_dictionary(records))
    invalid, valid = {}, []
    for path, obs in load_observations(args.observations):
        errs = [obs["_load_error"]] if "_load_error" in obs else validate_observation(obs)
        if errs:
            invalid[path.name] = errs
        else:
            valid.append(obs)
    dup = [tr for tr, n in collections.Counter(o["screen_code"] for o in valid).items() if n > 1]
    for tr in dup:
        invalid[f"{tr}(중복)"] = ["같은 TR 의 관찰 파일이 둘 이상"]
    valid = [o for o in valid if o["screen_code"] not in dup]

    results = {o["screen_code"]: judge(o, manual_by_tr.get(o["screen_code"])) for o in valid}
    obs_by_tr = {o["screen_code"]: o for o in valid}
    new_nodes = [observed_screen_node(o, args.as_of) for o in valid if results[o["screen_code"]]["outcome"] == "new"]
    edges, review = [], []
    for o in valid:
        if not o.get("exists", True):
            continue
        sid = manual_by_tr[o["screen_code"]]["id"] if o["screen_code"] in manual_by_tr else f"check:screen:{o['screen_code']}"
        e, r = observed_edges(o, sid, d, args.as_of)
        edges += e
        review += r
    item_ids = {n["id"] for n in bon.build_item_nodes(records, args.as_of)[0]}
    screen_ids = {r["id"] for r in records if r.get("type") == "screen"} | {n["id"] for n in new_nodes}
    edge_errs = boe.validate_edges(edges, item_ids, screen_ids)

    outcomes = collections.Counter(r["outcome"] for r in results.values())
    print(json.dumps({
        "observations": len(valid) + len(invalid), "valid": len(valid), "invalid": len(invalid),
        "outcomes": dict(outcomes), "conflicts": {tr: r["drift"] for tr, r in results.items() if r["outcome"] == "conflict"},
        "columns_not_in_manual": sum(len(r.get("columns_not_in_manual", [])) for r in results.values()),
        "observed_provides_edges": len(edges), "edges_needing_review": len(review), "edge_violations": len(edge_errs)},
        ensure_ascii=False))
    for name, errs in invalid.items():
        print(f"무효 {name}: {'; '.join(errs[:3])}", file=sys.stderr)
    for e in edge_errs[:10]:
        print("위반:", e, file=sys.stderr)
    if invalid or edge_errs:
        return 1
    if not args.check and valid:
        args.out_dir.mkdir(parents=True, exist_ok=True)
        registry = promote_registry(registry, results, obs_by_tr, args.as_of)
        args.registry.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in registry), encoding="utf-8")
        (args.out_dir / "observed_screens.jsonl").write_text("".join(json.dumps(n, ensure_ascii=False) + "\n" for n in new_nodes), encoding="utf-8")
        (args.out_dir / "edges_observed.jsonl").write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in edges), encoding="utf-8")
        (args.out_dir / "edges_observed_review.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in review), encoding="utf-8")
        print(f"updated {args.registry}, wrote observed_screens/edges_observed/edges_observed_review in {args.out_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

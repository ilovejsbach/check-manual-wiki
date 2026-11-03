#!/usr/bin/env python3
"""field-definitions.jsonl 의 정의가 화면 필드 레코드에 실제로 적용됐는지 점검하고, 안 된 쌍과 이유를 낸다.

고정 숫자(예: researched ≥ 68) 대신 '적용될 수 있는 (화면, 표시명) 쌍이 모두 적용됐는가'를 본다.
관찰 데이터가 바뀌어도(화면 추가, 시장 분류 변경) 기대값이 함께 움직인다.

쌍이 적용되지 않는 이유(build_screen_field_records 규칙과 같다):
  market_mismatch   정의의 categories 에 화면 시장이 없음
  own_definition    그 화면의 관찰이 같은 표시명에 자체 field_definitions 를 이미 가짐(정의를 얹지 않음)
  no_screen_record  화면 레코드가 없어 필드 레코드를 만들지 않음
  not_built         적용될 수 있는데 knowledge.jsonl 에 정의가 반영된 레코드가 없음(재생성 누락·버그)

사용:
  uv run python scripts/field_definition_coverage.py            # 요약, 미적용 쌍이 있으면 종료 코드 1
  uv run python scripts/field_definition_coverage.py --explain  # 적용 안 된 쌍을 모두 나열
"""
from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import build_check_wiki as builder  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge" / "check-expert" / "knowledge.jsonl"


def compute(observations: dict[str, dict], definitions: dict[str, dict], records: list[dict]) -> dict:
    screen_codes = {str(r["screen_code"]) for r in records if r.get("screen_code") and r.get("type") in {"screen", "observed_screen"}}
    by_id = {r["id"]: r for r in records if r.get("type") == "screen_field"}
    applied: list[tuple[str, str]] = []
    skipped: list[dict] = []
    for code, obs in sorted(observations.items()):
        own = set()
        for d in obs.get("field_definitions", []):
            if isinstance(d, dict):
                own.update({str(d.get("field") or d.get("concept") or "").strip(), str(d.get("concept") or "").strip()})
        for value in obs.get("observed_fields", []):
            label = str(value).strip()
            known = definitions.get(label)
            if not label or not known:
                continue
            category = obs.get("category")
            if known.get("categories") and category not in known["categories"]:
                skipped.append({"screen": code, "label": label, "reason": "market_mismatch", "detail": f"화면 시장={category}, 정의 시장={known['categories']}"})
            elif label in own:
                skipped.append({"screen": code, "label": label, "reason": "own_definition", "detail": "화면 관찰에 같은 표시명의 자체 정의가 있음"})
            elif code not in screen_codes:
                skipped.append({"screen": code, "label": label, "reason": "no_screen_record", "detail": "화면 레코드 없음"})
            else:
                concept = known.get("concept") or label
                field_id = f"check:field:{code}:{builder.slug(f'{label}-{concept}')}"
                rec = by_id.get(field_id)
                if rec and rec.get("definition_status") == "authoritative_general_definition" and rec.get("definition") == known["definition"]:
                    applied.append((code, label))
                else:
                    skipped.append({"screen": code, "label": label, "reason": "not_built", "detail": "레코드 없음" if not rec else f"정의 상태={rec.get('definition_status')}"})
    return {"applied": len(applied), "skipped": skipped,
            "not_built": [s for s in skipped if s["reason"] == "not_built"],
            "by_reason": dict(collections.Counter(s["reason"] for s in skipped)),
            "researched_total": sum(1 for r in by_id.values() if r.get("review_status") == "researched"),
            "field_total": len(by_id)}


def load_records(path: Path = KNOWLEDGE) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="필드 정의 적용 점검")
    ap.add_argument("--explain", action="store_true")
    args = ap.parse_args(argv)
    result = compute(builder.load_e2e_observations(), builder.load_field_definitions(), load_records())
    print(json.dumps({k: v for k, v in result.items() if k not in {"skipped", "not_built"}}, ensure_ascii=False))
    if args.explain:
        for s in result["skipped"]:
            print(f"  [{s['reason']}] 화면 {s['screen']} · {s['label']} — {s['detail']}")
    if result["not_built"]:
        print(f"실패: 적용될 수 있는데 반영되지 않은 쌍 {len(result['not_built'])}개 (--explain 으로 확인)")
        return 1
    print("통과: 적용될 수 있는 모든 쌍이 반영됨")
    return 0


if __name__ == "__main__":
    sys.exit(main())

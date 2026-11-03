#!/usr/bin/env python3
"""통합 후 생성물을 한 번에 다시 만들고 검증한다(윈도우·맥 공통).

JSONL·manifest·ZIP·생성 Markdown·온톨로지 내보내기는 병합하지 않고 이 스크립트로 재생성한다.
순서는 build_check_wiki 가 content/check-expert 의 모르는 파일을 지우므로 탐색기를 마지막에 두고,
TR 목록과 빌드가 고정점에 수렴하도록 build_tr_registry 와 build_check_wiki 를 번갈아 돈다.

사용:
  uv run python scripts/regenerate_all.py                 # 전체 (../check-e2e 가 있으면 E2E 가져오기 포함)
  uv run python scripts/regenerate_all.py --e2e-dir D:\\work\\check-e2e
  uv run python scripts/regenerate_all.py --skip-e2e      # E2E 가져오기 생략(원본이 없는 PC)
  uv run python scripts/regenerate_all.py --site          # 끝에 Quartz 빌드까지 (npx 필요)
  uv run python scripts/regenerate_all.py --list          # 단계만 출력
끝에 단계별 통과/실패 표와 기대값 점검 결과를 낸다. 하나라도 실패하면 종료 코드 1.
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KNOWLEDGE = ROOT / "knowledge" / "check-expert" / "knowledge.jsonl"
E2E_OUT = "sources/check-expert/e2e-observations.jsonl"


def py(script: str, *args: str) -> list[str]:
    return [sys.executable, f"scripts/{script}", *args]


def steps(e2e_dir: Path | None) -> list[tuple[str, list[str]]]:
    out: list[tuple[str, list[str]]] = []
    if e2e_dir:
        out.append(("E2E 관찰 가져오기", py("import_e2e_knowledge.py", str(e2e_dir), E2E_OUT, "--json")))
    out += [
        ("위키 빌드 1", py("build_check_wiki.py", "--json")),
        ("TR 목록 1", py("build_tr_registry.py")),
        ("위키 빌드 2", py("build_check_wiki.py", "--json")),
        ("TR 목록 2", py("build_tr_registry.py")),
        ("위키 빌드 3", py("build_check_wiki.py", "--json")),
        ("사례 의도 분류", py("classify_cases.py")),
        ("온톨로지 노드", py("build_ontology_nodes.py")),
        ("온톨로지 엣지", py("build_ontology_edges.py")),
        ("사례 엣지", py("build_ontology_case_edges.py")),
        ("미충족 요구", py("build_ontology_needs.py")),
        ("필드 우선순위", py("build_field_priority.py")),
        ("온톨로지 탐색기", py("build_ontology_explorer.py")),
        ("위키 검증", py("validate_check_wiki.py", "--json")),
        ("필드 정의 적용 점검", py("field_definition_coverage.py", "--explain")),
        ("검색 평가", py("eval_check_wiki.py", "--json")),
        ("도움말 앱 빌드", py("build_help_app.py", "--json")),
        ("pytest", [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider"]),
    ]
    return out


def run(name: str, cmd: list[str]) -> tuple[bool, float, str]:
    started = time.time()
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
    tail = (proc.stdout + proc.stderr).strip().splitlines()[-6:]
    return proc.returncode == 0, time.time() - started, "\n".join(tail)


def expectations() -> list[tuple[str, bool, str]]:
    checks: list[tuple[str, bool, str]] = []
    if not KNOWLEDGE.exists():
        return [("knowledge.jsonl 존재", False, str(KNOWLEDGE))]
    records = [json.loads(line) for line in KNOWLEDGE.read_text(encoding="utf-8").splitlines() if line.strip()]
    fields = [r for r in records if r.get("type") == "screen_field"]
    researched = sum(1 for r in fields if r.get("review_status") == "researched")
    checks.append(("researched 필드 수(참고, 관찰 데이터에 따라 달라짐)", True, f"{researched}/{len(fields)}"))
    none_links = [r["id"] for r in records if r.get("markdown_path") and "None" in str(r["markdown_path"])]
    checks.append(("markdown_path 에 None 없음", not none_links, f"{len(none_links)}건"))
    index = ROOT / "content" / "check-expert" / "업무-기능-색인.md"
    checks.append(("업무-기능-색인 에 [[None 없음", index.exists() and "[[None" not in index.read_text(encoding="utf-8"), ""))
    return checks


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="생성물 재생성과 검증")
    ap.add_argument("--e2e-dir", type=Path, default=ROOT.parent / "check-e2e")
    ap.add_argument("--skip-e2e", action="store_true")
    ap.add_argument("--site", action="store_true", help="Quartz 사이트 빌드까지 실행")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv)

    e2e_dir = None if args.skip_e2e else args.e2e_dir
    if e2e_dir and not e2e_dir.exists():
        print(f"[건너뜀] E2E 디렉터리 없음: {e2e_dir} (--e2e-dir 로 지정하거나 --skip-e2e)")
        e2e_dir = None
    plan = steps(e2e_dir)
    if args.site:
        npx = shutil.which("npx")
        if npx:
            plan.append(("Quartz 사이트 빌드", [npx, "quartz", "build", "--concurrency", "4"]))
        else:
            print("[건너뜀] npx 가 없어 Quartz 빌드를 생략합니다.")
    if args.list:
        for i, (name, cmd) in enumerate(plan, 1):
            print(f"{i:2d}. {name}: {' '.join(cmd[1:])}")
        return 0

    results = []
    for name, cmd in plan:
        ok, secs, tail = run(name, cmd)
        results.append((name, ok, secs, tail))
        print(f"[{'통과' if ok else '실패'}] {name} ({secs:.0f}s)", flush=True)
        if not ok:
            print(tail)
    print("\n기대값 점검")
    checked = expectations()
    for name, ok, note in checked:
        print(f"  [{'통과' if ok else '실패'}] {name} {note}")
    failed = [n for n, ok, _, _ in results if not ok] + [n for n, ok, _ in checked if not ok]
    print(f"\n{'모두 통과' if not failed else '실패: ' + ', '.join(failed)}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

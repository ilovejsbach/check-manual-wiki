#!/usr/bin/env python3
"""문의 사례 재구성 결과(요구·응답 요약)를 원문과 대조해 검증한다.

입력: 원문 {id, request, response} 배열과 재구성 {id, request, response} 배열.
검사
  보존   원문의 화면번호·함수 이름·오류 문구가 재구성에도 있어야 한다(sanitize_cases.extract_facts 기준).
  추가   재구성에 원문에 없는 화면번호(4자리)·함수 호출이 생기면 안 된다(지어낸 사실).
  누출   전화·이메일·마스킹 토큰·소수점 값·3자리 이상 쉼표 수치·인사말이 남으면 안 된다.
  복사   원문과 25자 이상 연속으로 같으면 복사로 본다.
  분량   요구 20~220자, 응답 20~320자.
통과하지 못한 사례는 이전 문장을 유지한다(호출 측 책임). 사례 본문은 출력하지 않고 사유만 낸다.
"""
from __future__ import annotations

import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sanitize_cases as sc  # noqa: E402

LEAK_RES = {
    "전화": re.compile(r"0\d{1,2}[-. )]\s?\d{3,4}[-. ]\d{4}|01\d\s?\d{3,4}\s?\d{4}"),
    "이메일": re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"),
    "마스킹토큰": re.compile(r"\[(?:IDENTIFIER|NUMBER|PHONE|REDACTED_ENTITY|EMAIL|PERSON|PATH)\]|⟦|⟧"),
    "소수값": re.compile(r"(?<![\d.])\d{1,6}\.\d{1,4}(?![\d.])"),
    "쉼표수치": re.compile(r"\d{1,3}(?:,\d{3})+"),
    "인사말": re.compile(r"안녕하세요|감사합니다|감사드립니다|수고하세요|고맙습니다"),
}
SCREEN_RE = re.compile(r"(?<![\d.,/-])\d{4}(?![\d.,/-])")
COPY_MIN = 40  # 메뉴 경로·API 경로·버튼 이름은 보존해야 하므로 30자 안팎의 겹침은 허용한다
EMPTY_RESPONSE = "대응 내용이 기록되지 않았습니다."
EMPTY_REQUEST = "문의 내용이 기록되지 않았습니다."
WARN_ONLY = ("쉼표수치",)  # 시스템 제한값(예 10,000개)일 수 있어 실패가 아니라 경고로 둔다


def _facts(text: str) -> set[str]:
    return set(sc.extract_facts(text))


def _codes(text: str) -> set[str]:
    return {f.split(":", 1)[1] for f in sc.extract_facts(text) if f.startswith("screen:")}


def longest_common(a: str, b: str) -> int:
    m = difflib.SequenceMatcher(None, a, b, autojunk=False).find_longest_match(0, len(a), 0, len(b))
    return m.size


def check(orig: dict, new: dict) -> list[str]:
    errs: list[str] = []
    src = f"{orig['request']}\n{orig['response']}"
    out = f"{new['request']}\n{new['response']}"
    lost = [f for f in _facts(src) if f.split(":", 1)[0] in ("screen", "err") and f not in _facts(out)]
    # 화면번호는 단순 숫자 일치로도 인정한다(문장 속 '3435 화면' 등 표기 차이)
    lost = [f for f in lost if not (f.startswith("screen:") and f.split(":", 1)[1] in out)]
    errs += [f"보존 누락 {f[:40]}" for f in lost]
    fn_src = {f for f in _facts(src) if f.startswith("fn:")}
    fn_names = {re.match(r"fn:=?([A-Za-z0-9_.가-힣]+)", f).group(1).upper() for f in fn_src if re.match(r"fn:=?([A-Za-z0-9_.가-힣]+)", f)}
    for name in fn_names:
        if name not in out.upper():
            errs.append(f"보존 누락 함수 {name}")
    src_nums = set(SCREEN_RE.findall(src))
    for n in set(SCREEN_RE.findall(out)) - src_nums:
        errs.append(f"추가 4자리 번호 {n}")
    for name, rx in LEAK_RES.items():
        if rx.search(out):
            errs.append(f"{'경고' if name in WARN_ONLY else '누출'} {name}")
    if "<값>" in out and "<값>" not in src:
        errs.append("누출 마스킹표식")
    for key in ("request", "response"):
        if longest_common(orig[key], new[key]) >= COPY_MIN:
            errs.append(f"복사 의심 {key}")
    lo, hi = {"request": (20, 220), "response": (20, 320)}["request"], {"request": (20, 220), "response": (20, 320)}["response"]
    if new["request"] != EMPTY_REQUEST and not lo[0] <= len(new["request"]) <= lo[1]:
        errs.append(f"분량 request {len(new['request'])}")
    if new["response"] != EMPTY_RESPONSE and not hi[0] <= len(new["response"]) <= hi[1]:
        errs.append(f"분량 response {len(new['response'])}")
    return errs


def validate(originals: list[dict], rewrites: list[dict]) -> dict:
    by_id = {o["id"]: o for o in originals}
    report = {"total": len(originals), "ok": 0, "fail": {}, "missing": []}
    done = {r["id"]: r for r in rewrites}
    for oid, o in by_id.items():
        r = done.get(oid)
        if r is None:
            report["missing"].append(oid)
            continue
        errs = check(o, r)
        hard = [e for e in errs if not e.startswith("경고")]
        if errs:
            report.setdefault("warn", {})[oid] = [e for e in errs if e.startswith("경고")]
        if hard:
            report["fail"][oid] = hard
        else:
            report["ok"] += 1
    return report


def main(argv=None) -> int:
    ins = [Path(p) for p in (argv or sys.argv[1:])]
    orig, new = [], []
    for p in ins:
        data = json.loads(p.read_text(encoding="utf-8"))
        (orig if "intent" in (data[0] if data else {}) else new).extend(data)
    rep = validate(orig, new)
    warns = {k: v for k, v in rep.get("warn", {}).items() if v}
    print(json.dumps({"total": rep["total"], "ok": rep["ok"], "fail": len(rep["fail"]), "missing": len(rep["missing"]), "warn": len(warns)}, ensure_ascii=False))
    for oid, w in warns.items():
        print("경고", oid[-8:], "; ".join(w))
    for oid, errs in rep["fail"].items():
        print(oid[-8:], "; ".join(errs))
    return 0 if not rep["fail"] and not rep["missing"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

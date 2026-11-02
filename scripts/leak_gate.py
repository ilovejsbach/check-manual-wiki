#!/usr/bin/env python3
"""공개 산출물 누출 게이트 (규칙 기반, 외부 호출 없음).

검사 항목 (위반 유형)
    phone      전화번호/내선
    email      이메일
    ip         IP 주소
    token      마스킹 토큰 [REDACTED_ENTITY] [IDENTIFIER] [NUMBER] [PERSON] [PHONE] [EMAIL] [PATH],
               잘린 토큰. ⟦ ⟧ 로 감싼 토큰(증상/함수 인자 보존)은 허용하고 info 로만 센다.
    origin     원본 위치 단서: PID복원, CRM데이터, row:N, !row, workbook:..., CRM-00000
    name       고유명사: --names-file(수동) + --names-from(자동 수집 원천) + 공개 텍스트 자체에
               접미사 규칙을 적용한 후보(name-candidate)
    date       구체 날짜·시각 (ISO, MM.DD, M월 D일, N시, HH:MM; 시장 고정 시각은 허용)
    ngram      --pair 로 짝지은 원문/변형본 레코드의 n-gram 겹침이 임계치 초과
    fact       --pair 로 짝지은 원문/변형본의 기술 사실(화면번호/함수식/오류문구) 불일치
    pair       짝의 줄 수 불일치

사용
    uv run --offline --no-sync python scripts/leak_gate.py tmp/sanitized [--json] \
        --names-file private/sanitize_names.txt \
        --pair sources/check-expert/manual-enrichment.jsonl=tmp/sanitized/manual-enrichment.jsonl
    위반이 하나라도 있으면 종료코드 1. 보고에는 일치한 값을 싣지 않고 유형·위치(파일:줄:열)만 싣는다.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterator

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sanitize_cases import (  # noqa: E402
    CLOCK_RE,
    EMAIL_RE,
    IP_RE,
    MARKET_TIMES,
    PARTIAL_TOKEN_RE,
    PHONE_RES,
    phone44_spans,
    SKIP_KEYS,
    TOKEN_RE,
    WRAP_L,
    WRAP_R,
    collect_names,
    extract_facts,
    find_function_spans,
    iter_strings,
    load_names_file,
    strip_protected,
)

SUFFIXES = {".md", ".jsonl", ".json", ".txt", ".csv"}
ORIGIN_RE = re.compile(
    r"[^\s`'\"|,\[\]]*(?:PID복원|CRM데이터)[^\s`'\"|,\[\]]*|[^\s`'\"|,\[\]]*!row:?\d*"
    r"|(?<![\w])row:\d+|workbook:[\w:]+|CRM-\d{3,6}"
)
DATE_GATE_RES = [
    re.compile(r"(?<!\d)20\d{2}[-./]\d{1,2}[-./]\d{1,2}(?!\d)"),
    re.compile(r"(?<![0-9A-Za-z])20\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])(?![0-9A-Za-z])"),
    re.compile(r"(?<!\d)\d{1,2}월\s*\d{1,2}일"),
    re.compile(r"(?<![\d.])(?:0[1-9]|1[0-2])\.(?:0[1-9]|[12]\d|3[01])(?![\d.])"),
    re.compile(r"(?<![\d:.])\d{1,2}\s*시(?!간|세|리|스|대|장|가)"),
]
FILENAME_RE = re.compile(r"[\w.-]+\.(?:xlsx?|csv|pdf|zip)\b")
EXCLUDE_TEXT_KEYS = {"markdown_path", "source_ref", "evidence_locator", "source_locator", "source_cell_ids",
                     "candidate_id", "candidate_ids", "signal_id"}
NGRAM_N = 8


def iter_files(paths: list[Path]) -> Iterator[Path]:
    for p in paths:
        if p.is_dir():
            yield from sorted(f for f in p.rglob("*") if f.is_file() and f.suffix in SUFFIXES)
        elif p.is_file():
            yield p


def _mask_functions(line: str) -> str:
    chars = list(line)
    spans = find_function_spans(line) + [m.span() for m in FILENAME_RE.finditer(line)]
    for s, e in spans:
        for i in range(s, e):
            chars[i] = " "
    return "".join(chars)


def _inside_wrap(line: str, idx: int) -> bool:
    return line.rfind(WRAP_L, 0, idx) > line.rfind(WRAP_R, 0, idx)


def scan_line(line: str, names: dict[str, str], slug: bool = False) -> list[tuple[str, int, str]]:
    """(type, column, note) 목록. 값 자체는 반환하지 않는다."""
    out: list[tuple[str, int, str]] = []
    for rx in PHONE_RES:
        for m in rx.finditer(line):
            out.append(("phone", m.start(), ""))
    for a, _ in phone44_spans(line, slug=slug):
        out.append(("phone", a, "4-4"))
    for m in EMAIL_RE.finditer(line):
        out.append(("email", m.start(), ""))
    for m in IP_RE.finditer(line):
        if m.group(0).count(".") == 3 and not re.fullmatch(r"\d\.\d\.\d\.\d", m.group(0)):
            out.append(("ip", m.start(), ""))
    for m in TOKEN_RE.finditer(line):
        if _inside_wrap(line, m.start()):
            out.append(("info-token-wrapped", m.start(), ""))
        else:
            out.append(("token", m.start(), m.group(1)))
    for m in PARTIAL_TOKEN_RE.finditer(line):
        out.append(("token", m.start(), "partial"))
    origin_spans = []
    for m in ORIGIN_RE.finditer(line):
        origin_spans.append(m.span())
        out.append(("origin", m.start(), ""))
    for name in names:
        i = line.find(name)
        while i != -1:
            out.append(("name", i, "dictionary"))
            i = line.find(name, i + len(name))
    masked = _mask_functions(line)
    for rx in DATE_GATE_RES:
        for m in rx.finditer(masked):
            if not any(a <= m.start() < b for a, b in origin_spans):
                out.append(("date", m.start(), ""))
    for m in CLOCK_RE.finditer(masked):
        if f"{int(m.group(1)):02d}:{m.group(2)}" not in MARKET_TIMES:
            out.append(("date", m.start(), "clock"))
    return out


def shingles(text: str, n: int = NGRAM_N) -> set[str]:
    t = re.sub(r"\s+", "", text)
    return {t[i : i + n] for i in range(len(t) - n + 1)}


def record_text(rec: Any) -> str:
    parts = []

    def walk(o: Any, key: str | None = None) -> None:
        if isinstance(o, dict):
            for k, v in o.items():
                walk(v, k)
        elif isinstance(o, list):
            for v in o:
                walk(v, key)
        elif isinstance(o, str) and key not in SKIP_KEYS and key not in EXCLUDE_TEXT_KEYS and len(o) >= 12:
            parts.append(o)

    walk(rec)
    return "\n\x00\n".join(parts)


def overlap(orig: str, pub: str) -> float:
    g = shingles(strip_protected(pub))
    if not g:
        return 0.0
    return len(g & shingles(strip_protected(orig))) / len(g)


def doc_key(p: Path) -> str:
    m = re.match(r"([0-9a-f]{16})-", p.name)
    return m.group(1) if m else f"{p.parent.name}/{p.name}"


def _fact_note(fo: list[str], fp: list[str]) -> str:
    miss, add_ = Counter(fo) - Counter(fp), Counter(fp) - Counter(fo)
    kinds = lambda c: dict(Counter(k.split(":", 1)[0] for k in c.elements()))  # noqa: E731
    return f"기술 사실 불일치 누락={kinds(miss)} 추가={kinds(add_)}"


def pair_checks(pairs: list[tuple[Path, Path]], thr: float, add: Any) -> dict[str, Any]:
    stats = {"records": 0, "mean_overlap": 0.0, "over_threshold": 0}
    total = 0.0
    for o, p in pairs:
        if o.is_dir() and p.is_dir():
            om = {doc_key(f): f for f in o.rglob("*.md")}
            units = []
            for f in sorted(p.rglob("*.md")):
                if doc_key(f) in om:
                    units.append((str(f), 1, om[doc_key(f)].read_text(encoding="utf-8"), f.read_text(encoding="utf-8")))
        else:
            ol = [json.loads(x) for x in o.read_text(encoding="utf-8").splitlines() if x.strip()]
            pl = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines() if x.strip()]
            if len(ol) != len(pl):
                add(str(p), 0, 0, "pair", f"줄 수 불일치 원문={len(ol)} 변형본={len(pl)}")
                continue
            units = [(str(p), i, record_text(a), record_text(b)) for i, (a, b) in enumerate(zip(ol, pl), 1)]
            # 기술 사실은 레코드 전체 문자열로 비교 (SKIP 키 포함 아님: 본문만)
            for (_, i, ot, pt) in units:
                fo, fp = extract_facts(ot), extract_facts(pt)
                if fo != fp:
                    add(str(p), i, 0, "fact", _fact_note(fo, fp))
        for (f, i, ot, pt) in units:
            if o.is_dir():
                fo, fp = extract_facts(ot), extract_facts(pt)
                if fo != fp:
                    add(f, i, 0, "fact", _fact_note(fo, fp))
            if len(re.sub(r"\s+", "", pt)) < NGRAM_N + 4:
                continue
            r = overlap(ot, pt)
            stats["records"] += 1
            total += r
            if r > thr:
                stats["over_threshold"] += 1
                add(f, i, 0, "ngram", f"{NGRAM_N}-gram 겹침 {r:.2f} > {thr:.2f}")
    if stats["records"]:
        stats["mean_overlap"] = round(total / stats["records"], 3)
    return stats


def run(targets: list[Path], names: dict[str, str], pairs: list[tuple[Path, Path]], thr: float) -> dict[str, Any]:
    violations: list[dict[str, Any]] = []
    info: Counter[str] = Counter()

    def add(file: str, line: int, col: int, typ: str, note: str) -> None:
        violations.append({"file": file, "line": line, "col": col, "type": typ, "note": note})

    cand_names: dict[str, str] = {}
    for f in iter_files(targets):
        # 경로(파일명) 검사: 줄 0
        for typ, col, note in scan_line(f.stem, names, slug=True):
            if typ.startswith("info"):
                info[typ] += 1
            else:
                add(str(f), 0, col, typ, note or "파일명")
        text = f.read_text(encoding="utf-8", errors="replace")
        for ln, line in enumerate(text.splitlines(), 1):
            for typ, col, note in scan_line(line, names):
                if typ.startswith("info"):
                    info[typ] += 1
                else:
                    add(str(f), ln, col, typ, note)
            for w in collect_names([line]):
                if w not in names:
                    cand_names[w] = f"{f}:{ln}"
                    add(str(f), ln, line.find(w), "name-candidate", "회사명 접미사 패턴")
    pstats = pair_checks(pairs, thr, add) if pairs else None
    by_type = Counter(v["type"] for v in violations)
    by_file: dict[str, Counter[str]] = {}
    for v in violations:
        by_file.setdefault(v["file"], Counter())[v["type"]] += 1
    return {
        "ok": not violations,
        "violation_count": len(violations),
        "by_type": dict(by_type),
        "by_file": {k: dict(c) for k, c in by_file.items()},
        "info": dict(info),
        "pair_stats": pstats,
        "violations": violations,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="공개 산출물 누출 게이트")
    ap.add_argument("targets", nargs="+", type=Path)
    ap.add_argument("--names-file", type=Path, default=Path("private/sanitize_names.txt"))
    ap.add_argument("--names-from", nargs="*", type=Path, default=[],
                    help="원문 파일/디렉터리: 접미사 규칙으로 회사명을 자동 수집해 사전에 추가")
    ap.add_argument("--pair", action="append", default=[], metavar="ORIG=PUBLIC")
    ap.add_argument("--ngram-threshold", type=float, default=0.8)
    ap.add_argument("--max-print", type=int, default=200)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    names = load_names_file(a.names_file)
    texts: list[str] = []
    for f in iter_files(a.names_from):
        for line in f.read_text(encoding="utf-8").splitlines():
            texts.append(line)
    if texts:
        # jsonl 은 문자열 값 단위로
        flat: list[str] = []
        for t in texts:
            try:
                flat += list(iter_strings(json.loads(t)))
            except json.JSONDecodeError:
                flat.append(t)
        names.update(collect_names(flat))
    pairs = []
    for s in a.pair:
        o, _, p = s.partition("=")
        pairs.append((Path(o), Path(p)))

    res = run(a.targets, names, pairs, a.ngram_threshold)
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        for v in res["violations"][: a.max_print]:
            print(f"{v['file']}:{v['line']}:{v['col']}: [{v['type']}] {v['note']}")
        if res["violation_count"] > a.max_print:
            print(f"... {res['violation_count'] - a.max_print}건 더 (--json 으로 전체)")
        print(f"위반 {res['violation_count']}건 {res['by_type']} / 허용(info) {res['info']}")
        if res["pair_stats"]:
            print(f"pair: {res['pair_stats']}")
    return 0 if res["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

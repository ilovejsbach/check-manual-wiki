#!/usr/bin/env python3
"""문의 사례(support_case)에서 '연결 키'를 추출하고 타입 있는 관계를 만든다.

독립 도구다. knowledge.jsonl 을 읽기만 하고 기존 빌더/데이터는 건드리지 않는다.
표준 라이브러리만 사용한다(항목 사전 파싱은 같은 디렉터리의 derive_item_links.py 재사용).

사용:
  uv run --offline --no-sync python scripts/derive_case_links.py \
      --knowledge knowledge/check-expert/knowledge.jsonl --out-dir tmp --report

산출물(out-dir):
  case_keys.jsonl        사례별 키(화면/제목/함수/항목/오류문구) - 값과 위치만, 본문 문장 없음
  case_links.jsonl       관계 목록 {from,to,relation,evidence,grade,confidence,...}
  case_candidates.jsonl  키 없는 사례의 검색 기반 후보(추정, needs_review) - 정답 아님
  case_report.json       전후 지표

개인정보: 본문 문장은 어떤 산출물에도 복사하지 않는다. 근거는 (섹션, 시작, 끝, sha8) 이다.
오류 문구는 짧고 마스킹 토큰이 없는 것만 값으로 남기고 나머지는 해시만 남긴다.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import derive_item_links as dil  # noqa: E402  (복사본: 항목코드표 파싱·정규화 재사용)

DEFAULT_KNOWLEDGE = Path("knowledge/check-expert/knowledge.jsonl")
DEFAULT_AS_OF = "2026-11-02"
SCHEMA_VERSION = "2.0"

# 임계치 (튜닝값)
SIM_THRESHOLD = 0.30        # similar_to 최소 점수
MAX_DEGREE = 4              # 사례 하나가 가질 수 있는 similar_to 총 차수(선택 2 + 피선택 2)
SIM_TOP_K = 2               # 사례당 상위 k
CAND_CONFIDENT = 0.10       # 이 점수 이상이면 confident 플래그(validate_candidates 구간표로 보정)
CAND_TOP_K = 3              # 키 없는 사례의 후보 수
MAX_ITEM_CANDIDATES = 5     # involves_item 링크로 내보낼 후보 코드 상한
TITLE_MIN_LEN = 4           # 화면 제목 일치 최소 길이(정규화 후)
TITLE_STRONG_LEN = 7        # 이 길이 이상이거나 문맥(화면/메뉴 인접, 따옴표)이 있어야 강한 제목 일치
ERROR_VALUE_MAX = 50        # 오류 문구 값을 그대로 남기는 최대 길이

TITLE_CTX_AFTER = re.compile(r"^\s*(?:화면|메뉴|조회|창)")
TITLE_CTX_BEFORE = re.compile(r"[\"'“‘\[「]$")
SCREEN_TITLE_BEFORE = re.compile(r"(?:\d{4}|TR\s*\d{4}|#\d{4}\])\s*[-–]?\s*$")
SCREEN_TITLE_AFTER = re.compile(r"^\s*(?:화면|메뉴|창)")
MASK_RE = re.compile(r"\[[A-Z][A-Z_]*\]")
KNOWN_FUNCS = {"CT", "CH", "CIS", "CTS", "CTD"}  # 항목코드표 시트 + 매뉴얼 함수 설명
FUNC_CALL_RE = re.compile(r"(?<![A-Za-z0-9])(CLIST|CTD|CTR|CTS|CIS|CRS|CT|CH)\s*\(")
FUNC_WORD_RE = re.compile(r"(?<![A-Za-z0-9])(CLIST|CTD|CTR|CTS|CIS|CT|CH)\s*(?:함수|수식)")

# 화면번호: 'TR 1234'/'tr1234' 는 그대로 신뢰. 단독 4자리는 연도(19xx/20xx)·금액·날짜·시각·단위
# 오탐이 많으므로 (a) 소수점/쉼표/하이픈/콜론 인접 제외 (b) 단위 접미 제외 (c) 실존 screen_code 만
# (d) 문맥(화면/번호/메뉴 인접 또는 '1234 - 제목')이 있어야 강한 키, 없으면 약한 키(추정).
TR_RE = re.compile(r"(?<![A-Za-z])[Tt][Rr]\s*[-_#]?\s*(\d{4})(?!\d)")
BARE4_RE = re.compile(r"(?<![\d.,\-/:~])(\d{4})(?![\d,]|\.\d|[\-/:]\d)")
UNIT_AFTER = re.compile(r"^\s*(?:년|월|일|원|개|주|종목|건|%|억|만|천|시|분|초|명|배|bps?|세|회|호|번째|틱|포인트|pt|점|위|조|달러|엔)(?![가-힣])|^\s*(?:년|월|일|원|개|주|건|억|만|천|시|분|초|명|배|회|호|점|위|조)(?=은|는|이|가|을|를|에|의|도|만|부터|까지|씩|짜리|간)")
CTX_BEFORE = re.compile(r"(?:화면|TR|tr|Tr|번호|코드|메뉴|창|#)\s*[:：#]?\s*(?:번호\s*)?$")
CTX_AFTER = re.compile(r"^\s*(?:번\s*)?(?:화면|메뉴|창|탭)|^\s*[-–—]\s*[가-힣A-Za-z]")

# 항목코드: 5자리는 '항목코드/FID' 인접 또는 함수 인자(따옴표 안)일 때만 인정
ITEM_CODE_CTX = re.compile(r"(?:항목\s*코드|항목\s*번호|FID|fid|item\s*code)\s*[:：=]?\s*[\"']?(\d{3,5})(?!\d)")
ITEM_CODE_ARG = re.compile(r"[\"'](\d{5})[\"']")

QUOTE_RE = re.compile(r"[\"“‘「『]([^\"”’」』\n]{4,80})[\"”’」』]|(?<![\w\[])'([^'\n]{4,80})'")
BRACKET_RE = re.compile(r"\[([^\[\]\n]{4,60})\]")
ERRCODE_RE = re.compile(r"(?:오류|에러|error)\s*(?:코드|code)?\s*[:：]?\s*(?:-?\d{1,6}|0x[0-9A-Fa-f]+)", re.I)
ERROR_WORDS = re.compile(r"오류|에러|error|실패|불가|없습니다|않습니다|않아|안됩니다|안 됩니다|권한|만료|exception|#N/A|#VALUE|#NAME|#REF", re.I)

# 일반어 화면 제목(너무 흔해서 제외)
GENERIC_TITLES = {"종합", "상세", "현황", "추이", "비교", "차트", "시세", "종목", "일별", "기간별", "주요", "투자자", "순위"}

FEATURE_SECTIONS = [
    (r"통합\s*검색", "check:manual:통합검색:기능-개요"),
    (r"통합\s*알림", "check:manual:통합알림창:기능-개요"),
    (r"시세\s*감시", "check:manual:시세감시:기능-개요"),
    (r"메신저", "check:manual:메신저-연계기능:기능-개요"),
    (r"정보\s*공유", "check:manual:사용자간-정보-공유:기능-개요"),
    (r"관심\s*종목\s*등록", "check:manual:관심종목등록:관심종목-등록하기"),
    (r"페이지\s*저장", "check:manual:PAGE-저장:페이지-저장하기"),
    (r"사용자\s*편집\s*화면", "check:manual:사용자편집화면-저장:4.-사용자-편집화면"),
    (r"메인\s*프레임", "check:manual:메인프레임:메인프레임-유형-소개"),
    (r"엑셀\s*데이터\s*연결", "check:manual:엑셀데이터-연결:엑셀데이터-연결하기"),
    (r"조회\s*마법사", "check:excel:manual:조회마법사"),
    (r"Ez\s*차트", "check:excel:manual:Ez-차트"),
    (r"템플릿", "check:excel:manual:메뉴와-템플릿"),
    (r"엑셀\s*프리미엄", "check:manual:엑셀-프리미엄:소개와-특징"),
]
FUNC_MANUAL_IDS = ["check:manual:엑셀-프리미엄:주요-함수-설명", "check:excel:manual:함수-설명"]
PAGE_INDEX_ID = "check:manual:source-page-index"
PLACEHOLDER_PREFIX = "check:enrichment:unmapped:"
# 상류 분류(case_topic)가 인프라·일반 문의인 사례: 특정 화면이 정답일 수 없어 '화면 연결 가능' 분모에서 따로 본다
NON_SCREEN_TOPICS = {"요구-오류/장애", "넷클라이언트", "요구-최적응대", "공통기능", "네트워크", "체크실행", "하드웨어",
                     "윈도우", "기타", "미분류", "조회정보 없음(이용 문의)", "체크화면", "체크메신저"}


# --------------------------------------------------------------------------- 공통

def is_strong(f: dict) -> bool:
    """화면 키가 강한 근거인가: TR/문맥 있는 번호, 충분히 긴 제목 또는 문맥 있는 제목."""
    return f["kind"] not in ("bare", "title_weak")


def sha8(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()[:8]


def load_records(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]


def split_sections(text: str) -> dict[str, str]:
    """사례 마크다운 -> {'S': 상황, 'A': 당시 대응, 'M': 의미 분류}. 안내문·검증 체크리스트는 버린다."""
    names = {"사용자가 겪은 상황": "S", "당시 대응": "A", "의미 분류": "M"}
    out = {"S": "", "A": "", "M": ""}
    cur = None
    buf: list[str] = []
    for line in (text or "").split("\n"):
        if line.startswith("## "):
            if cur:
                out[cur] = "\n".join(buf).strip("\n")
            cur = names.get(line[3:].strip())
            buf = []
        elif cur:
            buf.append(line)
    if cur:
        out[cur] = "\n".join(buf).strip("\n")
    return out


def span_ev(case: dict, section: str, start: int, end: int, raw: str) -> dict:
    return {"record_id": case["id"], "source_locator": case.get("source_locator"),
            "section": section, "start": start, "end": end, "sha8": sha8(raw)}


# --------------------------------------------------------------------------- 지식 인덱스

class Index:
    def __init__(self, records: list[dict]):
        self.by_id = {r["id"]: r for r in records}
        self.screens = [r for r in records if r.get("type") == "screen"]
        self.cases = [r for r in records if r.get("type") == "support_case"]
        self.screen_ids: dict[str, list[str]] = collections.defaultdict(list)
        for s in self.screens:
            self.screen_ids[str(s.get("screen_code"))].append(s["id"])
        # 제목 -> 코드 (일반어·짧은 제목·여러 화면이 공유하는 제목 제외)
        t2c: dict[str, set[str]] = collections.defaultdict(set)
        for s in self.screens:
            name = re.sub(r"^\s*\d{4}\s*-\s*", "", s.get("title") or "")
            key = dil.norm_full(name)
            if len(key) >= TITLE_MIN_LEN and key not in GENERIC_TITLES and not re.fullmatch(r"[\d\W]+", key):
                t2c[key].add(str(s["screen_code"]))
        self.title_prefix = {}
        for s_ in self.screens:
            nm = dil.norm_full(re.sub(r"^\s*\d{4}\s*-\s*", "", s_.get("title") or ""))
            if len(nm) >= 3 and nm not in GENERIC_TITLES:
                self.title_prefix.setdefault(str(s_["screen_code"]), nm[:3])
        self.title_to_code = {k: sorted(v) for k, v in t2c.items() if len(v) == 1}
        self.max_title_len = max((len(k) for k in self.title_to_code), default=0)
        self.items = dil.ItemDict(dil.parse_dictionary(records))
        self.code_to_name: dict[str, str] = {}
        for e in self.items.entries:
            self.code_to_name.setdefault(e["code"], e["name"])
        self.item_names = {k: v for k, v in self.items.by_full.items()
                           if len(k) >= dil.MIN_NORMALIZED_LEN and k not in dil.GENERIC
                           and not re.fullmatch(r"[\d\W_]+", k)}
        self.max_item_len = max((len(k) for k in self.item_names), default=0)
        # 실제 매뉴얼 문서(검색 후보 대상): 화면 + check:manual:* (색인 제외) + 엑셀 매뉴얼
        self.docs = [r for r in records if r["id"].startswith(("check:screen:", "check:excel:manual:"))
                     or (r["id"].startswith("check:manual:") and r["id"] != PAGE_INDEX_ID)]


def normalize_with_map(text: str) -> tuple[str, list[int]]:
    """공백 제거 + 소문자 + 률->율. 정규화 문자열 인덱스 -> 원문 인덱스 매핑을 함께 반환."""
    chars: list[str] = []
    idx: list[int] = []
    for i, ch in enumerate(text):
        if ch.isspace():
            continue
        chars.append(ch.lower().replace("률", "율"))
        idx.append(i)
    return "".join(chars), idx


# --------------------------------------------------------------------------- 키 추출

def extract_screen_codes(text: str, idx: Index, unknown: list | None = None) -> list[dict]:
    found: dict[str, dict] = {}

    def add(code: str, kind: str, s: int, e: int):
        if code not in idx.screen_ids:
            if unknown is not None and kind != "bare":
                unknown.append({"code": code, "kind": kind, "start": s, "end": e})
            return
        cur = found.get(code)
        rank = {"tr": 3, "ctx": 2, "bare": 1}[kind]
        if cur is None:
            found[code] = {"code": code, "kind": kind, "start": s, "end": e, "n": 1, "_r": rank}
        else:
            cur["n"] += 1
            if rank > cur["_r"]:
                cur.update(kind=kind, start=s, end=e, _r=rank)

    for m in TR_RE.finditer(text):
        add(m.group(1), "tr", m.start(), m.end())
    for m in BARE4_RE.finditer(text):
        code, s, e = m.group(1), m.start(1), m.end(1)
        if any(f["start"] <= s < f["end"] for f in found.values() if f["kind"] == "tr" and f["code"] == code):
            continue
        before, after = text[max(0, s - 12):s], text[e:e + 10]
        has_ctx = bool(CTX_BEFORE.search(before) or CTX_AFTER.match(after))
        if UNIT_AFTER.match(after) and not has_ctx:
            continue
        if not has_ctx and idx.title_prefix.get(code) and \
                dil.norm_full(text[e:e + 40]).startswith(idx.title_prefix[code]):
            has_ctx = True  # '1542 구성종목 ...' 처럼 번호 뒤에 그 화면의 제목이 이어지면 문맥으로 인정
        if code[:2] in ("19", "20") and not has_ctx:
            continue  # 연도 오탐 방지
        add(code, "ctx" if has_ctx else "bare", s, e)
    out = []
    for f in found.values():
        f.pop("_r")
        out.append(f)
    return sorted(out, key=lambda f: f["start"])


def extract_titles(text: str, idx: Index) -> list[dict]:
    norm, imap = normalize_with_map(text)
    out: dict[str, dict] = {}
    L = len(norm)
    for i in range(L):
        for j in range(i + TITLE_MIN_LEN, min(L, i + idx.max_title_len) + 1):
            codes = idx.title_to_code.get(norm[i:j])
            if codes:
                key = codes[0]
                # 영문/숫자만의 제목은 단어 경계 필요
                sub = norm[i:j]
                if re.fullmatch(r"[a-z0-9]+", sub):
                    if (i > 0 and norm[i - 1].isalnum() and norm[i - 1].isascii()) or \
                       (j < L and norm[j].isalnum() and norm[j].isascii()):
                        continue
                cur = out.get(key)
                s, e = imap[i], imap[j - 1] + 1
                if cur is None:
                    out[key] = {"code": key, "kind": "title", "start": s, "end": e, "n": 1, "_len": j - i}
                    ctx = TITLE_CTX_AFTER.match(text[e:e + 6]) or TITLE_CTX_BEFORE.search(text[max(0, s - 3):s])
                    if j - i < TITLE_STRONG_LEN and not ctx:
                        out[key]["kind"] = "title_weak"  # 짧은 제목은 일반 용어와 구분 불가
                else:
                    cur["n"] += 1
                    if j - i > cur["_len"]:
                        cur.update(start=s, end=e, _len=j - i)
    res = []
    for f in out.values():
        f.pop("_len")
        res.append(f)
    return sorted(res, key=lambda f: f["start"])


def extract_functions(text: str) -> list[dict]:
    found: dict[str, dict] = {}
    for rx, kind in ((FUNC_CALL_RE, "call"), (FUNC_WORD_RE, "mention")):
        for m in rx.finditer(text):
            name = m.group(1)
            cur = found.get(name)
            if cur is None:
                found[name] = {"name": name, "form": kind, "known": name in KNOWN_FUNCS,
                               "start": m.start(1), "end": m.end(1), "n": 1}
            else:
                cur["n"] += 1
                if kind == "call" and cur["form"] == "mention":
                    cur.update(form="call", start=m.start(1), end=m.end(1))
    return sorted(found.values(), key=lambda f: f["start"])


def extract_items(text: str, idx: Index) -> list[dict]:
    out: list[dict] = []
    seen_codes: set[str] = set()
    for rx in (ITEM_CODE_CTX, ITEM_CODE_ARG):
        for m in rx.finditer(text):
            code = m.group(1)
            if code in idx.code_to_name and code not in seen_codes:
                seen_codes.add(code)
                out.append({"match": "code", "codes": [code], "n_codes": 1, "ambiguous": False,
                            "start": m.start(1), "end": m.end(1), "name": idx.code_to_name[code]})
    norm, imap = normalize_with_map(text)
    L = len(norm)
    hits: list[tuple[int, int, str]] = []
    for i in range(L):
        for j in range(i + dil.MIN_NORMALIZED_LEN, min(L, i + idx.max_item_len) + 1):
            sub = norm[i:j]
            if sub in idx.item_names:
                a0, b0 = imap[i], imap[j - 1] + 1
                # '4101 현재가 화면' 처럼 화면 제목의 일부인 이름은 항목이 아니다
                if SCREEN_TITLE_BEFORE.search(text[max(0, a0 - 8):a0]) or SCREEN_TITLE_AFTER.match(text[b0:b0 + 6]):
                    continue
                if re.fullmatch(r"[a-z0-9]+", sub) and (
                        (i > 0 and norm[i - 1].isascii() and norm[i - 1].isalnum()) or
                        (j < L and norm[j].isascii() and norm[j].isalnum())):
                    continue
                hits.append((i, j, sub))
    # 최장 일치 우선: 더 긴 히트에 완전히 포함되는 히트 제거
    hits.sort(key=lambda h: (h[0] - h[1], h[0]))
    kept: list[tuple[int, int, str]] = []
    for h in hits:
        if not any(k[0] <= h[0] and h[1] <= k[1] for k in kept):
            kept.append(h)
    by_name: dict[str, dict] = {}
    for i, j, sub in sorted(kept):
        entries = idx.item_names[sub]
        codes = sorted({e["code"] for e in entries})
        cur = by_name.get(sub)
        if cur is None:
            by_name[sub] = {"match": "name", "name": entries[0]["name"], "codes": codes[:10],
                            "n_codes": len(codes), "ambiguous": len(codes) > 1,
                            "start": imap[i], "end": imap[j - 1] + 1, "n": 1}
        else:
            cur["n"] += 1
    for v in by_name.values():
        if v["codes"] and not (v["n_codes"] == 1 and v["codes"][0] in seen_codes):
            out.append(v)
    return sorted(out, key=lambda f: f["start"])


def extract_errors(text: str) -> tuple[list[dict], collections.Counter]:
    """따옴표/대괄호 인용구. 마스킹 토큰은 증상이 아니라 치환 토큰이므로 error_strings 에서 분리한다."""
    errs: list[dict] = []
    masks: collections.Counter = collections.Counter(m.group(0) for m in MASK_RE.finditer(text))
    seen: set[str] = set()
    cands = [(m.start(), m.end(), m.group(1) or m.group(2), "quote") for m in QUOTE_RE.finditer(text)]
    cands += [(m.start(), m.end(), m.group(1), "bracket") for m in BRACKET_RE.finditer(text)
              if not MASK_RE.fullmatch(m.group(0))]
    for s, e, val, kind in sorted(cands):
        v = val.strip()
        if not v or MASK_RE.fullmatch(f"[{v}]") or re.fullmatch(r"[A-Z_]+", v):
            continue
        h = sha8(v)
        if h in seen:
            continue
        seen.add(h)
        has_mask = bool(MASK_RE.search(v))
        error_like = bool(ERROR_WORDS.search(v))
        rec = {"kind": kind, "start": s, "end": e, "len": len(v), "sha8": h,
               "error_like": error_like, "has_mask_token": has_mask}
        if error_like and not has_mask and len(v) <= ERROR_VALUE_MAX:
            rec["value"] = v
        errs.append(rec)
    for m in ERRCODE_RE.finditer(text):
        h = sha8(m.group(0))
        if h not in seen:
            seen.add(h)
            errs.append({"kind": "errcode", "start": m.start(), "end": m.end(), "len": len(m.group(0)), "sha8": h,
                         "error_like": True, "has_mask_token": False, "value": m.group(0)})
    return errs, masks


def extract_feature_sections(text: str) -> list[dict]:
    out = []
    for pat, target in FEATURE_SECTIONS:
        m = re.search(pat, text)
        if m:
            out.append({"target": target, "start": m.start(), "end": m.end()})
    return out


def extract_case_keys(case: dict, idx: Index) -> dict:
    sec = split_sections(case.get("text", ""))
    keys = {"id": case["id"], "case_type": case.get("case_type"), "schema_version": SCHEMA_VERSION,
            "screen_codes": [], "screen_titles": [], "functions": [], "item_codes": [],
            "error_strings": [], "quoted_strings": [], "unresolved_screen_codes": [], "feature_sections": [], "mask_tokens": {}, "topic_screen_codes": []}
    masks_total: collections.Counter = collections.Counter()
    for sname in ("S", "A"):
        t = sec[sname]
        if not t.strip():
            continue
        unk: list = []
        for f in extract_screen_codes(t, idx, unk):
            keys["screen_codes"].append({**f, "section": sname, "grade": "auto_extracted" if is_strong(f) else "inferred",
                                         "sha8": sha8(t[f["start"]:f["end"]])})
        keys["unresolved_screen_codes"].extend({**u, "section": sname} for u in unk)
        for f in extract_titles(t, idx):
            keys["screen_titles"].append({**f, "section": sname, "grade": "auto_extracted" if is_strong(f) else "inferred", "sha8": sha8(t[f["start"]:f["end"]])})
        for f in extract_functions(t):
            keys["functions"].append({**f, "section": sname, "grade": "auto_extracted" if f["form"] == "call" else "inferred",
                                      "sha8": sha8(t[f["start"]:f["end"]])})
        for f in extract_items(t, idx):
            keys["item_codes"].append({**f, "section": sname, "grade": "auto_extracted" if f["match"] == "code" else "inferred",
                                       "sha8": sha8(t[f["start"]:f["end"]])})
        errs, masks = extract_errors(t)
        for e in errs:
            keys["error_strings" if e["error_like"] else "quoted_strings"].append({**e, "section": sname})
        masks_total.update(masks)
        for f in extract_feature_sections(t):
            keys["feature_sections"].append({**f, "section": sname, "sha8": sha8(t[f["start"]:f["end"]])})
    keys["mask_tokens"] = dict(masks_total)
    # 분류 라벨의 '업무·주제: NNNN - 제목' 은 기존 매핑 결과이므로 독립 근거가 아니다(별도 보관).
    for m in re.finditer(r"업무·주제:\s*(\d{4})\s*-", sec["M"]):
        if m.group(1) in idx.screen_ids:
            keys["topic_screen_codes"].append(m.group(1))
    keys["has_text_key"] = bool(keys["screen_codes"] or keys["screen_titles"] or keys["functions"]
                                or keys["item_codes"])
    keys["response_len"] = len(MASK_RE.sub("", sec["A"]).strip())
    return keys


# --------------------------------------------------------------------------- 관계 생성

def link(frm: str, to: str, relation: str, case: dict, ev: dict, grade: str, conf: float, **extra) -> dict:
    return {"from": frm, "to": to, "relation": relation, "evidence": ev, "grade": grade,
            "confidence": round(conf, 3), "review_status": "candidate" if grade == "auto_extracted" else "needs_review",
            "as_of": None, **extra}


SPEC_MAP = {"about_screen": "mentions_tr|mentions_title", "uses_function": "mentions_title(신규 제안: uses_function)",
            "involves_item": "mentions_title(신규 제안: involves_item)", "explained_in_manual": "explains 의 역(explained_by)",
            "resolves": "resolves", "similar_to": "similar_to(§3.1 semantic 대응)"}


def screen_page_range(idx: Index, sid: str) -> str | None:
    loc = idx.by_id[sid].get("source_locator")
    return str(loc) if loc else None


def build_links(keys_list: list[dict], idx: Index, as_of: str) -> list[dict]:
    links: dict[tuple, dict] = {}
    cases = {c["id"]: c for c in idx.cases}

    def put(l: dict):
        l["as_of"] = as_of
        k = (l["from"], l["to"], l["relation"])
        cur = links.get(k)
        if cur is None:
            l["n_evidence"] = 1
            l["vias"] = [l["via"]] if l.get("via") else []  # 같은 대상에 이르는 경로(함수 등)를 모두 보존한다
            links[k] = l
        else:
            cur["n_evidence"] += 1
            if l.get("via") and l["via"] not in cur["vias"]:
                cur["vias"].append(l["via"])
            if l["confidence"] > cur["confidence"]:
                n, vias = cur["n_evidence"], cur["vias"]
                cur.update({kk: vv for kk, vv in l.items() if kk not in ("n_evidence", "vias")})
                cur["n_evidence"], cur["vias"] = n, vias

    for k in keys_list:
        case = cases[k["id"]]
        cid = k["id"]
        ctype = k.get("case_type")
        # --- about_screen (본문 근거)
        screen_hit_codes: dict[str, str] = {}  # code -> 최고 section ('A' 우선 판정용)
        for f in k["screen_codes"] + k["screen_titles"]:
            conf = {"tr": 0.9, "ctx": 0.85, "bare": 0.4, "title": 0.7, "title_weak": 0.35}[f["kind"]]
            for sid in idx.screen_ids[f["code"]]:
                ev = {"record_id": cid, "source_locator": case.get("source_locator"), "section": f["section"],
                      "start": f["start"], "end": f["end"], "sha8": f["sha8"], "key_type": f["kind"]}
                put(link(cid, sid, "about_screen", case, ev, f["grade"], conf, spec_relation=SPEC_MAP["about_screen"]))
            screen_hit_codes.setdefault(f["code"], f["section"])
            if f["section"] == "A":
                screen_hit_codes[f["code"]] = "A"
        # --- uses_function
        for f in k["functions"]:
            conf = 0.9 if f["form"] == "call" else 0.6
            ev = {"record_id": cid, "source_locator": case.get("source_locator"), "section": f["section"],
                  "start": f["start"], "end": f["end"], "sha8": f["sha8"], "key_type": f["form"]}
            put(link(cid, f"check:func:{f['name']}", "uses_function", case, ev, f["grade"], conf,
                     known_function=f["known"], spec_relation=SPEC_MAP["uses_function"]))
            for mid in FUNC_MANUAL_IDS:
                if mid in idx.by_id:
                    put(link(cid, mid, "explained_in_manual", case, ev, "inferred", conf * 0.8,
                             via=f"check:func:{f['name']}", rule="function->excel_manual",
                             spec_relation=SPEC_MAP["explained_in_manual"]))
        # --- involves_item
        for f in k["item_codes"]:
            cands = f["codes"][:MAX_ITEM_CANDIDATES]
            base = 0.9 if f["match"] == "code" else 0.55
            conf = base / max(1, f["n_codes"]) ** 0.5
            ev = {"record_id": cid, "source_locator": case.get("source_locator"), "section": f["section"],
                  "start": f["start"], "end": f["end"], "sha8": f["sha8"], "key_type": f["match"]}
            for code in cands:
                put(link(cid, f"check:item:{code}", "involves_item", case, ev, f["grade"], conf,
                         ambiguous=f["ambiguous"], n_candidates=f["n_codes"], spec_relation=SPEC_MAP["involves_item"]))
        # --- explained_in_manual: (a) 기능 절 키워드 (b) 화면 -> 원문 페이지
        for f in k["feature_sections"]:
            if f["target"] in idx.by_id:
                ev = {"record_id": cid, "source_locator": case.get("source_locator"), "section": f["section"],
                      "start": f["start"], "end": f["end"], "sha8": f["sha8"], "key_type": "feature_keyword"}
                put(link(cid, f["target"], "explained_in_manual", case, ev, "inferred", 0.5,
                         rule="feature_keyword->manual_section", spec_relation=SPEC_MAP["explained_in_manual"]))
        # --- resolves (troubleshooting/faq, 증상-조치 구조: 응답이 실질 내용을 가질 때, 응답 쪽 키)
        if ctype in ("troubleshooting", "faq") and k["response_len"] >= 8:
            for f in k["screen_codes"] + k["screen_titles"]:
                if f["section"] != "A" or not is_strong(f):
                    continue
                for sid in idx.screen_ids[f["code"]]:
                    ev = {"record_id": cid, "source_locator": case.get("source_locator"), "section": "A",
                          "start": f["start"], "end": f["end"], "sha8": f["sha8"], "key_type": f["kind"]}
                    put(link(cid, sid, "resolves", case, ev, "inferred", 0.6, structure="symptom_action",
                             spec_relation=SPEC_MAP["resolves"]))
            for f in k["functions"]:
                if f["section"] == "A" and f["form"] == "call":
                    ev = {"record_id": cid, "source_locator": case.get("source_locator"), "section": "A",
                          "start": f["start"], "end": f["end"], "sha8": f["sha8"], "key_type": "call"}
                    put(link(cid, f"check:func:{f['name']}", "resolves", case, ev, "inferred", 0.55,
                             structure="symptom_action", spec_relation=SPEC_MAP["resolves"]))
    # --- 기존(legacy) 사례->화면 연결 이월: 본문 근거 유무를 표시
    body_codes = {k["id"]: {f["code"] for f in k["screen_codes"] + k["screen_titles"]} for k in keys_list}
    topic_codes = {k["id"]: set(k["topic_screen_codes"]) for k in keys_list}
    for c in idx.cases:
        for t in c.get("related_ids", []):
            if t.startswith("check:screen:") and t in idx.by_id:
                code = str(idx.by_id[t].get("screen_code"))
                if (c["id"], t, "about_screen") in links:
                    links[(c["id"], t, "about_screen")]["legacy_link"] = True
                    continue
                corrob = code in body_codes[c["id"]] or code in topic_codes[c["id"]]
                ev = {"record_id": c["id"], "source_locator": c.get("source_locator"), "section": None,
                      "key_type": "legacy_related_id"}
                l = link(c["id"], t, "about_screen", c, ev, "inferred", 0.5 if corrob else 0.35,
                         legacy_link=True, corroborated_by_label=corrob, spec_relation=SPEC_MAP["about_screen"])
                l["as_of"] = as_of
                l["n_evidence"] = 1
                links[(c["id"], t, "about_screen")] = l
    # --- 화면 -> 매뉴얼 원문 페이지 (about_screen 이 있는 모든 사례)
    for (frm, to, rel), l in list(links.items()):
        if rel != "about_screen" or l["confidence"] < 0.35:
            continue
        pages = screen_page_range(idx, to)
        if not pages or PAGE_INDEX_ID not in idx.by_id:
            continue
        ev = dict(l["evidence"])
        nl = link(frm, PAGE_INDEX_ID, "explained_in_manual", None, ev, "inferred", l["confidence"] * 0.8,
                  via=to, rule="screen.source_locator->manual_page", target_locator=f"PDF {pages}쪽",
                  spec_relation=SPEC_MAP["explained_in_manual"])
        nl["as_of"] = as_of
        nl["n_evidence"] = 1
        links.setdefault((frm, PAGE_INDEX_ID + "#" + to, "explained_in_manual"), nl)
    return list(links.values())


# --------------------------------------------------------------------------- TF-IDF

_WORD = re.compile(r"[가-힣]+|[A-Za-z]+\d*|\d+")


def case_text_for_sim(case: dict) -> str:
    sec = split_sections(case.get("text", ""))
    return MASK_RE.sub(" ", sec["S"] + "\n" + sec["A"])


def term_list(text: str) -> list[str]:
    terms: list[str] = []
    for w in _WORD.findall(text):
        wl = w.lower()
        if re.fullmatch(r"[가-힣]+", wl):
            if len(wl) == 1:
                continue
            terms.extend(wl[i:i + 2] for i in range(len(wl) - 1))
        elif re.fullmatch(r"\d+", wl):
            if len(wl) == 4:
                terms.append(wl)
        elif len(wl) >= 2:
            terms.append(wl)
    return terms


def build_tfidf(docs: dict[str, list[str]], max_df_ratio: float = 0.15) -> tuple[dict[str, dict[str, float]], dict[str, float]]:
    n = len(docs)
    df: collections.Counter = collections.Counter()
    for terms in docs.values():
        df.update(set(terms))
    idf = {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items() if c >= 2 and c <= max(max_df_ratio * n, 20)}  # 작은 코퍼스에서 전부 버려지지 않게 하한
    vecs: dict[str, dict[str, float]] = {}
    for did, terms in docs.items():
        tf = collections.Counter(t for t in terms if t in idf)
        v = {t: (1 + math.log(c)) * idf[t] for t, c in tf.items()}
        norm = math.sqrt(sum(x * x for x in v.values())) or 1.0
        vecs[did] = {t: x / norm for t, x in v.items()}
    return vecs, idf


def build_similar(keys_list: list[dict], idx: Index, as_of: str) -> tuple[list[dict], dict]:
    kmap = {k["id"]: k for k in keys_list}
    docs = {c["id"]: term_list(case_text_for_sim(c)) for c in idx.cases}
    vecs, idf = build_tfidf(docs)
    inv: dict[str, list[str]] = collections.defaultdict(list)
    for did, v in vecs.items():
        for t in v:
            inv[t].append(did)

    def keyset(k):
        return ({f"screen:{f['code']}" for f in k["screen_codes"] + k["screen_titles"] if is_strong(f)},
                {f"func:{f['name']}" for f in k["functions"]},
                {f"item:{c}" for f in k["item_codes"] if f["n_codes"] <= 3 for c in f["codes"]})

    ks = {cid: keyset(k) for cid, k in kmap.items()}
    key_inv: dict[str, list[str]] = collections.defaultdict(list)
    for cid, (a, b, c) in ks.items():
        for key in a | b:
            key_inv[key].append(cid)
    top: dict[str, list[tuple[float, str, float, tuple]]] = {}
    pairs_seen: set = set()
    for cid, v in vecs.items():
        acc: collections.Counter = collections.Counter()
        for t, w in v.items():
            for other in inv[t]:
                if other != cid:
                    acc[other] += w * vecs[other][t]
        extra = set()
        for key in ks[cid][0] | ks[cid][1]:
            if len(key_inv[key]) <= 40:
                extra.update(o for o in key_inv[key] if o != cid)
        scored = []
        for other in set(acc) | extra:
            cos = acc.get(other, 0.0)
            ss = ks[cid][0] & ks[other][0]
            sf = ks[cid][1] & ks[other][1]
            si = ks[cid][2] & ks[other][2]
            boost = (0.20 if ss else 0) + (0.10 if sf else 0) + (0.05 if si else 0)
            if cos < 0.12 and not (ss or sf):
                continue
            score = min(1.0, cos + boost)
            if score >= SIM_THRESHOLD:
                scored.append((score, other, cos, (sorted(ss), sorted(sf), sorted(si))))
        scored.sort(key=lambda x: (-x[0], x[1]))
        top[cid] = scored[:SIM_TOP_K]
    pairs: dict[tuple[str, str], dict] = {}
    # 허브 방지: 점수 높은 쌍부터 받되 한 사례의 총 차수는 MAX_DEGREE 이하
    flat = sorted(((sc, cid, o, cs, ks_) for cid, lst in top.items() for sc, o, cs, ks_ in lst),
                  key=lambda x: (-x[0], x[1], x[2]))
    degree: collections.Counter = collections.Counter()
    accepted: dict[str, list] = collections.defaultdict(list)
    for sc, cid, o, cs, ks_ in flat:
        key = tuple(sorted((cid, o)))
        if key in pairs_seen:
            accepted[cid].append((sc, o, cs, ks_))
            continue
        if degree[cid] >= MAX_DEGREE or degree[o] >= MAX_DEGREE:
            continue
        pairs_seen.add(key)
        degree[cid] += 1
        degree[o] += 1
        accepted[cid].append((sc, o, cs, ks_))
    for cid, lst in accepted.items():
        for score, other, cos, (ss, sf, si) in lst:
            a, b = sorted((cid, other))
            p = pairs.get((a, b))
            if p is None:
                pairs[(a, b)] = {"from": a, "to": b, "relation": "similar_to",
                                 "evidence": {"record_id": a, "source_locator": idx.by_id[a].get("source_locator"),
                                              "method": "tfidf_char_bigram+shared_keys"},
                                 "grade": "inferred", "confidence": round(score, 3), "review_status": "needs_review",
                                 "as_of": as_of, "mutual": False,
                                 "reason": {"tfidf_cosine": round(cos, 3), "shared_screens": ss, "shared_functions": sf,
                                            "shared_items": si, "near_duplicate": cos >= 0.9},
                                 "spec_relation": SPEC_MAP["similar_to"], "selected_by": [cid]}
            else:
                p["mutual"] = True
                p["selected_by"].append(cid)
                p["confidence"] = max(p["confidence"], round(score, 3))
    return list(pairs.values()), {"idf": idf, "vecs": vecs}


# --------------------------------------------------------------------------- 키 없는 사례의 후보 매핑

def doc_terms(r: dict) -> list[str]:
    text = re.sub(r"^> 출처:.*$", " ", r.get("text", ""), flags=re.M)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)|\(assets/[^)]*\)", " ", text)
    return term_list(r.get("title", "")) * 3 + term_list(text)


def words(text: str) -> list[str]:
    return [w.lower() for w in _WORD.findall(text) if re.fullmatch(r"[가-힣]{2,}|[A-Za-z]{2,}\d*", w)]


KNN_K = 10  # 이웃 사례 수
DOC_WEIGHT = 0.1  # 문서 검색 점수 가중(이웃 투표 대비 보조)


def build_candidates(keys_list: list[dict], idx: Index, as_of: str, only_ids: set[str],
                     screen_links: dict[str, set[str]]) -> list[dict]:
    """키 없는 사례의 후보 매핑(정답 아님).

    1) 이웃 투표: 본문이 비슷한 사례(TF-IDF 상위 K)가 이미 가진 화면 연결에 sim^2 가중 투표
       (기존 연결 대비 hit@3 약 55%, 문서 직접 검색은 약 21% 라서 주 신호로 쓴다)
    2) 문서 검색: 화면/매뉴얼 레코드와의 TF-IDF 코사인(보조 신호, 화면이 아닌 매뉴얼 절 후보 포함)
    """
    docs = {r["id"]: doc_terms(r) for r in idx.docs}
    dvecs, didf = build_tfidf(docs, max_df_ratio=0.4)
    cdocs = {c["id"]: term_list(case_text_for_sim(c)) for c in idx.cases}
    cvecs, cidf = build_tfidf(cdocs)
    inv: dict[str, list[str]] = collections.defaultdict(list)
    for cid, v in cvecs.items():
        for t in v:
            inv[t].append(cid)
    out = []
    cases = {c["id"]: c for c in idx.cases}
    for cid in sorted(only_ids):
        text = case_text_for_sim(cases[cid])
        scores: dict[str, dict] = {}
        acc: collections.Counter = collections.Counter()
        for t, w in cvecs[cid].items():
            for o in inv[t]:
                if o != cid:
                    acc[o] += w * cvecs[o][t]
        for o, sim in acc.most_common(KNN_K):
            for sid in screen_links.get(o, ()):
                e = scores.setdefault(sid, {"knn": 0.0, "doc": 0.0, "support": []})
                e["knn"] += sim * sim
                e["support"].append(o)
        q_terms = [t for t in term_list(text) if t in didf]
        if q_terms:
            tf = collections.Counter(q_terms)
            qv = {t: (1 + math.log(c)) * didf[t] for t, c in tf.items()}
            qn = math.sqrt(sum(x * x for x in qv.values())) or 1.0
            for did, dv in dvecs.items():
                sh = [t for t in qv if t in dv]
                if sh:
                    sc = sum(qv[t] * dv[t] for t in sh) / qn
                    if sc >= 0.05:
                        scores.setdefault(did, {"knn": 0.0, "doc": 0.0, "support": []})["doc"] = sc
        ranked = sorted(((e["knn"] + DOC_WEIGHT * e["doc"], did, e) for did, e in scores.items()), key=lambda x: (-x[0], x[1]))
        qwords = set(words(text))
        cand = []
        for sc, did, e in ranked[:CAND_TOP_K]:
            dwords = set(words(doc_terms_text(idx.by_id[did])))
            ev_tokens = sorted(qwords & dwords, key=lambda w: -didf.get(w[:2], 0))[:5]
            cand.append({"to": did, "relation": "about_screen" if did.startswith("check:screen:") else "explained_in_manual",
                         "score": round(sc, 4), "knn_score": round(e["knn"], 4), "doc_score": round(e["doc"], 4),
                         "support_cases": sorted(set(e["support"]))[:3], "evidence_tokens": ev_tokens,
                         "grade": "inferred", "review_status": "needs_review"})
        out.append({"case_id": cid, "candidates": cand, "as_of": as_of, "confident": bool(cand) and cand[0]["score"] >= CAND_CONFIDENT,
                    "note": "후보일 뿐 정답 확정 아님. 사람 검수 필요"})
    return out


def validate_candidates(keys_list: list[dict], idx: Index, links: list[dict], as_of: str) -> dict:
    """검색 후보의 신뢰도 보정: 기존(legacy) 화면 연결이 있고 본문에 화면 키가 없는 사례로 hit@1/@3 을 측정한다."""
    legacy: dict[str, set] = collections.defaultdict(set)
    for l in links:
        if l["relation"] == "about_screen" and l["evidence"].get("key_type") == "legacy_related_id":
            legacy[l["from"]].add(l["to"])
    body = {k["id"] for k in keys_list if k["screen_codes"] or k["screen_titles"]}
    ids = {cid for cid in legacy if cid not in body}
    scr_all: dict[str, set] = collections.defaultdict(set)
    for l in links:
        if l["relation"] == "about_screen":
            scr_all[l["from"]].add(l["to"])
    res = build_candidates(keys_list, idx, as_of, ids, scr_all)
    buckets: dict[str, list] = collections.defaultdict(lambda: [0, 0, 0])
    for r in res:
        if not r["candidates"]:
            continue
        top = r["candidates"][0]["score"]
        b = "<0.05" if top < 0.05 else "0.05-0.10" if top < 0.10 else "0.10-0.20" if top < 0.20 else ">=0.20"
        hit1 = r["candidates"][0]["to"] in legacy[r["case_id"]]
        hit3 = any(c["to"] in legacy[r["case_id"]] for c in r["candidates"])
        buckets[b][0] += 1
        buckets[b][1] += hit1
        buckets[b][2] += hit3
    tot = [sum(v[i] for v in buckets.values()) for i in range(3)]
    return {"validation_cases": tot[0], "hit_at_1": round(tot[1] / max(1, tot[0]), 3), "hit_at_3": round(tot[2] / max(1, tot[0]), 3),
            "by_top_score": {b: {"n": v[0], "hit@1": round(v[1] / max(1, v[0]), 3), "hit@3": round(v[2] / max(1, v[0]), 3)}
                             for b, v in sorted(buckets.items())},
            "note": "정답=기존 related_ids 화면 연결(자체도 검수 전). 본문 화면 키가 없는 사례만 대상"}


def doc_terms_text(r: dict) -> str:
    return (r.get("title", "") + " ") + re.sub(r"^> 출처:.*$", " ", r.get("text", ""), flags=re.M)


# --------------------------------------------------------------------------- 지표

def before_metrics(idx: Index, keys_list: list[dict]) -> dict:
    n = len(idx.cases)
    by = idx.by_id
    scr = sem_c = ph_links = 0
    scr_cases = ph_cases = excel_cases = real_manual_cases = 0
    sem_edges = 0
    func_cases = [k["id"] for k in keys_list if k["functions"]]
    excel_func = 0
    kmap = {k["id"]: k for k in keys_list}
    missing = 0
    for c in idx.cases:
        rel = c.get("related_ids", [])
        s = [t for t in rel if t.startswith("check:screen:")]
        if s:
            scr_cases += 1
        sem_edges += sum(1 for t in rel if t.startswith("check:support-case:"))
        p = [t for t in rel if t.startswith(PLACEHOLDER_PREFIX)]
        ph_links += len(p)
        ph_cases += bool(p)
        if any(t.startswith("check:manual:") for t in rel) and any(
                not t.startswith(("check:manual:source-page-index",)) for t in rel if t.startswith("check:manual:")):
            real_manual_cases += 1
        linked_codes = {str(by[t].get("screen_code")) for t in s if t in by}
        for f in kmap[c["id"]]["screen_codes"] + kmap[c["id"]]["screen_titles"]:
            if is_strong(f) and f["code"] not in linked_codes:
                missing += 1
        if any(t.startswith("check:excel:") or t.startswith("check:enrichment:excel:") for t in rel) and c["id"] in func_cases:
            excel_func += 1
    return {"cases": n, "cases_with_screen_link": scr_cases, "screen_link_ratio": round(scr_cases / n, 4),
            "body_screen_key_pairs_without_link": missing,
            "function_cases": len(func_cases), "function_cases_with_excel_link": excel_func,
            "case_to_case_edges": sem_edges, "case_to_case_avg": round(sem_edges / n, 2),
            "placeholder_links": ph_links, "placeholder_cases": ph_cases,
            "cases_with_real_manual_section_link": real_manual_cases}


def after_metrics(idx: Index, keys_list: list[dict], links: list[dict], sim: list[dict], cands: list[dict]) -> dict:
    n = len(idx.cases)
    kmap = {k["id"]: k for k in keys_list}
    scr_all: dict[str, set] = collections.defaultdict(set)
    scr_body: dict[str, set] = collections.defaultdict(set)
    excel_f: set[str] = set()
    real_man: set[str] = set()
    ph = 0
    for l in links:
        if l["relation"] == "about_screen":
            scr_all[l["from"]].add(l["to"])
            if not l.get("legacy_link") or l["evidence"].get("key_type") != "legacy_related_id":
                scr_body[l["from"]].add(l["to"])
        if l["relation"] == "explained_in_manual" and l["to"].startswith(("check:excel:", "check:manual:")):
            real_man.add(l["from"])
            if l.get("rule") == "function->excel_manual":
                excel_f.add(l["from"])
        if l["to"].startswith(PLACEHOLDER_PREFIX):
            ph += 1
    func_cases = {k["id"] for k in keys_list if k["functions"]}
    cand_ids = {c["case_id"] for c in cands if c["candidates"] and c["confident"]}
    missing = 0
    for k in keys_list:
        for f in k["screen_codes"] + k["screen_titles"]:
            if not is_strong(f):
                continue
            if not any(idx.by_id[s].get("screen_code") == f["code"] for s in scr_all[k["id"]]):
                missing += 1
    strong_ids = {k["id"] for k in keys_list if any(is_strong(f) for f in k["screen_codes"] + k["screen_titles"])}
    sim_n = len(sim)
    deg = collections.Counter()
    for p in sim:
        deg[p["from"]] += 1
        deg[p["to"]] += 1
    page_cases = {l["from"] for l in links if l["to"] == PAGE_INDEX_ID}
    applicable = [c["id"] for c in idx.cases if c.get("case_topic") not in NON_SCREEN_TOPICS]
    app_set = set(applicable)
    leg = [l for l in links if l["relation"] == "about_screen" and l["evidence"].get("key_type") == "legacy_related_id"]
    return {
        "screen_applicable_cases": len(applicable),
        "screen_ratio_among_applicable_incl_legacy": round(len(app_set & set(scr_all)) / max(1, len(applicable)), 4),
        "screen_ratio_among_applicable_incl_confident_candidates": round(len(app_set & (set(scr_all) | cand_ids)) / max(1, len(applicable)), 4),
        "legacy_only_screen_links": len(leg),
        "legacy_only_links_corroborated_by_label": sum(1 for l in leg if l.get("corroborated_by_label")),
        "legacy_only_links_uncorroborated": sum(1 for l in leg if not l.get("corroborated_by_label")),
        "cases_with_screen_link_body_only": len(scr_body), "screen_ratio_body_only": round(len(scr_body) / n, 4),
        "cases_with_screen_link_incl_legacy": len(scr_all), "screen_ratio_incl_legacy": round(len(scr_all) / n, 4),
        "cases_with_screen_link_or_confident_candidate": len(set(scr_all) | cand_ids),
        "screen_ratio_incl_confident_candidates": round(len(set(scr_all) | cand_ids) / n, 4),
        "body_screen_key_pairs_without_link": missing, "cases_with_strong_screen_key": len(strong_ids),
        "function_cases": len(func_cases), "function_cases_with_excel_link": len(func_cases & excel_f),
        "function_excel_ratio": round(len(func_cases & excel_f) / max(1, len(func_cases)), 4),
        "case_to_case_edges_stored_once": sim_n, "case_to_case_avg_per_case": round(sim_n / n, 3),
        "case_to_case_avg_degree": round(2 * sim_n / n, 3), "case_to_case_max_degree": max(deg.values(), default=0),
        "placeholder_links": ph,
        "cases_with_real_manual_section_link": len(real_man), "real_manual_ratio": round(len(real_man) / n, 4),
        "cases_with_manual_page_pointer": len(page_cases), "page_pointer_ratio": round(len(page_cases) / n, 4),
    }


def compare_semantic(idx: Index, links: list[dict], sim: list[dict]) -> dict:
    """기존 case->case(semantic) 엣지를 새 관계로 대체할 수 있는지: 새 similar_to 보존율, 공유 키 설명률."""
    old = set()
    for c in idx.cases:
        for t in c.get("related_ids", []):
            if t.startswith("check:support-case:"):
                old.add(tuple(sorted((c["id"], t))))
    new_pairs = {tuple(sorted((p["from"], p["to"]))) for p in sim}
    scr: dict[str, set] = collections.defaultdict(set)
    for l in links:
        if l["relation"] in ("about_screen", "uses_function", "involves_item") and l["confidence"] >= 0.5:
            scr[l["from"]].add(l["to"])
    explained = sum(1 for a, b in old if scr[a] & scr[b])
    return {"old_pairs_undirected": len(old), "new_similar_pairs": len(new_pairs),
            "old_pairs_retained_in_new": len(old & new_pairs),
            "old_pairs_explained_by_shared_key": explained,
            "old_pairs_explained_ratio": round(explained / max(1, len(old)), 4),
            "new_pairs_not_in_old": len(new_pairs - old)}


def run(knowledge: Path, out_dir: Path, as_of: str) -> dict:
    records = load_records(knowledge)
    idx = Index(records)
    keys_list = [extract_case_keys(c, idx) for c in idx.cases]
    links = build_links(keys_list, idx, as_of)
    sim, _ = build_similar(keys_list, idx, as_of)
    any_screen = {l["from"] for l in links if l["relation"] == "about_screen"}
    no_key_ids = {k["id"] for k in keys_list if k["id"] not in any_screen}
    no_key_all = {k["id"] for k in keys_list if not k["has_text_key"]}
    scr_all: dict[str, set] = collections.defaultdict(set)
    for l in links:
        if l["relation"] == "about_screen":
            scr_all[l["from"]].add(l["to"])
    cands = build_candidates(keys_list, idx, as_of, no_key_ids, scr_all)
    all_links = links + sim

    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "case_keys.jsonl").open("w", encoding="utf-8") as fh:
        for k in keys_list:
            fh.write(json.dumps(k, ensure_ascii=False) + "\n")
    with (out_dir / "case_links.jsonl").open("w", encoding="utf-8") as fh:
        for l in all_links:
            fh.write(json.dumps(l, ensure_ascii=False) + "\n")
    with (out_dir / "case_candidates.jsonl").open("w", encoding="utf-8") as fh:
        for c in cands:
            fh.write(json.dumps(c, ensure_ascii=False) + "\n")

    key_counts = {
        "cases_with_screen_code": sum(bool(k["screen_codes"]) for k in keys_list),
        "cases_with_strong_screen_code": sum(any(is_strong(f) for f in k["screen_codes"]) for k in keys_list),
        "cases_with_screen_title": sum(bool(k["screen_titles"]) for k in keys_list),
        "cases_with_function": sum(bool(k["functions"]) for k in keys_list),
        "cases_with_item": sum(bool(k["item_codes"]) for k in keys_list),
        "cases_with_item_code_match": sum(any(f["match"] == "code" for f in k["item_codes"]) for k in keys_list),
        "cases_with_error_like_string": sum(any(e["error_like"] for e in k["error_strings"]) for k in keys_list),
        "cases_with_any_text_key": sum(k["has_text_key"] for k in keys_list),
        "cases_without_any_text_key": len(no_key_all),
        "cases_without_any_screen_link_candidates_searched": len(no_key_ids),
        "cases_without_any_key_of_any_kind": sum(1 for k in keys_list if not (k["screen_codes"] or k["screen_titles"] or k["functions"] or k["item_codes"])),
        "cases_with_unresolved_screen_code": sum(bool(k["unresolved_screen_codes"]) for k in keys_list),
        "top_unresolved_screen_codes": collections.Counter(u["code"] for k in keys_list for u in k["unresolved_screen_codes"]).most_common(10),
        "cases_with_mask_token": sum(bool(k["mask_tokens"]) for k in keys_list),
        "cases_with_feature_section_keyword": sum(bool(k["feature_sections"]) for k in keys_list),
    }
    rel_counts = collections.Counter(l["relation"] for l in all_links)
    grade_counts = collections.Counter((l["relation"], l["grade"]) for l in all_links)
    ph_replaced = ph_total = 0
    for c in idx.cases:
        if any(t.startswith(PLACEHOLDER_PREFIX) for t in c.get("related_ids", [])):
            ph_total += 1
    have_real = {l["from"] for l in all_links if l["relation"] in ("about_screen", "uses_function", "explained_in_manual")
                 and l["to"] != PAGE_INDEX_ID}
    ph_cases = [c["id"] for c in idx.cases if any(t.startswith(PLACEHOLDER_PREFIX) for t in c.get("related_ids", []))]
    ph_replaced = sum(1 for c in ph_cases if c in have_real)
    ph_cand = sum(1 for c in cands if c["case_id"] in set(ph_cases) and c["candidates"] and c["confident"])
    report = {
        "as_of": as_of, "cases": len(idx.cases),
        "key_counts": key_counts,
        "relation_counts": dict(rel_counts),
        "relation_grade_counts": {f"{k[0]}/{k[1]}": v for k, v in grade_counts.items()},
        "before": before_metrics(idx, keys_list),
        "after": after_metrics(idx, keys_list, links, sim, cands),
        "placeholder": {"cases_with_placeholder_before": len(ph_cases), "replaced_by_real_link": ph_replaced,
                        "not_replaced_but_has_confident_candidate": ph_cand,
                        "new_placeholder_links": sum(1 for l in all_links if l["to"].startswith(PLACEHOLDER_PREFIX))},
        "semantic_vs_similar": compare_semantic(idx, links, sim),
        "candidate_validation": validate_candidates(keys_list, idx, links, as_of),
        "candidates": {"cases_with_candidates": sum(1 for c in cands if c["candidates"]), "cases_confident": sum(1 for c in cands if c["confident"]), "cases_total": len(cands)},
        "new_node_ids": {"functions": sorted({l["to"] for l in all_links if l["to"].startswith("check:func:")}),
                         "items_count": len({l["to"] for l in all_links if l["to"].startswith("check:item:")})},
    }
    (out_dir / "case_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--knowledge", type=Path, default=DEFAULT_KNOWLEDGE)
    ap.add_argument("--out-dir", type=Path, default=Path("tmp"))
    ap.add_argument("--as-of", default=DEFAULT_AS_OF)
    ap.add_argument("--report", action="store_true", help="전후 지표를 stdout 에 JSON 으로 출력")
    args = ap.parse_args(argv)
    report = run(args.knowledge, args.out_dir, args.as_of)
    if args.report:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""문의 사례(support_case) 공개용 변형기 (규칙 기반, 외부 호출 없음).

목적
    PUBLIC 레포에 올라가는 문의 사례에서 개인·기관 식별 단서를 제거하거나
    "자연스러운 일반화"로 바꾼다. 화면번호·TR·함수 호출식·오류 문구·처리 결과 같은
    기술 사실은 변형 전후가 같아야 한다 (scripts/leak_gate.py 가 검증).

규칙 요약
    1. 전화번호/내선/이메일/URL/IP        -> 제거 또는 '상담 창구' 등으로 일반화.
       '- 전화번호 : ...' 필드는 통째로 제거.
    2. 회사·기관·사람 고유명사             -> 사전으로 '한 증권사', '한 자산운용사', '고객사',
       '담당자' 등 문맥 일반어로 치환. 사전 = (a) 입력 텍스트에서 접미사 규칙으로 자동 수집
       + (b) --names-file(수동 목록). 실제 회사명 목록은 공개 레포에 두면 그 자체가 누출이므로
       코드에는 넣지 않고 gitignore 된 private/ 아래 파일로만 받는다.
    3. 구체적 날짜·시각                   -> '해당 일자', '오전'/'오후', '그 시각'. 시장 고정 시각
       (09:00, 15:30 등)은 기술 사실로 보고 유지.
    4. 원본 위치 단서 ('CRM데이터(PID복원)!row:12', '20260101!row:4', workbook:..., 'PID복원',
       'CRM-00001')                     -> 제거하고 솔트 해시 source_ref ('sref:xxxxxxxxxxxx',
       'case-xxxxxxxx') 로 대체. 원본<->변형본 대응은 이 해시로만 가능.
       JSON 레코드의 evidence_locator/source_locator 키는 source_ref 로 바뀌고
       source_cell_ids 는 삭제된다.
    5. 인사말/자기소개 ('안녕하세요. 체크+ 입니다.', '감사합니다.') 제거, 일부 어미 정리.

마스킹 토큰 vs 고객이 말한 실제 증상 (설계)
    원본에는 상류 비식별화가 남긴 자리표시자 [REDACTED_ENTITY] [IDENTIFIER] [NUMBER]
    [PERSON] [PHONE] [EMAIL] [PATH] 가 섞여 있다. 두 경우를 구분한다.
      (A) 자리표시자: 원래 값이 지워진 자리. 문맥 일반어로 치환한다
          ([REDACTED_ENTITY]->고객사, [IDENTIFIER]->특정 종목, [NUMBER]->특정 수치,
           [PERSON]->담당자, [PHONE]->상담 창구, [EMAIL]->공식 문의 채널, [PATH]->특정 경로).
      (B) 증상 문자열: 고객이 "함수가 '[NUMBER]' 로 표시된다" 처럼 화면에 보인 값을 말한 문장.
          판정 규칙: 토큰이 따옴표로 단독으로 감싸이고 뒤 20자 안에 표시 동사(표시/나오/뜨/출력/
          보이/반환...)가 있거나, 토큰 바로 뒤가 '(으)로|라고|라는 + 표시 동사' 인 경우.
          증상 토큰은 지우지 않고 ⟦[NUMBER]⟧ 처럼 ⟦ ⟧ 로 감싸 "자리표시자가 아님"을 명시한다.
      함수 호출식·보존 오류 문구 안의 토큰은 인자가 가려진 것이므로 역시 ⟦ ⟧ 로 감싼다.
      따라서 공개 산출물에서 맨 [NUMBER] 는 0건이어야 하고 ⟦[NUMBER]⟧ 는 허용(증상/인자 보존).
      기술 사실 비교는 ⟦ ⟧ 를 벗긴 정규형으로 한다 (extract_facts).

보존 목록 (변형 전후 동일해야 함)
    - 화면번호: '화면번호 : 1234, 5678', '1234 화면', '[1234]', 'TR 1234'
    - 함수 호출식: '=CT(...)', 'CLIST(...)' (괄호 균형 기준 전체)
    - 오류 문구: #NAME? 등 엑셀 오류 코드, 오류 단서(오류/없습니다/불가/비활성/null ...)가 있는
      따옴표 문구
    - 처리 결과 문장은 일반 본문에 남기며 (고유명사/전화/날짜만 변형) 별도 규칙으로 건드리지 않는다.

한계 (사람 검수 필요): 문장 단위 재서술은 규칙만으로는 하지 못한다. 문장 구조는 원문과
    상당 부분 겹치므로 leak_gate 의 n-gram 겹침 지표로 정도를 보고하고, 임계 초과분은 사람이
    다시 써야 한다.

사용
    uv run --offline --no-sync python scripts/sanitize_cases.py \
        sources/check-expert/manual-enrichment.jsonl knowledge/check-expert/knowledge.jsonl \
        content/check-expert/문의-대응 -o tmp/sanitized --report tmp/sanitized/report.json
    (출력과 .sanitize_salt 는 커밋 금지)
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import secrets
import sys
from collections import Counter
from pathlib import Path
from typing import Any

SENT_L, SENT_R = "", ""
WRAP_L, WRAP_R = "⟦", "⟧"

TOKEN_NAMES = ("REDACTED_ENTITY", "IDENTIFIER", "NUMBER", "PERSON", "PHONE", "EMAIL", "PATH")
TOKEN_RE = re.compile(r"\[(" + "|".join(TOKEN_NAMES) + r")\]")
PARTIAL_TOKEN_RE = re.compile(r"\[(?:R|RE|RED\w*|I|ID\w*|N|NU\w*|P|PE\w*|PH\w*|PA\w*|E|EM\w*)(?=$|\.md$)")

TOKEN_WORDS = {
    "REDACTED_ENTITY": "고객사",
    "IDENTIFIER": "특정 종목",
    "NUMBER": "특정 수치",
    "PERSON": "담당자",
    "PHONE": "상담 창구",
    "EMAIL": "공식 문의 채널",
    "PATH": "특정 경로",
}

# ---------------------------------------------------------------- 패턴
PHONE_FIELD_RE = re.compile(
    r"(?:(?<=\s)|^)-?[ \t]*전화번호[ \t]*[:：][ \t]*(?:\[PHONE\]|\d[\d\- ()]*\d|-(?=\s))?"
)
PHONE_RES = [
    re.compile(r"(?<![0-9A-Za-z-])0\d{1,2}[-. )]\s?\d{3,4}[-. ]\d{4}(?![0-9A-Za-z-])"),
    re.compile(r"(?<![0-9A-Za-z-])01\d[ ]?\d{3,4}[ ]?\d{4}(?![0-9A-Za-z-])"),
    re.compile(r"(?<![0-9A-Za-z-])\d{3}-\d{4}(?![0-9A-Za-z-])"),
    re.compile(r"(?:내선|전화|연락처|TEL\.?|Tel\.?|T\.|직통)\s*[:：]?\s*\d{3,4}-\d{4}(?![0-9A-Za-z-])"),
    re.compile(r"(?:내선|ext\.?)\s*[:：]?\s*\d{3,5}"),
]
PHONE44_RE = re.compile(r"(?<![0-9A-Za-z-])(\d{4})-(\d{4})(?![0-9A-Za-z-])")


PHONE44_SLUG_RE = re.compile(r"(?<![0-9A-Za-z])(\d{4})-(\d{4})(?![0-9A-Za-z])")


def phone44_spans(text: str, slug: bool = False) -> list[tuple[int, int]]:
    """'1234-5678' 처럼 4-4 자리 전화번호 추정. 화면번호 범위('1147-1148')와 구분하려고
    화면/TR/번/~ 문맥이 가깝거나 두 수가 50 이내로 가까우면 제외한다."""
    out = []
    for m in (PHONE44_SLUG_RE if slug else PHONE44_RE).finditer(text):
        a, b = int(m.group(1)), int(m.group(2))
        ctx = text[max(0, m.start() - 6) : m.start()] + " " + text[m.end() : m.end() + 6]
        if re.search(r"화면|TR|번|~|\uE000", ctx) or abs(a - b) <= 50:
            continue
        out.append(m.span())
    return out


PHONE_CUE_RE = re.compile(r"(?:내선|전화번호?|연락처|TEL\.?|직통)\s*[:：]?\s*\[PHONE\]")
EMAIL_RE = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
URL_RE = re.compile(r"https?://[^\s)\]'\"]+")
IP_RE = re.compile(r"(?<![\d.])\d{1,3}(?:\.\d{1,3}){3}(?![\d.])")

LOCATOR_RE = re.compile(r"[^\s`'\"|,()\[\]]*(?:\([^\s()]*\))?[^\s`'\"|,()\[\]]*!row:\d+")
ROW_RE = re.compile(r"(?<![\w])row:\d+")
WORKBOOK_RE = re.compile(r"workbook:[\w:]+")
CRM_ID_RE = re.compile(r"CRM-\d{3,6}")
LOC_WORD_RE = re.compile(r"CRM데이터|PID복원")

GREETING_RE = re.compile(
    r"안녕하세요[.,! ]*(?:\[(?:REDACTED_ENTITY|IDENTIFIER|PERSON)\]\+?[가-힣\s]{0,8}?입니다[.!]?)?\s*"
)
CLOSING_RE = re.compile(r"\s*(?:감사합니다|수고하세요|고맙습니다)[.!]*\s*$")
ENDING_MAP = [
    (re.compile(r"문의\s*드립니다"), "문의"),
    (re.compile(r"문의\s*드리겠습니다"), "문의"),
    (re.compile(r"안내\s*부탁\s*드리겠습니다|안내\s*부탁\s*드립니다"), "안내 요청"),
    (re.compile(r"확인\s*부탁\s*드립니다|확인\s*부탁\s*드리겠습니다"), "확인 요청"),
]

FN_START_RE = re.compile(r"(?<![A-Za-z0-9_.])(=?)([A-Z][A-Za-z0-9_.]{1,})\(")
FN_EQ_KO_RE = re.compile(r"(?<![A-Za-z0-9_.가-힣])=([가-힣][가-힣A-Za-z0-9_.]*)\(")
YAML_KEY_RE = re.compile(r"^\s*(?:-\s+)?[\w가-힣_-]+:\s*$")
EXCEL_ERR_RE = re.compile(r"#(?:NAME\?|VALUE!|REF!|DIV/0!|N/A|NUM!|NULL!|SPILL!|CALC!)")
ERR_CUE_RE = re.compile(
    r"오류|에러|없습니다|없다|불가|실패|비활성|권한|null|Exception|[Ee]rror|잘못|존재하지|찾을 수|접근|액세스|엑세스|만료"
)
QUOTE_RES = [
    re.compile(r"(?<![A-Za-z0-9])'([^'\n|]{6,120})'(?![A-Za-z0-9])"),
    re.compile(r'(?<![A-Za-z0-9])"([^"\n|]{6,120})"(?![A-Za-z0-9])'),
    re.compile(r"‘([^’\n]{6,150})’"),
    re.compile(r"“([^”\n]{6,150})”"),
    re.compile(r"「([^」\n]{6,150})」"),
]
SCREEN_RES = [
    re.compile(r"화면번호\s*[:：]\s*[\d,\s/]*\d"),
    re.compile(r"(?<![\d/.])\d{4}[ \t]*(?:번[ \t]*)?화면"),
    re.compile(r"화면[ \t]*\d{4}(?![\d/.:-])"),
    re.compile(r"\[\d{4}\]"),
    re.compile(r"TR[ \t]*[:#]?[ \t]*\d{4}(?!\d)"),
]

DISPLAY_VERB = r"(?:표시|나오|나옵|나와|뜨|뜹|뜸|출력|보이|보입|보여|찍히|찍혀|반환|리턴)"
SYMPTOM_RES = [
    re.compile(r"['\"‘“「]\s*\[(?:" + "|".join(TOKEN_NAMES) + r")\]\s*['\"’”」][^\n]{0,20}?" + DISPLAY_VERB),
    re.compile(r"\[(?:" + "|".join(TOKEN_NAMES) + r")\]\s*(?:으로|로|라고|라는|이라고)\s*" + DISPLAY_VERB),
]

DATE_RES = [
    (re.compile(r"(?<!\d)20\d{2}[-./]\d{1,2}[-./]\d{1,2}(?!\d)"), "해당 일자"),
    (re.compile(r"(?<!\d)20\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])(?!\d)"), "해당 일자"),
    (re.compile(r"(?<!\d)\d{1,2}월\s*\d{1,2}일"), "해당 일자"),
    (re.compile(r"(?<![\d.])(?:0[1-9]|1[0-2])\.(?:0[1-9]|[12]\d|3[01])(?![\d.])"), "해당 일자"),
]
AMPM_RE = re.compile(r"(오전|오후)\s*\d{1,2}\s*시(?:\s*\d{1,2}\s*분)?(?:\s*경)?")
HOUR_RE = re.compile(r"(?<![\d:.])(\d{1,2})\s*시(?!간|세|리|스|대|장|가)(?:\s*\d{1,2}\s*분)?")
CLOCK_RE = re.compile(r"(?<![\d.:])([01]?\d|2[0-3]):([0-5]\d)(?![\d:])")
MARKET_TIMES = {"08:00", "08:30", "08:45", "09:00", "15:20", "15:30", "15:45", "18:00"}

TITLE_NAME_RE = re.compile(
    r"(?<![가-힣])([가-힣]{2,3})\s?(님|과장님?|차장님?|부장님?|대리님?|팀장님?|주임님?|매니저님?|책임님?|사원님?)"
)
SURNAMES = set("김이박최정강조윤장임한오서신권황안송류전홍고문양손배백허유남심노하곽성차주우구나민진지엄채원천방공현함변염여추도소석선설마길연위표명기반왕금옥육인맹제모탁국어은편용예경봉")
NOT_NAME_STEMS = {"고객", "담당", "사용", "관리", "이용", "직원", "운영", "선생", "사장", "회원", "해당", "기관", "투자",
                  "고객사", "사용자", "관리자", "운용", "문의", "신청", "요청", "확인", "가입", "대표", "본부"}

SUFFIX_CLASS = {
    "자산운용": "한 자산운용사", "자산": "한 자산운용사", "투자증권": "한 증권사", "증권": "한 증권사",
    "캐피탈": "한 캐피탈사", "저축은행": "한 저축은행", "은행": "한 은행", "생명": "한 보험사",
    "화재": "한 보험사", "카드": "한 카드사",
}
SUFFIX_ORDER = ["자산운용", "투자증권", "저축은행", "캐피탈", "증권", "은행", "생명", "화재", "카드", "자산"]
JOSA = set("은는이가을를의에와과로도만께서")
GENERIC_STEMS = {
    "기초", "지수", "금융", "총", "순", "위험", "무형", "해외", "국내", "외화", "유동", "고정", "운용", "보유",
    "부실", "담보", "기타", "수익", "평가", "실물", "대체", "투자", "시중", "시장", "단기금융", "유동화",
    "상장", "파생결합", "신종자본", "주식관련", "후순위", "채권", "외국계", "지방", "특수", "일반", "전체",
    "사모", "공모", "집합투자", "우선", "보통", "관련", "해당", "연계", "기준", "대상", "종목", "개별", "금융투자",
    "주식", "원화", "외국", "상품", "신용", "자기", "타인", "발행", "예탁", "이자", "비상장", "상환", "만기",
    "유무형", "유형", "재고", "주당순", "준비", "카드", "개인", "법인", "기관", "공통", "정상", "환매", "구조화", "선물", "옵션", "장외", "장내", "ETF", "ETN",
}
GENERIC_STEM_ENDINGS = ("화", "금융", "채", "상품", "연계", "관련", "지수", "기초", "유가", "매매", "보유", "가능",
                        "신종", "인수권", "매도", "예수", "수익자", "대여", "대차", "관계회사", "잡", "비유동", "리스", "당좌")
GENERIC_STEM_PREFIXES = ("기타", "단기", "장기", "만기", "매도", "상호", "예금")
WORD_RE = re.compile(r"[가-힣]{3,}")


# ---------------------------------------------------------------- 이름 사전
def collect_names(texts: list[str]) -> dict[str, str]:
    """접미사 규칙으로 회사명 후보를 자동 수집한다. {이름: 치환어}."""
    found: dict[str, str] = {}
    for t in texts:
        for w in WORD_RE.findall(t):
            cands = [w]
            if len(w) > 3 and w[-1] in JOSA:
                cands.append(w[:-1])
            if len(w) > 4 and w[-2] in JOSA:
                cands.append(w[:-2])
            for c in cands:
                for suf in SUFFIX_ORDER:
                    if c.endswith(suf) and len(c) > len(suf):
                        stem = c[: -len(suf)]
                        if not (2 <= len(stem) <= 6):
                            break
                        if stem in GENERIC_STEMS or stem.endswith(GENERIC_STEM_ENDINGS) or stem.startswith(GENERIC_STEM_PREFIXES):
                            break
                        if suf == "자산" and len(stem) > 3:
                            break
                        found[c] = SUFFIX_CLASS[suf]
                        break
    return found


def load_names_file(path: Path | None) -> dict[str, str]:
    """수동 목록. 한 줄에 `이름` 또는 `이름<TAB>치환어`. '#' 주석."""
    out: dict[str, str] = {}
    if not path or not path.exists():
        return out
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, _, repl = line.partition("\t")
        out[name.strip()] = repl.strip() or "고객사"
    return out


# ---------------------------------------------------------------- 사실 추출 (게이트와 공유)
BREAK_CHARS = "\n`…"


def _balanced(text: str, open_idx: int, limit: int = 600) -> tuple[int | None, int]:
    """(닫는 괄호 다음 인덱스 또는 None, 탐색을 멈춘 인덱스)."""
    depth = 0
    for i in range(open_idx, min(len(text), open_idx + limit)):
        c = text[i]
        if c in BREAK_CHARS or text.startswith("]]", i):
            return None, i
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i + 1, i
    return None, min(len(text), open_idx + limit)


def find_function_spans(text: str) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    pos = 0
    while True:
        cands = []
        m1 = FN_START_RE.search(text, pos)
        if m1:
            cands.append(m1)
        m2 = FN_EQ_KO_RE.search(text, pos)
        if m2:
            cands.append(m2)
        if not cands:
            break
        m = min(cands, key=lambda x: x.start())
        open_idx = m.end() - 1
        end, stop = _balanced(text, open_idx)
        eq = text[m.start()] == "="
        if end is None:
            pos = max(m.end(), stop)  # 잘린 호출식: 끊긴 곳까지를 보존 대상으로
            if eq:
                spans.append((m.start(), max(m.end(), stop)))
            continue
        body = text[open_idx + 1 : end - 1]
        looks_fn = eq or "," in body or re.search(r"['\"]|\[(?:" + "|".join(TOKEN_NAMES) + r")\]|^\s*\d+\s*$", body)
        if looks_fn:
            spans.append((m.start(), end))
        pos = end
    return spans


def find_error_spans(text: str) -> list[tuple[int, int]]:
    chars = list(text)
    for a, b in find_function_spans(text):
        for i in range(a, b):
            chars[i] = " "
    masked = "".join(chars)
    spans = [m.span() for m in EXCEL_ERR_RE.finditer(masked)]
    for rx in QUOTE_RES:
        for m in rx.finditer(masked):
            ls = masked.rfind("\n", 0, m.start()) + 1
            le = masked.find("\n", m.end())
            le = len(masked) if le == -1 else le
            if YAML_KEY_RE.match(masked[ls : m.start()]) and not masked[m.end() : le].strip():
                continue  # `title: "..."` 처럼 YAML 값 전체를 감싼 따옴표
            if ERR_CUE_RE.search(m.group(1)) and not TOKEN_RE.fullmatch(m.group(1).strip()):
                spans.append(m.span())
    return spans


def find_screen_spans(text: str) -> list[tuple[int, int]]:
    return [m.span() for rx in SCREEN_RES for m in rx.finditer(text)]


def _norm_fact(s: str) -> str:
    s = s.replace(WRAP_L, "").replace(WRAP_R, "")
    return re.sub(r"\s+", "", s)


LINK_TARGET_RE = re.compile(r"\[\[(?!(?:REDACTED_ENTITY|IDENTIFIER|NUMBER|PERSON|PHONE|EMAIL|PATH)\])(?:(?!\]\]|\|)[^\n])+")


def extract_facts(text: str) -> list[str]:
    """기술 사실(화면번호/함수식/오류문구)을 정규형 목록으로 반환한다. 정렬된 목록 비교용.
    위키링크 대상(슬러그)은 파일명 변형의 영향을 받으므로 제외한다."""
    text = LINK_TARGET_RE.sub("[[", text)
    facts: list[str] = []
    for s, e in find_function_spans(text):
        facts.append("fn:" + _norm_fact(text[s:e]))
    for s, e in find_error_spans(text):
        facts.append("err:" + _norm_fact(text[s:e]))
    for rx in SCREEN_RES:
        for m in rx.finditer(text):
            for n in re.findall(r"(?<!\d)\d{4}(?!\d)", m.group(0)):
                facts.append("screen:" + n)
    return sorted(facts)


def strip_protected(text: str) -> str:
    """겹침 계산 등에서 기술 사실 구간을 제거한 텍스트."""
    text = LINK_TARGET_RE.sub("[[", text)
    spans = sorted(find_function_spans(text) + find_error_spans(text) + find_screen_spans(text))
    out, last = [], 0
    for s, e in spans:
        if s < last:
            continue
        out.append(text[last:s])
        last = e
    out.append(text[last:])
    return " ".join(out)


# ---------------------------------------------------------------- 컨텍스트
class Ctx:
    def __init__(self, salt: str, names: dict[str, str]):
        self.salt = salt
        self.names = dict(sorted(names.items(), key=lambda kv: -len(kv[0])))
        self.stats: Counter[str] = Counter()
        self.flags: Counter[str] = Counter()

    def h(self, kind: str, value: str, n: int = 12) -> str:
        return hashlib.sha256(f"{self.salt}|{kind}|{value}".encode()).hexdigest()[:n]

    def sref(self, locator: str) -> str:
        return "sref:" + self.h("loc", locator)


class _Store:
    def __init__(self) -> None:
        self.items: list[str] = []

    def put(self, s: str) -> str:
        self.items.append(s)
        return f"{SENT_L}{len(self.items) - 1}{SENT_R}"

    def restore(self, text: str) -> str:
        for _ in range(3):
            text = re.sub(SENT_L + r"(\d+)" + SENT_R, lambda m: self.items[int(m.group(1))], text)
            if SENT_L not in text:
                break
        return text


def _wrap_tokens(s: str) -> str:
    return TOKEN_RE.sub(lambda m: WRAP_L + m.group(0) + WRAP_R, s)


def _merge_spans(spans: list[tuple[int, int]]) -> list[tuple[int, int]]:
    out: list[tuple[int, int]] = []
    for s, e in sorted(spans):
        if out and s < out[-1][1]:
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def _protect(text: str, store: _Store, spans: list[tuple[int, int]], wrap: bool, ctx: "Ctx | None" = None) -> str:
    out, last = [], 0
    for s, e in _merge_spans(spans):
        out.append(text[last:s])
        seg = text[s:e]
        if ctx is not None:  # 고유명사는 보존 구간 안에서도 치환 (프라이버시 우선)
            for name, repl in ctx.names.items():
                seg = seg.replace(name, repl)
        out.append(store.put(_wrap_tokens(seg) if wrap else seg))
        last = e
    out.append(text[last:])
    return "".join(out)


# ---------------------------------------------------------------- 텍스트 변형
def sanitize_text(text: str, ctx: Ctx) -> str:
    if not text:
        return text
    st = ctx.stats
    store = _Store()

    # 위키링크 대상: 경로 규칙과 동일하게 (파일명 변형과 링크가 어긋나지 않도록)
    def _wl(m: re.Match[str]) -> str:
        return store.put("[[" + sanitize_path(m.group(1), ctx))

    text = re.sub(r"\[\[(?!(?:REDACTED_ENTITY|IDENTIFIER|NUMBER|PERSON|PHONE|EMAIL|PATH)\])((?:(?!\]\]|\|)[^\n])+)", _wl, text)

    # 1) 원본 위치 단서 -> 해시
    def _loc(m: re.Match[str]) -> str:
        st["locator->sref"] += 1
        return store.put(ctx.sref(m.group(0)))

    text = LOCATOR_RE.sub(_loc, text)
    text, n = ROW_RE.subn("", text); st["row-clue"] += n
    text, n = WORKBOOK_RE.subn("", text); st["workbook-clue"] += n
    text, n = LOC_WORD_RE.subn("", text); st["origin-word"] += n
    text = CRM_ID_RE.sub(lambda m: (st.update({"crm-id": 1}), store.put("case-" + ctx.h("crm", m.group(0), 8)))[1], text)

    # 2) 보존 구간 보호 (함수식, 오류 문구, 화면 참조) -- 안의 토큰은 ⟦ ⟧ 로 감싸고 고유명사는 치환
    text = _protect(text, store, find_function_spans(text) + find_error_spans(text), True, ctx)
    text = _protect(text, store, find_screen_spans(text), False, ctx)

    # 3) 연락처
    text, n = PHONE_FIELD_RE.subn(lambda m: "" if re.match(r"\s*-", text[m.end():m.end() + 4]) else "- ", text)
    st["phone-field"] += n
    text, n = EMAIL_RE.subn("공식 문의 채널", text); st["email"] += n
    text, n = URL_RE.subn("공개 링크", text); st["url"] += n
    text, n = IP_RE.subn("특정 주소", text); st["ip"] += n
    for rx in PHONE_RES:
        text, n = rx.subn("상담 창구", text); st["phone"] += n
    for a, b in reversed(phone44_spans(text)):
        text = text[:a] + "상담 창구" + text[b:]
        st["phone"] += 1
    text, n = PHONE_CUE_RE.subn("상담 창구", text); st["phone"] += n
    text, n = re.subn(r"(?:내선|전화번호?|연락처)\s*[:：]?\s*(?:\[PHONE\])", "상담 창구", text); st["phone"] += n
    text = TOKEN_RE.sub(lambda m: "상담 창구" if m.group(1) == "PHONE" else m.group(0), text)

    # 4) 인사말/어미
    text, n = GREETING_RE.subn("", text); st["greeting"] += n
    text, n = CLOSING_RE.subn("", text); st["closing"] += n
    for rx, rep in ENDING_MAP:
        text = rx.sub(rep, text)

    # 5) 마스킹 토큰: 증상(⟦ ⟧ 보존) vs 자리표시자(일반어)
    sym_spans = [m.span() for rx in SYMPTOM_RES for m in rx.finditer(text)]
    if sym_spans:
        out, last = [], 0
        for s, e in _merge_spans(sym_spans):
            out.append(_tok_words(text[last:s], st))
            seg = text[s:e]
            st["symptom-token-kept"] += len(TOKEN_RE.findall(seg))
            out.append(store.put(_wrap_tokens(seg)))
            last = e
        out.append(_tok_words(text[last:], st))
        text = "".join(out)
    else:
        text = _tok_words(text, st)
    text = PARTIAL_TOKEN_RE.sub("", text)

    # 6) 고유명사
    for name, repl in ctx.names.items():
        if name in text:
            text = text.replace(name, repl)
            st["name-dict"] += 1
    text = _titled_names(text, ctx)

    # 7) 날짜/시각
    for rx, rep in DATE_RES:
        text, n = rx.subn(rep, text); st["date"] += n
    text, n = AMPM_RE.subn(lambda m: m.group(1), text); st["time"] += n
    text, n = HOUR_RE.subn(lambda m: "오후" if int(m.group(1)) >= 12 else "오전", text); st["time"] += n

    def _clock(m: re.Match[str]) -> str:
        if f"{int(m.group(1)):02d}:{m.group(2)}" in MARKET_TIMES:
            return m.group(0)
        st["time"] += 1
        return "그 시각"

    text = CLOCK_RE.sub(_clock, text)

    # 8) 정리
    text = re.sub(r"(고객사|특정 종목|특정 수치|담당자|상담 창구|한 [가-힣]+사|해당 일자)(?:[\s,/·]+\1)+", r"\1", text)
    text = re.sub(r"기관\s*고객사", "해당 기관", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"\s+([,.])", r"\1", text)
    text = text.strip(" \t") if "\n" not in text else text
    return store.restore(text)


def neutralize_tokens(text: str) -> str:
    """마스킹 토큰만 일반어로 바꾸는 최소 변형. 날짜·고유명사·인사말·원본 위치는 건드리지 않는다.
    함수식·오류 문구·증상 문장 안의 토큰은 ⟦ ⟧ 로 감싸 보존한다(sanitize_text 5단계와 같은 규칙)."""
    if not text or "[" not in text:
        return text
    st: Counter[str] = Counter()
    store = _Store()
    text = _protect(text, store, find_function_spans(text) + find_error_spans(text), True)
    text = _protect(text, store, find_screen_spans(text), False)
    sym_spans = [m.span() for rx in SYMPTOM_RES for m in rx.finditer(text)]
    out, last = [], 0
    for a, b in _merge_spans(sym_spans):
        out.append(_tok_words(text[last:a], st))
        out.append(store.put(_wrap_tokens(text[a:b])))
        last = b
    out.append(_tok_words(text[last:], st))
    text = PARTIAL_TOKEN_RE.sub("", "".join(out))
    text = re.sub(r"(고객사|특정 종목|특정 수치|담당자|상담 창구|공식 문의 채널|특정 경로)(?:[\s,/·]+\1)+", r"\1", text)
    text = re.sub(r"특정 종목\s*(종목|코드)", "특정 종목", text)
    return store.restore(text)


def _tok_words(seg: str, st: Counter[str]) -> str:
    def rep(m: re.Match[str]) -> str:
        st["token->word"] += 1
        return TOKEN_WORDS[m.group(1)]

    return TOKEN_RE.sub(rep, seg)


def _titled_names(text: str, ctx: Ctx) -> str:
    def rep(m: re.Match[str]) -> str:
        stem = m.group(1)
        if stem[0] not in SURNAMES or stem in NOT_NAME_STEMS or any(stem.startswith(s) for s in NOT_NAME_STEMS):
            return m.group(0)
        ctx.stats["person-guess"] += 1
        return "담당자님" if m.group(2).endswith("님") else "담당자 " + m.group(2)

    return TITLE_NAME_RE.sub(rep, text)


def sanitize_path(path: str, ctx: Ctx) -> str:
    """파일 경로/슬러그용: 공백 대신 하이픈, 잘린 토큰 제거, 날짜·시각 일반화."""
    p = TOKEN_RE.sub(lambda m: TOKEN_WORDS[m.group(1)], path)
    p = PARTIAL_TOKEN_RE.sub("", p)
    for name, repl in ctx.names.items():
        p = p.replace(name, repl)
    p = LOC_WORD_RE.sub("", p)
    for a, b in reversed(phone44_spans(p, slug=True)):
        p = p[:a] + "상담-창구" + p[b:]
    for rx, rep in DATE_RES:
        p = rx.sub(rep, p)
    p = AMPM_RE.sub(lambda m: m.group(1), p)
    p = HOUR_RE.sub(lambda m: "오후" if int(m.group(1)) >= 12 else "오전", p)
    p = re.sub(r"\s+", "-", p)
    p = re.sub(r"-{2,}", "-", p)
    return p.replace("-.md", ".md")


# ---------------------------------------------------------------- JSON 레코드
SKIP_KEYS = {"id", "type", "schema_version", "target_id", "related_ids", "source", "screen_code", "category",
             "review_status", "mapping_status", "case_type", "case_facets", "evidence_type"}
LOCATOR_KEYS = {"evidence_locator", "source_locator"}
DROP_KEYS = {"source_cell_ids"}


def sanitize_obj(obj: Any, ctx: Ctx, key: str | None = None) -> Any:
    if isinstance(obj, dict):
        out: dict[str, Any] = {}
        for k, v in obj.items():
            if k in DROP_KEYS:
                ctx.stats["dropped-source-cells"] += 1
                continue
            if k in LOCATOR_KEYS and isinstance(v, str):
                out["source_ref"] = ctx.sref(v)
                ctx.stats["locator->sref"] += 1
                continue
            if k == "markdown_path" and isinstance(v, str):
                out[k] = sanitize_path(v, ctx)
                continue
            nk = sanitize_text(k, ctx) if isinstance(k, str) and k not in SKIP_KEYS else k
            out[nk] = sanitize_obj(v, ctx, k)
        return out
    if isinstance(obj, list):
        return [sanitize_obj(v, ctx, key) for v in obj]
    if isinstance(obj, str):
        if key in SKIP_KEYS:
            return CRM_ID_RE.sub(lambda m: "case-" + ctx.h("crm", m.group(0), 8), obj)
        return sanitize_text(obj, ctx)
    return obj


def iter_strings(obj: Any):
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield k
            yield from iter_strings(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from iter_strings(v)
    elif isinstance(obj, str):
        yield obj


def resolve_salt(arg: str | None, outdir: Path) -> str:
    if arg:
        return arg
    if os.environ.get("SANITIZE_SALT"):
        return os.environ["SANITIZE_SALT"]
    f = outdir / ".sanitize_salt"
    if f.exists():
        return f.read_text().strip()
    outdir.mkdir(parents=True, exist_ok=True)
    s = secrets.token_hex(16)
    f.write_text(s)
    return s


def review_flags(text: str) -> list[str]:
    """규칙이 판단하지 못해 사람 검수가 필요한 잔여 패턴."""
    t = strip_protected(text)
    flags = []
    if re.search(r"(?<![\d.,])\d{7,}(?![\d])", t):
        flags.append("long-digit-run")
    if re.search(r"[A-Z][a-z]{2,}(?:\s[A-Z][a-z]{2,})+", t):
        flags.append("latin-proper-noun-guess")
    if re.search(r"[가-힣]{2,4}(?:\s)?(?:담당|대리|과장|차장|부장|팀장)(?!자)", t):
        flags.append("title-name-leftover")
    if re.search(r"(?:(?:이|그|저|해당)\s)?(?:지점|센터|본점|지사)\b", t):
        flags.append("org-unit-mention")
    return flags


def process_jsonl(src: Path, dst: Path, ctx: Ctx, report: dict) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    flags_by_ref: dict[str, list[str]] = {}
    with src.open(encoding="utf-8") as fi, dst.open("w", encoding="utf-8") as fo:
        for i, line in enumerate(fi, 1):
            if not line.strip():
                continue
            rec = sanitize_obj(json.loads(line), ctx)
            fo.write(json.dumps(rec, ensure_ascii=False) + "\n")
            fl = sorted({f for s in iter_strings(rec) for f in review_flags(s)})
            if fl:
                flags_by_ref[f"{dst.name}:{i}"] = fl
    report.setdefault("review_flags", {}).update(flags_by_ref)


def process_md_dir(src: Path, dst: Path, ctx: Ctx, report: dict) -> None:
    for f in sorted(src.rglob("*.md")):
        rel = f.relative_to(src)
        new_rel = Path(*[sanitize_path(p, ctx) for p in rel.parts])
        out = dst / new_rel
        out.parent.mkdir(parents=True, exist_ok=True)
        body = sanitize_text(f.read_text(encoding="utf-8"), ctx)
        out.write_text(body, encoding="utf-8")
        fl = review_flags(body)
        if fl:
            report.setdefault("review_flags", {})[str(new_rel)] = fl


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("inputs", nargs="+", type=Path, help="*.jsonl 파일 또는 *.md 디렉터리")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--names-file", type=Path, default=Path("private/sanitize_names.txt"))
    ap.add_argument("--emit-names", type=Path, help="자동 수집한 회사명 후보 저장(로컬 전용, 커밋 금지)")
    ap.add_argument("--salt")
    ap.add_argument("--report", type=Path)
    a = ap.parse_args(argv)

    texts: list[str] = []
    for p in a.inputs:
        if p.is_dir():
            texts += [f.read_text(encoding="utf-8") + " " + f.name for f in p.rglob("*.md")]
        else:
            for line in p.open(encoding="utf-8"):
                if line.strip():
                    texts += list(iter_strings(json.loads(line)))
    auto = collect_names(texts)
    names = {**auto, **load_names_file(a.names_file)}
    if a.emit_names:
        a.emit_names.parent.mkdir(parents=True, exist_ok=True)
        a.emit_names.write_text("\n".join(f"{k}\t{v}" for k, v in sorted(names.items())) + "\n", encoding="utf-8")

    ctx = Ctx(resolve_salt(a.salt, a.out), names)
    report: dict[str, Any] = {"auto_names": len(auto), "manual_names": len(names) - len(auto)}
    for p in a.inputs:
        if p.is_dir():
            process_md_dir(p, a.out / p.name, ctx, report)
        else:
            process_jsonl(p, a.out / p.name, ctx, report)
    report["rule_counts"] = dict(ctx.stats)
    report["review_flag_counts"] = dict(Counter(f for v in report.get("review_flags", {}).values() for f in v))
    if a.report:
        a.report.parent.mkdir(parents=True, exist_ok=True)
        a.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"rule_counts": report["rule_counts"], "review_flag_counts": report["review_flag_counts"]},
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())

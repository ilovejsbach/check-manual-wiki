#!/usr/bin/env python3
"""문의 사례(support_case)를 '문의 의도'와 '시장 영역'으로 규칙 분류한다: ontology/case_classes.jsonl.

본문 키(TR·제목·함수·항목)가 없는 사례도 어떤 종류의 문의인지, 어느 영역인지 알 수 있게 한다.
  intent  screen_finding(화면 찾기) / data_availability(데이터 제공 여부) / data_error(수치 오류·정정 요청) /
          env_setup(설치·환경·접속) / account_access(계정·권한) / howto(사용법) / empty(내용 미기재) / other
  domain  채권 주식 선물 옵션 외환 ETP ELW 펀드 해외 경제지표 (여러 개 가능, 없으면 빈 목록)
근거는 사례 제목과 '사용자가 겪은 상황' 절의 키워드뿐이다(외부 모델 호출 없음). 등급은 auto_extracted, 검수 전이다.
사례 본문·원본 위치는 출력에 넣지 않는다.

사용:
  uv run --offline --no-sync python scripts/classify_cases.py          # 쓰기
  uv run --offline --no-sync python scripts/classify_cases.py --check  # 검증만
"""
from __future__ import annotations

import argparse
import collections
import json
import re
import sys
from pathlib import Path

DEFAULT_KNOWLEDGE = Path("knowledge/check-expert/knowledge.jsonl")
DEFAULT_OUT = Path("ontology/case_classes.jsonl")
DEFAULT_AS_OF = "2026-11-02"

# 순서가 우선순위다. 앞 규칙이 먼저 맞으면 그것을 쓴다.
INTENT_RULES: list[tuple[str, re.Pattern]] = [
    ("screen_finding", re.compile(r"화면(이|은)?\s*(있|어디|뭐)|어디(서|에서|에)\s*(볼|확인|조회|찾)|메뉴(가|는|에서)?\s*(어디|있)|찾(을|는|고)\s*수|볼\s*수\s*있는\s*(화면|메뉴)|조회\s*(가능한|할\s*수)\s*화면|리스트\s*확인")),
    ("env_setup", re.compile(r"설치|재설치|단말\s*교체|교체|초기화|포맷|윈도우|맥\b|MAC\b|네트워크|방화벽|접속\s*(이|이\s*안|불가|오류)|연결\s*(이|이\s*안|불가|오류)|VPN|원격|공인\s*IP|사내망|서버\s*(점검|장애)|실행\s*(이|이\s*안|불가|오류)|안\s*열|먹통|멈춤|튕", re.I)),
    ("account_access", re.compile(r"계정|아이디|비밀번호|패스워드|사용자\s*로그인\s*처리|로그인\s*(이\s*안|불가|실패|오류)|권한|인증서|OTP|사용자\s*(등록|추가|삭제)|라이선스|라이센스|재택\s*근무|접속하고자", re.I)),
    ("data_error", re.compile(r"오류|틀리|틀린|다르|상이|불일치|잘못|누락|안\s*나|안나|안\s*보|안보|표시\s*(가\s*)?(안|오류)|수정\s*요청|정정|변경되어|반영\s*(이\s*)?(안|늦|지연)|업데이트\s*(가\s*)?(안|늦)|갱신")),
    ("data_availability", re.compile(r"제공|확인\s*(가능|할\s*수)|가능한가|가능할까|있나요|있을까요|입수|언제|추가\s*(요청|가능)|지원\s*(하|되)|항목|데이터")),
    ("howto", re.compile(r"방법|어떻게|사용법|설정|하려면|하는\s*법|절차|문의\s*드립니다|문의드립니다")),
]
EMPTY = re.compile(r"문의\s*내용\s*미기재")
DOMAIN_RULES: dict[str, re.Pattern] = {
    "채권": re.compile(r"채권|국채|회사채|CB\b|전환가액|전환사채|금리|발행정보|당발|신용등급|BIS|KTB|스프레드", re.I),
    "주식": re.compile(r"주식|종목|코스피|코스닥|KOSPI|KOSDAQ|NXT|넥스트레이드|상장|배당|증자|감자|시가총액|호가|체결|거래량"),
    "선물": re.compile(r"선물|베이시스|미결제|만기|롤오버"),
    "옵션": re.compile(r"옵션|콜|풋|내재변동성|IV\b|행사가"),
    "외환": re.compile(r"외환|환율|달러|원화|USD|FX|스왑포인트|NDF"),
    "ETP": re.compile(r"ETF|ETN|ETP|NAV|괴리율|iNAV|PDF\b|구성종목", re.I),
    "ELW": re.compile(r"ELW|워런트"),
    "펀드": re.compile(r"펀드|수익증권|운용사|기준가"),
    "해외": re.compile(r"해외|미국|중국|일본|유럽|나스닥|다우|S&P|글로벌"),
    "경제지표": re.compile(r"경제지표|GDP|CPI|물가지수|금리\s*결정|PMI"),
}
SITUATION = re.compile(r"## 사용자가 겪은 상황\s*\n+(.+?)(?:\n## |\Z)", re.S)


def case_text(rec: dict) -> str:
    """분류 근거: 제목(사례 유형 접두 제외) + '사용자가 겪은 상황' 절. 응답 절은 쓰지 않는다."""
    title = re.sub(r"^[^—]+—\s*", "", rec.get("title") or "")
    m = SITUATION.search(rec.get("text") or "")
    return f"{title}\n{m.group(1).strip() if m else ''}"


def classify(rec: dict) -> dict:
    t = case_text(rec)
    if EMPTY.search(t) and len(t.strip()) < 40:
        intent, rule = "empty", "empty"
    else:
        intent, rule = "other", None
        for name, pat in INTENT_RULES:
            m = pat.search(t)
            if m:
                intent, rule = name, m.group(0)[:20]
                break
    domains = [d for d, pat in DOMAIN_RULES.items() if pat.search(t)]
    return {"case_id": rec["id"], "intent": intent, "intent_rule": rule, "domains": domains}


def compute(records: list[dict], as_of: str) -> list[dict]:
    out = []
    for r in records:
        if r.get("type") != "support_case":
            continue
        c = classify(r)
        c.update({"grade": "auto_extracted", "review_status": "candidate", "as_of": as_of})
        out.append(c)
    return sorted(out, key=lambda c: c["case_id"])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="사례 의도·영역 분류")
    ap.add_argument("--knowledge", type=Path, default=DEFAULT_KNOWLEDGE)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--as-of", default=DEFAULT_AS_OF)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    records = [json.loads(l) for l in args.knowledge.read_text(encoding="utf-8").splitlines() if l.strip()]
    rows = compute(records, args.as_of)
    print(json.dumps({"cases": len(rows), "intent": dict(collections.Counter(r["intent"] for r in rows)),
                      "with_domain": sum(1 for r in rows if r["domains"]),
                      "domain": dict(collections.Counter(d for r in rows for d in r["domains"]))}, ensure_ascii=False))
    if not args.check:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
        print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""CHECK Expert 로컬 설치의 항목·시장 메타(xlp_meta.sqlite)를 CSV로 추출한다.

원천: <설치폴더>\\CheckXL\\system\\xlp_meta.sqlite (앱이 쓰는 SQLite, 평문 UTF-8).
8003 「데이터항목 검색」 화면이 보여 주는 항목코드(FID)·시장코드(MID)·데이터 형식의 출처다.
시세 값은 이 DB에 없다. 구조 ID와 이름만 나온다.

읽기 전용: 앱이 쓰고 있는 파일을 건드리지 않도록 임시 폴더에 복사해서 읽는다.

사용:
  uv run python scripts/extract_check_meta.py
  uv run python scripts/extract_check_meta.py --src D:\\CheckExpert\\CheckXL\\system\\xlp_meta.sqlite
  uv run python scripts/extract_check_meta.py --check      # 파일을 쓰지 않고 건수만 점검
"""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import io
import json
import shutil
import sqlite3
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SRC = Path(r"C:\KOSCOM\CheckExpert\CheckXL\system\xlp_meta.sqlite")
DEFAULT_OUT = ROOT / "sources" / "check-expert" / "check-meta"

# 8003 화면 캡처(2026-11-03)에서 직접 확인한 DATA_TYPE → CH_Type 표기. 나머지는 확인 전이라 비워 둔다.
OBSERVED_CH_TYPE = {
    19: "UINT(숫자)",   # 15001 현재가, 14531 매수호가1, 15020 체결량
    3: "INT(숫자)",     # 15472 대비, 15004 등락률, 15009 시가
    4: "LNLN(숫자)",    # 15015 거래량, 15023 거래대금, 15028 시가총액
    17: "UCHAR(숫자)",  # 15006 등락구분
}

# (파일 이름, 질의, 헤더, gzip 여부)
TABLES = [
    ("fgid.csv", "SELECT FGID, DSCRPTN FROM FGID_LIST_TBL ORDER BY FGID",
     ["fgid", "name"], False),
    ("sid.csv", "SELECT SID, DSCRPTN FROM SID_LIST_TBL ORDER BY SID",
     ["sid", "name"], False),
    ("mid.csv",
     "SELECT m.MID, m.DEF, m.DSCRPTN, m.TODAY_FID, m.PREV_DAY_FID, m.CI_TYPE_FID, m.CI_TYPE_FID2,"
     " (SELECT COUNT(*) FROM MID_FID_TBL x WHERE x.MID = m.MID) FROM MID_LIST_TBL m ORDER BY m.MID",
     ["mid", "def", "name", "today_fid", "prev_day_fid", "ci_type_fid", "ci_type_fid2", "fid_count"], False),
    ("fid.csv",
     "SELECT f.FID, f.FGID, g.DSCRPTN, f.KEY_TYPE, f.DSCRPTN, f.TICK, f.INTRA, f.HISTORY,"
     " (SELECT COUNT(*) FROM MID_FID_TBL x WHERE x.FID = f.FID)"
     " FROM FID_LIST_TBL f LEFT JOIN FGID_LIST_TBL g ON g.FGID = f.FGID ORDER BY f.FID",
     ["fid", "fgid", "fgid_name", "key_type", "name", "tick", "intra", "history", "mid_count"], False),
    ("sid_mid.csv", "SELECT SID, MID, DATE_FID, TIME_FID FROM SID_MID_TBL ORDER BY SID, MID",
     ["sid", "mid", "date_fid", "time_fid"], False),
    ("sid_ref.csv", "SELECT DATA_KIND, SID, HID, DSCRPTN FROM SID_REF_TBL ORDER BY DATA_KIND, SID, HID",
     ["data_kind", "sid", "hid", "name"], False),
    ("hfid_oper.csv",
     "SELECT FID, INQRY_TYPE, SRC_FID, RFID1, RFID2, RFID3, RFID4, HFILL_TYPE FROM HFID_OPER_LIST_TBL"
     " ORDER BY FID, INQRY_TYPE, SRC_FID",
     ["fid", "inqry_type", "src_fid", "rfid1", "rfid2", "rfid3", "rfid4", "hfill_type"], False),
    ("intrfid.csv",
     "SELECT FID, KIND, SUM_TYPE, FILL_TYPE, FILL_FID, REL_FID1, REL_FID2, RATIO, ROUND_TYPE FROM INTRFID_LIST_TBL"
     " ORDER BY FID, KIND",
     ["fid", "kind", "sum_type", "fill_type", "fill_fid", "rel_fid1", "rel_fid2", "ratio", "round_type"], False),
    ("mid_fid.csv.gz",
     "SELECT MID, FID, DATA_TYPE, LEN, CNT, DEC_POS, XLP_DATA_TYPE FROM MID_FID_TBL ORDER BY MID, FID",
     ["mid", "fid", "data_type", "len", "cnt", "dec_pos", "xlp_data_type"], True),
    ("sid_mid_fid.csv.gz",
     "SELECT SID, MID, FID FROM SID_MID_FID_TBL ORDER BY SID, MID, FID",
     ["sid", "mid", "fid"], True),
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def render_csv(rows, header) -> bytes:
    buf = io.StringIO(newline="")
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(header)
    n = 0
    for r in rows:
        w.writerow(["" if v is None else v for v in r])
        n += 1
    return buf.getvalue().encode("utf-8"), n


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--src", type=Path, default=DEFAULT_SRC)
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    ap.add_argument("--check", action="store_true", help="파일을 쓰지 않고 건수만 점검")
    args = ap.parse_args()

    if not args.src.exists():
        print(f"원천 DB 없음: {args.src}", file=sys.stderr)
        return 2

    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "xlp_meta.sqlite"
        shutil.copyfile(args.src, copy)
        src_hash = sha256(copy)
        con = sqlite3.connect(f"file:{copy}?mode=ro", uri=True)
        counts: dict[str, int] = {}
        outputs: dict[str, bytes] = {}
        for name, sql, header, gz in TABLES:
            data, n = render_csv(con.execute(sql), header)
            counts[name] = n
            outputs[name] = gzip.compress(data, mtime=0) if gz else data
        # 관찰로 확인한 DATA_TYPE 표기
        data, n = render_csv(sorted(OBSERVED_CH_TYPE.items()), ["data_type", "ch_type_observed"])
        counts["data_type_observed.csv"] = n
        outputs["data_type_observed.csv"] = data
        # 무결성 점검: MID_FID 의 FID·MID 가 마스터에 모두 있어야 한다
        orphan_fid = con.execute(
            "SELECT COUNT(DISTINCT FID) FROM MID_FID_TBL WHERE FID NOT IN (SELECT FID FROM FID_LIST_TBL)").fetchone()[0]
        # 이름 없는 MID: 매핑에는 쓰이지만 MID_LIST 에 없다(폐지·내부용 추정). 오류가 아니라 경고로 둔다.
        orphan_mids = [r[0] for r in con.execute(
            "SELECT DISTINCT MID FROM MID_FID_TBL WHERE MID NOT IN (SELECT MID FROM MID_LIST_TBL) ORDER BY MID")]
        orphan_mid = len(orphan_mids)
        con.close()

    manifest = {
        "source": "CheckXL/system/xlp_meta.sqlite",
        "source_sha256": src_hash,
        "app_version": "CheckExpert 4.0.0.000",
        "grade": "local_install_meta",
        "contains_market_values": False,
        "row_counts": counts,
        "integrity": {
            "mid_fid_orphan_fid": orphan_fid,
            "unnamed_mid_count": orphan_mid,
            "unnamed_mids": orphan_mids,
        },
    }
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    if args.check:
        return 0 if orphan_fid == 0 else 1

    args.out.mkdir(parents=True, exist_ok=True)
    for name, data in outputs.items():
        (args.out / name).write_bytes(data)
    (args.out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0 if orphan_fid == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())

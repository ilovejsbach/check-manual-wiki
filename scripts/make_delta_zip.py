"""KCM 위키 내부망 반입용 델타 zip 생성 (표준 라이브러리만 사용).

Quartz 가 빌드한 정적 결과물(public)과 이전 빌드의 매니페스트(파일별 sha256)를 비교해
바뀌었거나 새로 생긴 파일만 zip 으로 묶는다. 내부망 PC 에는 압축 해제와 git 뿐이므로
zip 안 경로는 저장소 루트 기준(=public 기준)이며, 풀어서 덮어쓰기만 하면 사이트가 완성된다.

사용법:
  python3 scripts/make_delta_zip.py --source-commit <데이터 커밋 해시> <public> [옵션]
    --prev-manifest FILE   이전 빌드의 매니페스트. 생략하면 --out-dir 의 manifest_latest.json
                           을 쓰고, 그것도 없으면 첫 실행(전체 zip)으로 본다.
    --out-dir DIR          zip 과 매니페스트를 쓸 폴더 (기본: public 의 상위 폴더 아래 delta-out)
    --external {fail,warn,off}  외부 도메인 로드(src/href/url()/@import) 검사 (기본 fail)
    --allow-host HOST      외부 검사에서 허용할 호스트(반복 가능)
    --stamp YYYYMMDDTHHMMSSZ   생성 시각 고정(테스트용; 기본 현재 UTC)
  --source-commit 은 소스 데이터(위키 마크다운 저장소) 커밋 해시. 기록용이다.

출력 (OUT_DIR):
  kcm_wiki_delta_<UTC 시각>.zip   파일명 = 이름순이 곧 생성순 (인터넷 PC 가 그대로 전송)
  manifest_<UTC 시각>.json        zip 안 _delivery/manifest.json 과 같은 내용 (다음 실행의 입력)
  manifest_latest.json            위의 사본 (다음 실행 기본 입력)

zip 구성:
  - 바뀐/새 파일 (public 기준 상대 경로 그대로)
  - 항상 담는 목차·파생 파일: index.html, 404.html, sitemap.xml, index.xml,
    static/contentIndex.json, static/encryptedContentIndex.json (바뀌지 않았어도 담는다.
    사이트 전체에서 파생돼 늦게 만든 zip 것이 항상 옳다)
  - 공통 자산(static/*.css, *.js 등)은 해시가 이름에 붙어 있어 바뀐 것만 담는다
  - _delivery/manifest.json : published_at(UTC), source_commit, 모든 파일의 sha256
  - _delivery/deleted.txt   : 이전 빌드에는 있었으나 이번에는 없는 파일(한 줄에 하나).
    압축 해제로는 지워지지 않으니 사람이 git rm 으로 정리한다.
  - _delivery/README_INTRANET.md : 반입 절차 짧은 안내

순서 무관 원칙(ANA): 여러 zip 을 어떤 순서로 풀어도 마지막에 published_at 이 가장 늦은
(=이름이 가장 뒤인) zip 을 한 번 더 풀면 결과가 같다. 목차·파생 파일과 _delivery/ 가 모든 zip 에
들어 있기 때문이다. 나머지 파일은 내용 해시로 식별되는 같은 사이트 상태의 것이다.

게시 금지 문자열 검사: 담을 파일(전체 public)에 '/Users/', 'lib-ops', 'vault-finance' 가 있으면
zip 을 만들지 않고 종료 코드 2 로 실패한다.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ALWAYS_INCLUDE = (
    "index.html",
    "404.html",
    "sitemap.xml",
    "index.xml",
    "static/contentIndex.json",
    "static/encryptedContentIndex.json",
)
FORBIDDEN = ("/Users/", "lib-ops", "vault-finance")
DELIVERY_DIR = "_delivery"
ZIP_PREFIX = "kcm_wiki_delta_"
STAMP_RE = re.compile(r"^\d{8}T\d{6}Z$")
SKIP_NAMES = {".DS_Store"}

# 외부 로드 후보: HTML 의 src= / <link href=> , CSS 의 url() / @import
_ATTR_RE = re.compile(r"""<(script|img|iframe|source|video|audio|embed|link)\b[^>]*?\b(?:src|href)\s*=\s*["']((?:https?:)?//[^"']+)["'][^>]*>""", re.I)
_CSS_RE = re.compile(r"""(?:url\(\s*["']?|@import\s+["'])((?:https?:)?//[^"')\s]+)""", re.I)
_NONLOAD_REL = re.compile(r"""rel\s*=\s*["'](?:canonical|alternate|me|author|license|next|prev|search)""", re.I)

INTRANET_README = """# 내부망 반입 (KCM 위키)

1. git 작업 폴더에서 git pull
2. 받은 zip 을 전부 그 폴더에 풀기 (순서 무관)
3. 이름이 가장 뒤인 zip(가장 늦게 만든 것)을 한 번 더 풀기
4. _delivery/deleted.txt 에 적힌 파일이 있으면 git rm
5. git add -A, commit, push
"""


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def scan_site(public: Path) -> dict[str, str]:
    """public 의 모든 파일 -> sha256 (키는 '/' 구분 상대 경로)."""
    out: dict[str, str] = {}
    for p in sorted(public.rglob("*")):
        if p.is_file() and p.name not in SKIP_NAMES:
            rel = p.relative_to(public).as_posix()
            if rel.split("/", 1)[0] == DELIVERY_DIR:
                continue
            out[rel] = sha256_file(p)
    return out


def load_manifest(path: Path | None) -> dict[str, str] | None:
    if path is None or not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    files = data.get("files")
    if not isinstance(files, dict):
        raise ValueError(f"매니페스트에 files 가 없습니다: {path}")
    return files


def plan(current: dict[str, str], prev: dict[str, str] | None):
    """(zip 에 담을 경로 목록, 삭제된 경로 목록)."""
    if prev is None:
        return sorted(current), []
    include = {n for n, h in current.items() if prev.get(n) != h}
    include.update(n for n in ALWAYS_INCLUDE if n in current)
    deleted = sorted(n for n in prev if n not in current)
    return sorted(include), deleted


def find_forbidden(public: Path, names) -> list[tuple[str, str]]:
    hits = []
    needles = [(s, s.encode()) for s in FORBIDDEN]
    for n in names:
        data = (public / n).read_bytes()
        for s, b in needles:
            if b in data:
                hits.append((n, s))
    return hits


def find_external(public: Path, names, allow_hosts=()) -> list[tuple[str, str]]:
    hits = []
    allow = {h.lower() for h in allow_hosts}

    def bad(url: str) -> bool:
        host = re.sub(r"^(?:https?:)?//", "", url).split("/", 1)[0].split(":")[0].lower()
        return host not in allow

    for n in names:
        suffix = n.rsplit(".", 1)[-1].lower() if "." in n else ""
        if suffix not in ("html", "htm", "css", "svg"):
            continue
        text = (public / n).read_text(encoding="utf-8", errors="ignore")
        if suffix in ("html", "htm", "svg"):
            for m in _ATTR_RE.finditer(text):
                if m.group(1).lower() == "link" and _NONLOAD_REL.search(m.group(0)):
                    continue
                if bad(m.group(2)):
                    hits.append((n, m.group(2)))
        if suffix in ("css", "html", "htm"):
            for m in _CSS_RE.finditer(text):
                if bad(m.group(1)):
                    hits.append((n, m.group(1)))
    return hits


def build(public: Path, out_dir: Path, source_commit: str, prev_manifest: Path | None = None,
          external: str = "fail", allow_hosts=(), stamp: str | None = None) -> dict:
    """델타 zip 을 만들고 결과 요약 dict 를 돌려준다. 금지 문자열·외부 로드(fail)면 SystemExit."""
    public = public.resolve()
    if not (public / "index.html").is_file():
        raise SystemExit(f"public 에 index.html 이 없습니다: {public}")
    if not re.fullmatch(r"[0-9a-fA-F]{7,64}", source_commit or ""):
        raise SystemExit("--source-commit 은 16진수 커밋 해시여야 합니다")
    stamp = stamp or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if not STAMP_RE.match(stamp):
        raise SystemExit("stamp 형식은 YYYYMMDDTHHMMSSZ")
    out_dir.mkdir(parents=True, exist_ok=True)

    current = scan_site(public)
    prev = load_manifest(prev_manifest)
    include, deleted = plan(current, prev)

    # 금지 문자열은 담을 파일이 아니라 사이트 전체를 본다 (안 바뀐 파일도 같은 사이트의 일부).
    hits = find_forbidden(public, sorted(current))
    if hits:
        for n, s in hits[:50]:
            print(f"[금지 문자열] {n}: {s}", file=sys.stderr)
        raise SystemExit(2)
    if external != "off":
        ext = find_external(public, include, allow_hosts)
        for n, u in ext[:50]:
            print(f"[외부 로드] {n}: {u}", file=sys.stderr)
        if ext and external == "fail":
            raise SystemExit(3)

    manifest = {
        "published_at": stamp,
        "source_commit": source_commit,
        "base": "full" if prev is None else "delta",
        "file_count": len(current),
        "files": current,
    }
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    out_zip = out_dir / f"{ZIP_PREFIX}{stamp}.zip"
    fixed = (1980, 1, 1, 0, 0, 0)  # 같은 입력 -> 같은 zip

    def put(zf, arc, data):
        zi = zipfile.ZipInfo(arc, fixed)
        zi.compress_type = zipfile.ZIP_DEFLATED
        zi.external_attr = 0o644 << 16
        zf.writestr(zi, data)

    with zipfile.ZipFile(out_zip, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for n in include:
            put(zf, n, (public / n).read_bytes())
        put(zf, f"{DELIVERY_DIR}/manifest.json", manifest_text)
        put(zf, f"{DELIVERY_DIR}/deleted.txt", "".join(d + "\n" for d in deleted))
        put(zf, f"{DELIVERY_DIR}/README_INTRANET.md", INTRANET_README)
    (out_dir / f"manifest_{stamp}.json").write_text(manifest_text, encoding="utf-8")
    (out_dir / "manifest_latest.json").write_text(manifest_text, encoding="utf-8")
    return {"zip": out_zip, "stamp": stamp, "included": include, "deleted": deleted,
            "total": len(current), "full": prev is None}


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="KCM 위키 델타 zip 생성 (자세한 설명은 파일 상단 docstring)")
    ap.add_argument("public", type=Path, help="Quartz 빌드 결과 폴더")
    ap.add_argument("--source-commit", required=True, help="소스 데이터 커밋 해시")
    ap.add_argument("--prev-manifest", type=Path, default=None)
    ap.add_argument("--out-dir", type=Path, default=None)
    ap.add_argument("--external", choices=("fail", "warn", "off"), default="fail")
    ap.add_argument("--allow-host", action="append", default=[])
    ap.add_argument("--stamp", default=None)
    a = ap.parse_args(argv)
    out_dir = a.out_dir or (a.public.resolve().parent / "delta-out")
    prev = a.prev_manifest or (out_dir / "manifest_latest.json")
    r = build(a.public, out_dir, a.source_commit, prev, a.external, a.allow_host, a.stamp)
    z = r["zip"]
    kind = "전체" if r["full"] else "델타"
    print(f"{kind} zip: {z} ({z.stat().st_size / 1e6:.1f}MB)")
    print(f"담은 파일 {len(r['included'])} / 사이트 전체 {r['total']}, 삭제 {len(r['deleted'])}, published_at {r['stamp']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

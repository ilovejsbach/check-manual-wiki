#!/usr/bin/env bash
# 그래프 플러그인이 런타임에 CDN(jsdelivr)에서 받는 d3·pixi 를 로컬 서빙으로 바꾼다.
# 사용: scripts/postbuild-vendor.sh <빌드 출력 폴더>   (플러그인 소스는 건드리지 않고 결과물만 고친다)
set -euo pipefail
OUT="${1:?빌드 출력 폴더를 지정하라}"
HERE="$(cd "$(dirname "$0")" && pwd)"
mkdir -p "$OUT/static/vendor"
cp "$HERE/vendor/d3.min.js" "$HERE/vendor/pixi.min.js" "$OUT/static/vendor/"
python3 -I - "$OUT" <<'PY'
import sys, pathlib
out = pathlib.Path(sys.argv[1]) / 'static'
# 그래프 스크립트는 postscript 가 import() 로 불러오는 ES 모듈이라 import.meta.url 이 static/scripts/ 안의 자기 위치다.
base = 'new URL("../vendor/%s",import.meta.url).href'
subs = {
  '"https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js"': base % 'd3.min.js',
  '"https://cdn.jsdelivr.net/npm/pixi.js@8/dist/pixi.js"': base % 'pixi.min.js',
}
n = 0
for p in out.rglob('*.js'):
    t = p.read_text(encoding='utf-8')
    if 'cdn.jsdelivr.net' not in t:
        continue
    for a, b in subs.items():
        if a in t:
            t = t.replace(a, b); n += 1
    p.write_text(t, encoding='utf-8')
print('치환', n, '건')
if n != 2:
    sys.exit('그래프 스크립트의 CDN URL 패턴이 바뀌었다: 치환 2건 기대, ' + str(n))
PY

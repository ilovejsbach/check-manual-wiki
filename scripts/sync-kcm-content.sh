#!/usr/bin/env bash
# kcm 위키 데이터(읽기 전용)를 content/ 로 동기화한다. content/ 는 생성물이라 손으로 고치지 않는다.
set -euo pipefail

SRC="${KCM_SRC:-/Users/koscom/workspace/vault-finance/wiki-korean-capital-markets}"
DEST="$(cd "$(dirname "$0")/.." && pwd)/content"

mkdir -p "$DEST"
# 게시 대상만 허용 목록으로 복사한다. 제외: wiki/_meta, wiki/CLAUDE.md, work, books, supplements 작업용 문서·jsonl·json
rsync -a --delete --prune-empty-dirs \
  --include='/wiki/' \
  --include='/wiki/index.md' \
  --include='/wiki/chapters/***' \
  --include='/wiki/concepts/***' \
  --include='/wiki/institutions/***' \
  --include='/wiki/regulations/***' \
  --include='/wiki/metrics/***' \
  --include='/wiki/books/' \
  --include='/wiki/books/kcm.md' \
  --include='/supplements/' \
  --include='/supplements/timeline.md' \
  --include='/supplements/by-chapter.md' \
  --include='/supplements/by-page.md' \
  --include='/supplements/README.md' \
  --include='/supplements/part2/' \
  --include='/supplements/part2/themes.md' \
  --include='/supplements/part2/README.md' \
  --include='/supplements/part2/unassigned.md' \
  --exclude='*' \
  "$SRC/" "$DEST/"
# wiki/ 를 사이트 루트로 올린다 (wiki/index.md -> content/index.md)
if [ -d "$DEST/wiki" ]; then
  rsync -a "$DEST/wiki/" "$DEST/" && rm -rf "$DEST/wiki"
fi
find "$DEST" -name '*.md' | wc -l

# ---- 화면용 후처리 (데이터 원본은 건드리지 않고 content/ 사본만 변환한다) ----
# 1) [src: kcm pN] / [src: kcm pN-M] -> 작은 각주 "원본 p.N" (시행 예정 등 다른 문구는 건드리지 않음)
# 2) 모든 페이지 본문 맨 앞에 "초안(사람 검토 전)" 콜아웃, 홈에는 저작권·출처 고지 추가
python3 -I - "$DEST" <<'PY'
import re, sys, pathlib
dest = pathlib.Path(sys.argv[1])
SRC = re.compile(r'\[src:\s*kcm\s+p(\d+(?:\s*[-–]\s*\d+)?)\s*\]')
DRAFT = ("> [!warning] 초안 (사람 검토 전)\n"
         "> 이 문서는 사람의 검토를 거치지 않은 초안입니다. 내용이 틀렸거나 최신이 아닐 수 있습니다.\n\n")
HOME = ("\n\n---\n\n"
        "**출처와 저작권 고지**\n\n"
        "이 위키는 엄경식, 『한국 자본시장의 이해』, 한울엠플러스, 2023을 바탕으로 한 독자 이해를 위한 요약·정리이며 원문 전재가 아닙니다. "
        "원문의 저작권은 저자와 출판사에 있습니다. 본문의 \"원본 p.N\"은 원본 PDF의 쪽 번호입니다. "
        "현재 모든 문서는 초안(사람 검토 전)입니다.\n")
FM = re.compile(r'\A(---\n.*?\n---\n)', re.S)
for p in dest.rglob('*.md'):
    t = p.read_text(encoding='utf-8')
    t = t.replace('`[src: kcm pN]`', '"원본 p.N"')  # timeline 안내문의 토큰 설명(코드 표기)
    t = SRC.sub(lambda m: '<sup class="src-ref">원본 p.' + re.sub(r'\s*[-–]\s*', '-', m.group(1)) + '</sup>', t)
    m = FM.match(t)
    head, body = (m.group(1), t[m.end():]) if m else ('', t)
    body = body.lstrip('\n')
    if p.relative_to(dest).as_posix() == 'index.md':
        body = body.rstrip('\n') + HOME
    if head and not re.search(r'^description:', head, re.M):
        # 초안 콜아웃이 description·검색 미리보기를 차지하지 않도록 첫 일반 문단으로 description 을 만든다
        for line in body.splitlines():
            s = line.strip()
            if s.startswith('- '):
                s = s[2:].strip()
            if not s or s[0] in '#>-|<*`' or s.startswith('(') or s.startswith('[['):
                continue
            s = re.sub(r'<sup class="src-ref">.*?</sup>', '', s)
            s = re.sub(r'\[\[(?:[^\]|]*\|)?([^\]]*)\]\]', r'\1', s).replace('"', "'").strip()
            if len(s) > 120:
                s = s[:119].rstrip() + '…'
            if s:
                head = head[:-4] + 'description: "' + s + '"\n---\n'
                break
    p.write_text(head + '\n' + DRAFT + body, encoding='utf-8')
PY
echo "남은 [src: 개수: $(grep -rc '\[src:' "$DEST" | awk -F: '{s+=$NF} END{print s+0}')"

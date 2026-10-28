# 인터넷망 PC → 맥: 망간전송이 zip 을 거부함 - favicon.ico 가 실제로는 PNG (2026-10-28, 수정 요청)

## 증상
법령 전체본 `kcm_law_delta_20261028T054340Z.zip` 을 망간자료전송으로 보내자 전송 검사가 거부했다.
> 파일(kcm_law_delta_20261028T054340Z.zip) 내 허용되지 않은 파일이 포함되어 있습니다. **[위변조된 확장자] favicon.ico(image/png)**

## 원인 (zip 을 열어 확인)
zip 루트의 `favicon.ico` 는 확장자만 `.ico` 이고 **내용은 PNG**(앞 바이트 `89 50 4E 47`)다. Quartz 가 PNG 데이터를 그대로 `favicon.ico` 로 내보낸다.
확장자와 실제 형식이 다른 파일은 이것 하나뿐이다. 세 zip 모두 같다:
- `kcm_law_delta_20261028T054340Z.zip` (법령)
- `kcm_wiki_delta_20261028T042859Z.zip`, `kcm_wiki_delta_20261027T031707Z.zip` (kcm) — **kcm 도 같은 이유로 막힌다.**

## 요청 (맥 빌드 후처리에서, 둘 중 하나)
1. **`favicon.ico` 를 진짜 ICO 로 만든다** — 같은 PNG 를 ICO 컨테이너(앞 바이트 `00 00 01 00`)로 감싼다(PNG 내장 ICO 가능). 사이트 동작은 그대로다.
2. 또는 **`favicon.ico` 를 zip(사이트)에서 뺀다.** 페이지의 `<link rel="icon">` 이 `static/icon.png` 를 가리키는지 확인해 달라(브라우저가 `/favicon.ico` 를 직접 요청해 404 가 나는 것 정도는 무해).
`postbuild-vendor.sh` 옆 후처리(`postbuild-*`)에 넣고, **`make_delta_zip.py` 에 검사를 하나 더**: 항목 확장자(png/jpg/gif/pdf/ico/webp)와 앞 바이트가 어긋나면 zip 을 만들지 않게 해 달라. 이쪽 받기 모듈(`Test-KcmDeltaZip`)은 이미 같은 검사를 넣어 어긋난 zip 을 받는 즉시 거부한다(종료 코드 17).

## 주의
- 수정 후에는 두 사이트를 **새 날짜 릴리스로 다시** 올려야 한다(기존 릴리스의 자산 교체·삭제는 하지 않는다는 규칙 유지). 법령·kcm 모두 새 `published_at`.
- 이쪽이 방금 받은 위 3개 zip 은 격리했고, 법령 발송은 취소 처리(발송 이력 되돌림)했다. 업무망에는 아무것도 도착하지 않았다.
- 같은 검사에서 걸릴 수 있는 다른 항목: 법령 zip 에 `.hwp` 8개, `.pdf` 221개가 있다. 이번 거부 사유에는 없었지만, hwp 가 다음 거부 사유가 되면 알려 주겠다.
- 앞서 보낸 질문(`from-intranet-pc-2026-10-28-law-edition.md`)의 답도 기다린다.

# 게시 테스트 피드백: kcm 위키 로컬 시험 빌드 (2026-10-20)

환경: Node v22.23.3(임시, 스크래치 폴더 압축 해제, 전역 설정 불변), Quartz 5.0.0, 브랜치 `kcm-publish-test`. push·레포 생성·배포 없음.
동기화: `scripts/sync-kcm-content.sh`(rsync 허용 목록) → `content/` 381개 md (위키 374 + 보완 7). 설정: `quartz.config.yaml`.

| # | 항목 | 결과 | 근거 | 몫 |
|---|---|---|---|---|
| 1 | 빌드 | 성공, 약 30~45초(파싱 28초). 오류 없음. 경고: 미추적 파일 날짜(git 날짜 부정확, 무해) | build log | 설정 |
| 1a | 수학 오탈 | latex 플러그인 켜면 `$`가 든 6개 파일에서 한글이 수식으로 파싱되는 경고 189건. 수식이 없어 latex 플러그인 **끔** | 첫 빌드 로그 | 설정(해결) |
| 2 | 페이지 수 | md 381개 모두 html 생성(누락 0). 전체 html 1047 = 문서 381 + 별칭 리다이렉트 + 폴더 목차 페이지 | check.py | 정상 |
| 3 | 깨진 위키링크 | 위키링크 2511건 중 **1건**: `supplements/timeline.md`의 `[[held]]` (held.md는 게시 제외라 대상 없음). 표 안 `[[slug\|표시]]`는 정상 렌더 | check.py | 데이터: timeline의 `[[held]]`를 평문으로 바꾸거나 링크 제거 |
| 4 | 별칭·충돌 | 별칭 412개, 서로 다른 문서에 걸친 중복 별칭 0, 문서 slug 중복은 README 2개(`supplements/README`, `supplements/part2/README`)뿐이며 폴더가 달라 URL 충돌 없음. 별칭은 리다이렉트 페이지로 동작 | check.py | 정상 (README는 `supplements-readme` 식 개명 권장, 선택) |
| 5 | `[src: kcm pN]` | 글자 그대로 노출(4630건). 본문 끝에 대괄호 텍스트로 보임 | concepts/a-blox.html | 결정 필요: "원본 p.N" 각주형으로 바꾸기를 권장. 데이터는 그대로 두고 동기화 단계 또는 Quartz 변환 쪽에서 처리할 예정(설정 몫) |
| 6 | frontmatter | `status: draft`는 Quartz `draft`와 무관해 페이지가 빠지지 않음(draft:true 0건). 화면에는 `aliases`만 "Properties" 상자로 노출. `status`/`type`은 노출 안 됨. 따라서 "초안" 표시는 별도로 넣어야 함 | HTML | 설정(초안 배너 추가 예정) |
| 7 | 한국어 검색·그래프·목차 | **브라우저 확장이 연결되지 않아 동작 미확인**(검색 한국어 토큰화는 실제 확인 필요). 목차(TOC)는 우측에 생성됨. 그래프는 아래 8번 이유로 끔 | — | 설정, 재확인 필요 |
| 8 | 외부 리소스 | 기본 설정은 구글 폰트 CSS/preconnect, cdnjs preconnect, 그래프 런타임의 `cdn.jsdelivr.net`(d3, pixi) 요청이 있음. 조치: 폰트 플러그인·og-image·그래프 끔, 폰트는 시스템 폰트, Head.tsx의 cdnjs preconnect 한 줄 삭제(코어 패치). 결과: 페이지가 요청하는 외부 스크립트·CSS·폰트 0건. 남은 것은 푸터의 Quartz 링크와 본문의 출처 URL 링크(클릭 전엔 요청 없음). mermaid(cdnjs)는 코드 블록이 없어 로드 안 됨 | 빌드 결과 grep | 설정 |
| 9 | 내부 경로 | `/Users/`, `lib-ops`, `vault-finance` 0건(html·css·js 전체) | grep | 정상 |
| 10 | 큰 페이지 | timeline.html 1.2MB(405개 절, 본문 약 925KB), by-chapter.html 1.2MB, themes 약 150KB. 검색 색인 `contentIndex.json` 2.4MB(timeline 362KB, by-chapter 354KB가 가장 큼). 브라우저 렌더 시간은 미측정. 초기 로드 2.4MB 색인이 부담이면 분할 요청 가능 | du, json | 실측 후 판단(데이터 분할 요청은 아직 하지 않음) |
| 11 | 저작권 고지 | 아직 없음(푸터는 Quartz 기본). 사이트 전체 푸터와 홈에 서지(엄경식, 한울엠플러스, 2023)·"요약·정리이며 원문 전재 아님"·초안 표시를 넣을 예정 | — | 설정 |

## 데이터 쪽 요청 (lib-ops)
1. `supplements/timeline.md`의 `[[held]]` 링크 제거(또는 게시 대상 문서로 바꿈).
2. (선택) README 2개의 파일명 구분.
그 외 데이터 결함은 발견하지 못했다. 시행 예정 표기는 변환하지 않고 그대로 둔다.

## 다음 (작가 확인 필요)
- 초안 배너·저작권 푸터·"원본 p.N" 변환 구현, 브라우저 검색 확인.
- 게시 레포 이름·Pages 주소 정하기, 레포 생성과 origin 변경(작가 확인 후).
- 델타 zip 스크립트(빌드 결과물 기준, 목차 포함).

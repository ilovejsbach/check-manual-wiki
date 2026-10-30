# 개발 환경

## Python 규칙

- Python 도구는 시스템 Python이나 전역 `pip`를 사용하지 않는다.
- 프로젝트 루트의 `pyproject.toml`과 `uv.lock`을 기준으로 `uv sync`를 실행한다.
- 스크립트와 테스트는 각각 `uv run python ...`, `uv run pytest`로 실행한다.
- 생성되는 `.venv`는 Git에 커밋하지 않는다.

## 원본과 생성물

- `CHECK_SRC`가 가리키는 외부 폴더(기본값 `sources/check-expert/`)에는 공식 사이트에서 받은 원본을 변경하지 않고 보존한다.
- 원본과 `content/`는 생성 데이터이므로 Git에 커밋하지 않는다.
- `content/`의 Markdown은 `scripts/build_check_wiki.py`로 다시 생성할 수 있어야 한다.
- 각 생성 문서는 원본 파일, PDF 페이지 또는 Excel 시트를 출처 메타데이터로 기록한다.

## 생성·검증·조회

```powershell
uv run python scripts/build_check_wiki.py --json
uv run python scripts/validate_check_wiki.py --json
uv run python scripts/query_check_wiki.py "1300" --json
uv run pytest
```

Quartz 빌드 후 `public/check-expert/api/knowledge.jsonl`과 `manifest.json`은 프로그램에서
HTTP로 직접 받을 수 있다. 사람용 위키와 기계용 데이터는 같은 생성 과정과 ID를 공유한다.

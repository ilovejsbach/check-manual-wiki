import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from build_check_wiki import frontmatter, screen_code, slug


def test_slug_normalizes_for_paths() -> None:
    assert slug(" 1300 - 주식현재가 ") == "1300-주식현재가"


def test_screen_code_accepts_only_four_digit_token() -> None:
    assert screen_code("1300 - 주식현재가") == "1300"
    assert screen_code("12345 데이터") is None


def test_frontmatter_supports_alias_lists() -> None:
    rendered = frontmatter(
        title="화면",
        description="설명",
        tags=["CHECK"],
        source="manual.pdf",
        extra={"aliases": ["1300", "TR1300"]},
    )
    assert '  - "1300"' in rendered
    assert '  - "TR1300"' in rendered

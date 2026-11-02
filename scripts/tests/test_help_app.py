import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import build_help_app


class HelpAppBuildTest(unittest.TestCase):
    def test_build_exports_searchable_records_and_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "knowledge.jsonl"
            output = root / "dist"
            source.write_text(
                json.dumps(
                    {
                        "id": "check:screen:1300",
                        "type": "screen",
                        "title": "주식현재가",
                        "aliases": ["TR1300"],
                        "screen_code": "1300",
                        "source": "manual.pdf",
                        "source_locator": "10",
                        "related_ids": [],
                        "text": "현재가 조회",
                    },
                    ensure_ascii=False,
                )
                + "\n",
                encoding="utf-8",
            )
            previous = build_help_app.APP_SOURCE
            try:
                build_help_app.APP_SOURCE = Path(__file__).resolve().parents[2] / "help-app"
                manifest = build_help_app.build(source, output)
            finally:
                build_help_app.APP_SOURCE = previous
            self.assertEqual(manifest["record_count"], 1)
            self.assertTrue((output / "index.html").exists())
            records = json.loads((output / "data" / "knowledge.json").read_text(encoding="utf-8"))
            self.assertEqual(records[0]["screen_code"], "1300")
            self.assertEqual(records[0]["title"], "주식현재가")


if __name__ == "__main__":
    unittest.main()

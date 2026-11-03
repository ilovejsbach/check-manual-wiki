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
            records = [
                {
                    "id": "check:screen:1300",
                    "type": "screen",
                    "title": "주식현재가",
                    "aliases": ["TR1300"],
                    "screen_code": "1300",
                    "source": "manual.pdf",
                    "source_locator": "10",
                    "related_ids": ["check:field:1300:per"],
                    "text": "현재가 조회",
                },
                {
                    "id": "check:field:1300:per",
                    "type": "screen_field",
                    "title": "주가수익비율(PER) — TR 1300",
                    "aliases": ["PER"],
                    "screen_code": "1300",
                    "field_label": "PER",
                    "concept": "주가수익비율(PER)",
                    "formula": "주가 / EPS",
                    "unit": "배",
                    "related_ids": ["check:screen:1300"],
                    "text": "PER 정의",
                },
            ]
            source.write_text(
                "".join(json.dumps(record, ensure_ascii=False) + "\n" for record in records),
                encoding="utf-8",
            )
            previous = build_help_app.APP_SOURCE
            try:
                build_help_app.APP_SOURCE = Path(__file__).resolve().parents[2] / "help-app"
                manifest = build_help_app.build(source, output)
            finally:
                build_help_app.APP_SOURCE = previous
            self.assertEqual(manifest["record_count"], 2)
            self.assertEqual(manifest["screen_field_count"], 1)
            self.assertTrue((output / "index.html").exists())
            records = json.loads((output / "data" / "knowledge.json").read_text(encoding="utf-8"))
            self.assertEqual(records[0]["screen_code"], "1300")
            self.assertEqual(records[0]["title"], "주식현재가")
            self.assertEqual(records[1]["formula"], "주가 / EPS")


if __name__ == "__main__":
    unittest.main()

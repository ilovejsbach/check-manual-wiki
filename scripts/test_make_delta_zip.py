import sys, tempfile, unittest, zipfile, json
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import make_delta_zip as m

C = "abc1234"


def mk(root: Path, files: dict):
    for k, v in files.items():
        p = root / k
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(v, encoding="utf-8")


BASE = {"index.html": "<html>i</html>", "404.html": "x", "a.html": "A", "b.html": "B",
        "static/contentIndex.json": "{}", "static/s-1.css": "c"}


class T(unittest.TestCase):
    def setUp(self):
        self.d = Path(tempfile.mkdtemp())
        self.pub = self.d / "pub"
        mk(self.pub, BASE)
        self.out = self.d / "out"

    def names(self, r):
        return set(zipfile.ZipFile(r["zip"]).namelist())

    def test_full_then_delta(self):
        r1 = m.build(self.pub, self.out, C, None, stamp="20260101T000000Z")
        self.assertTrue(r1["full"])
        self.assertTrue(set(BASE) <= self.names(r1))
        mk(self.pub, {"a.html": "A2", "new.html": "N"})
        (self.pub / "b.html").unlink()
        r2 = m.build(self.pub, self.out, C, self.out / "manifest_latest.json", stamp="20260102T000000Z")
        n = self.names(r2)
        self.assertIn("a.html", n); self.assertIn("new.html", n)
        self.assertNotIn("static/s-1.css", n)
        self.assertIn("index.html", n); self.assertIn("static/contentIndex.json", n)
        self.assertEqual(r2["deleted"], ["b.html"])
        z = zipfile.ZipFile(r2["zip"])
        self.assertEqual(z.read("_delivery/deleted.txt").decode(), "b.html\n")
        mf = json.loads(z.read("_delivery/manifest.json"))
        self.assertEqual(mf["published_at"], "20260102T000000Z")
        self.assertEqual(mf["source_commit"], C)
        self.assertEqual(set(mf["files"]), set(m.scan_site(self.pub)))

    def test_forbidden(self):
        mk(self.pub, {"a.html": "path /Users/x"})
        with self.assertRaises(SystemExit) as e:
            m.build(self.pub, self.out, C, None)
        self.assertEqual(e.exception.code, 2)
        self.assertFalse(list(self.out.glob("*.zip")))
        for bad in ("lib-ops", "vault-finance"):
            mk(self.pub, {"a.html": bad})
            with self.assertRaises(SystemExit):
                m.build(self.pub, self.out, C, None)

    def test_external(self):
        mk(self.pub, {"a.html": '<link href="https://fonts.googleapis.com/css" rel="stylesheet">'})
        with self.assertRaises(SystemExit) as e:
            m.build(self.pub, self.out, C, None)
        self.assertEqual(e.exception.code, 3)
        r = m.build(self.pub, self.out, C, None, external="warn", stamp="20260101T000000Z")
        self.assertTrue(r["zip"].exists())
        # 일반 앵커와 canonical 은 외부 로드가 아니다
        mk(self.pub, {"a.html": '<a href="https://x.org">x</a><link rel="canonical" href="https://x.org/a">'})
        self.assertEqual(m.find_external(self.pub, ["a.html"]), [])
        mk(self.pub, {"s.css": "@import url(//cdnjs.cloudflare.com/x.css);"})
        self.assertEqual(len(m.find_external(self.pub, ["s.css"])), 1)

    def test_order_independent(self):
        r1 = m.build(self.pub, self.out, C, None, stamp="20260101T000000Z")
        mk(self.pub, {"a.html": "A2", "index.html": "<html>i2</html>"})
        r2 = m.build(self.pub, self.out, C, self.out / "manifest_latest.json", stamp="20260102T000000Z")
        outs = []
        for order in ([r1, r2, r2], [r2, r1, r2]):
            t = Path(tempfile.mkdtemp())
            for r in order:
                zipfile.ZipFile(r["zip"]).extractall(t)
            outs.append({p.relative_to(t).as_posix(): p.read_bytes() for p in t.rglob("*") if p.is_file()})
        self.assertEqual(outs[0], outs[1])


if __name__ == "__main__":
    unittest.main()

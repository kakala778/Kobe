from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from scripts.verify_site import verify_site


class VerifySiteTests(unittest.TestCase):
    def make_site(self, root: Path, html: str) -> None:
        (root / "index.html").write_text(html, encoding="utf-8")
        (root / "styles.css").write_text("body {}", encoding="utf-8")
        (root / "script.js").write_text("console.log('ok');", encoding="utf-8")

    def test_valid_site_has_no_errors(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_site(
                root,
                '<link rel="stylesheet" href="styles.css">'
                '<script src="script.js"></script>',
            )
            self.assertEqual(verify_site(root), [])

    def test_missing_required_file_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("<main></main>", encoding="utf-8")
            errors = verify_site(root)
            self.assertIn("Missing required file: styles.css", errors)
            self.assertIn("Missing required file: script.js", errors)

    def test_missing_local_reference_is_reported(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_site(root, '<img src="images/missing.png" alt="">')
            self.assertIn(
                "Missing local reference: images/missing.png",
                verify_site(root),
            )

    def test_external_and_fragment_references_are_ignored(self) -> None:
        with TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_site(
                root,
                '<a href="#about">About</a>'
                '<a href="https://example.com">External</a>'
                '<a href="mailto:hello@example.com">Email</a>',
            )
            self.assertEqual(verify_site(root), [])


if __name__ == "__main__":
    unittest.main()

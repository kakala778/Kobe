from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import unquote, urlsplit


REQUIRED_FILES = ("index.html", "styles.css", "script.js")
REFERENCE_ATTRIBUTES = {
    "a": ("href",),
    "img": ("src",),
    "link": ("href",),
    "script": ("src",),
}
IGNORED_SCHEMES = {"data", "http", "https", "mailto", "tel"}


class ReferenceParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []
        self.has_icon = False

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag == "link":
            attributes = dict(attrs)
            rel_tokens = (attributes.get("rel") or "").lower().split()
            self.has_icon = self.has_icon or "icon" in rel_tokens

        wanted = REFERENCE_ATTRIBUTES.get(tag, ())
        for name, value in attrs:
            if name in wanted and value:
                self.references.append(value)


def local_reference_path(root: Path, reference: str) -> Path | None:
    if reference.startswith(("#", "//")):
        return None

    parsed = urlsplit(reference)
    if parsed.scheme.lower() in IGNORED_SCHEMES:
        return None

    decoded_path = unquote(parsed.path)
    if not decoded_path:
        return None

    candidate = (root / decoded_path.lstrip("/")).resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError:
        return candidate
    return candidate


def verify_site(root: Path) -> list[str]:
    root = root.resolve()
    errors: list[str] = []

    for filename in REQUIRED_FILES:
        if not (root / filename).is_file():
            errors.append(f"Missing required file: {filename}")

    index_path = root / "index.html"
    if not index_path.is_file():
        return errors

    parser = ReferenceParser()
    parser.feed(index_path.read_text(encoding="utf-8"))

    if not parser.has_icon:
        errors.append("Missing favicon declaration")

    for reference in parser.references:
        candidate = local_reference_path(root, reference)
        if candidate is None:
            continue
        try:
            display_path = candidate.relative_to(root).as_posix()
        except ValueError:
            errors.append(f"Local reference escapes site root: {reference}")
            continue
        if not candidate.is_file():
            errors.append(f"Missing local reference: {display_path}")

    return errors


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    errors = verify_site(root)
    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    print("Site verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

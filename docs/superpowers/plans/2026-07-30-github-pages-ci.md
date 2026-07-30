# GitHub Pages 与最小 CI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将纯静态作品集从 `main` 根目录发布到 GitHub Pages，并增加不依赖第三方包的自动检查。

**Architecture:** 项目继续直接运行现有 HTML、CSS 和原生 JavaScript。Python 标准库脚本负责检查核心文件和本地资源引用，GitHub Actions 在 push 与 Pull Request 上运行该脚本、单元测试和 JavaScript 语法检查；GitHub Pages 直接托管 `main:/`。

**Tech Stack:** HTML、CSS、原生 JavaScript、Python 3.13 标准库、Node.js 24、GitHub Actions、GitHub Pages、Playwright CLI。

## Global Constraints

- 网站不需要构建步骤，也没有第三方运行依赖。
- 检查脚本不安装第三方 Python 或 npm 包。
- GitHub Pages 来源固定为 `main` 分支根目录 `/`。
- 不创建 `gh-pages` 分支，不添加自定义域名。
- 不使用强制推送，不改写已有提交历史。
- 暂不把 CI 设置为 `main` 的必需状态检查。

---

## File Structure

- `scripts/verify_site.py`：检查核心文件和 HTML 中的本地资源引用，提供可测试的 `verify_site(root)` 接口。
- `tests/test_verify_site.py`：使用 Python `unittest` 验证缺失文件、缺失本地引用和外部引用处理。
- `.github/workflows/ci.yml`：在 push 与 Pull Request 上执行检查。
- `README.md`：说明线上地址、发布来源和本地检查命令。

### Task 1: 站点检查脚本

**Files:**
- Create: `scripts/verify_site.py`
- Create: `tests/test_verify_site.py`

**Interfaces:**
- Consumes: 一个包含静态站点文件的 `pathlib.Path` 根目录。
- Produces: `verify_site(root: Path) -> list[str]`，无错误时返回空列表；命令行入口在失败时返回退出码 1。

- [ ] **Step 1: 写入失败测试**

创建 `tests/test_verify_site.py`：

```python
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
```

- [ ] **Step 2: 运行测试并确认因实现缺失而失败**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: FAIL，错误包含 `ModuleNotFoundError` 或无法导入 `scripts.verify_site`。

- [ ] **Step 3: 写入最小实现**

创建 `scripts/verify_site.py`：

```python
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

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
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
```

- [ ] **Step 4: 运行单元测试**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
```

Expected: 4 tests，全部 `ok`。

- [ ] **Step 5: 检查真实站点**

Run:

```powershell
python scripts/verify_site.py
node --check script.js
```

Expected: 输出 `Site verification passed.`，两个命令退出码均为 0。

### Task 2: GitHub Actions 与项目说明

**Files:**
- Create: `.github/workflows/ci.yml`
- Modify: `README.md`

**Interfaces:**
- Consumes: Task 1 的 `scripts/verify_site.py` 和 `tests/test_verify_site.py`。
- Produces: 名为 `CI` 的 GitHub Actions 工作流，以及用户可复制的本地检查命令。

- [ ] **Step 1: 创建 CI 工作流**

创建 `.github/workflows/ci.yml`：

```yaml
name: CI

on:
  push:
    branches:
      - main
  pull_request:

permissions:
  contents: read

jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v7

      - name: Set up Python
        uses: actions/setup-python@v7
        with:
          python-version: "3.13"

      - name: Set up Node.js
        uses: actions/setup-node@v7
        with:
          node-version: "24"

      - name: Run verifier tests
        run: python -m unittest discover -s tests -p "test_*.py" -v

      - name: Verify site files
        run: python scripts/verify_site.py

      - name: Check JavaScript syntax
        run: node --check script.js
```

- [ ] **Step 2: 补充 README**

在 `README.md` 的项目介绍之后新增：

````markdown
## 在线访问

GitHub Pages：<https://kakala778.github.io/Kobe/>

网站直接从 `main` 分支根目录发布，不需要构建步骤。

## 自动检查

每次推送到 `main` 或更新 Pull Request 时，GitHub Actions 会检查核心文件、本地资源引用和 JavaScript 语法。

本地运行相同检查：

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/verify_site.py
node --check script.js
```
````

- [ ] **Step 3: 运行全部本地检查**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/verify_site.py
node --check script.js
git diff --check
```

Expected: 4 tests 通过，站点检查通过，JavaScript 语法检查退出码 0，`git diff --check` 无输出。

- [ ] **Step 4: 检查改动范围**

Run:

```powershell
git status -sb
git diff -- .github/workflows/ci.yml scripts/verify_site.py tests/test_verify_site.py README.md
```

Expected: 只包含计划文档、CI、检查脚本、测试和 README 的预期改动。

### Task 3: 提交、推送与 Pages 配置

**Files:**
- Commit: `.github/workflows/ci.yml`
- Commit: `scripts/verify_site.py`
- Commit: `tests/test_verify_site.py`
- Commit: `README.md`
- Commit: `docs/superpowers/plans/2026-07-30-github-pages-ci.md`

**Interfaces:**
- Consumes: Task 1 与 Task 2 的已验证文件，以及已存在的 4 个本地提交。
- Produces: 同步的 `origin/main`、启用的 GitHub Pages 和首次 CI 运行。

- [ ] **Step 1: 确认 GitHub 登录与推送目标**

Run:

```powershell
gh auth status
git remote -v
git status -sb
```

Expected: `kakala778` 登录有效，`origin` 指向 `https://github.com/kakala778/Kobe.git`，工作区只有预期文件。

- [ ] **Step 2: 提交实施文件**

Run:

```powershell
git add -- .github/workflows/ci.yml scripts/verify_site.py tests/test_verify_site.py README.md docs/superpowers/plans/2026-07-30-github-pages-ci.md
git commit -m "添加 GitHub Pages 最小 CI"
```

Expected: 创建一个包含 CI、检查脚本、测试、README 和实施计划的提交。

- [ ] **Step 3: 再次运行提交后检查**

Run:

```powershell
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/verify_site.py
node --check script.js
git status -sb
```

Expected: 所有检查通过，`main` 领先 `origin/main`，工作区干净。

- [ ] **Step 4: 正常推送 main**

Run:

```powershell
git push origin main
```

Expected: 推送成功；不使用 `--force`。

- [ ] **Step 5: 开启 GitHub Pages**

Run:

```powershell
$payload = '{"source":{"branch":"main","path":"/"}}'
$payload | gh api --method POST repos/kakala778/Kobe/pages --input -
```

Expected: API 返回 Pages 配置，其中 `source.branch` 为 `main`、`source.path` 为 `/`。

- [ ] **Step 6: 等待 CI 完成**

Run:

```powershell
$runId = gh run list -R kakala778/Kobe --workflow CI --limit 1 --json databaseId --jq '.[0].databaseId'
gh run watch $runId -R kakala778/Kobe --exit-status
```

Expected: 退出码 0，最新 CI 结论为 `success`。

- [ ] **Step 7: 等待 Pages 发布**

Run:

```powershell
gh api repos/kakala778/Kobe/pages --jq '{status,html_url,source,https_enforced}'
```

Expected: `html_url` 为 `https://kakala778.github.io/Kobe/`，`source.branch` 为 `main`，最终 `status` 为 `built`。

### Task 4: 线上浏览器验收

**Files:**
- No repository changes.

**Interfaces:**
- Consumes: 已发布的 `https://kakala778.github.io/Kobe/`。
- Produces: HTTP、桌面浏览器、控制台和 375px 响应式验收证据。

- [ ] **Step 1: 检查 HTTP**

Run:

```powershell
$response = Invoke-WebRequest -Uri 'https://kakala778.github.io/Kobe/' -UseBasicParsing
$response.StatusCode
$response.Content -match '<title>'
```

Expected: 状态码 200，标题匹配结果为 `True`。

- [ ] **Step 2: 使用 Playwright 打开线上页面**

Run:

```powershell
& 'D:\Dev\Tools\Git\bin\bash.exe' 'C:\Users\iq\.codex\skills\playwright\scripts\playwright_cli.sh' open 'https://kakala778.github.io/Kobe/'
& 'D:\Dev\Tools\Git\bin\bash.exe' 'C:\Users\iq\.codex\skills\playwright\scripts\playwright_cli.sh' snapshot
& 'D:\Dev\Tools\Git\bin\bash.exe' 'C:\Users\iq\.codex\skills\playwright\scripts\playwright_cli.sh' console error
```

Expected: 快照包含作品集主要标题；控制台没有 JavaScript 错误。

- [ ] **Step 3: 检查 375px 布局**

Run:

```powershell
& 'D:\Dev\Tools\Git\bin\bash.exe' 'C:\Users\iq\.codex\skills\playwright\scripts\playwright_cli.sh' resize 375 812
& 'D:\Dev\Tools\Git\bin\bash.exe' 'C:\Users\iq\.codex\skills\playwright\scripts\playwright_cli.sh' eval '() => ({ viewport: document.documentElement.clientWidth, content: document.documentElement.scrollWidth })'
```

Expected: `viewport` 与 `content` 均为 375，没有横向溢出。

- [ ] **Step 4: 关闭浏览器并复核同步状态**

Run:

```powershell
& 'D:\Dev\Tools\Git\bin\bash.exe' 'C:\Users\iq\.codex\skills\playwright\scripts\playwright_cli.sh' close
git status -sb
git rev-list --left-right --count origin/main...main
```

Expected: 工作区干净，左右计数均为 0。

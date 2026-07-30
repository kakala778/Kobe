# GitHub Pages 与最小 CI 设计

## 目标

把 `kakala778/Kobe` 发布为可公开访问的 GitHub Pages 网站，并为现有纯静态作品集增加最小、稳定、容易理解的自动检查。

## 当前状态

- 网站只使用 HTML、CSS 和原生 JavaScript。
- 网站不需要构建步骤，也没有第三方运行依赖。
- 本地 `main` 比远程 `origin/main` 领先 3 个已提交的工作流文档提交。
- GitHub Pages 尚未开启。
- 仓库尚无 GitHub Actions 工作流。
- `main` 已禁止强制推送和删除，但仍允许正常推送。

## 发布方案

GitHub Pages 直接从 `main` 分支根目录 `/` 发布。

选择这一方案是因为网站无需构建。源文件与线上文件保持一致，发布路径直观，也不需要维护额外的部署分支或自定义构建工作流。

预计公开地址为：

```text
https://kakala778.github.io/Kobe/
```

## CI 方案

新增一个 GitHub Actions 工作流，在以下事件发生时运行：

- 向 `main` 推送；
- 创建或更新 Pull Request。

工作流执行以下检查：

1. 确认 `index.html`、`styles.css` 和 `script.js` 存在。
2. 使用项目内的 Python 标准库检查脚本读取 `index.html`，确认其中引用的本地 CSS 和 JavaScript 文件真实存在。
3. 使用 Node.js 的 `node --check script.js` 检查 JavaScript 语法。

检查脚本不安装第三方 Python 或 npm 包，不改变网站运行方式。

## 文件职责

- `.github/workflows/ci.yml`：定义 GitHub Actions 的触发条件和检查步骤。
- `scripts/verify_site.py`：使用 Python 标准库检查核心文件和 HTML 中的本地资源引用。
- `README.md`：补充线上地址、自动检查和发布方式说明。

## 推送与发布顺序

1. 在本地运行检查脚本和 JavaScript 语法检查。
2. 提交 CI、检查脚本和 README 说明。
3. 将 `main` 的全部本地提交正常推送到 `origin/main`。
4. 通过 GitHub API 将 Pages 来源设为 `main` 和 `/`。
5. 等待 CI 与 Pages 部署完成。

不使用强制推送，不改写已有提交历史。

## 错误处理

- 本地检查失败时不提交 CI 改动，先定位并修复根因。
- 推送失败时保留本地提交，不重置或强制推送。
- CI 失败时读取具体 Actions 日志，只修改导致失败的最小范围。
- Pages 配置失败时先读取仓库 Pages 状态和 API 错误，不反复修改无关设置。

## 验收标准

- 本地 `scripts/verify_site.py` 运行成功。
- 本地 `node --check script.js` 运行成功。
- `main` 已与 `origin/main` 同步。
- GitHub Actions 最新一次 CI 运行结论为 `success`。
- GitHub Pages 状态为已发布。
- 线上地址返回成功状态，并能显示作品集首页。
- 真实浏览器中页面主要内容可见，控制台没有 JavaScript 错误。
- 375px 宽度下页面没有横向溢出。

## 明确不做

- 不引入 React、Vue、构建工具或包管理器。
- 不创建 `gh-pages` 分支。
- 不添加自定义域名。
- 不要求 Pull Request 审核。
- 不把 CI 设为 `main` 的必需状态检查；等 CI 稳定运行后再单独决定。

# Lightweight Codex Workflow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Persist the approved lightweight Superpowers policy as a reversible user-level Codex instruction without changing the portfolio application or plugin files.

**Architecture:** Add one clearly marked policy block to the currently empty user-level `C:\Users\iq\.codex\AGENTS.md`. Project-level `AGENTS.md` files continue to provide project-specific commands and checks, while direct user instructions can override automatic task classification at any time.

**Tech Stack:** Markdown, Codex `AGENTS.md`, Windows PowerShell 5.1, SHA-256 file verification

## Global Constraints

- 工作流强度：轻量模式。
- 分级方式：Codex 自动判断，用户可以随时覆盖。
- 安全底线：系统调试与完成前验证始终保留。
- 首次试用：等待下一次真实任务，不创建练习项目。
- 当前作品集：不因为配置工作流而修改网页功能。
- GitHub：读取可以直接进行，写入前继续询问。
- Do not modify `C:\Users\iq\.codex\config.toml`.
- Do not modify any file under `C:\Users\iq\.codex\plugins\cache`.
- Do not modify the portfolio's existing `AGENTS.md`.
- Do not install dependencies, create a worktree, push, deploy, or write to GitHub.

---

## File Structure

- Modify: `C:\Users\iq\.codex\AGENTS.md` — contains the personal lightweight Superpowers policy that applies across projects.
- Preserve unchanged: `C:\Users\iq\OneDrive\Desktop\Codex_workspace\vibecoding\my-portfolio\AGENTS.md` — retains portfolio-specific constraints and browser checks.
- Preserve unchanged: `C:\Users\iq\.codex\config.toml` — no feature or permission changes are required.
- Preserve unchanged: `C:\Users\iq\.codex\plugins\cache\openai-curated-remote\superpowers\6.2.0` — installed plugin content is immutable for this task.

### Task 1: Persist and verify the lightweight policy

**Files:**

- Modify: `C:\Users\iq\.codex\AGENTS.md`
- Preserve: `C:\Users\iq\OneDrive\Desktop\Codex_workspace\vibecoding\my-portfolio\AGENTS.md`
- Preserve: `C:\Users\iq\.codex\config.toml`

**Interfaces:**

- Consumes: Codex's user-level `AGENTS.md` instruction discovery and the installed `superpowers:*` Skills.
- Produces: One `LIGHTWEIGHT-SUPERPOWERS` policy block with deterministic task classification, safety floors, user overrides, and rollback markers.

- [ ] **Step 1: Run the pre-change acceptance check and verify it fails**

Run:

```powershell
$path = 'C:\Users\iq\.codex\AGENTS.md'
$text = [System.IO.File]::ReadAllText($path)
$required = @(
  '<!-- BEGIN LIGHTWEIGHT-SUPERPOWERS -->',
  '## 自动分级',
  '## 不可省略的安全底线',
  '## 用户覆盖语句',
  '<!-- END LIGHTWEIGHT-SUPERPOWERS -->'
)
$missing = @($required | Where-Object { -not $text.Contains($_) })
if ($missing.Count -gt 0) {
  Write-Error ('Missing lightweight policy markers or sections: ' + ($missing -join ', '))
  exit 1
}
```

Expected: exit code `1` with `Missing lightweight policy markers or sections`, because the file is currently empty.

- [ ] **Step 2: Add the exact lightweight policy block**

Use `apply_patch` to add this exact UTF-8 Markdown content to `C:\Users\iq\.codex\AGENTS.md`:

```markdown
<!-- BEGIN LIGHTWEIGHT-SUPERPOWERS -->
# 个人 Codex 轻量工作流

目标：优先保持 Vibe Coding 的速度；只有任务复杂度或风险确实需要时，才启用完整工程流程。

## 自动分级

- 简单任务：文字、颜色、间距、说明或一到两个文件的低风险小改动。直接检查相关文件、做最小修改并运行针对性验证；不强制设计文档、实施计划、TDD、worktree 或 Agent。
- 中等任务：新增有限功能、影响两到三个相关文件，或有不止一种合理实现。先简短确认需求与完成标准，再实现并验证重要行为。
- 复杂或高风险任务：多文件结构调整、新框架或重要依赖、登录、权限、用户数据、支付、数据库、部署、云资源、难以回滚的操作，或多个实施阶段。使用 brainstorming → writing-plans → 必要的隔离与 TDD → 审查 → verification-before-completion。
- 只有至少两个互不依赖的任务才考虑并行 Agent。
- 只有较大功能确实需要保护当前稳定分支时才创建 Git worktree。

## 按需能力

- 新增功能或改变行为时按复杂度使用 brainstorming；设计获批且包含多个实施步骤时才使用 writing-plans。
- 功能实现或程序错误修复按风险使用 test-driven-development；纯文案、颜色和间距修改不强行 TDD。
- 较大改动完成后使用 requesting-code-review；收到审查意见时用 receiving-code-review 先验证建议。
- 真实网页交互、控制台、响应式布局或截图验收使用 playwright。
- 新建视觉型前端或明确要求重新设计、现代化时使用 frontend-app-builder；普通小改不触发。

## 不可省略的安全底线

- 出现错误、测试失败或异常行为时，必须使用 systematic-debugging：先复现、收集证据并找到根因，再做最小修复。
- 宣布完成、修复或通过前，必须使用 verification-before-completion：在当前任务中重新运行能证明结论的完整检查并阅读输出。
- 删除、覆盖、不可逆操作、安装依赖、提交、推送、部署或外部写入必须遵守当前用户指令与权限边界。
- GitHub 读取可以直接进行；评论、Issue、Pull Request、推送、合并等远程写入前必须询问。

## 上下文与验证

- 开始任务先确认当前目录、仓库状态、适用 Skill 和相关文件；不无目的地加载整个项目。
- 长任务在关键阶段更新计划；需求变化时先更新当前理解。
- 验证强度与风险匹配：文案检查目标文本和 diff；网页改动检查结构、视觉和控制台；交互改动运行可重复行为检查；Bug 修复先复现失败再验证修复与回归。
- 无法实际运行的检查必须明确标为“未验证”，不能用推测代替证据。
- 不把本地完成误报成已经推送或部署，不自动扩大外部账号或云服务权限。

## 用户覆盖语句

用户可以随时用以下指令覆盖自动分级：

- “这次简化流程”
- “这次使用完整流程”
- “先只分析，不修改”
- “不要安装依赖”
- “不要提交或推送”
- “只修改这些文件：……”
- “完成后先给我看 diff”

最新、最明确的用户指令优先。项目级 AGENTS.md 继续补充具体项目的技术、命令和验证规则。
<!-- END LIGHTWEIGHT-SUPERPOWERS -->
```

- [ ] **Step 3: Re-run the acceptance check and verify it passes**

Run:

```powershell
$path = 'C:\Users\iq\.codex\AGENTS.md'
$text = [System.IO.File]::ReadAllText($path)
$required = @(
  '<!-- BEGIN LIGHTWEIGHT-SUPERPOWERS -->',
  '## 自动分级',
  '## 按需能力',
  '## 不可省略的安全底线',
  '## 上下文与验证',
  'systematic-debugging',
  'verification-before-completion',
  'playwright',
  'frontend-app-builder',
  'GitHub 读取可以直接进行',
  '这次简化流程',
  '这次使用完整流程',
  '<!-- END LIGHTWEIGHT-SUPERPOWERS -->'
)
$missing = @($required | Where-Object { -not $text.Contains($_) })
$beginCount = ([regex]::Matches($text, '<!-- BEGIN LIGHTWEIGHT-SUPERPOWERS -->')).Count
$endCount = ([regex]::Matches($text, '<!-- END LIGHTWEIGHT-SUPERPOWERS -->')).Count
$placeholderPattern = '\b(T' + 'BD|T' + 'ODO|FIX' + 'ME)\b|待' + '定|稍后' + '补充'
$placeholders = [regex]::Matches($text, $placeholderPattern).Count
if ($missing.Count -gt 0 -or $beginCount -ne 1 -or $endCount -ne 1 -or $placeholders -ne 0) {
  [pscustomobject]@{
    Missing = $missing
    BeginMarkers = $beginCount
    EndMarkers = $endCount
    Placeholders = $placeholders
  } | ConvertTo-Json -Depth 4
  exit 1
}
[pscustomobject]@{
  Result = 'PASS'
  BeginMarkers = $beginCount
  EndMarkers = $endCount
  Placeholders = $placeholders
} | ConvertTo-Json
```

Expected: exit code `0` and JSON containing `"Result": "PASS"`, one begin marker, one end marker, and zero placeholders.

- [ ] **Step 4: Verify project, config, plugin, and Git isolation**

Run:

```powershell
$projectAgents = 'C:\Users\iq\OneDrive\Desktop\Codex_workspace\vibecoding\my-portfolio\AGENTS.md'
$config = 'C:\Users\iq\.codex\config.toml'
$plugin = 'C:\Users\iq\.codex\plugins\cache\openai-curated-remote\superpowers\6.2.0'
$git = 'D:\Dev\Tools\Git\cmd\git.exe'
$repo = 'C:\Users\iq\OneDrive\Desktop\Codex_workspace\vibecoding\my-portfolio'

$projectHash = (Get-FileHash -LiteralPath $projectAgents -Algorithm SHA256).Hash
$configHash = (Get-FileHash -LiteralPath $config -Algorithm SHA256).Hash
$skillCount = @(Get-ChildItem -LiteralPath (Join-Path $plugin 'skills') -Directory).Count
$missingSkills = @(
  Get-ChildItem -LiteralPath (Join-Path $plugin 'skills') -Directory |
    Where-Object { -not (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) }
).Count
$gitStatus = (& $git -C $repo status --short --branch) -join "`n"
$porcelain = (& $git -C $repo status --porcelain) -join "`n"

if ($projectHash -ne '7E01F49372411D4A0116AF98CE51D8A2D0812BD6DE2E7296C82C66560241F3CA') {
  Write-Error "Portfolio AGENTS.md changed unexpectedly: $projectHash"
  exit 1
}
if ($configHash -ne '32356EB129FB0E0BC1C0DEEC0B2EF389A5FA9C599E76BED3E5D8CD157BAB5030') {
  Write-Error "Codex config.toml changed unexpectedly: $configHash"
  exit 1
}
if ($skillCount -ne 14 -or $missingSkills -ne 0) {
  Write-Error "Superpowers skill verification failed: count=$skillCount missing=$missingSkills"
  exit 1
}
if ($gitStatus -notmatch '^## main\.\.\.origin/main') {
  Write-Error "Unexpected portfolio Git state: $gitStatus"
  exit 1
}
if ($porcelain.Length -ne 0) {
  Write-Error "Portfolio contains uncommitted changes: $porcelain"
  exit 1
}

[pscustomobject]@{
  Result = 'PASS'
  ProjectAgentsHash = $projectHash
  ConfigHash = $configHash
  SuperpowersSkills = $skillCount
  MissingSkillFiles = $missingSkills
  PortfolioGitStatus = $gitStatus
  PortfolioUncommittedChanges = 0
} | ConvertTo-Json -Depth 4
```

Expected: exit code `0`, `"Result": "PASS"`, 14 Superpowers Skills, zero missing Skill files, unchanged project/config hashes, zero uncommitted project changes, and a `main...origin/main` Git status line. The repository may be ahead because the approved design and plan are local commits; no remote write is allowed in this task.

- [ ] **Step 5: Record the live acceptance gate**

Do not create a synthetic project. Tell the user:

```text
轻量规则已写入用户级 AGENTS.md。它会从新的 Codex 任务开始稳定生效。
下一次真实任务将作为首次验收：检查自动分级是否准确、错误是否先定位、完成前是否有新验证证据，以及 GitHub 写入前是否询问。
```

Do not claim that behavioral acceptance has passed until a new real task demonstrates the rules.

- [ ] **Step 6: Document rollback**

Tell the user that rollback consists of removing only the text from:

```text
<!-- BEGIN LIGHTWEIGHT-SUPERPOWERS -->
```

through:

```text
<!-- END LIGHTWEIGHT-SUPERPOWERS -->
```

Removing this block must not uninstall Superpowers, edit `config.toml`, or change any project file.

## Final Verification

Before reporting implementation complete:

1. Re-run Steps 3 and 4 in full.
2. Confirm both commands exit `0`.
3. Confirm `C:\Users\iq\.codex\AGENTS.md` contains exactly one marked block.
4. Confirm no browser, dependency, worktree, push, deployment, or GitHub write occurred.
5. Report behavioral validation as pending until the next real Codex task.

# 小林的个人作品集

这是一个适合零基础学习者阅读和修改的静态个人作品集。它只使用 HTML、CSS 和原生 JavaScript，不需要安装第三方依赖。

## 功能

- 自我介绍、作品、技能与联系方式；
- 页面内导航；
- 明暗主题切换；
- 刷新后保留主题选择；
- 手机和桌面自适应；
- 清楚的键盘焦点样式；
- 尊重系统的“减少动态效果”设置。

## 文件结构

```text
my-portfolio/
├── index.html   网页的内容和结构
├── styles.css   网页的颜色、排版和布局
├── script.js    明暗主题切换
├── README.md    使用说明
└── AGENTS.md    Codex 的长期项目规则
```

## 方法一：直接打开

在文件资源管理器或 Finder 中双击 `index.html`。

如果主题无法在刷新后保存，或浏览器行为异常，请改用下面的本地服务器方法。

## 方法二：使用 Python 本地服务器

### Windows

1. 在 VS Code 中打开本项目文件夹。
2. 选择“终端”→“新建终端”。
3. 运行以下命令之一：

```powershell
py -m http.server 8000
```

如果 `py` 不可用：

```powershell
python -m http.server 8000
```

4. 在浏览器打开 <http://localhost:8000>。

### macOS

1. 在 VS Code 中打开本项目文件夹。
2. 选择“终端”→“新建终端”。
3. 运行：

```bash
python3 -m http.server 8000
```

4. 在浏览器打开 <http://localhost:8000>。

### 停止服务器

回到正在运行服务器的终端，按 `Ctrl + C`。

## 验证主题切换

1. 打开首页。
2. 点击“切换为深色”。
3. 确认背景、文字、卡片和边框一起变化。
4. 确认按钮文字变成“切换为浅色”。
5. 刷新页面，确认仍保留刚才的主题。
6. 按 `F12` 打开浏览器开发者工具，确认控制台没有红色错误。

## 修改自己的内容

### 修改姓名和介绍

打开 `index.html`，搜索“小林”，替换为自己的名字。再修改首屏和“关于我”中的文字。

### 修改邮箱

在 `index.html` 中找到：

```html
<a class="primary-link" href="mailto:hello@example.com">
  hello@example.com
</a>
```

把两个 `hello@example.com` 都替换为自己的邮箱。

### 修改颜色

打开 `styles.css`，修改最上方 `:root` 中的颜色变量。例如主色是：

```css
--color-accent: #245c45;
```

### 修改作品卡片

打开 `index.html`，在 `class="project-grid"` 的区域中修改每个 `<article>` 里的标题和说明。

## 常见问题

### 页面没有样式

- 确认 `styles.css` 与 `index.html` 在同一文件夹；
- 确认 HTML 中写的是 `href="styles.css"`；
- 保存全部文件后强制刷新浏览器。

### 主题按钮没有反应

- 确认真实文件名是 `script.js`；
- 确认 HTML 中写的是 `src="script.js"`，没有多余的 `s`；
- 打开浏览器控制台，检查是否有 404 或 JavaScript 错误。

### 8000 端口被占用

改用：

```text
python -m http.server 8080
```

Windows 也可以用：

```text
py -m http.server 8080
```

macOS 可以用：

```text
python3 -m http.server 8080
```

然后打开 <http://localhost:8080>。

## 隐私提醒

网页源代码会被访问者看到。不要把密码、API Key、身份证号或其他秘密写入 HTML、CSS 或 JavaScript。

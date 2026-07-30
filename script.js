const root = document.documentElement;
const themeToggle = document.querySelector("#theme-toggle");
const storageKey = "portfolio-theme";

function getSavedTheme() {
  try {
    return localStorage.getItem(storageKey);
  } catch {
    return null;
  }
}

function saveTheme(theme) {
  try {
    localStorage.setItem(storageKey, theme);
  } catch {
    // 存储不可用时，当前页面的主题切换仍然可以继续使用。
  }
}

function getInitialTheme() {
  const savedTheme = getSavedTheme();

  if (savedTheme === "light" || savedTheme === "dark") {
    return savedTheme;
  }

  const prefersDark = window.matchMedia(
    "(prefers-color-scheme: dark)"
  ).matches;

  return prefersDark ? "dark" : "light";
}

function applyTheme(theme) {
  root.dataset.theme = theme;

  const isDark = theme === "dark";
  themeToggle.setAttribute("aria-pressed", String(isDark));
  themeToggle.textContent = isDark ? "切换为浅色" : "切换为深色";
}

applyTheme(getInitialTheme());

themeToggle.addEventListener("click", () => {
  const nextTheme =
    root.dataset.theme === "dark" ? "light" : "dark";

  applyTheme(nextTheme);
  saveTheme(nextTheme);
});

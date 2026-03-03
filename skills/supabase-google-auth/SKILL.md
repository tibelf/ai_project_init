---
name: supabase-google-auth
description: Guide for integrating Google OAuth login into Supabase + React projects. Use when user asks to add Google login, integrate Gmail account sign-in, implement Supabase Google OAuth, use supabase signInWithOAuth, add Google login button, set up Auth Provider, create login dialog, or implement auth-gating. Covers Google Cloud Console setup, Supabase provider configuration, React Auth Hook pattern, LoginPromptDialog, and route protection.
---

# Supabase + Google OAuth 集成指南

在 Supabase + React 项目中集成 Google 账号登录，分三步完成：
配置 → React 实现 → 路由保护。

## 实现流程

### Step 1：Google Cloud + Supabase Console 配置

读取详细步骤：`references/supabase-console-setup.md`

要点：
- 在 Google Cloud Console 创建 OAuth 2.0 Client ID
- 将 `https://<project-id>.supabase.co/auth/v1/callback` 加入授权重定向 URI
- 在 Supabase Console → Authentication → Providers → Google 中填入 Client ID / Secret
- 配置环境变量 `VITE_SUPABASE_URL` 和 `VITE_SUPABASE_PUBLISHABLE_KEY`

### Step 2：React 实现

读取完整代码模式：`references/react-patterns.md`

共三个模式：

**Pattern 1 — Auth Hook（`useAuth.tsx`）**
- 创建 `AuthContext` + `AuthProvider`
- `supabase.auth.onAuthStateChange` 监听状态变化
- `supabase.auth.getSession()` 初始化已有 session
- 导出 `{ user, loading, signOut }`
- 在 `App.tsx` 根节点包裹 `<AuthProvider>`

**Pattern 2 — LoginPromptDialog**
- 调用 `supabase.auth.signInWithOAuth({ provider: 'google', options: { redirectTo: window.location.origin } })`
- `useEffect` 检测 `user` 变为非 null 时自动关闭弹窗
- 包含完整 Google 官方 SVG 图标

**Pattern 3 — Auth-Gating 路由保护**
- 邮箱白名单：`ALLOWED_EMAILS.includes(user.email)` → 不在列表则 `<Navigate to="/" />`
- 普通路由保护：未登录重定向
- 公开页面触发登录：点击受保护操作时弹出 LoginPromptDialog

### Step 3：可选 i18n 支持

如项目使用 `react-i18next`，将登录相关字符串提取到翻译文件：
- `auth.loginTitle`、`auth.loginDescription`、`auth.googleLogin`
- 用 `const { t } = useTranslation()` 替换硬编码字符串

详见 `references/react-patterns.md` 末尾的 i18n 章节。

## 参考文件

| 文件 | 内容 |
|------|------|
| `references/supabase-console-setup.md` | Google Cloud Console + Supabase Console 完整配置步骤、环境变量、常见错误 |
| `references/react-patterns.md` | 三个 React 模式的完整代码：Auth Hook、LoginPromptDialog、路由保护 |

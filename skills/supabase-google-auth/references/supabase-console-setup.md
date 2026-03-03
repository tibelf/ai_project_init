# Supabase Console + Google Cloud OAuth 配置指南

## 1. Google Cloud Console — 创建 OAuth 2.0 凭据

1. 打开 [Google Cloud Console](https://console.cloud.google.com/) → APIs & Services → Credentials
2. 点击「Create Credentials」→「OAuth 2.0 Client ID」
3. Application type 选「Web application」
4. 在「Authorized redirect URIs」中添加：
   - 生产环境：`https://<your-project-id>.supabase.co/auth/v1/callback`
   - 本地开发：`http://localhost:8080`（或你的本地端口）
5. 保存后获得 **Client ID** 和 **Client Secret**

> **Consent Screen**：首次创建时需先配置 OAuth Consent Screen（User Type 选 External），
> 至少填写 App name、User support email、Developer contact information，
> 否则 OAuth 流程会报错。

---

## 2. Supabase Console — 启用 Google Provider

1. 进入 Supabase 项目 → Authentication → Providers → Google
2. 将「Enable Sign in with Google」开关打开
3. 填入第一步获得的 Client ID 和 Client Secret
4. 保存

---

## 3. 环境变量配置

在项目根目录 `.env`（或 `.env.local`）中配置：

```env
VITE_SUPABASE_URL=https://<your-project-id>.supabase.co
VITE_SUPABASE_PUBLISHABLE_KEY=<your-anon-public-key>
```

> `VITE_SUPABASE_PUBLISHABLE_KEY` 即 Supabase 控制台的 **anon/public key**，
> 可在 Project Settings → API 中找到。

---

## 4. Supabase 客户端初始化

```typescript
// src/integrations/supabase/client.ts
import { createClient } from '@supabase/supabase-js';

const SUPABASE_URL = import.meta.env.VITE_SUPABASE_URL;
const SUPABASE_PUBLISHABLE_KEY = import.meta.env.VITE_SUPABASE_PUBLISHABLE_KEY;

export const supabase = createClient(SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY, {
  auth: {
    storage: localStorage,
    persistSession: true,
    autoRefreshToken: true,
  }
});
```

---

## 5. 常见问题排查

| 问题 | 原因 | 解决方案 |
|------|------|----------|
| `redirect_uri_mismatch` | Google Cloud 中未添加 callback URI | 在 Authorized redirect URIs 中添加 Supabase callback URL |
| `Access blocked: This app's request is invalid` | Consent Screen 未配置 | 在 Google Cloud 完成 OAuth Consent Screen 配置 |
| 登录后没有跳回页面 | `redirectTo` 域名不在允许列表 | Supabase Console → Authentication → URL Configuration 添加站点域名 |
| 本地 `localhost` 登录失败 | 未添加本地重定向 URI | Google Cloud Console 中加入 `http://localhost:<port>` |

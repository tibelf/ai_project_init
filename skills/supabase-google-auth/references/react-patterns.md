# React 实现模式：Supabase Google OAuth

以下三个模式取自真实生产项目，可直接复用。

---

## Pattern 1：Auth Hook（`useAuth.tsx`）

统一管理登录状态，通过 React Context 向全局暴露 `user`、`loading`、`signOut`。

```tsx
// src/hooks/useAuth.tsx
import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { supabase } from "@/integrations/supabase/client";
import type { User } from "@supabase/supabase-js";

interface AuthContextType {
  user: User | null;
  loading: boolean;
  signOut: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  loading: true,
  signOut: async () => {},
});

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // 监听登录/登出状态变化
    const { data: { subscription } } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    // 初始化时读取已有 session（页面刷新后恢复状态）
    supabase.auth.getSession().then(({ data: { session } }) => {
      setUser(session?.user ?? null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const signOut = async () => {
    await supabase.auth.signOut();
  };

  return (
    <AuthContext.Provider value={{ user, loading, signOut }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
```

**接入方式**：在 `App.tsx` 或路由根节点用 `<AuthProvider>` 包裹应用。

```tsx
// App.tsx
import { AuthProvider } from "@/hooks/useAuth";

function App() {
  return (
    <AuthProvider>
      {/* routes */}
    </AuthProvider>
  );
}
```

---

## Pattern 2：LoginPromptDialog（登录对话框）

触发 Google OAuth 跳转，登录成功后自动关闭弹窗。

```tsx
// src/components/LoginPromptDialog.tsx
import { useEffect } from "react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { supabase } from "@/integrations/supabase/client";
import { useAuth } from "@/hooks/useAuth";

interface LoginPromptDialogProps {
  open: boolean;
  onClose: () => void;
}

const LoginPromptDialog = ({ open, onClose }: LoginPromptDialogProps) => {
  const { user } = useAuth();

  // 登录成功后自动关闭弹窗
  useEffect(() => {
    if (user && open) {
      onClose();
    }
  }, [user, open, onClose]);

  const handleGoogleLogin = async () => {
    await supabase.auth.signInWithOAuth({
      provider: 'google',
      options: {
        redirectTo: window.location.origin,
      },
    });
  };

  return (
    <Dialog open={open} onOpenChange={(v) => !v && onClose()}>
      <DialogContent className="sm:max-w-[400px]">
        <DialogHeader>
          <DialogTitle className="text-center">登录</DialogTitle>
          <DialogDescription className="text-center">
            登录后可使用完整功能
          </DialogDescription>
        </DialogHeader>
        <button
          onClick={handleGoogleLogin}
          className="flex items-center justify-center gap-3 w-full py-3 rounded-xl border border-border bg-card hover:bg-secondary transition-colors text-sm font-medium text-foreground"
        >
          {/* Google Logo SVG */}
          <svg className="w-5 h-5" viewBox="0 0 24 24">
            <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.1z" fill="#4285F4" />
            <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
            <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" fill="#FBBC05" />
            <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
          </svg>
          使用 Google 账号登录
        </button>
      </DialogContent>
    </Dialog>
  );
};

export default LoginPromptDialog;
```

**使用方式**：

```tsx
const [showLogin, setShowLogin] = useState(false);

// 在需要登录才能操作的地方触发
const handleRestrictedAction = () => {
  if (!user) {
    setShowLogin(true);
    return;
  }
  // 执行操作
};

return (
  <>
    <button onClick={handleRestrictedAction}>筛选</button>
    <LoginPromptDialog open={showLogin} onClose={() => setShowLogin(false)} />
  </>
);
```

---

## Pattern 3：Auth-Gating 路由保护

### 3a. 邮箱白名单（管理后台）

只允许特定邮箱访问，其他用户重定向到首页。

```tsx
// src/pages/Dashboard.tsx
import { Navigate, Outlet } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";

const ALLOWED_EMAILS = ["admin@example.com"];

const Dashboard = () => {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center">加载中...</div>;
  }

  if (!user || !ALLOWED_EMAILS.includes(user.email ?? "")) {
    return <Navigate to="/" replace />;
  }

  return <Outlet />;
};

export default Dashboard;
```

### 3b. 普通路由保护（仅需登录）

```tsx
const ProtectedRoute = ({ children }: { children: ReactNode }) => {
  const { user, loading } = useAuth();

  if (loading) return <div>加载中...</div>;
  if (!user) return <Navigate to="/" replace />;

  return <>{children}</>;
};
```

### 3c. 公开页面触发登录（onClick / onFocus）

适用于主页功能按钮——未登录时弹出登录框而不是跳转页面。

```tsx
const { user } = useAuth();
const [showLogin, setShowLogin] = useState(false);

const handleSearch = () => {
  if (!user) {
    setShowLogin(true);
    return;
  }
  // 执行搜索
};

const handleFilterChange = () => {
  if (!user) {
    setShowLogin(true);
    return;
  }
  // 应用筛选
};
```

---

## i18n 支持（可选）

如果项目使用 `react-i18next`，将硬编码字符串替换为翻译键：

```tsx
// 替换前
<DialogTitle>登录</DialogTitle>

// 替换后
const { t } = useTranslation();
<DialogTitle>{t("auth.loginTitle")}</DialogTitle>
```

在 `src/i18n/locales/zh.json` 中添加：
```json
{
  "auth": {
    "loginTitle": "登录",
    "loginDescription": "登录后可使用完整功能",
    "googleLogin": "使用 Google 账号登录"
  }
}
```

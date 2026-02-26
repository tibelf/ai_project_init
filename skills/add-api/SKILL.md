---
name: add-api
description: |
  为 xhs-api 项目新增 API 端点的标准化流程。当用户说"新增接口"、"添加 API"、"创建端点"、"加一个 API"或需要扩展 REST API 时使用此 skill。自动生成适配器、路由、模型代码，并指导完成测试和文档。
---

# XHS API 新增接口流程

## 概述

本项目采用 **适配器模式** + **FastAPI 路由**，新增 API 需创建/修改 4 个文件。

## 必需信息

开始前确认：
1. **端点名称**：如 `search`、`comment`
2. **HTTP 方法**：POST（默认）或 GET
3. **请求参数**：必填和可选字段
4. **小红书 API**：目标 URL 和请求格式

## 步骤 1: 定义请求模型

编辑 `api/models.py`，参考现有模型添加：

```python
class YourRequest(BaseModel):
    """请求描述"""

    param1: str = Field(
        ...,
        description="参数描述",
        min_length=1,
        max_length=100,
        examples=["example"],
    )
    param2: Optional[str] = Field(None, description="可选参数")

    @field_validator("param1")
    @classmethod
    def validate_param1(cls, v):
        if not v or v.isspace():
            raise ValueError("param1 不能为空")
        return v.strip()
```

## 步骤 2: 创建适配器

新建 `api/adapters/your_adapter.py`，使用 `assets/adapter_template.py` 模板。

关键约定：
- 继承 `BaseAdapter`
- 方法用 `@staticmethod` + `async def`
- 用 `BaseAdapter.temp_cookies_file()` 管理临时文件
- 用 `BaseAdapter.handle_script_error()` 处理异常
- 返回完整 API 响应，不过滤字段

## 步骤 3: 创建路由

新建 `api/routes/your_route.py`，使用 `assets/route_template.py` 模板。

路由标准模式：
- `router = APIRouter(prefix="/api/v1/xxx", tags=["标签"])`
- 依赖注入：`api_key: str = Depends(verify_api_key)`
- Cookies Header：`cookies: str = Header(..., alias="X-XHS-Cookies")`
- 用 `build_success_response()` 构造响应

## 步骤 4: 注册路由

编辑 `api/main.py`：

```python
from api.routes import your_route
app.include_router(your_route.router)
```

## 步骤 5: 编写测试

### 5.1 单元测试
在 `tests/unit/` 创建测试文件，覆盖：
- 认证检查（无 key、无效 key → 401）
- 参数验证（缺字段 → 422）
- 成功响应格式

运行单元测试：
```bash
pytest tests/unit/ -v
```

### 5.2 集成测试
编辑 `tests/integration/test_api.py`，添加新端点测试：
- 添加 `test_xxx` 函数
- 更新测试计数（如 3/4 → 4/5）
- 在 `main()` 中添加 `results.append()`

**注意**：对于写入类接口（如发布、删除），集成测试只验证参数校验，不实际执行操作。

运行集成测试：
```bash
./tools/dev.sh  # 先启动服务
python tests/integration/test_api.py
```

### 5.3 手动测试脚本（可选但推荐）

对于重要的 API 端点，建议在 `tests/manual/` 创建专门的测试脚本，进行全面的功能验证。

新建 `tests/manual/test_xxx.py`，使用 `assets/manual_test_template.py` 模板。

手动测试脚本特点：
- 针对单个 API 端点进行全面功能测试
- 测试所有参数组合和边界条件
- 支持多环境（local/remote）
- 验证响应字段完整性
- 适合在开发完成后进行端到端验证

运行手动测试：
```bash
./tools/dev.sh  # 先启动服务
python tests/manual/test_xxx.py
python tests/manual/test_xxx.py --env remote
python tests/manual/test_xxx.py --server http://localhost:8888
```

手动测试脚本应覆盖：
- 所有参数的有效值组合
- 边界条件（空值、特殊字符、超长输入）
- 响应字段完整性验证
- 多环境支持（local/remote）

## 步骤 6: 更新文档

### 6.1 新建 API 文档
创建 `docs/api/your_endpoint.md`，包含：
- 请求方式、URL
- Headers 说明（Authorization、X-XHS-Cookies）
- 请求参数表格
- 响应参数说明
- 成功/失败响应示例
- cURL 用法
- Python 用法示例
- 错误码表
- 注意事项

### 6.2 更新端点列表
在 `docs/api/README.md` 添加端点条目：
```markdown
| POST | `/api/v1/xxx/endpoint` | 功能描述 |
```

### 6.3 更新 CLAUDE 文档引用
编辑 `.claude/docs/api-reference.md`：
- 在端点列表表格中添加新端点
- 添加端点详情章节（参数、响应示例）

### 6.4 记录 Session 决策
按 CLAUDE.md 工作流规则，更新 `.claude/tasks/SESSION.md`：
- Why：为何新增此 API
- What changed：用户/开发者可见的变化
- New concepts：新模块、新配置
- Scope：影响的路径/模块
- Breaking：是否有破坏性变更

### 6.5 导出适配器（可选）
如需要在其他地方导入适配器，编辑 `api/adapters/__init__.py`：
```python
from api.adapters.xxx_adapter import XxxAdapter
__all__ = [..., "XxxAdapter"]
```

### 6.6 更新项目 README（如涉及用户指引）
如果新 API 需要用户了解，编辑根目录 `README.md`：
- 在功能列表中添加新端点
- 添加使用示例（如有必要）

### 6.7 错误码文档（如有新错误码）
如有新错误码，更新 `docs/ERROR_CODES.md`

## 验证

```bash
./tools/dev.sh                    # 启动服务
# 访问 http://localhost:8000/docs  # Swagger UI 测试
pytest -v                         # 运行全部测试
```

## 文件清单

| 步骤 | 文件 | 操作 |
|------|------|------|
| 1 | `api/models.py` | 新增请求模型 |
| 2 | `api/adapters/xxx_adapter.py` | 新建 |
| 3 | `api/routes/xxx.py` | 新建 |
| 4 | `api/main.py` | 注册路由 |
| 5.1 | `tests/unit/test_xxx.py` | 新建单元测试 |
| 5.2 | `tests/integration/test_api.py` | 添加集成测试 |
| 5.3 | `tests/manual/test_xxx.py` | 新建手动测试脚本（可选）|
| 6.1 | `docs/api/xxx.md` | 新建 API 文档 |
| 6.2 | `docs/api/README.md` | 更新端点列表 |
| 6.3 | `.claude/docs/api-reference.md` | 更新端点列表和详情 |
| 6.4 | `.claude/tasks/SESSION.md` | 记录决策 |
| 6.5 | `api/adapters/__init__.py` | 导出适配器（可选）|
| 6.6 | `README.md` | 更新项目 README（如涉及用户指引）|
| 6.7 | `docs/ERROR_CODES.md` | 更新错误码（如有新错误码）|

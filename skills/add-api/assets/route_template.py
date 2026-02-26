"""
路由模板 - 复制此文件并重命名为 your_route.py

使用方法：
1. 复制此文件到 api/routes/
2. 重命名为 xxx.py
3. 替换 TODO 注释处的内容
4. 在 api/main.py 中注册路由
"""
from fastapi import APIRouter, Header, Depends, Request
import uuid
import time

from api.models import YourRequest, SuccessResponse  # TODO: 导入正确的请求模型
from api.auth import verify_api_key
from api.adapters.your_adapter import YourAdapter  # TODO: 导入正确的适配器
from api.utils.signature_manager import SignatureManager
from api.utils.response import build_success_response
from api.utils.logger import logger

# TODO: 修改 prefix 和 tags
router = APIRouter(prefix="/api/v1/xxx", tags=["功能名"])


@router.post("/endpoint", response_model=SuccessResponse)  # TODO: 修改路径和方法
async def your_endpoint(  # TODO: 重命名函数
    request_body: YourRequest,  # TODO: 使用正确的请求模型
    request: Request,
    cookies: str = Header(..., alias="X-XHS-Cookies", description="小红书 Cookies（JSON 字符串）"),
    api_key: str = Depends(verify_api_key),
):
    """
    TODO: 端点描述

    Args:
        request_body: 请求体
        cookies: Cookies Header
        api_key: API Key（通过依赖注入验证）

    Returns:
        SuccessResponse: 标准化响应

    Raises:
        HTTPException: 认证失败、参数错误、API 调用失败等
    """
    request_id = str(uuid.uuid4())
    start_time = time.time()

    logger.info(f"收到请求: request_id={request_id}")

    try:
        # 获取 SignatureManager 单例
        sig_manager = await SignatureManager.get_instance()

        # TODO: 调用适配器方法
        result_data = await YourAdapter.your_method(
            param1=request_body.param1,
            cookies_str=cookies,
            signature_manager=sig_manager,
        )

        # 构造成功响应
        execution_time_ms = (time.time() - start_time) * 1000
        return build_success_response(
            data=result_data,
            request_id=request_id,
            execution_time_ms=execution_time_ms
        )

    except Exception as e:
        logger.error(f"请求失败: request_id={request_id}, error={str(e)}")
        raise

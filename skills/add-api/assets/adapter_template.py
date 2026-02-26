"""
适配器模板 - 复制此文件并重命名为 your_adapter.py

使用方法：
1. 复制此文件到 api/adapters/
2. 重命名为 xxx_adapter.py
3. 替换 TODO 注释处的内容
"""
import json
import requests
from typing import Dict, Optional

from api.adapters.base_adapter import BaseAdapter
from api.utils.signature_manager import SignatureManager
from api.utils.logger import logger


class YourAdapter(BaseAdapter):  # TODO: 重命名类
    """
    TODO: 适配器描述
    """

    @staticmethod
    async def your_method(  # TODO: 重命名方法
        param1: str,  # TODO: 定义参数
        cookies_str: str,
        signature_manager: SignatureManager,
        param2: Optional[str] = None,  # TODO: 可选参数
    ) -> Dict:
        """
        TODO: 方法描述

        Args:
            param1: 参数1描述
            cookies_str: Cookies JSON 字符串
            signature_manager: SignatureManager 实例

        Returns:
            Dict: 完整的 API 响应数据

        Raises:
            SignatureGenerationError: 签名生成失败
            APICallError: API 调用失败
        """
        try:
            async with BaseAdapter.temp_cookies_file(cookies_str) as cookies_path:
                logger.info(f"开始请求: param1={param1[:8]}...")

                # 加载 Cookies
                with open(cookies_path, "r", encoding="utf-8") as f:
                    cookies_data = json.load(f)

                # 处理 Cookies 格式（列表 vs 字典）
                if isinstance(cookies_data, list):
                    cookies = {item["name"]: item["value"] for item in cookies_data}
                elif isinstance(cookies_data, dict):
                    cookies = cookies_data
                else:
                    raise ValueError("Cookies 格式不正确")

                # TODO: 修改 URL 和请求方法
                url = "https://edith.xiaohongshu.com/api/sns/web/v1/xxx"
                method = "POST"  # 或 "GET"

                # TODO: 构建请求体（POST）或查询参数（GET）
                body = {
                    "param1": param1,
                    # 添加其他参数
                }

                # 序列化请求体
                body_str = json.dumps(body, ensure_ascii=False, separators=(",", ":"))
                body_bytes = body_str.encode("utf-8")

                # 生成签名
                # POST: 传递 body 对象
                # GET: 传递 None
                x_s, x_s_common, x_t = await signature_manager.generate_signature(
                    url, method, body  # GET 请求改为 None
                )

                # 构建请求头
                headers = {
                    "Content-Type": "application/json;charset=UTF-8",
                    "x-b3-traceid": x_t,
                    "x-s": x_s,
                    "x-s-common": x_s_common,
                    "x-t": x_t,
                    "x-xray-traceid": x_t,
                }

                # 发送请求
                logger.debug(f"发送请求: {method} {url}")

                # TODO: 根据方法选择
                if method == "POST":
                    resp = requests.post(url, data=body_bytes, headers=headers, cookies=cookies)
                else:
                    resp = requests.get(url, headers=headers, cookies=cookies)

                # 检查响应
                if resp.status_code != 200:
                    logger.error(f"API 调用失败: HTTP {resp.status_code}")
                    raise RuntimeError(f"API 调用失败: HTTP {resp.status_code}")

                resp_json = resp.json()
                logger.info("✅ 请求成功")

                return resp_json

        except Exception as e:
            logger.error(f"请求失败: {e}", exc_info=True)
            BaseAdapter.handle_script_error(e)

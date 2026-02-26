#!/usr/bin/env python3
"""
小红书笔记配图生成工具
通过七牛云代理调用 Gemini API 生成图片
固定使用 4:3 比例，适配小红书笔记封面
"""

import argparse
import base64
import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError


API_URL = "https://api.qnaigc.com/v1/images/generations"
MODEL = "gemini-3.0-pro-image-preview"

# 小红书笔记固定使用 4:3 比例
DEFAULT_ASPECT_RATIO = "4:3"
DEFAULT_RESOLUTION = "2K"


def generate_image(prompt: str, output: str = None, resolution: str = DEFAULT_RESOLUTION) -> str:
    """
    生成小红书笔记配图

    Args:
        prompt: 图片描述（建议包含中文文字要求）
        output: 输出文件路径，如果为 None 则输出 base64
        resolution: 分辨率，默认 2K

    Returns:
        输出文件路径或 base64 字符串
    """
    api_key = os.environ.get("QINIU_API_KEY")
    if not api_key:
        print("错误: 未设置 QINIU_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "image_config": {
            "aspect_ratio": DEFAULT_ASPECT_RATIO,
            "output_resolution": resolution
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    try:
        req = Request(API_URL, data=json.dumps(payload).encode(), headers=headers, method="POST")
        with urlopen(req, timeout=120) as response:
            result = json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        print(f"API 请求失败 ({e.code}): {error_body}", file=sys.stderr)
        sys.exit(1)
    except URLError as e:
        print(f"网络错误: {e.reason}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"请求异常: {e}", file=sys.stderr)
        sys.exit(1)

    if "data" not in result or not result["data"]:
        print(f"API 返回格式错误: {result}", file=sys.stderr)
        sys.exit(1)

    b64_json = result["data"][0].get("b64_json")
    if not b64_json:
        print(f"API 未返回图片数据: {result}", file=sys.stderr)
        sys.exit(1)

    if output:
        image_data = base64.b64decode(b64_json)
        with open(output, "wb") as f:
            f.write(image_data)
        print(f"图片已保存: {output}")
        return output
    else:
        print(b64_json)
        return b64_json


def main():
    parser = argparse.ArgumentParser(
        description="小红书笔记配图生成工具（固定 4:3 比例）",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成 AI 工具推荐配图
  %(prog)s -p "现代科技插画，展示AI自动填写PDF表单，中文文字'智能填表'突出显示，简洁科技风格" -o cover.png

  # 生成笔记工具配图
  %(prog)s -p "数字化笔记概念图，中文'第二大脑'文字，蓝色科技感配色" -o note-cover.png

  # 生成 4K 高清配图
  %(prog)s -p "AI助手概念图，中文'效率神器'" --resolution 4K -o hero.png

注意：
  - 图片比例固定为 4:3，适配小红书笔记封面
  - 如需在图片中显示文字，请在 prompt 中明确指定中文内容
"""
    )
    parser.add_argument("-p", "--prompt", required=True, help="图片描述（建议在 prompt 中指定需要显示的中文文字）")
    parser.add_argument("--resolution", default=DEFAULT_RESOLUTION, choices=["1K", "2K", "4K"], help="分辨率 (默认: 2K)")
    parser.add_argument("-o", "--output", help="输出文件路径（如不指定则输出 base64）")

    args = parser.parse_args()
    generate_image(args.prompt, args.output, args.resolution)


if __name__ == "__main__":
    main()

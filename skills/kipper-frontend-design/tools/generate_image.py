#!/usr/bin/env python3
"""
Gemini 图片生成工具
通过七牛云代理调用 Gemini API 生成图片
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

ASPECT_RATIOS = ["1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"]
RESOLUTIONS = ["1K", "2K", "4K"]


def generate_image(prompt: str, aspect_ratio: str = "16:9", resolution: str = "2K", output: str = None) -> str:
    """
    生成图片

    Args:
        prompt: 图片描述
        aspect_ratio: 宽高比
        resolution: 分辨率
        output: 输出文件路径，如果为 None 则输出 base64

    Returns:
        输出文件路径或 base64 字符串
    """
    api_key = os.environ.get("QINIU_API_KEY")
    if not api_key:
        print("错误: 未设置 QINIU_API_KEY 环境变量", file=sys.stderr)
        sys.exit(1)

    if aspect_ratio not in ASPECT_RATIOS:
        print(f"错误: 不支持的宽高比 {aspect_ratio}，支持: {', '.join(ASPECT_RATIOS)}", file=sys.stderr)
        sys.exit(1)

    if resolution not in RESOLUTIONS:
        print(f"错误: 不支持的分辨率 {resolution}，支持: {', '.join(RESOLUTIONS)}", file=sys.stderr)
        sys.exit(1)

    payload = {
        "model": MODEL,
        "prompt": prompt,
        "image_config": {
            "aspect_ratio": aspect_ratio,
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
        description="Gemini 图片生成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 生成图片并保存到文件
  %(prog)s -p "A futuristic city skyline at sunset" -o hero.png

  # 生成正方形图片
  %(prog)s -p "Minimalist logo design" -r 1:1 -o logo.png

  # 生成 4K 高清图片
  %(prog)s -p "Abstract gradient background" --resolution 4K -o bg.png

  # 输出 base64（用于内嵌 HTML）
  %(prog)s -p "Icon of a rocket" -r 1:1
"""
    )
    parser.add_argument("-p", "--prompt", required=True, help="图片描述（建议使用英文）")
    parser.add_argument("-r", "--ratio", default="16:9", choices=ASPECT_RATIOS, help="宽高比 (默认: 16:9)")
    parser.add_argument("--resolution", default="2K", choices=RESOLUTIONS, help="分辨率 (默认: 2K)")
    parser.add_argument("-o", "--output", help="输出文件路径（如不指定则输出 base64）")

    args = parser.parse_args()
    generate_image(args.prompt, args.ratio, args.resolution, args.output)


if __name__ == "__main__":
    main()

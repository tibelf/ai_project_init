#!/usr/bin/env python3
"""
XXX API 完整功能测试

测试所有参数组合：
- 参数1: 选项A / 选项B / 选项C
- 参数2: 可选值（不传=默认）
- count: 返回结果数量

用法:
  python tests/manual/test_xxx.py
  python tests/manual/test_xxx.py --env remote
  python tests/manual/test_xxx.py --server http://localhost:8888
"""
import requests
import json
import sys
import argparse
import time
from pathlib import Path
from typing import Optional


def load_config():
    """加载测试配置"""
    config_file = Path(__file__).parent.parent.parent / 'test_config.json'

    if not config_file.exists():
        print("❌ 配置文件不存在: test_config.json")
        print("💡 提示: 请复制 test_config.json.example 为 test_config.json 并修改配置")
        sys.exit(1)

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ 配置文件格式错误: {e}")
        sys.exit(1)


def load_cookies(cookies_file):
    """加载 cookies"""
    if cookies_file.startswith('/'):
        cookies_path = Path(cookies_file)
    else:
        cookies_path = Path(__file__).parent.parent.parent / cookies_file

    if not cookies_path.exists():
        print(f"❌ Cookies 文件不存在: {cookies_path}")
        print("💡 提示: 请确保 cookies.json 文件存在")
        sys.exit(1)

    try:
        with open(cookies_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Cookies 文件格式错误: {e}")
        sys.exit(1)


def call_api(server_url: str, api_key: str, cookies_str: str,
             param1: str, param2: str = None) -> dict:
    """
    调用 API

    根据实际 API 修改：
    - HTTP 方法（POST/GET）
    - 端点路径
    - 请求参数
    """
    headers = {
        'Authorization': f'Bearer {api_key}',
        'X-XHS-Cookies': cookies_str,
        'Content-Type': 'application/json'
    }

    data = {'param1': param1}
    if param2:
        data['param2'] = param2

    try:
        resp = requests.post(
            f"{server_url}/api/v1/xxx/endpoint",
            headers=headers,
            json=data,
            timeout=120
        )

        if resp.status_code == 200:
            return resp.json()
        else:
            return {
                'success': False,
                'error': {'code': resp.status_code, 'message': resp.text[:200]}
            }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': {'code': -1, 'message': str(e)}
        }


def parse_response(result: dict) -> tuple[bool, any, Optional[str]]:
    """
    解析 API 响应

    返回: (success, data, error_message)

    根据实际响应结构调整解析逻辑
    """
    if not result.get('success'):
        error = result.get('error', {})
        return False, None, f"code={error.get('code')}, msg={error.get('message')}"

    inner_data = result.get('data', {})
    inner_code = inner_data.get('code', 0)
    inner_success = inner_data.get('success', True)
    inner_msg = inner_data.get('msg', '')

    if inner_code != 0 or inner_success is False:
        return False, None, f"业务错误: code={inner_code}, msg={inner_msg}"

    return True, inner_data.get('data'), None


def test_basic_functionality(server_url: str, api_key: str, cookies_str: str) -> bool:
    """测试基本功能"""
    print("\n" + "=" * 60)
    print("🧪 测试 1/N: 基本功能")
    print("=" * 60)

    result = call_api(server_url, api_key, cookies_str, "test_value")
    success, data, error = parse_response(result)

    if success:
        print("✅ 基本功能正常")
        # 可以添加更多验证逻辑
        return True
    else:
        print(f"❌ 失败: {error}")
        return False


def test_parameter_variations(server_url: str, api_key: str, cookies_str: str) -> bool:
    """测试参数变体"""
    print("\n" + "=" * 60)
    print("🧪 测试 2/N: 参数变体")
    print("=" * 60)

    # 根据实际 API 修改测试用例
    test_cases = [
        ("value1", "描述1"),
        ("value2", "描述2"),
        ("value3", "描述3"),
    ]

    all_passed = True
    for value, desc in test_cases:
        result = call_api(server_url, api_key, cookies_str, value)
        success, data, error = parse_response(result)

        if success:
            print(f"  {desc}:".ljust(20) + "✅ 通过")
        else:
            print(f"  {desc}:".ljust(20) + f"❌ {error}")
            all_passed = False

        time.sleep(1)  # 避免请求过快

    return all_passed


def test_edge_cases(server_url: str, api_key: str, cookies_str: str) -> bool:
    """测试边界条件"""
    print("\n" + "=" * 60)
    print("🧪 测试 3/N: 边界条件")
    print("=" * 60)

    all_passed = True

    # 空值测试（预期报错）
    print("\n  空值测试:")
    result = call_api(server_url, api_key, cookies_str, "")
    success, data, error = parse_response(result)
    if not success:
        print(f"    空字符串:".ljust(25) + f"✅ 预期报错")
    else:
        print(f"    空字符串:".ljust(25) + f"⚠️  意外成功")

    time.sleep(1)

    # 特殊字符测试
    print("\n  特殊字符测试:")
    special_values = [
        ("🎮测试", "emoji"),
        ("测试！！", "标点"),
        ("test & value", "符号"),
    ]

    for value, desc in special_values:
        result = call_api(server_url, api_key, cookies_str, value)
        success, data, error = parse_response(result)

        if success:
            print(f"    {desc}:".ljust(25) + "✅ 通过")
        else:
            print(f"    {desc}:".ljust(25) + f"⚠️  {error[:30]}")

        time.sleep(1)

    # 超长输入测试
    print("\n  超长输入测试:")
    long_value = "测试" * 50  # 100 个字符
    result = call_api(server_url, api_key, cookies_str, long_value)
    success, data, error = parse_response(result)

    if success:
        print(f"    {len(long_value)}字符:".ljust(25) + "✅ 通过")
    else:
        print(f"    {len(long_value)}字符:".ljust(25) + f"⚠️  {error[:30]}")

    return all_passed


def test_response_fields(server_url: str, api_key: str, cookies_str: str) -> bool:
    """验证响应字段完整性"""
    print("\n" + "=" * 60)
    print("🧪 测试 4/N: 响应字段验证")
    print("=" * 60)

    result = call_api(server_url, api_key, cookies_str, "test_value")
    success, data, error = parse_response(result)

    if not success:
        print(f"  ❌ 请求失败: {error}")
        return False

    all_passed = True

    # 根据实际 API 响应结构修改必需字段列表
    required_fields = ['field1', 'field2', 'field3']

    print("\n  必需字段检查:")
    for field in required_fields:
        if isinstance(data, dict):
            value = data.get(field)
        else:
            value = None

        if value is not None:
            display_value = str(value)[:30] + "..." if len(str(value)) > 30 else value
            print(f"    {field}:".ljust(20) + f"✅ {display_value}")
        else:
            print(f"    {field}:".ljust(20) + "❌ 缺失或为空")
            all_passed = False

    return all_passed


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='XXX API 完整功能测试')
    parser.add_argument('--env', choices=['local', 'remote'],
                       help='测试环境（local 或 remote）')
    parser.add_argument('--server', help='自定义服务器地址（覆盖 env 配置）')
    args = parser.parse_args()

    # 加载配置
    config = load_config()

    # 确定使用的环境
    env = args.env or config.get('default_env', 'local')
    server_url = args.server or config[env]['server_url']
    api_key = config['api_key']
    cookies_file = config.get('cookies_file', 'cookies.json')

    print("╔═══════════════════════════════════════════════════════╗")
    print("║      XXX API 完整功能测试                              ║")
    print("╚═══════════════════════════════════════════════════════╝")
    print(f"\n🔗 测试环境: {env} ({config[env]['description']})")
    print(f"🔗 服务地址: {server_url}")

    # 加载 cookies
    print("\n📦 加载 Cookies...")
    cookies_json = load_cookies(cookies_file)
    cookies_str = json.dumps(cookies_json)
    print(f"✅ Cookies 加载成功 ({len(cookies_json)} 个)")

    # 运行测试
    results = []

    results.append(("基本功能", test_basic_functionality(server_url, api_key, cookies_str)))
    results.append(("参数变体", test_parameter_variations(server_url, api_key, cookies_str)))
    results.append(("边界条件", test_edge_cases(server_url, api_key, cookies_str)))
    results.append(("响应字段验证", test_response_fields(server_url, api_key, cookies_str)))

    # 汇总结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name:20s} {status}")
        if not passed:
            all_passed = False

    print("=" * 60)

    if all_passed:
        print("\n🎉 所有测试通过！")
        return 0
    else:
        print("\n⚠️  部分测试未通过，请检查输出详情。")
        return 1


if __name__ == '__main__':
    sys.exit(main())

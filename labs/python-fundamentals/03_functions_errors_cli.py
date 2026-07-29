"""
阅读路线：
1. 看 parse_args()，理解 argparse 如何接收命令行参数。
2. 看 validate_age()，理解异常处理和 raise。
3. 看 main()，理解命令行输入如何进入业务函数。

运行命令：
python3 labs/python-fundamentals/03_functions_errors_cli.py --question "孩子不写作业怎么办？" --age 8

学习目标：
- 把脚本变成可重复运行的命令行工具。
- 学会对输入做基础校验。
- 理解异常信息应该让人能定位问题。
"""

import argparse


def validate_age(age: int) -> int:
    """校验年龄范围。失败时抛出异常，让调用者知道原因。"""
    if age < 0:
        raise ValueError("年龄不能小于 0")
    if age > 18:
        raise ValueError("这个学习示例只处理 0 到 18 岁")
    return age


def build_short_advice(question: str, age: int) -> str:
    """一个最小业务函数：根据问题和年龄返回建议文本。"""
    valid_age = validate_age(age)
    return f"孩子年龄 {valid_age}，问题是：{question}。建议先共情，再拆成小步骤。"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Python 函数、异常和 CLI 学习脚本")
    parser.add_argument("--question", required=True, help="家长的问题")
    parser.add_argument("--age", type=int, required=True, help="孩子年龄")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        advice = build_short_advice(args.question, args.age)
    except ValueError as error:
        raise SystemExit(f"输入错误：{error}") from error

    print("=== Python 函数、异常、命令行参数 ===")
    print(advice)


if __name__ == "__main__":
    main()


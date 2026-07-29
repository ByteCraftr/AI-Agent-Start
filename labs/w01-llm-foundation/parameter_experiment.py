#!/usr/bin/env python3
"""
Compare how LLM generation parameters change Parenting Copilot outputs.

This script intentionally keeps two modes:
1. Default mode writes a Markdown table with request payloads and expected effects.
2. --call-api mode sends non-streaming scenarios to OpenAI and records real answers.

Why default to payload comparison?
- Some models do not support temperature or top_p.
- Real calls need OPENAI_API_KEY and network access.
- For learning, inspecting payload differences is the safest first step.
"""

from __future__ import annotations

# 这里全部使用 Python 标准库，不引入第三方依赖。
# 标准库可以理解成 Python 自带的 SDK，安装 Python 后就能直接 import。
import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from parenting_advisor import (
    DEFAULT_MODEL,
    SYSTEM_INSTRUCTIONS,
    call_openai,
    extract_output_text,
)


# 常量通常用全大写命名，表示“程序运行时一般不会修改它”。
# 这不是 Python 语法强制，只是工程约定。
DEFAULT_QUESTION = "孩子写作业总是拖延，我应该怎么引导？"

# Path 表示一个文件路径对象，比普通字符串更适合做路径拼接、取父目录、写文件。
# 小例子：
#   path = Path("a/b/result.md")
#   path.parent  # 得到 Path("a/b")
DEFAULT_OUTPUT = Path("labs/w01-llm-foundation/parameter_experiment_results.md")


# @dataclass 会自动帮我们生成 __init__ 等样板代码。
# frozen=True 表示 Scenario 创建后字段不能再被修改，适合表示“实验配置”。
#
# 不用 dataclass 时，大概需要手写：
#   class Scenario:
#       def __init__(self, name, max_output_tokens):
#           self.name = name
#           self.max_output_tokens = max_output_tokens
#
# 用 dataclass 后，只需要声明字段，Python 自动生成构造函数：
#   Scenario(name="stable_default", max_output_tokens=800)
@dataclass(frozen=True)
class Scenario:
    # 下面这些是类型注解：name 应该是 str，max_output_tokens 应该是 int。
    # 类型注解不会在运行时自动拦截错误，但能帮助 IDE、读代码的人和类型检查工具理解结构。
    name: str
    max_output_tokens: int

    # float | None 表示这个字段可以是 float，也可以是 None。
    # None 在 Python 里表示“没有值”，类似 Kotlin/Java 里的 null。
    temperature: float | None = None
    top_p: float | None = None

    # 字段后面的 = False / = "" 是默认值。
    # 创建 Scenario 时不传这些字段，就会使用默认值。
    stream: bool = False
    expected_effect: str = ""
    product_judgment: str = ""


# SCENARIOS 是一个列表，里面每个元素都是 Scenario 对象。
# 小例子：
#   numbers = [1, 2, 3]
#   users = [{"name": "Alice"}, {"name": "Bob"}]
# 这里是：
#   scenarios = [Scenario(...), Scenario(...)]
SCENARIOS = [
    Scenario(
        name="stable_default",
        max_output_tokens=800,
        expected_effect="不显式发送采样参数，优先观察模型默认行为。",
        product_judgment="适合作为教育建议的基线输出。",
    ),
    Scenario(
        name="short_budget",
        max_output_tokens=180,
        expected_effect="输出预算很小，建议更容易变短或被截断。",
        product_judgment="不适合复杂亲子问题，容易丢失边界和步骤。",
    ),
    Scenario(
        name="long_budget",
        max_output_tokens=1400,
        expected_effect="输出空间更充足，可以包含原因、步骤和注意事项。",
        product_judgment="适合需要解释和行动计划的问题，但要避免啰嗦。",
    ),
    Scenario(
        name="higher_temperature",
        max_output_tokens=800,
        temperature=0.9,
        expected_effect="随机性更强，措辞和建议角度可能更发散。",
        product_judgment="可用于头脑风暴，不适合默认教育建议。",
    ),
    Scenario(
        name="lower_top_p",
        max_output_tokens=800,
        top_p=0.5,
        expected_effect="候选词范围更窄，输出通常更保守。",
        product_judgment="可能更稳定，但也可能降低多样性和细腻度。",
    ),
    Scenario(
        name="streaming_shape",
        max_output_tokens=800,
        stream=True,
        expected_effect="返回方式变成流式，用户能更快看到首段内容。",
        product_judgment="改善等待体验，但不等于内容更可靠。",
    ),
]


def build_experiment_payload(
    question: str,
    model: str,
    scenario: Scenario,
) -> dict[str, Any]:
    """把一个实验场景转换成 OpenAI Responses API 的请求体。"""

    # dict[str, Any] 表示：这是一个字典，key 是字符串，value 可以是任意类型。
    # Any 用在这里是因为 payload 里既有字符串、数字、布尔值，也有嵌套列表和字典。
    payload: dict[str, Any] = {
        "model": model,
        "instructions": SYSTEM_INSTRUCTIONS,

        # input 是一个 list，里面放消息对象。
        # 现在只有一条 user 消息；未来多轮对话时，可以继续往这个列表追加历史消息。
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": question,
                    }
                ],
            }
        ],
        "max_output_tokens": scenario.max_output_tokens,
    }

    # 只有当字段不是 None 时才加入 payload。
    # 这样做的原因：有些模型不支持 temperature/top_p，默认发送反而会让 API 报错。
    if scenario.temperature is not None:
        payload["temperature"] = scenario.temperature
    if scenario.top_p is not None:
        payload["top_p"] = scenario.top_p

    # stream 是布尔值。只有 True 时才发送，表示请求流式返回。
    if scenario.stream:
        payload["stream"] = True

    return payload


def compact_payload(payload: dict[str, Any]) -> str:
    """只保留表格里最值得观察的参数，避免把完整 prompt 塞进结果表。"""

    interesting_keys = ["model", "temperature", "top_p", "max_output_tokens", "stream"]

    # 这是 dict comprehension，意思是“用一行 for 循环生成一个新 dict”。
    # 等价写法：
    #   compact = {}
    #   for key in interesting_keys:
    #       if key in payload:
    #           compact[key] = payload[key]
    compact = {key: payload[key] for key in interesting_keys if key in payload}

    # json.dumps 把 Python dict 转成 JSON 字符串。
    # ensure_ascii=False 表示中文不要变成 \uXXXX，方便人读。
    return json.dumps(compact, ensure_ascii=False)


def call_scenario(payload: dict[str, Any], api_key: str) -> tuple[str, str]:
    """调用一个实验场景，返回状态和输出文本。"""

    # tuple[str, str] 表示返回一个二元组，例如：
    #   ("ok", "模型回答")
    #   ("error", "错误原因")
    # 调用方可以写：status, output = call_scenario(...)

    if payload.get("stream"):
        # payload.get("stream") 会读取字典里的 stream。
        # 如果 key 不存在，get 默认返回 None，不会像 payload["stream"] 那样抛 KeyError。
        return "skipped", "streaming 场景本脚本只记录请求形态，不做 SSE 解析。"

    try:
        # try/except 用来处理可能失败的代码。
        # 这里网络、鉴权、模型参数不支持等问题都可能让 call_openai 抛 RuntimeError。
        response_body = call_openai(payload, api_key)
    except RuntimeError as exc:
        # exc 是捕获到的异常对象。str(exc) 会变成可读的错误信息。
        return "error", str(exc)

    answer = extract_output_text(response_body)
    if not answer:
        return "error", "API 调用成功，但没有提取到文本输出。"

    # Markdown 表格里直接放多行文本会破坏表格结构，所以把换行替换成 <br>。
    return "ok", answer.replace("\n", "<br>")


def render_markdown(
    question: str,
    model: str,
    rows: list[tuple[Scenario, dict[str, Any], str, str]],
) -> str:
    """把实验结果渲染成 Markdown 文本。"""

    # rows 的类型看起来长：list[tuple[Scenario, dict[str, Any], str, str]]
    # 拆开理解：
    # - list[...]：这是一个列表。
    # - tuple[...]：列表里的每一项是一个固定长度元组。
    # - Scenario：实验场景。
    # - dict[str, Any]：该场景的请求 payload。
    # - str, str：调用状态和输出内容。

    # lines 是字符串列表。先把每一行放进去，最后用 "\n".join(lines) 拼成完整文件。
    # 这样比不断做 markdown = markdown + "..." 更清晰，也更高效。
    lines = [
        "# W1-T3 模型参数对比实验",
        "",
        f"- 问题：{question}",
        f"- 模型：`{model}`",
        "",
        "## 对比表",
        "",
        "| 场景 | 参数 | 预期影响 | Parenting Copilot 判断 | 调用状态 | 输出摘录 |",
        "| --- | --- | --- | --- | --- | --- |",
    ]

    # for 循环逐行处理实验结果。
    # 因为 rows 里的每一项是四个元素的 tuple，所以可以直接拆成四个变量。
    for scenario, payload, status, output in rows:
        # 字符串切片 output[:360] 表示最多取前 360 个字符。
        output_preview = output[:360] + ("..." if len(output) > 360 else "")
        lines.append(
            # f-string 是 Python 常用的字符串模板写法。
            # 例如：name = "Tom"; f"hello {name}" 会得到 "hello Tom"。
            "| "
            f"`{scenario.name}` | "
            f"`{compact_payload(payload)}` | "
            f"{scenario.expected_effect} | "
            f"{scenario.product_judgment} | "
            f"{status} | "
            f"{output_preview} |"
        )

    # extend 会把另一个列表里的多行内容追加到 lines 末尾。
    # append 是追加一个元素，extend 是追加多个元素。
    lines.extend(
        [
            "",
            "## 初步结论",
            "",
            "- 教育类建议默认应该更稳定：低随机性、足够输出预算、明确安全边界。",
            "- `max_output_tokens` 太小会直接影响完整性，可能让建议缺少原因、步骤或风险提醒。",
            "- `temperature` 或 `top_p` 更适合探索不同表达和方案，不适合作为高风险场景的默认配置。",
            "- `streaming` 主要改善交互体验，不负责提升答案质量；内容可靠性仍要靠 prompt、结构化输出、校验和安全策略。",
            "",
            "## 复盘问题",
            "",
            "- 什么时候应该让模型更发散，什么时候应该更稳定？",
            "- 如果一个回答被截断，产品上应该如何提示或自动恢复？",
        ]
    )

    # join 把字符串列表合并成一个大字符串。
    # 最后的 + "\n" 是让生成的 Markdown 文件以换行结尾，这是文本文件的常见习惯。
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    """定义命令行参数，并把用户输入解析成 args 对象。"""

    # argparse 是 Python 标准库里的命令行解析工具。
    # 运行 python3 parameter_experiment.py --help 时，帮助文档就是它生成的。
    parser = argparse.ArgumentParser(
        description="Compare Parenting Copilot LLM parameter payloads and optional outputs."
    )

    # 位置参数：用户可以直接在命令后面写问题。
    # nargs="?" 表示这个参数可选；不写时使用 DEFAULT_QUESTION。
    parser.add_argument(
        "question",
        nargs="?",
        default=DEFAULT_QUESTION,
        help="Question used for every scenario.",
    )

    # 可选参数：以 --model 形式传入。
    # os.getenv 会读取环境变量；如果没有设置，就使用 DEFAULT_MODEL。
    parser.add_argument(
        "--model",
        default=os.getenv("PARENTING_ADVISOR_MODEL", DEFAULT_MODEL),
        help=f"Model name. Default: {DEFAULT_MODEL}",
    )

    # type=Path 表示 argparse 会把命令行字符串转换成 Path 对象。
    # 例如 --output result.md 最终会得到 Path("result.md")。
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Markdown result path. Default: {DEFAULT_OUTPUT}",
    )

    # action="store_true" 表示这是一个开关。
    # 命令里出现 --call-api，args.call_api 就是 True；不出现就是 False。
    parser.add_argument(
        "--call-api",
        action="store_true",
        help="Call OpenAI for non-streaming scenarios. Requires OPENAI_API_KEY.",
    )
    return parser.parse_args()


def main() -> int:
    """程序主入口：解析参数、执行实验、写入 Markdown。"""

    args = parse_args()

    # API key 只从环境变量读取，不写进代码。
    api_key = os.getenv("OPENAI_API_KEY")

    # 如果用户要求真实调用 API，但没有 key，就提前返回明确错误。
    # 返回 2 是命令行程序常见约定：参数或环境配置不正确。
    if args.call_api and not api_key:
        print(
            "Missing OPENAI_API_KEY. Run without --call-api for payload-only mode.",
            file=sys.stderr,
        )
        return 2

    # rows 用来收集每个实验场景的结果。
    # 这里没有提前写复杂类型注解，是为了让初学时更易读；Python 会根据 append 的内容运行。
    rows = []
    for scenario in SCENARIOS:
        payload = build_experiment_payload(args.question, args.model, scenario)

        # 如果传了 --call-api 并且 api_key 存在，就真实调用模型。
        # 否则只生成 payload，用来学习“不同参数如何进入请求体”。
        if args.call_api and api_key:
            status, output = call_scenario(payload, api_key)
        else:
            status = "payload-only"
            output = "未调用 API；本行用于观察请求参数形态。"

        # append 会把一个元素放到列表末尾。
        # 这里放进去的是一个四元组：(场景, payload, 状态, 输出)。
        rows.append((scenario, payload, status, output))

    markdown = render_markdown(args.question, args.model, rows)

    # args.output.parent 是输出文件所在目录。
    # mkdir(..., exist_ok=True) 表示：如果目录不存在就创建；如果已存在也不要报错。
    args.output.parent.mkdir(parents=True, exist_ok=True)

    # write_text 是 Path 对象提供的便捷写文件方法。
    # encoding="utf-8" 确保中文写入正常。
    args.output.write_text(markdown, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


# 这段是 Python 脚本的常见入口写法。
# 当文件被直接运行时，__name__ == "__main__" 成立，会执行 main()。
# 如果未来被另一个 Python 文件 import，这段不会自动执行。
if __name__ == "__main__":
    # raise SystemExit(main()) 会把 main() 的返回值变成命令行退出码。
    # 例如 main 返回 0 表示成功，返回 2 表示配置错误。
    raise SystemExit(main())

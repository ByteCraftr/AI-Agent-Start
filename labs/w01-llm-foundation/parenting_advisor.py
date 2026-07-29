#!/usr/bin/env python3
"""
Parenting Copilot 的第一个 LLM API 调用示例。

阅读路线：
1. 先看常量区：理解我们要调用哪个 API、默认用哪个模型、限制输出多长。
2. 再看 SYSTEM_INSTRUCTIONS：理解 system prompt 如何给模型设定角色和安全边界。
3. 再看 build_payload：理解“用户问题”如何被组装成 HTTP 请求体。
4. 再看 call_openai：理解 Python 如何真正发起一次 HTTP POST。
5. 再看 extract_output_text：理解如何从模型返回的 JSON 中取出文本回答。
6. 最后看 main：理解命令行程序的完整执行顺序。

注意：
- 不要把 API key 写进代码。API key 必须通过环境变量 OPENAI_API_KEY 读取。
- LLM API 虽然也是 HTTP API，但返回内容是模型生成的，不是普通后端接口的稳定 DTO。
- max_output_tokens 会影响回答是否完整；如果回答像被截断，可以适当调大。
- 有些模型不支持 temperature，所以本例默认不发送 temperature。
"""

from __future__ import annotations  # 允许在旧版本 Python 中使用更现代的类型注解写法。

import argparse  # 用来读取命令行参数，例如问题文本、模型名、输出长度。
import json  # 用来把 Python dict 转成 JSON，也用来解析 API 返回的 JSON。
import os  # 用来读取环境变量，例如 OPENAI_API_KEY。
import sys  # 用来向 stderr 打印错误信息，并返回不同退出码。
import urllib.error  # 用来捕获 HTTP 错误和网络错误。
import urllib.request  # Python 标准库里的 HTTP 请求工具。


API_URL = "https://api.openai.com/v1/responses"  # OpenAI Responses API 的 HTTP 地址。
DEFAULT_MODEL = "gpt-5-mini"  # 默认模型；注意：这个模型不支持 temperature 参数。
DEFAULT_MAX_OUTPUT_TOKENS = 1200  # 默认最多生成多少输出 token；太小可能导致回答不完整。


# system prompt：告诉模型它应该扮演什么角色、遵守什么边界。
# 注意：这是“产品安全边界”的第一层，不是最终安全系统。
SYSTEM_INSTRUCTIONS = """
You are Parenting Copilot, a parent-supervised education assistant.
Give practical, respectful, low-risk suggestions.
Do not diagnose children or replace teachers, doctors, or mental health professionals.
If the situation may involve harm, abuse, self-harm, or immediate danger, recommend seeking qualified help.
Answer in Simplified Chinese.
""".strip()


def build_payload(
    question: str,  # 用户输入的亲子教育问题。
    model: str,  # 要调用的模型名称。
    temperature: float | None,  # 可选随机性参数；None 表示不发送这个字段。
    max_output_tokens: int,  # 模型回答的最大长度预算。
) -> dict:
    """把程序里的参数组装成 OpenAI Responses API 需要的请求体。"""

    # payload 是最终会被 json.dumps 转成 JSON、发送给 OpenAI API 的请求体。
    payload = {
        # model 决定这次请求使用哪个模型能力。
        "model": model,
        # instructions 是 Responses API 里的高层指令，类似 system prompt。
        "instructions": SYSTEM_INSTRUCTIONS,
        # input 是用户输入。这里用列表结构，为未来多轮对话和多模态输入留空间。
        "input": [
            {
                # role=user 表示这条消息来自用户。
                "role": "user",
                # content 是消息内容列表；一个消息里可以包含文本、图片等不同内容块。
                "content": [
                    {
                        # type=input_text 表示这是文本输入。
                        "type": "input_text",
                        # text 才是真正的问题正文。
                        "text": question,
                    }
                ],
            }
        ],
        # max_output_tokens 限制模型最多输出多少 token。
        # 注意：如果你觉得回答“没有输出完整”，第一优先检查这里是否太小。
        "max_output_tokens": max_output_tokens,
    }

    # 注意：不是所有模型都支持 temperature。
    # 所以这里采用“只有用户显式传入才发送”的策略，避免默认请求报 400。
    if temperature is not None:
        # temperature 越高，回答越发散；教育建议类通常不建议一开始调太高。
        payload["temperature"] = temperature

    # 返回请求体，交给 call_openai 发送。
    return payload


def extract_output_text(response_body: dict) -> str:
    """从 OpenAI API 返回的 JSON 结构中提取最终文本。"""

    # 新版 Responses API 常见情况下会直接给 output_text。
    # 如果存在且是字符串，直接 strip 去掉前后空白后返回。
    if isinstance(response_body.get("output_text"), str):
        return response_body["output_text"].strip()

    # 有些返回结构会把内容放在 output -> content -> text 里。
    # text_parts 用来收集所有文本片段，最后拼成完整回答。
    text_parts: list[str] = []

    # 遍历 output 数组；每个 item 可能代表模型的一段输出或工具调用结果。
    for item in response_body.get("output", []):
        # 遍历每个 item 里的 content 数组。
        for content in item.get("content", []):
            # 只提取 type=output_text 的文本内容。
            if content.get("type") == "output_text" and content.get("text"):
                # 把这一段文本加入列表，后面统一拼接。
                text_parts.append(content["text"])

    # 用换行拼接多个文本片段，并去掉前后空白。
    return "\n".join(text_parts).strip()


def call_openai(payload: dict, api_key: str) -> dict:
    """发送 HTTP POST 请求到 OpenAI API，并返回解析后的 JSON。"""

    # OpenAI API 需要 JSON 请求体，所以先把 dict 转成 JSON 字符串。
    # encode("utf-8") 是因为 urllib 发送 body 时需要 bytes。
    body = json.dumps(payload).encode("utf-8")

    # Request 对象描述一次 HTTP 请求：URL、请求体、请求头、请求方法。
    request = urllib.request.Request(
        # 请求地址。
        API_URL,
        # 请求体，也就是上面编码后的 JSON。
        data=body,
        # 请求头：包含鉴权信息和内容类型。
        headers={
            # 注意：Bearer 后面是 API key；不要把 key 写进代码或提交到仓库。
            "Authorization": f"Bearer {api_key}",
            # 告诉服务器：这次请求体是 JSON。
            "Content-Type": "application/json",
        },
        # Responses API 用 POST，因为我们要提交一段输入并创建一次模型响应。
        method="POST",
    )

    # 网络请求可能失败，所以必须放进 try/except。
    try:
        # timeout=60 表示最多等待 60 秒，避免程序无限卡住。
        with urllib.request.urlopen(request, timeout=60) as response:
            # response.read() 读出 bytes，decode 转成字符串，json.loads 转成 dict。
            return json.loads(response.read().decode("utf-8"))

    # HTTPError 表示服务器返回了非 2xx 状态码，例如 400、401、429。
    except urllib.error.HTTPError as exc:
        # 读取服务器返回的错误体，里面通常包含具体错误原因。
        error_body = exc.read().decode("utf-8", errors="replace")
        # 抛出 RuntimeError，让 main 统一打印错误并返回退出码。
        raise RuntimeError(f"OpenAI API returned HTTP {exc.code}: {error_body}") from exc

    # URLError 表示网络层失败，例如断网、DNS 失败、连接超时。
    except urllib.error.URLError as exc:
        # 把网络错误包装成更容易理解的 RuntimeError。
        raise RuntimeError(f"Network error while calling OpenAI API: {exc.reason}") from exc

    # JSONDecodeError 表示服务器返回内容不是合法 JSON。
    except json.JSONDecodeError as exc:
        # 这类错误少见，但真实工程里要处理，避免程序崩得不清楚。
        raise RuntimeError("OpenAI API returned a non-JSON response.") from exc


def parse_args() -> argparse.Namespace:
    """定义并解析命令行参数。"""

    # ArgumentParser 负责生成 --help 文档，并把命令行输入解析成对象。
    parser = argparse.ArgumentParser(
        # description 会显示在 --help 输出里。
        description="Ask the first Parenting Copilot LLM question."
    )

    # 位置参数 question：用户可以直接在命令后面输入问题。
    parser.add_argument(
        # 参数名叫 question。
        "question",
        # nargs="?" 表示这个参数可选；不传时使用 default。
        nargs="?",
        # 默认问题，方便第一次运行时不用输入太多内容。
        default="孩子写作业总是拖延，我应该怎么引导？",
        # help 会显示在 --help 输出里。
        help="Parenting question to send to the model.",
    )

    # 可选参数 --model：允许用户切换模型。
    parser.add_argument(
        # 命令行写法，例如：--model gpt-5-mini。
        "--model",
        # 优先读 PARENTING_ADVISOR_MODEL 环境变量，否则使用 DEFAULT_MODEL。
        default=os.getenv("PARENTING_ADVISOR_MODEL", DEFAULT_MODEL),
        # help 中展示默认模型，方便学习时观察。
        help=f"Model name. Default: {DEFAULT_MODEL}",
    )

    # 可选参数 --temperature：控制随机性，但默认不发送。
    parser.add_argument(
        # 命令行写法，例如：--temperature 0.2。
        "--temperature",
        # 把命令行字符串转成 float。
        type=float,
        # 默认 None，表示请求体中不包含 temperature 字段。
        default=None,
        # 注意：gpt-5-mini 不支持 temperature，所以这个参数只给支持它的模型使用。
        help=(
            "Optional sampling randomness. Some models, including the default, "
            "do not support this parameter."
        ),
    )

    # 可选参数 --max-output-tokens：控制回答长度。
    parser.add_argument(
        # 命令行写法，例如：--max-output-tokens 1500。
        "--max-output-tokens",
        # 把命令行字符串转成 int。
        type=int,
        # 默认输出上限。
        default=DEFAULT_MAX_OUTPUT_TOKENS,
        # 注意：如果回答被截断，可以优先调大这个值。
        help=f"Response length budget. Default: {DEFAULT_MAX_OUTPUT_TOKENS}",
    )

    # 可选参数 --dry-run：只打印请求体，不真的调用 API。
    parser.add_argument(
        # 命令行写法：--dry-run。
        "--dry-run",
        # action="store_true" 表示只要出现这个参数，值就是 True。
        action="store_true",
        # dry-run 非常适合学习和调试 payload。
        help="Print the request payload without calling the API.",
    )

    # 解析命令行参数，并返回 argparse.Namespace 对象。
    return parser.parse_args()


def main() -> int:
    """程序入口：串起参数解析、请求构建、API 调用和输出打印。"""

    # 第一步：读取命令行参数。
    args = parse_args()

    # 第二步：根据命令行参数构建 OpenAI API 请求体。
    payload = build_payload(
        # 用户问题。
        question=args.question,
        # 使用哪个模型。
        model=args.model,
        # 可选 temperature；默认 None，不发送。
        temperature=args.temperature,
        # 输出 token 上限。
        max_output_tokens=args.max_output_tokens,
    )

    # 如果用户传了 --dry-run，只打印请求体，不调用 API。
    if args.dry_run:
        # ensure_ascii=False 保证中文正常显示，而不是变成 \uXXXX。
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        # 返回 0 表示程序正常结束。
        return 0

    # 第三步：从环境变量读取 API key。
    # 注意：这里是最重要的安全点之一，不要改成硬编码字符串。
    api_key = os.getenv("OPENAI_API_KEY")

    # 如果没有设置 OPENAI_API_KEY，就给出明确提示。
    if not api_key:
        # 错误信息打印到 stderr，方便和正常输出区分。
        print(
            "Missing OPENAI_API_KEY. Set it before running, for example:\n"
            "export OPENAI_API_KEY='your_api_key_here'",
            file=sys.stderr,
        )
        # 返回 2 表示参数或环境配置错误。
        return 2

    # 第四步：真正调用 OpenAI API，并提取文本回答。
    try:
        # 发送 HTTP 请求，拿到完整 JSON 响应。
        response_body = call_openai(payload, api_key)
        # 从 JSON 响应中提取最终文本。
        answer = extract_output_text(response_body)

    # RuntimeError 是我们在 call_openai 里包装过的可读错误。
    except RuntimeError as exc:
        # 把错误打印到 stderr。
        print(str(exc), file=sys.stderr)
        # 返回 1 表示调用失败。
        return 1

    # 如果 API 调用成功，但没有提取到文本，就打印完整 JSON 方便调试。
    if not answer:
        # 注意：这通常意味着响应结构和我们的解析逻辑不匹配。
        print("The API call succeeded, but no text answer was found.", file=sys.stderr)
        # 打印完整响应，方便下一步调整 extract_output_text。
        print(json.dumps(response_body, ensure_ascii=False, indent=2))
        # 返回 1，因为对这个命令行工具来说，没有文本就是失败。
        return 1

    # 第五步：把模型回答打印到标准输出。
    print(answer)

    # 返回 0 表示成功。
    return 0


# Python 文件被直接运行时，__name__ 会等于 "__main__"。
if __name__ == "__main__":
    # raise SystemExit(main()) 会把 main 的返回码交给操作系统。
    raise SystemExit(main())

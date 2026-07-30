#!/usr/bin/env python3
"""
Parenting Copilot prompt layering experiment.

阅读路线：
1. 先看 PromptMessage：理解一次 LLM 调用里的 message 结构。
2. 再看 build_system_prompt：理解稳定身份和安全边界放在哪里。
3. 再看 build_task_prompt：理解每次用户问题变化时，变化的部分是什么。
4. 再看 build_format_prompt：理解昨天的 ParentingAdvice schema 如何进入 prompt。
5. 最后运行 main：观察两个不同问题下，哪些 prompt 稳定，哪些 prompt 变化。

运行：
    python3 labs/w02-structured-output/prompt_templates.py

今天先不用真实 API。原因是 W2-T2 的核心是 prompt 分层的工程边界：
system prompt 和 format prompt 应该稳定，task prompt 才跟随用户输入变化。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from parenting_advice_schema import build_json_schema


@dataclass(frozen=True)
class PromptMessage:
    """一次 LLM 调用中的单条 message。

    dataclass 用来表达稳定的数据结构，类似 Android/Kotlin 里的 data class。
    role 表示这条消息的职责，例如 system 或 user。
    content 是真正给模型阅读的文本。
    """

    role: str
    content: str

    def to_api_dict(self) -> dict[str, str]:
        """转换成常见 LLM API 使用的 dict 形状。"""

        return {
            "role": self.role,
            "content": self.content,
        }


def build_system_prompt() -> str:
    """构建稳定的 Agent 身份、能力边界和安全边界。

    system prompt 不应该跟随每个用户问题频繁变化。
    它类似项目里的 AGENTS.md：定义这个 Agent 长期遵守的协作协议。
    """

    return """You are Parenting Copilot, a parent-supervised educational support agent.

Your job:
- Help parents observe, communicate, and choose low-risk next actions.
- Give practical parenting suggestions, not absolute judgments.
- Keep the child respected and avoid blame-based advice.

Safety boundaries:
- Do not diagnose children or parents.
- Do not replace teachers, doctors, therapists, or emergency services.
- If the situation suggests self-harm, abuse, severe violence, or urgent danger,
  recommend immediate professional or emergency help.
- When information is insufficient, ask a clarifying question before giving strong advice."""


def build_task_prompt(
    user_question: str,
    child_age: int | None,
    context: str,
) -> str:
    """构建本次请求的任务 prompt。

    这里放会随用户输入变化的信息：问题、孩子年龄、场景和家长期望。
    特殊用法：int | None 表示 child_age 可以是整数，也可以为空。
    这能表达真实产品里“家长没有提供年龄”的情况。
    """

    age_text = "unknown" if child_age is None else str(child_age)

    return f"""User question:
{user_question}

Known context:
- child_age: {age_text}
- situation: {context}

Task:
Analyze the parenting situation, decide the advice category and risk level,
then produce one structured ParentingAdvice response."""


def build_format_prompt(schema: dict[str, Any]) -> str:
    """构建稳定的输出格式 prompt。

    format prompt 连接昨天的结构化输出实验：
    Python schema -> JSON Schema -> 模型输出要求 -> 本地校验。
    """

    schema_text = json.dumps(schema, ensure_ascii=False, indent=2)

    return f"""Return only valid JSON that matches this JSON Schema.
Do not include markdown fences, commentary, or extra keys.

JSON Schema:
{schema_text}"""


def build_prompt_messages(
    user_question: str,
    child_age: int | None,
    context: str,
) -> list[PromptMessage]:
    """组合一次 LLM 调用需要的 messages。

    工程边界：
    - system message 承载稳定行为边界。
    - user message 承载本次任务和输出格式。
    - 输出格式也可以放到独立 developer/tool 指令里；这里先用最小通用形态。
    """

    schema = build_json_schema()
    task_prompt = build_task_prompt(user_question, child_age, context)
    format_prompt = build_format_prompt(schema)

    return [
        PromptMessage(role="system", content=build_system_prompt()),
        PromptMessage(role="user", content=f"{task_prompt}\n\n{format_prompt}"),
    ]


def print_prompt_case(
    case_name: str,
    user_question: str,
    child_age: int | None,
    context: str,
) -> list[PromptMessage]:
    """打印一个样例的分层 prompt，方便命令行观察。"""

    messages = build_prompt_messages(user_question, child_age, context)

    print(f"\n=== {case_name} ===")
    for index, message in enumerate(messages, start=1):
        print(f"\n--- message {index}: {message.role} ---")
        print(message.content)

    return messages


def main() -> int:
    """命令行入口：对比两个问题下 prompt 的稳定部分和变化部分。"""

    schema = build_json_schema()
    format_prompt = build_format_prompt(schema)

    first_messages = print_prompt_case(
        case_name="homework delay",
        user_question="孩子写作业总拖拉，我一催他就哭，怎么办？",
        child_age=8,
        context="三年级，最近两周明显拖延，家长希望减少冲突。",
    )
    second_messages = print_prompt_case(
        case_name="school conflict",
        user_question="孩子说不想去学校，说同学总笑他，我应该怎么问？",
        child_age=10,
        context="五年级，最近三天抗拒上学，家长还不了解具体发生了什么。",
    )

    print("\n=== stability check ===")
    first_task_prompt = build_task_prompt(
        "孩子写作业总拖拉，我一催他就哭，怎么办？",
        8,
        "三年级，最近两周明显拖延，家长希望减少冲突。",
    )
    second_task_prompt = build_task_prompt(
        "孩子说不想去学校，说同学总笑他，我应该怎么问？",
        10,
        "五年级，最近三天抗拒上学，家长还不了解具体发生了什么。",
    )

    print(f"system prompt stable: {first_messages[0].content == second_messages[0].content}")
    print(f"task prompt changed: {first_task_prompt != second_task_prompt}")
    print(
        "format prompt stable: "
        f"{format_prompt == build_format_prompt(schema)}"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

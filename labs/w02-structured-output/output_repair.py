#!/usr/bin/env python3
"""
Parenting Copilot output validation and repair experiment.

阅读路线：
1. 先看 RepairResult：理解一次输出恢复流程需要返回什么状态。
2. 再看 extract_json_candidate：理解哪些“包装问题”可以由代码修复。
3. 再看 parse_and_validate_advice：理解 parse 和 validate 是两层不同失败。
4. 最后运行 main：观察合法输出、可修复输出、不可修复输出的区别。

运行：
    python3 labs/w02-structured-output/output_repair.py

今天不用真实 API。原因是 W2-T3 的核心是可靠性控制流：
LLM 可能输出坏内容，Agent 必须先检测、有限修复，失败时安全降级。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from parenting_advice_schema import ParentingAdvice, validate_parenting_advice


@dataclass(frozen=True)
class RepairResult:
    """一次模型输出处理后的结果。

    dataclass 让成功、失败、是否尝试修复这些状态被明确表达出来。
    真实产品中，UI、日志、评估系统都可以消费这类稳定结果。
    """

    success: bool
    advice: ParentingAdvice | None
    error_message: str | None
    fallback_message: str | None
    repair_attempted: bool


def build_fallback_message() -> str:
    """构建给家长看的安全降级文案。

    fallback 不依赖模型的业务判断，所以内容要保守、低风险、可执行。
    它不能假装已经生成了可靠建议，只能引导用户补充信息或寻求帮助。
    """

    return (
        "这次没有生成可靠的结构化建议。请先补充孩子年龄、事情持续多久、"
        "最近一次发生的具体场景，以及是否存在自伤、暴力、被欺负或紧急危险。"
        "如果已经存在紧急危险，请优先联系当地紧急服务、学校老师、医生或心理健康专业人士。"
    )


def extract_json_candidate(raw_text: str) -> tuple[str, bool]:
    """从模型原始文本中提取可能的 JSON object。

    这里故意只修“包装问题”：
    - 去掉 markdown ```json 代码块。
    - 去掉 JSON 前后的解释性文字。

    不在这里猜业务字段，例如缺失 risk_level 时自动填 low。
    对 Parenting Copilot 来说，业务判断错误必须暴露出来。
    """

    text = raw_text.strip()

    if text.startswith("```"):
        lines = text.splitlines()
        if lines and lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        return "\n".join(lines).strip(), True

    first_brace = text.find("{")
    last_brace = text.rfind("}")
    if first_brace != -1 and last_brace != -1 and first_brace < last_brace:
        candidate = text[first_brace : last_brace + 1]
        return candidate, candidate != text

    return text, False


def parse_json_object(json_text: str) -> dict[str, Any]:
    """把文本解析成 JSON object。

    特殊用法：json.loads 只说明文本是合法 JSON，不说明它符合业务合同。
    所以后面还必须调用 validate_parenting_advice。
    """

    try:
        parsed = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON text: {exc.msg}.") from exc

    if not isinstance(parsed, dict):
        raise ValueError("parsed JSON must be an object.")

    return parsed


def parse_and_validate_advice(raw_text: str) -> RepairResult:
    """执行 parse -> validate -> limited repair -> fallback 的最小流程。"""

    try:
        parsed = parse_json_object(raw_text)
        advice = validate_parenting_advice(parsed)
    except ValueError as first_error:
        repaired_text, repair_attempted = extract_json_candidate(raw_text)
        if not repair_attempted:
            return RepairResult(
                success=False,
                advice=None,
                error_message=str(first_error),
                fallback_message=build_fallback_message(),
                repair_attempted=False,
            )

        try:
            repaired_parsed = parse_json_object(repaired_text)
            repaired_advice = validate_parenting_advice(repaired_parsed)
        except ValueError as repair_error:
            return RepairResult(
                success=False,
                advice=None,
                error_message=str(repair_error),
                fallback_message=build_fallback_message(),
                repair_attempted=True,
            )

        return RepairResult(
            success=True,
            advice=repaired_advice,
            error_message=None,
            fallback_message=None,
            repair_attempted=True,
        )

    return RepairResult(
        success=True,
        advice=advice,
        error_message=None,
        fallback_message=None,
        repair_attempted=False,
    )


VALID_JSON_TEXT = """
{
  "category": "learning",
  "risk_level": "low",
  "summary": "孩子写作业拖延，先把任务拆小并降低催促冲突。",
  "possible_reasons": [
    "任务太大，孩子不知道从哪里开始。",
    "家长催促让孩子把作业和冲突绑定在一起。"
  ],
  "action_steps": [
    "先和孩子一起选出最容易开始的一小题。",
    "用 15 分钟一段的方式完成，并在结束后复盘卡点。"
  ],
  "communication_script": "我先不催你，我们一起看看第一步可以从哪里开始。",
  "professional_boundary": "如果拖延伴随持续焦虑、睡眠问题或强烈亲子冲突，建议联系老师或专业人士。"
}
"""


MARKDOWN_WRAPPED_JSON_TEXT = f"""
```json
{VALID_JSON_TEXT.strip()}
```
"""


EXPLANATION_WRAPPED_JSON_TEXT = f"""
下面是结构化建议：

{VALID_JSON_TEXT.strip()}

希望这能帮助你。
"""


INVALID_JSON_TEXT = """
{
  "category": "learning",
  "risk_level": "low",
  "summary": "少了一个逗号会导致 JSON 解析失败"
  "possible_reasons": ["这里前面缺少逗号"]
}
"""


BUSINESS_INVALID_JSON_TEXT = """
{
  "category": "homework",
  "risk_level": "low",
  "summary": "这个 JSON 格式合法，但 category 不符合业务枚举。",
  "possible_reasons": ["模型用了 schema 外的类别。"],
  "action_steps": ["不要自动猜成 learning。"],
  "communication_script": "我们先确认这属于哪类问题。",
  "professional_boundary": "边界字段不能空。"
}
"""


def print_case_result(case_name: str, raw_text: str) -> None:
    """打印一个样例的输出处理结果，便于命令行观察。"""

    result = parse_and_validate_advice(raw_text)

    print(f"\n=== {case_name} ===")
    print(f"success: {result.success}")
    print(f"repair_attempted: {result.repair_attempted}")

    if result.advice is not None:
        print(json.dumps(result.advice.to_json_dict(), ensure_ascii=False, indent=2))
        return

    print(f"error: {result.error_message}")
    print(f"fallback: {result.fallback_message}")


def main() -> int:
    """命令行入口：演示 5 类模型输出的恢复结果。"""

    print_case_result("valid JSON", VALID_JSON_TEXT)
    print_case_result("markdown wrapped JSON", MARKDOWN_WRAPPED_JSON_TEXT)
    print_case_result("explanation wrapped JSON", EXPLANATION_WRAPPED_JSON_TEXT)
    print_case_result("invalid JSON syntax", INVALID_JSON_TEXT)
    print_case_result("business invalid JSON", BUSINESS_INVALID_JSON_TEXT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

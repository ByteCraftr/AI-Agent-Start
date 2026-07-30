#!/usr/bin/env python3
"""
Parenting Copilot structured output schema experiment.

阅读路线：
1. 先看 RiskLevel 和 AdviceCategory：理解枚举如何限制字段只能取固定值。
2. 再看 ParentingAdvice：理解 Agent 最终回答的结构化契约。
3. 再看 validate_parenting_advice：理解“模型输出”如何被本地代码校验。
4. 最后运行 main：观察合法样例通过、非法样例失败。

运行：
    python3 labs/w02-structured-output/parenting_advice_schema.py

今天先不用真实 API。原因是 W2-T1 的核心不是“调用模型”，而是先定义：
模型必须输出什么结构，代码如何判断它是否可信。
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, TypeVar


class RiskLevel(str, Enum):
    """风险等级枚举。

    Enum 用来表达“只能从固定选项里选一个”。
    str, Enum 组合的好处：枚举值本身也是字符串，后续更容易转成 JSON。

    对应 Pydantic 思路：
    - Pydantic 也常用 Enum 限制字段取值。
    - 如果模型输出 "high_risk"，校验通过。
    - 如果模型输出 "very_bad"，校验失败。
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    EMERGENCY = "emergency"


class AdviceCategory(str, Enum):
    """建议类别枚举，用来约束 Parenting Copilot 当前处理的问题类型。"""

    LEARNING = "learning"
    EMOTION = "emotion"
    COMMUNICATION = "communication"
    BEHAVIOR = "behavior"
    SCHOOL = "school"
    SAFETY = "safety"


EnumT = TypeVar("EnumT", bound=Enum)


@dataclass(frozen=True)
class ParentingAdvice:
    """Parenting Copilot 的结构化输出契约。

    dataclass 会自动生成 __init__，让这个类更像一个稳定 DTO。
    frozen=True 表示对象创建后不能被随便改字段，适合表示一次校验后的结果。

    这里先用标准库实现，是因为当前环境没有安装 Pydantic。
    后续切换到 Pydantic 时，字段设计可以基本保留，只是把手写校验交给库。
    """

    category: AdviceCategory
    risk_level: RiskLevel
    summary: str
    possible_reasons: list[str]
    action_steps: list[str]
    communication_script: str
    professional_boundary: str

    def to_json_dict(self) -> dict[str, Any]:
        """转换成可 JSON 序列化的 dict。

        特殊用法：Enum 不能直接假设所有 JSON 工具都能处理。
        所以这里显式使用 .value，把 RiskLevel.LOW 转成字符串 "low"。
        """

        return {
            "category": self.category.value,
            "risk_level": self.risk_level.value,
            "summary": self.summary,
            "possible_reasons": self.possible_reasons,
            "action_steps": self.action_steps,
            "communication_script": self.communication_script,
            "professional_boundary": self.professional_boundary,
        }


def require_non_empty_text(data: dict[str, Any], field_name: str) -> str:
    """读取并校验一个必填字符串字段。"""

    value = data.get(field_name)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"`{field_name}` must be a non-empty string.")
    return value.strip()


def require_non_empty_text_list(data: dict[str, Any], field_name: str) -> list[str]:
    """读取并校验一个必填字符串列表字段。"""

    value = data.get(field_name)
    if not isinstance(value, list) or not value:
        raise ValueError(f"`{field_name}` must be a non-empty list.")

    cleaned_items: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(
                f"`{field_name}[{index}]` must be a non-empty string."
            )
        cleaned_items.append(item.strip())

    return cleaned_items


def validate_enum(enum_type: type[EnumT], raw_value: Any, field_name: str) -> EnumT:
    """把模型输出的字符串校验成 Enum。

    type[Enum] 是一个稍难的类型注解：
    - Enum 表示某个枚举值，例如 RiskLevel.LOW。
    - type[Enum] 表示某个枚举类，例如 RiskLevel 这个类本身。

    这让同一个函数既能校验 RiskLevel，也能校验 AdviceCategory。
    """

    if not isinstance(raw_value, str):
        raise ValueError(f"`{field_name}` must be a string.")

    try:
        return enum_type(raw_value)
    except ValueError as exc:
        allowed_values = ", ".join(item.value for item in enum_type)
        raise ValueError(
            f"`{field_name}` must be one of: {allowed_values}. Got: {raw_value!r}."
        ) from exc


def validate_object_shape(raw_output: Any) -> dict[str, Any]:
    """校验模型输出的顶层 JSON 形状。

    对应 JSON Schema 里的两个字段：
    - "type": "object"：模型输出必须是 JSON object，对应 Python 的 dict。
    - "additionalProperties": False：不能出现 schema 没定义的额外字段。

    这是一个重要工程点：schema 只是声明契约，本地校验函数才真正执行契约。
    """

    if not isinstance(raw_output, dict):
        raise ValueError("model output must be a JSON object.")

    schema = build_json_schema()
    allowed_fields = set(schema["properties"])
    extra_fields = set(raw_output) - allowed_fields
    if extra_fields:
        raise ValueError(f"unexpected fields: {sorted(extra_fields)}.")

    return raw_output


def build_json_schema() -> dict[str, Any]:
    """生成给模型和工程系统共用的 JSON Schema。

    JSON Schema 是跨语言的输出契约：
    - Prompt 可以把它交给模型，要求模型按这个结构回答。
    - 后端可以用它校验模型输出。
    - Android 或 Web 也能根据同一份字段设计生成 UI state。

    Pydantic 通常能从模型类自动生成 JSON Schema。
    当前环境没有安装 Pydantic，所以这里先手写最小版本，方便理解底层结构。
    """

    return {
        # 顶层必须是 JSON object，也就是 Python 里的 dict。
        # 这能拒绝模型只返回一段字符串、数组或数字。
        "type": "object",
        # 不允许输出 schema 没声明的字段。
        # 这能避免模型临时添加 confidence、diagnosis 等业务系统不认识的字段。
        "additionalProperties": False,
        "required": [
            "category",
            "risk_level",
            "summary",
            "possible_reasons",
            "action_steps",
            "communication_script",
            "professional_boundary",
        ],
        "properties": {
            "category": {
                "type": "string",
                "enum": [item.value for item in AdviceCategory],
            },
            "risk_level": {
                "type": "string",
                "enum": [item.value for item in RiskLevel],
            },
            "summary": {"type": "string", "minLength": 1},
            "possible_reasons": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string", "minLength": 1},
            },
            "action_steps": {
                "type": "array",
                "minItems": 1,
                "items": {"type": "string", "minLength": 1},
            },
            "communication_script": {"type": "string", "minLength": 1},
            "professional_boundary": {"type": "string", "minLength": 1},
        },
    }


def validate_parenting_advice(raw_output: Any) -> ParentingAdvice:
    """把一个模型输出 dict 校验成 ParentingAdvice。

    在真实 Agent 里，这个函数站在 LLM 和业务系统之间：
    - LLM 负责生成候选答案。
    - 校验器负责判断这个答案能不能进入后续流程。
    - 业务系统只消费校验通过的 ParentingAdvice。
    """

    data = validate_object_shape(raw_output)

    category = validate_enum(
        AdviceCategory,
        data.get("category"),
        "category",
    )
    risk_level = validate_enum(
        RiskLevel,
        data.get("risk_level"),
        "risk_level",
    )

    return ParentingAdvice(
        category=category,
        risk_level=risk_level,
        summary=require_non_empty_text(data, "summary"),
        possible_reasons=require_non_empty_text_list(data, "possible_reasons"),
        action_steps=require_non_empty_text_list(data, "action_steps"),
        communication_script=require_non_empty_text(data, "communication_script"),
        professional_boundary=require_non_empty_text(
            data,
            "professional_boundary",
        ),
    )


VALID_MODEL_OUTPUT: dict[str, Any] = {
    "category": "learning",
    "risk_level": "low",
    "summary": "孩子写作业拖延，先把它当成执行功能和任务拆分问题处理。",
    "possible_reasons": [
        "任务太大，孩子不知道从哪里开始。",
        "写作业过程缺少可见的阶段反馈。",
    ],
    "action_steps": [
        "把作业拆成 15 分钟一段的小任务。",
        "先和孩子确认今天最难的一项，再从最小步骤开始。",
        "结束后复盘哪个步骤最卡，而不是只评价快慢。",
    ],
    "communication_script": "我看到你还没开始，我们先不急着批评。你觉得第一步最难的是哪一块？",
    "professional_boundary": "如果长期伴随明显焦虑、睡眠问题或强烈冲突，建议寻求老师或专业人士帮助。",
}


INVALID_MODEL_OUTPUT: dict[str, Any] = {
    "category": "homework",  # 非法：不在 AdviceCategory 允许值里。
    "risk_level": "low",
    "summary": "",
    "possible_reasons": [],
    "action_steps": ["直接严格惩罚孩子"],
    "communication_script": "快点写。",
    "professional_boundary": "无",
}


EXTRA_FIELD_MODEL_OUTPUT: dict[str, Any] = {
    **VALID_MODEL_OUTPUT,
    "diagnosis": "孩子可能有注意力问题",  # 非法：schema 没有声明这个字段。
}


NON_OBJECT_MODEL_OUTPUT = [
    "孩子写作业拖延，建议先沟通。"
]  # 非法：顶层不是 JSON object。


def print_validation_result(name: str, raw_output: Any) -> None:
    """打印一个样例的校验结果，便于命令行观察。"""

    print(f"\n=== {name} ===")
    try:
        advice = validate_parenting_advice(raw_output)
    except ValueError as exc:
        print("validation: failed")
        print(f"reason: {exc}")
        return

    print("validation: passed")
    print(json.dumps(advice.to_json_dict(), ensure_ascii=False, indent=2))


def main() -> int:
    """命令行入口：分别校验一个合法输出和一个非法输出。"""

    print("=== json schema fields ===")
    schema = build_json_schema()
    print(", ".join(schema["required"]))

    print_validation_result("valid model output", VALID_MODEL_OUTPUT)
    print_validation_result("invalid model output", INVALID_MODEL_OUTPUT)
    print_validation_result("extra field model output", EXTRA_FIELD_MODEL_OUTPUT)
    print_validation_result("non-object model output", NON_OBJECT_MODEL_OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Parenting Copilot context sufficiency experiment.

阅读路线：
1. 先看 RequiredSlot：理解 Agent 在回答前需要哪些关键信息。
2. 再看 ContextSufficiencyResult：理解“信息是否足够”也是稳定输出合同。
3. 再看 ContextSufficiencyChecker.check：理解如何从当前输入和已有状态里判断缺口。
4. 最后运行 main：观察信息不足时如何追问，信息充分时如何放行。

运行：
    python3 labs/w03-agent-core/context_sufficiency.py

今天先不用真实 LLM。原因是 W3-T2 的核心不是生成更漂亮的回答，
而是让 Agent 学会在上下文不足时先停下来追问。
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum


class RequiredSlot(str, Enum):
    """Agent 在生成亲子建议前需要确认的关键信息槽位。

    Slot filling 不是保存完整聊天记录，而是把对决策有用的信息整理成字段。
    """

    CHILD_AGE = "child_age"
    DURATION = "duration"
    SITUATION = "situation"
    PARENT_GOAL = "parent_goal"


class NextStep(str, Enum):
    """上下文检查之后，Agent 应该进入的下一步。

    这里把下一步限制成枚举，避免后续 Agent Loop 靠猜字符串决定流程。
    """

    ASK_CLARIFYING_QUESTION = "ask_clarifying_question"
    GENERATE_ADVICE = "generate_advice"
    SAFETY_RESPONSE = "safety_response"


@dataclass(frozen=True)
class SlotCheckResult:
    """单个槽位的检查结果。

    value 是最小实验里的“已识别证据”，不是最终要展示给用户的正式资料。
    """

    slot: RequiredSlot
    is_filled: bool
    value: str | None
    reason: str


@dataclass(frozen=True)
class ContextSufficiencyResult:
    """信息充分性检查的稳定输出合同。

    Agent Loop 后续只需要读这个结果，就能知道该追问、该回答，还是该走安全响应。
    """

    is_sufficient: bool
    next_step: NextStep
    missing_slots: tuple[RequiredSlot, ...]
    clarifying_question: str | None
    slot_results: tuple[SlotCheckResult, ...]
    reason: str


@dataclass(frozen=True)
class EvaluationCase:
    """用于验收最小实验的样例。

    existing_context 模拟多轮状态：上一轮已经收集到的信息可以继续使用。
    """

    user_input: str
    expected_next_step: NextStep
    expected_missing_slots: tuple[RequiredSlot, ...]
    existing_context: dict[RequiredSlot, str] | None = None


class ContextSufficiencyChecker:
    """判断当前信息是否足够进入建议生成。

    这个类的边界很窄：
    - 它不生成完整建议。
    - 它不做意图分类。
    - 它只判断上下文够不够，并生成最多两个追问。
    """

    def check(
        self,
        user_input: str,
        existing_context: dict[RequiredSlot, str] | None = None,
    ) -> ContextSufficiencyResult:
        """检查用户输入和已有多轮状态是否已经补齐关键槽位。

        existing_context 是 W3-T2 的多轮状态最小模型。
        第一轮缺的信息，第二轮用户补充后，可以放在这里继续参与判断。
        """

        if contains_high_risk_signal(user_input):
            return ContextSufficiencyResult(
                is_sufficient=False,
                next_step=NextStep.SAFETY_RESPONSE,
                missing_slots=(),
                clarifying_question=None,
                slot_results=(),
                reason="输入包含自伤、严重暴力或紧急危险信号，优先进入安全响应。",
            )

        context = existing_context or {}
        slot_results = (
            self._check_child_age(user_input, context),
            self._check_duration(user_input, context),
            self._check_situation(user_input, context),
            self._check_parent_goal(user_input, context),
        )
        missing_slots = tuple(
            result.slot for result in slot_results if not result.is_filled
        )

        if not missing_slots:
            return ContextSufficiencyResult(
                is_sufficient=True,
                next_step=NextStep.GENERATE_ADVICE,
                missing_slots=(),
                clarifying_question=None,
                slot_results=slot_results,
                reason="年龄、持续时间、具体场景和家长目标都已具备，可以进入建议生成。",
            )

        return ContextSufficiencyResult(
            is_sufficient=False,
            next_step=NextStep.ASK_CLARIFYING_QUESTION,
            missing_slots=missing_slots,
            clarifying_question=build_clarifying_question(missing_slots),
            slot_results=slot_results,
            reason="当前上下文不足，先用最少追问补齐会改变建议方向的信息。",
        )

    def _check_child_age(
        self,
        user_input: str,
        context: dict[RequiredSlot, str],
    ) -> SlotCheckResult:
        if RequiredSlot.CHILD_AGE in context:
            return filled_from_context(RequiredSlot.CHILD_AGE, context)

        match = re.search(r"\d+\s*(岁|年级)|[一二三四五六七八九十]+年级", user_input)
        if match:
            return SlotCheckResult(
                slot=RequiredSlot.CHILD_AGE,
                is_filled=True,
                value=match.group(0),
                reason="输入中出现年龄或年级信息。",
            )

        return missing(RequiredSlot.CHILD_AGE, "缺少孩子年龄或年级。")

    def _check_duration(
        self,
        user_input: str,
        context: dict[RequiredSlot, str],
    ) -> SlotCheckResult:
        if RequiredSlot.DURATION in context:
            return filled_from_context(RequiredSlot.DURATION, context)

        duration_words = (
            "最近",
            "持续",
            "已经",
            "每天",
            "一周",
            "两周",
            "三周",
            "一个月",
            "半年",
            "一年",
        )
        if contains_any_keyword(user_input, duration_words):
            return SlotCheckResult(
                slot=RequiredSlot.DURATION,
                is_filled=True,
                value=first_matching_keyword(user_input, duration_words),
                reason="输入中出现持续时间或频率信息。",
            )

        return missing(RequiredSlot.DURATION, "缺少问题持续多久或发生频率。")

    def _check_situation(
        self,
        user_input: str,
        context: dict[RequiredSlot, str],
    ) -> SlotCheckResult:
        if RequiredSlot.SITUATION in context:
            return filled_from_context(RequiredSlot.SITUATION, context)

        situation_words = (
            "写作业",
            "作业",
            "考试",
            "学校",
            "同学",
            "老师",
            "刷手机",
            "游戏",
            "睡觉",
            "吃饭",
            "顶嘴",
            "吵架",
            "哭",
            "焦虑",
            "发脾气",
        )
        if contains_any_keyword(user_input, situation_words):
            return SlotCheckResult(
                slot=RequiredSlot.SITUATION,
                is_filled=True,
                value=first_matching_keyword(user_input, situation_words),
                reason="输入中出现具体问题场景。",
            )

        return missing(RequiredSlot.SITUATION, "缺少具体发生场景。")

    def _check_parent_goal(
        self,
        user_input: str,
        context: dict[RequiredSlot, str],
    ) -> SlotCheckResult:
        if RequiredSlot.PARENT_GOAL in context:
            return filled_from_context(RequiredSlot.PARENT_GOAL, context)

        goal_words = (
            "我想",
            "我希望",
            "希望",
            "目标",
            "减少",
            "改善",
            "让他",
            "让她",
            "愿意",
            "不要",
        )
        if contains_any_keyword(user_input, goal_words):
            return SlotCheckResult(
                slot=RequiredSlot.PARENT_GOAL,
                is_filled=True,
                value=first_matching_keyword(user_input, goal_words),
                reason="输入中出现家长期望或改变目标。",
            )

        return missing(RequiredSlot.PARENT_GOAL, "缺少家长希望改变什么。")


def contains_high_risk_signal(text: str) -> bool:
    """高风险信号优先于普通追问，避免安全问题被 slot filling 拖住。"""

    high_risk_words = (
        "自伤",
        "不想活",
        "轻生",
        "打到流血",
        "严重霸凌",
        "被威胁",
        "离家出走",
        "紧急",
    )
    return contains_any_keyword(text, high_risk_words)


def contains_any_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    """判断文本是否包含任一关键词。"""

    return any(keyword in text for keyword in keywords)


def first_matching_keyword(text: str, keywords: tuple[str, ...]) -> str | None:
    """返回第一个命中的关键词，方便打印最小证据。"""

    for keyword in keywords:
        if keyword in text:
            return keyword
    return None


def filled_from_context(
    slot: RequiredSlot,
    context: dict[RequiredSlot, str],
) -> SlotCheckResult:
    """从多轮状态里读取已经补齐的信息。"""

    return SlotCheckResult(
        slot=slot,
        is_filled=True,
        value=context[slot],
        reason="上一轮对话状态中已经补齐。",
    )


def missing(slot: RequiredSlot, reason: str) -> SlotCheckResult:
    """构造缺失槽位结果，避免每个检查函数重复写样板代码。"""

    return SlotCheckResult(
        slot=slot,
        is_filled=False,
        value=None,
        reason=reason,
    )


def build_clarifying_question(missing_slots: tuple[RequiredSlot, ...]) -> str:
    """根据缺失槽位生成最多两个追问。

    追问策略：一次最多问两个，优先问最影响建议方向的信息。
    """

    question_by_slot = {
        RequiredSlot.CHILD_AGE: "孩子多大，或现在几年级？",
        RequiredSlot.DURATION: "这种情况大概持续多久、发生频率怎样？",
        RequiredSlot.SITUATION: "通常是在什么具体场景下发生？",
        RequiredSlot.PARENT_GOAL: "你最希望先改变什么：减少冲突、建立习惯，还是理解原因？",
    }
    priority = (
        RequiredSlot.CHILD_AGE,
        RequiredSlot.DURATION,
        RequiredSlot.SITUATION,
        RequiredSlot.PARENT_GOAL,
    )

    selected_questions: list[str] = []
    for slot in priority:
        if slot in missing_slots:
            selected_questions.append(question_by_slot[slot])
        if len(selected_questions) == 2:
            break

    return "我先确认两个关键信息：" + " ".join(selected_questions)


EVALUATION_CASES = [
    EvaluationCase(
        user_input="孩子不爱写作业怎么办？",
        expected_next_step=NextStep.ASK_CLARIFYING_QUESTION,
        expected_missing_slots=(
            RequiredSlot.CHILD_AGE,
            RequiredSlot.DURATION,
            RequiredSlot.PARENT_GOAL,
        ),
    ),
    EvaluationCase(
        user_input="8岁孩子最近两周每天写作业拖到10点，我想减少冲突怎么办？",
        expected_next_step=NextStep.GENERATE_ADVICE,
        expected_missing_slots=(),
    ),
    EvaluationCase(
        user_input="孩子说不想活了，还提到想自伤。",
        expected_next_step=NextStep.SAFETY_RESPONSE,
        expected_missing_slots=(),
    ),
    EvaluationCase(
        user_input="8岁，最近两周。",
        existing_context={
            RequiredSlot.SITUATION: "写作业拖延",
            RequiredSlot.PARENT_GOAL: "减少亲子冲突",
        },
        expected_next_step=NextStep.GENERATE_ADVICE,
        expected_missing_slots=(),
    ),
    EvaluationCase(
        user_input="孩子老是刷手机。",
        expected_next_step=NextStep.ASK_CLARIFYING_QUESTION,
        expected_missing_slots=(
            RequiredSlot.CHILD_AGE,
            RequiredSlot.DURATION,
            RequiredSlot.PARENT_GOAL,
        ),
    ),
    EvaluationCase(
        user_input="10岁孩子最近一个月每天睡前刷手机，我希望让她更早睡觉。",
        expected_next_step=NextStep.GENERATE_ADVICE,
        expected_missing_slots=(),
    ),
    EvaluationCase(
        user_input="孩子考试前焦虑，我想知道怎么支持他。",
        expected_next_step=NextStep.ASK_CLARIFYING_QUESTION,
        expected_missing_slots=(
            RequiredSlot.CHILD_AGE,
            RequiredSlot.DURATION,
        ),
    ),
]


def print_context_check(case_index: int, case: EvaluationCase) -> bool:
    """打印一个样例的信息充分性检查结果，并返回是否符合预期。"""

    checker = ContextSufficiencyChecker()
    result = checker.check(case.user_input, case.existing_context)
    passed = (
        result.next_step == case.expected_next_step
        and result.missing_slots == case.expected_missing_slots
    )
    status = "PASS" if passed else "FAIL"

    print(f"\n=== Case {case_index}: {status} ===")
    print(f"input: {case.user_input}")
    print(f"next_step: {result.next_step.value}")
    print(f"is_sufficient: {result.is_sufficient}")
    print(f"missing_slots: {[slot.value for slot in result.missing_slots]}")
    print(f"clarifying_question: {result.clarifying_question}")
    print(f"reason: {result.reason}")
    return passed


def main() -> int:
    """命令行入口：用样例验收信息充分性判断与追问策略。"""

    passed_count = 0
    for index, case in enumerate(EVALUATION_CASES, start=1):
        if print_context_check(index, case):
            passed_count += 1

    total_count = len(EVALUATION_CASES)
    print(f"\nSummary: {passed_count}/{total_count} cases passed.")

    if passed_count != total_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

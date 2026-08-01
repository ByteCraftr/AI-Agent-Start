#!/usr/bin/env python3
"""
Parenting Copilot minimal Agent Loop experiment.

阅读路线：
1. 先看 AgentAction：理解 Agent 最终只能选择系统认识的动作。
2. 再看 AgentRunRecord：理解一次 run 需要留下可追踪记录。
3. 再看 ParentingAgent.run：理解 observe -> reason -> act -> persist 的最小循环。
4. 最后运行 main：观察 3 类输入分别进入追问、建议和安全响应。

运行：
    python3 labs/w03-agent-core/parenting_agent.py

今天先不用真实 LLM。原因是 W3-T3 的核心是 Agent Loop 编排边界：
Router 决定“去哪条流程”，Context Checker 决定“信息够不够”，
Agent Loop 负责按顺序组织这些判断，并记录下一步动作。
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from context_sufficiency import (
    ContextSufficiencyChecker,
    ContextSufficiencyResult,
    NextStep,
    RequiredSlot,
)
from intent_router import Intent, IntentRouter, RouteResult, build_default_router


class AgentAction(str, Enum):
    """Agent Loop 对外可执行的动作类型。

    这里的动作是最小实验版本，不是真实工具调用。
    后续 W4 Tool Calling 会把部分 action 扩展成真正的外部能力。
    """

    ASK_CLARIFYING_QUESTION = "ask_clarifying_question"
    GENERATE_ADVICE = "generate_advice"
    SAFETY_RESPONSE = "safety_response"


@dataclass(frozen=True)
class AgentRunRecord:
    """一次 Agent 运行的可追踪记录。

    普通函数通常只关心 return value；Agent Loop 还要保留中间决策，
    这样后续才能做多轮状态、记忆、评估和故障排查。
    """

    user_input: str
    route: RouteResult
    context_check: ContextSufficiencyResult
    action: AgentAction
    response: str


class ParentingAgent:
    """Parenting Copilot 的最小 Agent Loop。

    这个类只做编排：
    - observe: 接收用户输入和已有上下文。
    - reason: 运行 Intent Router 和信息充分性检查。
    - act: 根据 reason 结果选择下一步动作。
    - persist: 记录本次运行结果。
    """

    def __init__(
        self,
        router: IntentRouter,
        context_checker: ContextSufficiencyChecker,
    ) -> None:
        self.router = router
        self.context_checker = context_checker
        self.run_history: list[AgentRunRecord] = []

    def run(
        self,
        user_input: str,
        existing_context: dict[RequiredSlot, str] | None = None,
    ) -> AgentRunRecord:
        """运行一次 observe -> reason -> act -> persist。

        existing_context 是 W3-T2 的最小多轮状态模型。
        后续 Memory 章节会把它替换成更正式的短期状态和长期记忆。
        """

        route = self.router.classify(user_input)
        context_check = self.context_checker.check(user_input, existing_context)
        action = self._choose_action(route, context_check)
        response = self._build_response(action, route, context_check)

        record = AgentRunRecord(
            user_input=user_input,
            route=route,
            context_check=context_check,
            action=action,
            response=response,
        )
        self.run_history.append(record)
        return record

    def _choose_action(
        self,
        route: RouteResult,
        context_check: ContextSufficiencyResult,
    ) -> AgentAction:
        """把上游判断收敛成一个动作。

        安全优先级最高：Router 或 Context Checker 任一方发现高风险，
        都不能继续走普通追问或建议生成。
        """

        if route.safety_priority or context_check.next_step == NextStep.SAFETY_RESPONSE:
            return AgentAction.SAFETY_RESPONSE

        if context_check.next_step == NextStep.ASK_CLARIFYING_QUESTION:
            return AgentAction.ASK_CLARIFYING_QUESTION

        return AgentAction.GENERATE_ADVICE

    def _build_response(
        self,
        action: AgentAction,
        route: RouteResult,
        context_check: ContextSufficiencyResult,
    ) -> str:
        """构造最小响应文本。

        真实系统里这里会调用不同 Handler。今天只用固定文案证明编排链路。
        """

        if action == AgentAction.SAFETY_RESPONSE:
            return (
                "我注意到这里可能有安全风险。请先确认孩子当前是否安全；"
                "如果存在自伤、暴力、被威胁或紧急危险，请立即联系当地紧急服务、"
                "学校老师、医生或心理健康专业人士。"
            )

        if action == AgentAction.ASK_CLARIFYING_QUESTION:
            return context_check.clarifying_question or "我需要再确认一些关键信息。"

        return (
            f"已进入 {route.intent.value} 处理流程。基于当前信息，下一步可以生成"
            "一份结构化亲子建议；本实验先用固定文案代替真实 LLM。"
        )


@dataclass(frozen=True)
class EvaluationCase:
    """用于验收最小 Agent Loop 的样例。"""

    user_input: str
    expected_action: AgentAction
    expected_intent: Intent
    existing_context: dict[RequiredSlot, str] | None = None


EVALUATION_CASES = [
    EvaluationCase(
        user_input="孩子不爱写作业怎么办？",
        expected_action=AgentAction.ASK_CLARIFYING_QUESTION,
        expected_intent=Intent.LEARNING,
    ),
    EvaluationCase(
        user_input="8岁孩子最近两周每天写作业拖到10点，我想减少冲突怎么办？",
        expected_action=AgentAction.GENERATE_ADVICE,
        expected_intent=Intent.LEARNING,
    ),
    EvaluationCase(
        user_input="孩子说不想活了，还提到想自伤。",
        expected_action=AgentAction.SAFETY_RESPONSE,
        expected_intent=Intent.HIGH_RISK,
    ),
]


def build_default_agent() -> ParentingAgent:
    """构建当前 W3 最小 Agent。"""

    return ParentingAgent(
        router=build_default_router(),
        context_checker=ContextSufficiencyChecker(),
    )


def print_agent_run(case_index: int, case: EvaluationCase) -> bool:
    """打印一次 Agent Loop 的运行记录，并返回是否符合预期。"""

    agent = build_default_agent()
    record = agent.run(case.user_input, case.existing_context)
    passed = (
        record.action == case.expected_action
        and record.route.intent == case.expected_intent
    )
    status = "PASS" if passed else "FAIL"

    print(f"\n=== Case {case_index}: {status} ===")
    print(f"input: {record.user_input}")
    print(f"observe: user_input received")
    print(
        "reason: "
        f"intent={record.route.intent.value}, "
        f"next_step={record.context_check.next_step.value}"
    )
    print(f"act: {record.action.value}")
    print(f"persist: run_history_count={len(agent.run_history)}")
    print(f"response: {record.response}")
    return passed


def main() -> int:
    """命令行入口：用 3 个样例验收最小 Agent Loop。"""

    passed_count = 0
    for index, case in enumerate(EVALUATION_CASES, start=1):
        if print_agent_run(index, case):
            passed_count += 1

    total_count = len(EVALUATION_CASES)
    print(f"\nSummary: {passed_count}/{total_count} cases passed.")

    if passed_count != total_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

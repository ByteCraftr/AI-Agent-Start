#!/usr/bin/env python3
"""
Parenting Copilot intent router experiment.

阅读路线：
1. 先看 Intent：理解当前 Agent 能识别哪些问题类型。
2. 再看 RouteResult：理解 Router 不直接回答，只返回分流决策。
3. 再看 IntentRouter.classify：理解最小规则分类器如何工作。
4. 最后运行 main：观察 10 个亲子教育问题被分到哪些流程。

运行：
    python3 labs/w03-agent-core/intent_router.py

今天先不用真实 LLM。原因是 W3-T1 的核心是 Agent 分流边界：
Router 决定“去哪儿”，Handler 决定“怎么处理”，Agent Loop 决定“按什么顺序运行”。
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class Intent(str, Enum):
    """用户问题意图枚举。

    Enum 用来限制 Router 只能返回系统认识的处理流程。
    这和 W2 的 AdviceCategory 很接近，但这里表达的是“输入问题该走哪条路”。
    """

    LEARNING = "learning"
    EMOTION = "emotion"
    COMMUNICATION = "communication"
    BEHAVIOR = "behavior"
    SCHOOL_RELATIONSHIP = "school_relationship"
    HIGH_RISK = "high_risk"


@dataclass(frozen=True)
class RouteResult:
    """Intent Router 的稳定输出合同。

    特殊用法：dataclass(frozen=True) 适合表示一次已经做出的分流决策。
    后续 Agent Loop 可以安全地把它交给对应 Handler，而不是继续猜字符串含义。
    """

    intent: Intent
    confidence: float
    reason: str
    safety_priority: bool


@dataclass(frozen=True)
class IntentRule:
    """一条可解释的意图规则。

    当前用关键词做最小实验。真实系统里可以替换成 LLM classifier、
    embedding classifier 或混合策略，但 RouteResult 接口应尽量稳定。
    """

    intent: Intent
    keywords: tuple[str, ...]
    reason: str
    confidence: float
    safety_priority: bool = False


class IntentRouter:
    """把用户输入分流到对应处理流程。

    Router 的边界很窄：
    - 它不生成完整建议。
    - 它不保存记忆。
    - 它只判断当前输入更像哪类问题，并说明理由。
    """

    def __init__(self, rules: list[IntentRule]) -> None:
        self.rules = rules

    def classify(self, user_input: str) -> RouteResult:
        """根据用户输入返回分流结果。

        规则顺序是一个工程决策：高风险规则必须先匹配。
        如果先匹配普通学习或学校问题，可能把霸凌、自伤等信号误分到普通流程。
        """

        normalized_input = user_input.lower()

        for rule in self.rules:
            if contains_any_keyword(normalized_input, rule.keywords):
                return RouteResult(
                    intent=rule.intent,
                    confidence=rule.confidence,
                    reason=rule.reason,
                    safety_priority=rule.safety_priority,
                )

        return RouteResult(
            intent=Intent.COMMUNICATION,
            confidence=0.45,
            reason="没有命中明确规则，默认进入亲子沟通流程并优先追问背景。",
            safety_priority=False,
        )


def contains_any_keyword(text: str, keywords: tuple[str, ...]) -> bool:
    """判断文本是否包含任一关键词。

    这里保持简单可观察。它不是最终算法，只是为了让分类边界先跑起来。
    """

    return any(keyword in text for keyword in keywords)


def build_default_router() -> IntentRouter:
    """构建 Parenting Copilot 当前最小路由器。

    高风险放在最前面，这是安全产品的优先级规则。
    """

    return IntentRouter(
        rules=[
            IntentRule(
                intent=Intent.HIGH_RISK,
                keywords=(
                    "自伤",
                    "不想活",
                    "轻生",
                    "打到流血",
                    "严重霸凌",
                    "被威胁",
                    "离家出走",
                    "紧急",
                ),
                reason="输入包含自伤、暴力、严重霸凌或紧急危险信号。",
                confidence=0.95,
                safety_priority=True,
            ),
            IntentRule(
                intent=Intent.SCHOOL_RELATIONSHIP,
                keywords=(
                    "同学",
                    "老师",
                    "学校",
                    "校园",
                    "被排挤",
                    "不想上学",
                    "转学",
                ),
                reason="问题主要发生在学校、同伴关系或师生互动场景。",
                confidence=0.82,
            ),
            IntentRule(
                intent=Intent.EMOTION,
                keywords=(
                    "哭",
                    "害怕",
                    "焦虑",
                    "生气",
                    "情绪",
                    "难过",
                    "崩溃",
                    "发脾气",
                ),
                reason="问题主要与孩子的情绪表达、压力或调节困难有关。",
                confidence=0.8,
            ),
            IntentRule(
                intent=Intent.LEARNING,
                keywords=(
                    "作业",
                    "写字",
                    "考试",
                    "成绩",
                    "学习",
                    "拖延",
                    "注意力",
                    "阅读",
                ),
                reason="问题主要与学习任务、作业启动、成绩或注意力有关。",
                confidence=0.84,
            ),
            IntentRule(
                intent=Intent.BEHAVIOR,
                keywords=(
                    "刷手机",
                    "游戏",
                    "睡觉",
                    "吃饭",
                    "起床",
                    "习惯",
                    "撒谎",
                    "磨蹭",
                ),
                reason="问题主要与日常行为习惯、规则执行或家庭节奏有关。",
                confidence=0.78,
            ),
            IntentRule(
                intent=Intent.COMMUNICATION,
                keywords=(
                    "顶嘴",
                    "不听",
                    "沟通",
                    "吵架",
                    "不理我",
                    "怎么说",
                    "亲子关系",
                ),
                reason="问题主要与亲子沟通方式、冲突表达或关系修复有关。",
                confidence=0.76,
            ),
        ]
    )


EVALUATION_CASES: list[tuple[str, Intent]] = [
    ("孩子一写作业就拖延，坐下十分钟还没开始。", Intent.LEARNING),
    ("孩子考试前很焦虑，晚上一直说自己肯定考不好。", Intent.EMOTION),
    ("我一提醒他就顶嘴，说我只会催他。", Intent.COMMUNICATION),
    ("孩子每天刷手机停不下来，睡觉时间越来越晚。", Intent.BEHAVIOR),
    ("孩子说在学校被同学排挤，不想上学。", Intent.SCHOOL_RELATIONSHIP),
    ("孩子说不想活了，还提到想自伤。", Intent.HIGH_RISK),
    ("老师说孩子上课注意力不集中，经常漏听要求。", Intent.SCHOOL_RELATIONSHIP),
    ("孩子吃饭很磨蹭，每天早上起床也拖很久。", Intent.BEHAVIOR),
    ("孩子最近很容易生气，妹妹碰一下玩具就崩溃。", Intent.EMOTION),
    ("我不知道怎么说，他才愿意聊学习计划。", Intent.LEARNING),
]


def print_route(case_index: int, question: str, expected_intent: Intent) -> bool:
    """打印一个样例的路由结果，并返回是否符合预期。"""

    router = build_default_router()
    result = router.classify(question)
    passed = result.intent == expected_intent
    status = "PASS" if passed else "FAIL"

    print(f"\n=== Case {case_index}: {status} ===")
    print(f"question: {question}")
    print(f"expected: {expected_intent.value}")
    print(f"actual: {result.intent.value}")
    print(f"confidence: {result.confidence}")
    print(f"safety_priority: {result.safety_priority}")
    print(f"reason: {result.reason}")
    return passed


def main() -> int:
    """命令行入口：用 10 个样例验收 Intent Router。"""

    passed_count = 0

    for index, (question, expected_intent) in enumerate(EVALUATION_CASES, start=1):
        if print_route(index, question, expected_intent):
            passed_count += 1

    total_count = len(EVALUATION_CASES)
    print(f"\nSummary: {passed_count}/{total_count} cases passed.")

    if passed_count != total_count:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

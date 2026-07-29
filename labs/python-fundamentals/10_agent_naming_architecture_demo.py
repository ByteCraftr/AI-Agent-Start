"""
阅读路线：
1. 看 dataclass：Request、State、Response，把 Agent 边界命名清楚。
2. 看 SafetyChecker、IntentRouter、ParentingAdvisor，理解职责拆分。
3. 看 trace_steps，理解 Agent 执行过程如何被记录。

运行命令：
python3 labs/python-fundamentals/10_agent_naming_architecture_demo.py --question "孩子写作业总是拖延怎么办？" --age 8

学习目标：
- 把 notes/python/06 里的命名和架构边界落成可运行代码。
- 区分 request、state、prompt、raw_response、parsed_response、response。
- 看到 Parenting Copilot 的最小架构骨架。
"""

import argparse
import json
from dataclasses import asdict, dataclass, field
from typing import Literal, Protocol


RiskLevel = Literal["low", "medium", "high"]
Intent = Literal["learning", "emotion", "behavior", "high_risk", "unknown"]


@dataclass
class ParentingRequest:
    user_question: str
    child_age: int | None = None


@dataclass
class AgentState:
    request: ParentingRequest
    intent: Intent = "unknown"
    risk_level: RiskLevel = "low"
    step_count: int = 0
    trace_steps: list[str] = field(default_factory=list)

    def add_step(self, step_name: str) -> None:
        self.step_count += 1
        self.trace_steps.append(step_name)


@dataclass
class AdviceResponse:
    answer: str
    risk_level: RiskLevel
    should_escalate: bool
    trace_steps: list[str]


class LlmClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class FakeLlmClient:
    def generate(self, prompt: str) -> str:
        return json.dumps(
            {
                "answer": "先和孩子确认卡在哪里，再把作业拆成一个 10 分钟能完成的小步骤。",
                "risk_level": "low",
                "should_escalate": False,
            },
            ensure_ascii=False,
        )


class SafetyChecker:
    def classify(self, user_question: str) -> RiskLevel:
        high_risk_keywords = ["不想活", "自伤", "伤害自己"]
        if any(keyword in user_question for keyword in high_risk_keywords):
            return "high"
        return "low"


class IntentRouter:
    def route(self, user_question: str) -> Intent:
        if "作业" in user_question or "学习" in user_question:
            return "learning"
        if "发脾气" in user_question or "哭" in user_question:
            return "emotion"
        return "unknown"


class ParentingAdvisor:
    def __init__(
        self,
        llm_client: LlmClient,
        safety_checker: SafetyChecker,
        intent_router: IntentRouter,
    ) -> None:
        self.llm_client = llm_client
        self.safety_checker = safety_checker
        self.intent_router = intent_router

    def answer(self, request: ParentingRequest) -> AdviceResponse:
        state = AgentState(request=request)

        state.add_step("safety_check")
        state.risk_level = self.safety_checker.classify(request.user_question)
        if state.risk_level == "high":
            return AdviceResponse(
                answer="这个情况可能涉及安全风险，请优先联系当地紧急服务或专业人士。",
                risk_level="high",
                should_escalate=True,
                trace_steps=state.trace_steps,
            )

        state.add_step("intent_route")
        state.intent = self.intent_router.route(request.user_question)

        state.add_step("build_prompt")
        prompt = self._build_prompt(state)

        state.add_step("llm_call")
        raw_response = self.llm_client.generate(prompt)

        state.add_step("parse_response")
        parsed_response = json.loads(raw_response)

        return AdviceResponse(
            answer=parsed_response["answer"],
            risk_level=parsed_response["risk_level"],
            should_escalate=parsed_response["should_escalate"],
            trace_steps=state.trace_steps,
        )

    def _build_prompt(self, state: AgentState) -> str:
        return (
            "你是一个亲子教育助手。"
            "请给出低风险、家长可监督执行的建议。\n"
            f"孩子年龄：{state.request.child_age}\n"
            f"问题类型：{state.intent}\n"
            f"家长问题：{state.request.user_question}"
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agent 命名与架构边界演示")
    parser.add_argument("--question", required=True)
    parser.add_argument("--age", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request = ParentingRequest(user_question=args.question, child_age=args.age)
    advisor = ParentingAdvisor(
        llm_client=FakeLlmClient(),
        safety_checker=SafetyChecker(),
        intent_router=IntentRouter(),
    )
    response = advisor.answer(request)

    print("=== Agent 命名与架构边界演示 ===")
    print(json.dumps(asdict(response), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


"""
阅读路线：
1. 看 ParentingRequest 和 LlmClient，理解数据结构和接口。
2. 看 build_prompt()，理解如何把业务输入变成 prompt。
3. 看 run_agent()，理解最小 Agent 调用链。
4. 看 main()，理解 CLI 参数如何进入 Agent。

运行命令：
python3 labs/python-fundamentals/08_mini_parenting_advisor.py --question "孩子拖延写作业怎么办？" --age 8

学习目标：
- 把 argparse、dataclass、Protocol、logging、json 串成一个最小 Agent。
- 使用 Fake LLM 避免真实网络调用。
- 输出结构化 JSON，方便后续测试和评估。
"""

import argparse
import json
import logging
from dataclasses import dataclass
from typing import Protocol


logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


@dataclass
class ParentingRequest:
    question: str
    child_age: int


class LlmClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class FakeLlmClient:
    def generate(self, prompt: str) -> str:
        return "先接住孩子情绪，再把任务拆成 10 分钟的小步骤。"


def build_prompt(request: ParentingRequest) -> str:
    return (
        "你是一个亲子教育助手。"
        "请给出低风险、家长可监督执行的建议。\n"
        f"孩子年龄：{request.child_age}\n"
        f"家长问题：{request.question}"
    )


def classify_risk(question: str) -> str:
    high_risk_keywords = ["不想活", "自伤", "伤害自己"]
    if any(keyword in question for keyword in high_risk_keywords):
        return "high"
    return "low"


def run_agent(request: ParentingRequest, llm_client: LlmClient) -> dict:
    logger.info("开始运行 Parenting Copilot 最小 Agent")
    risk_level = classify_risk(request.question)

    if risk_level == "high":
        return {
            "answer": "这个情况可能涉及安全风险，请优先联系当地紧急服务或专业人士。",
            "risk_level": "high",
            "should_escalate": True,
            "source": "safety_checker",
        }

    prompt = build_prompt(request)
    answer = llm_client.generate(prompt)
    return {
        "answer": answer,
        "risk_level": "low",
        "should_escalate": False,
        "source": "fake_llm",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="最小 Parenting Copilot Agent")
    parser.add_argument("--question", required=True, help="家长的问题")
    parser.add_argument("--age", type=int, required=True, help="孩子年龄")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request = ParentingRequest(question=args.question, child_age=args.age)
    result = run_agent(request, FakeLlmClient())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


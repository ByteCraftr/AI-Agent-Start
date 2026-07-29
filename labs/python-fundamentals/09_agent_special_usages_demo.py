"""
阅读路线：
1. 看类型定义：TypedDict、Literal、dataclass、Protocol。
2. 看 parse_json_response()，理解 raise from 保留错误原因。
3. 看 main()，理解 argparse、logging、json、入口保护如何组合。

运行命令：
python3 labs/python-fundamentals/09_agent_special_usages_demo.py --question "孩子害怕上学怎么办？" --age 7

学习目标：
- 把 notes/python/05 里的特殊写法落成可运行代码。
- 理解这些写法为什么在 LLM Agent 中常见。
- 看到 Fake LLM 返回 JSON 后如何解析。
"""

import argparse
import json
import logging
from dataclasses import dataclass
from typing import Literal, Protocol, TypedDict


logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)

RiskLevel = Literal["low", "medium", "high"]


class AgentOutput(TypedDict):
    answer: str
    risk_level: RiskLevel
    should_escalate: bool


@dataclass
class ParentingRequest:
    question: str
    child_age: int | None


class LlmClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class FakeJsonLlmClient:
    def generate(self, prompt: str) -> str:
        logger.info("FakeJsonLlmClient 收到 prompt，返回稳定 JSON")
        return json.dumps(
            {
                "answer": "先确认孩子害怕的具体原因，再和孩子约定一个可完成的小行动。",
                "risk_level": "low",
                "should_escalate": False,
            },
            ensure_ascii=False,
        )


def build_prompt(request: ParentingRequest) -> str:
    age_text = "未知" if request.child_age is None else str(request.child_age)
    return f"孩子年龄：{age_text}。家长问题：{request.question}"


def parse_json_response(raw_text: str) -> AgentOutput:
    try:
        data = json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise ValueError("模型返回的内容不是合法 JSON") from error

    required_fields = ["answer", "risk_level", "should_escalate"]
    for field_name in required_fields:
        if field_name not in data:
            raise ValueError(f"模型返回缺少必要字段：{field_name}")

    return {
        "answer": str(data["answer"]),
        "risk_level": data["risk_level"],
        "should_escalate": bool(data["should_escalate"]),
    }


def run_demo(request: ParentingRequest, llm_client: LlmClient) -> AgentOutput:
    prompt = build_prompt(request)
    raw_response = llm_client.generate(prompt)
    return parse_json_response(raw_response)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="LLM Agent Python 特殊写法演示")
    parser.add_argument("--question", required=True)
    parser.add_argument("--age", type=int)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request = ParentingRequest(question=args.question, child_age=args.age)
    output = run_demo(request, FakeJsonLlmClient())
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()


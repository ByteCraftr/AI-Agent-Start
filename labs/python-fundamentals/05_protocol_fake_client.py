"""
阅读路线：
1. 看 LlmClient Protocol，理解接口契约。
2. 看 FakeLlmClient，理解为什么测试时不用真实 LLM。
3. 看 Advisor，理解业务代码依赖接口而不是具体实现。

运行命令：
python3 labs/python-fundamentals/05_protocol_fake_client.py

学习目标：
- 理解 Protocol 在 Python 里的接口作用。
- 看到 Fake LLM 如何让 Agent 代码可测试。
- 建立 Android Repository interface 类比。
"""

from typing import Protocol


class LlmClient(Protocol):
    """只定义能力契约：能根据 prompt 生成文本。"""

    def generate(self, prompt: str) -> str:
        ...


class FakeLlmClient:
    """Fake 实现：不联网、不花钱、输出稳定。"""

    def generate(self, prompt: str) -> str:
        return f"Fake LLM 回答：我收到了 prompt：{prompt}"


class Advisor:
    """业务类：只依赖 LlmClient 契约。"""

    def __init__(self, llm_client: LlmClient) -> None:
        self.llm_client = llm_client

    def answer(self, question: str) -> str:
        prompt = f"请用低风险方式回答亲子教育问题：{question}"
        return self.llm_client.generate(prompt)


def main() -> None:
    advisor = Advisor(FakeLlmClient())
    answer = advisor.answer("孩子拖延写作业怎么办？")

    print("=== Python Protocol 与 Fake Client ===")
    print(answer)


if __name__ == "__main__":
    main()


"""
阅读路线：
1. 看 ParentingQuestion，理解 dataclass 数据对象。
2. 看 SafetyChecker 和 ParentingAdvisor，理解组合关系。
3. 看 Message/UserMessage，理解继承关系。

运行命令：
python3 labs/python-fundamentals/04_classes_composition_inheritance.py

学习目标：
- 理解类不是为了炫技，而是为了表达稳定职责。
- 掌握组合优先于继承。
- 看到 Agent 业务对象如何协作。
"""

from dataclasses import dataclass


@dataclass
class ParentingQuestion:
    """dataclass 适合表达一组稳定字段。"""
    text: str
    child_age: int


class SafetyChecker:
    """安全检查器：只负责风险判断。"""

    def is_high_risk(self, question: ParentingQuestion) -> bool:
        high_risk_keywords = ["不想活", "自伤", "伤害自己"]
        return any(keyword in question.text for keyword in high_risk_keywords)


class ParentingAdvisor:
    """建议生成器：组合 SafetyChecker，不自己实现所有细节。"""

    def __init__(self, safety_checker: SafetyChecker) -> None:
        self.safety_checker = safety_checker

    def answer(self, question: ParentingQuestion) -> str:
        if self.safety_checker.is_high_risk(question):
            return "这个情况可能涉及安全风险，请优先寻求专业帮助。"
        return "先接住孩子情绪，再和孩子一起拆小任务。"


class Message:
    """父类：表达消息的共同结构。"""

    def __init__(self, content: str) -> None:
        self.content = content


class UserMessage(Message):
    """子类：用户消息是 Message 的一种。"""


def main() -> None:
    question = ParentingQuestion(text="孩子不写作业怎么办？", child_age=8)
    advisor = ParentingAdvisor(SafetyChecker())
    user_message = UserMessage(question.text)

    print("=== Python 类、组合、继承 ===")
    print(f"UserMessage.content = {user_message.content}")
    print(advisor.answer(question))


if __name__ == "__main__":
    main()


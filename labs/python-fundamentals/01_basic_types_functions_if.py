"""
阅读路线：
1. 先看 main()，理解脚本从哪里开始执行。
2. 再看 classify_age_stage()，理解 if-elif-else。
3. 最后看 build_prompt() 和 build_result()，理解函数输入输出。

运行命令：
python3 labs/python-fundamentals/01_basic_types_functions_if.py

学习目标：
- 认识 Python 基础类型。
- 理解变量命名、函数、调用和 if-else。
- 看到 Parenting Copilot 里最小的一次输入处理。
"""


def classify_age_stage(child_age: int) -> str:
    """根据孩子年龄返回阶段标签。"""
    if child_age < 3:
        return "toddler"
    if child_age < 7:
        return "preschool"
    return "school_age"


def is_high_risk(question: str) -> bool:
    """用最小关键词规则演示风险判断。真实产品不能只靠关键词。"""
    high_risk_keywords = ["不想活", "自伤", "伤害自己"]
    return any(keyword in question for keyword in high_risk_keywords)


def build_prompt(question: str, child_age: int) -> str:
    """把业务输入组装成给 LLM 的 prompt。"""
    age_stage = classify_age_stage(child_age)
    return f"孩子阶段：{age_stage}。家长问题：{question}"


def build_result(question: str, child_age: int) -> dict:
    """把多个小函数串起来，返回结构化 dict。"""
    return {
        "question": question,
        "child_age": child_age,
        "age_stage": classify_age_stage(child_age),
        "is_high_risk": is_high_risk(question),
        "prompt": build_prompt(question, child_age),
    }


def main() -> None:
    """脚本入口：准备数据并打印结果。"""
    user_question = "孩子不写作业怎么办？"
    child_age = 8

    result = build_result(user_question, child_age)

    print("=== Python 基础：类型、函数、if-else ===")
    print(f"字符串 str：{user_question}")
    print(f"整数 int：{child_age}")
    print(f"布尔 bool：{result['is_high_risk']}")
    print(f"字典 dict：{result}")


if __name__ == "__main__":
    main()


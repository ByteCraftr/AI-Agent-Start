"""
阅读路线：
1. 看 build_parenting_cases()，认识 list 和 dict。
2. 看 summarize_cases()，理解 for 循环和 set 去重。
3. 看 save_and_load_summary()，理解 pathlib 文件读写。

运行命令：
python3 labs/python-fundamentals/02_collections_loops_files.py

学习目标：
- 练习 list、dict、set。
- 理解循环如何处理多条样例。
- 用 pathlib 写入和读取一个临时学习文件。
"""

from pathlib import Path


def build_parenting_cases() -> list[dict]:
    """构造多条亲子教育样例。list 负责保存多条，dict 负责描述一条。"""
    return [
        {"id": 1, "topic": "learning", "question": "孩子不写作业怎么办？"},
        {"id": 2, "topic": "emotion", "question": "孩子总是发脾气怎么办？"},
        {"id": 3, "topic": "learning", "question": "孩子考试前紧张怎么办？"},
    ]


def summarize_cases(cases: list[dict]) -> dict:
    """遍历样例并统计主题。"""
    topics = set()
    questions = []

    for case in cases:
        topics.add(case["topic"])
        questions.append(case["question"])

    return {
        "case_count": len(cases),
        "topics": sorted(topics),
        "questions": questions,
    }


def save_and_load_summary(summary: dict) -> str:
    """用 pathlib 演示文件写入和读取。"""
    output_dir = Path(__file__).resolve().parent / "tmp_outputs"
    output_dir.mkdir(exist_ok=True)

    output_path = output_dir / "case_summary.txt"
    text = (
        f"样例数量：{summary['case_count']}\n"
        f"主题：{', '.join(summary['topics'])}\n"
        f"第一条问题：{summary['questions'][0]}\n"
    )
    output_path.write_text(text, encoding="utf-8")
    return output_path.read_text(encoding="utf-8")


def main() -> None:
    cases = build_parenting_cases()
    summary = summarize_cases(cases)
    loaded_text = save_and_load_summary(summary)

    print("=== Python 集合类型、循环、文件读写 ===")
    print(summary)
    print("--- 从文件读回来的内容 ---")
    print(loaded_text)


if __name__ == "__main__":
    main()


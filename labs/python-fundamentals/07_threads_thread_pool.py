"""
阅读路线：
1. 看 evaluate_case()，理解每条评估样例的处理函数。
2. 看 ThreadPoolExecutor，理解线程池如何批量执行。
3. 看结果顺序，理解 executor.map 会按输入顺序返回结果。

运行命令：
python3 labs/python-fundamentals/07_threads_thread_pool.py

学习目标：
- 理解线程池适合 I/O 等待型任务。
- 看到批量评估 Agent 样例的基本形态。
- 注意不要在多线程里随意修改共享变量。
"""

import time
from concurrent.futures import ThreadPoolExecutor


def evaluate_case(question: str) -> dict:
    """模拟一次评估。sleep 代表网络等待或 LLM 调用等待。"""
    time.sleep(0.1)
    return {
        "question": question,
        "passed": "怎么办" in question,
    }


def main() -> None:
    questions = [
        "孩子不写作业怎么办？",
        "孩子总是发脾气怎么办？",
        "孩子害怕上学怎么办？",
    ]

    print("=== Python 线程池：批量评估样例 ===")

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(evaluate_case, questions))

    for result in results:
        print(result)


if __name__ == "__main__":
    main()


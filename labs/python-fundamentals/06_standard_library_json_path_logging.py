"""
阅读路线：
1. 看 build_result()，理解 dict 如何表达结构化结果。
2. 看 save_json()，理解 json 和 pathlib。
3. 看 logger，理解 logging 替代 print 的工程价值。

运行命令：
python3 labs/python-fundamentals/06_standard_library_json_path_logging.py

学习目标：
- 使用 json 输出中文结构化结果。
- 使用 pathlib 管理路径。
- 使用 logging 记录流程。
"""

import json
import logging
from pathlib import Path


logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger(__name__)


def build_result() -> dict:
    return {
        "answer": "先共情，再拆小任务。",
        "risk_level": "low",
        "source": "standard_library_demo",
    }


def save_json(result: dict) -> Path:
    output_dir = Path(__file__).resolve().parent / "tmp_outputs"
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "advice_result.json"

    json_text = json.dumps(result, ensure_ascii=False, indent=2)
    output_path.write_text(json_text, encoding="utf-8")
    return output_path


def main() -> None:
    logger.info("开始构造结构化结果")
    result = build_result()

    logger.info("开始写入 JSON 文件")
    output_path = save_json(result)

    print("=== Python 标准库：json、pathlib、logging ===")
    print(f"文件已写入：{output_path}")
    print(output_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()


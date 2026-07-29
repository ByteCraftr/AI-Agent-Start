---
type: concept
topic: Python 高级
project: Parenting Copilot
status: draft
tags:
  - python
  - standard-library
  - threading
---

# Python 高级：标准库、并发、线程、工程习惯

## 1. 标准库是什么

标准库是 Python 自带的一组模块，不需要额外安装。它类似 Android/Kotlin/JDK 自带库，覆盖文件、路径、时间、JSON、日志、并发、测试、网络、数据结构等基础能力。

学习 Agent 项目时，先熟悉标准库非常重要，因为很多实验不需要马上上框架。

## 2. 常用标准库清单

文件和路径：

- `pathlib`：面向对象地处理路径。
- `os`：环境变量、系统交互。
- `shutil`：复制、移动、删除文件树。
- `tempfile`：创建临时文件和目录。

数据和序列化：

- `json`：读写 JSON。
- `csv`：读写 CSV。
- `dataclasses`：定义轻量数据对象。
- `enum`：定义枚举。
- `collections`：提供 `defaultdict`、`Counter`、`deque` 等容器。

时间和日志：

- `datetime`：日期和时间。
- `time`：耗时、sleep。
- `logging`：工程日志。

类型和抽象：

- `typing`：类型提示。
- `abc`：抽象基类。
- `inspect`：检查函数、类、签名等运行时信息。

并发和进程：

- `threading`：线程。
- `concurrent.futures`：线程池和进程池。
- `asyncio`：异步 I/O。
- `subprocess`：调用外部命令。

网络和 API：

- `urllib.request`：基础 HTTP 请求。
- `http.client`：底层 HTTP 客户端。

测试和调试：

- `unittest`：标准库测试框架。
- `pdb`：调试器。
- `traceback`：异常堆栈处理。

## 3. Agent 项目里最常用的标准库

优先掌握：

- `json`：LLM 请求和结构化输出都离不开 JSON。
- `os`：从环境变量读取 `OPENAI_API_KEY`。
- `pathlib`：读写 prompt、样例、评估数据。
- `dataclasses`：表达输入、输出、中间结果。
- `typing`：让函数和类的契约更清楚。
- `logging`：记录调用、耗时、错误。
- `time` / `datetime`：记录耗时和时间戳。
- `concurrent.futures`：并发跑多条评估样例。
- `unittest`：写最小自动化测试。

## 4. pathlib 示例

```python
from pathlib import Path

root = Path("labs")
file_path = root / "sample.json"

if file_path.exists():
    text = file_path.read_text(encoding="utf-8")
```

注意：`Path` 比字符串拼路径更稳，跨平台更清楚。

## 5. json 示例

```python
import json

payload = {
    "question": "孩子不写作业怎么办？",
    "child_age": 8,
}

text = json.dumps(payload, ensure_ascii=False, indent=2)
data = json.loads(text)
```

- `dumps`：Python 对象转 JSON 字符串。
- `loads`：JSON 字符串转 Python 对象。
- `ensure_ascii=False`：中文保持可读。

## 6. logging 示例

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("start parenting advisor")
```

注意：真实项目优先用 `logging`，不要到处 `print`。`print` 适合临时学习和小实验。

## 7. 线程是什么

线程是在同一个进程里同时执行多条任务路径。Python 的线程适合 I/O 密集型任务，比如：

- 同时请求多个 HTTP API。
- 同时读取多个文件。
- 后台写日志或处理队列。

不适合：

- 用线程提升大量 CPU 计算性能。
- 在多个线程里随意修改同一个变量。

注意：CPython 有 GIL，全局解释器锁会限制同一时刻执行 Python 字节码的线程数量。所以 CPU 密集任务通常考虑多进程或其他计算方案。

## 8. threading 示例

```python
import threading


def worker(name: str) -> None:
    print(f"start {name}")


thread = threading.Thread(target=worker, args=("task-1",))
thread.start()
thread.join()
```

- `start()`：启动线程。
- `join()`：等待线程结束。

注意：初学时知道线程存在即可。Agent 批量评估更建议先用 `concurrent.futures.ThreadPoolExecutor`。

## 9. ThreadPoolExecutor 示例

```python
from concurrent.futures import ThreadPoolExecutor


def evaluate_case(case_id: int) -> str:
    return f"case-{case_id}: ok"


with ThreadPoolExecutor(max_workers=4) as executor:
    results = list(executor.map(evaluate_case, [1, 2, 3, 4]))

print(results)
```

这适合后续同时跑多个 LLM 评估样例。它比手动创建多个线程更容易管理。

## 10. 线程安全的基本原则

- 尽量不要让多个线程同时修改同一个对象。
- 多线程共享数据时，使用锁、队列或不可变数据。
- API 调用失败要单独处理，不能让一个任务失败拖垮全部任务。
- 记录每个任务的输入、输出、错误和耗时。

## 11. 高级学习顺序

1. 先掌握 `json`、`pathlib`、`os`、`dataclasses`、`typing`。
2. 再掌握 `logging`、`unittest`、`datetime`。
3. 需要批量评估时学习 `concurrent.futures`。
4. 需要高并发网络服务时再系统学习 `asyncio`。


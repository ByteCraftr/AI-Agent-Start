---
type: concept
topic: Python 特殊用法与 LLM Agent 开发
project: Parenting Copilot
status: draft
tags:
  - python
  - ai-agent
  - llm-agent
  - engineering
---

# Python 特殊用法：LLM Agent 开发中要特别注意的写法

这篇不是完整语法手册，而是把 LLM Agent 开发里经常出现、但初学 Python 时容易忽略的特殊用法单独标出来。

学习重点：

- 看到这些写法时，不要只背语法，要理解它们解决的工程问题。
- 写 [[../../product/parenting-copilot-prd|Parenting Copilot]] 代码时，优先用这些方式让输入、输出、边界和测试更清楚。
- 每个例子都尽量保持可运行，后续可以迁移到 `labs/python-fundamentals/`。

## 1. `if __name__ == "__main__"`：让文件既能运行，也能被导入

Agent 脚本经常既要“直接运行”，又要“被测试文件导入”。这行代码就是入口保护。

```python
def main() -> None:
    print("运行 Parenting Copilot 最小示例")


if __name__ == "__main__":
    main()
```

注意：

- 直接运行这个文件时，`__name__` 等于 `"__main__"`，会执行 `main()`。
- 其他文件 `import` 它时，不会自动执行 `main()`。
- 这能避免测试时刚导入模块就发起真实 LLM 请求。

## 2. 类型提示：让 Agent 的输入输出契约更清楚

LLM Agent 很容易出现“传进去是字符串，出来可能是字符串、字典、空值、异常”的混乱。类型提示能提前把契约写清楚。

```python
def build_prompt(question: str, child_age: int) -> str:
    return f"孩子年龄：{child_age}。家长问题：{question}"
```

注意：

- `question: str` 不是运行时强制校验，而是工程契约。
- `-> str` 表示函数应该返回字符串。
- 后续配合编辑器、类型检查工具、测试会更有价值。

## 3. `Optional`：明确“可能没有值”

LLM 响应、配置、环境变量经常可能为空。不要用模糊的变量表达“可能没有”。

```python
import os
from typing import Optional


def read_api_key() -> Optional[str]:
    return os.environ.get("OPENAI_API_KEY")


api_key = read_api_key()
if api_key is None:
    print("没有配置 OPENAI_API_KEY")
```

注意：

- `Optional[str]` 表示返回值可能是 `str`，也可能是 `None`。
- 判断空值时优先写 `is None`，比 `== None` 更符合 Python 习惯。
- API key 只能从环境变量读取，不要写进代码或笔记。

## 4. `dataclass`：表达 Agent 的结构化输入输出

Agent 工程不要让所有数据都散在 `dict` 里。`dataclass` 适合表达内部数据结构。

```python
from dataclasses import dataclass


@dataclass
class ParentingRequest:
    question: str
    child_age: int


@dataclass
class AdviceResult:
    answer: str
    risk_level: str
    should_escalate: bool


request = ParentingRequest(question="孩子不写作业怎么办？", child_age=8)
result = AdviceResult(
    answer="先共情，再把任务拆小。",
    risk_level="low",
    should_escalate=False,
)

print(request)
print(result)
```

注意：

- `dataclass` 适合内部结构，不等于外部 API schema。
- LLM 结构化输出进入系统后，仍然要校验字段是否存在、类型是否正确。
- 如果数据结构开始复杂，可以再学习 Pydantic。

## 5. `TypedDict`：给 JSON 字典加类型说明

LLM API 请求体、响应体通常是 JSON，也就是 Python 里的 `dict`。`TypedDict` 可以描述字典里应该有哪些字段。

```python
from typing import TypedDict


class LlmPayload(TypedDict):
    model: str
    input: str
    max_output_tokens: int


def build_payload(prompt: str) -> LlmPayload:
    return {
        "model": "gpt-5-mini",
        "input": prompt,
        "max_output_tokens": 800,
    }
```

注意：

- `TypedDict` 主要帮助人和工具理解结构。
- 它不会自动阻止运行时传错字段。
- 真正生产级校验要配合 schema 校验或 Pydantic。

## 6. `Literal`：限制状态值只能是几个固定选项

Agent 里常有状态：风险等级、工具调用状态、任务状态。不要到处写随意字符串。

```python
from typing import Literal

RiskLevel = Literal["low", "medium", "high"]


def classify_risk(question: str) -> RiskLevel:
    if "不想活" in question:
        return "high"
    return "low"
```

注意：

- `Literal` 适合固定枚举值。
- 对 LLM 输出尤其重要，因为模型可能返回你没预期的词。
- 如果状态很多，也可以用 `Enum`。

## 7. `Enum`：让状态值更稳定

```python
from enum import Enum


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


def classify_risk(question: str) -> RiskLevel:
    if "不想活" in question:
        return RiskLevel.HIGH
    return RiskLevel.LOW
```

注意：

- `Enum` 比裸字符串更不容易写错。
- 输出 JSON 时通常使用 `risk.value`。
- 简单脚本里 `Literal` 更轻，长期项目里 `Enum` 更稳。

## 8. `Protocol`：让真实 LLM 和 Fake LLM 可以互换

Agent 测试时不能每次都真实调用模型。`Protocol` 可以定义“只要长得像这个接口就能用”。

```python
from typing import Protocol


class LlmClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class FakeLlmClient:
    def generate(self, prompt: str) -> str:
        return "这是 Fake LLM 的回答，用于测试。"


class ParentingAdvisor:
    def __init__(self, llm_client: LlmClient) -> None:
        self.llm_client = llm_client

    def answer(self, question: str) -> str:
        prompt = f"请回答亲子教育问题：{question}"
        return self.llm_client.generate(prompt)


advisor = ParentingAdvisor(FakeLlmClient())
print(advisor.answer("孩子拖延写作业怎么办？"))
```

注意：

- 这相当于 Android 里的接口注入。
- 真实 LLM client 和 fake client 都实现 `generate()`，业务代码不关心具体实现。
- 这是写可测试 Agent 的关键方式。

## 9. `try / except / raise from`：保留错误原因

LLM Agent 经常遇到网络错误、鉴权错误、解析错误。不要吞掉异常。

```python
import json


def parse_json_response(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise ValueError("模型返回的内容不是合法 JSON") from error
```

注意：

- `raise ... from error` 会保留原始异常链。
- 这样日志里能看到真正失败原因。
- Agent 解析结构化输出时，这个写法非常常见。

## 10. `with` 上下文管理器：自动关闭资源

读写文件、打开网络连接、使用线程池时，常见 `with`。

```python
from pathlib import Path


path = Path("sample_prompt.txt")

with path.open("w", encoding="utf-8") as file:
    file.write("请回答一个亲子教育问题。")
```

注意：

- `with` 代码块结束后，会自动关闭文件。
- 比手动 `file.close()` 更安全。
- 后续线程池、数据库连接也经常使用 `with`。

## 11. `pathlib`：不要手写字符串路径

```python
from pathlib import Path


project_root = Path(__file__).resolve().parents[2]
prompt_path = project_root / "notes" / "python" / "README.md"

print(prompt_path)
print(prompt_path.exists())
```

注意：

- `Path(__file__)` 表示当前 Python 文件路径。
- `.resolve()` 转成绝对路径。
- `/` 在 `Path` 里表示拼接路径，不是除法。

## 12. `json.dumps(..., ensure_ascii=False)`：让中文 JSON 可读

```python
import json


result = {
    "answer": "先共情，再拆小任务。",
    "risk_level": "low",
}

print(json.dumps(result, ensure_ascii=False, indent=2))
```

注意：

- 不加 `ensure_ascii=False`，中文会变成 Unicode 转义。
- `indent=2` 适合学习、日志和调试。
- 生产日志要注意不要输出隐私和 API key。

## 13. `logging`：正式代码不要只靠 `print`

```python
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("开始处理家长问题")
logger.warning("检测到可能需要升级处理的风险表达")
```

注意：

- `print` 适合学习和临时调试。
- `logging` 适合正式流程，可以区分 info、warning、error。
- Agent 项目里日志要避免记录儿童隐私、完整对话和密钥。

## 14. `argparse`：让脚本可以从命令行传参

```python
import argparse


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--age", type=int, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(f"问题：{args.question}")
    print(f"年龄：{args.age}")


if __name__ == "__main__":
    main()
```

运行：

```bash
python3 demo.py --question "孩子不写作业怎么办？" --age 8
```

注意：

- `argparse` 适合把学习脚本变成可重复运行的实验工具。
- `type=int` 会把命令行字符串转换成整数。
- 参数校验失败时，`argparse` 会自动给出错误提示。

## 15. `ThreadPoolExecutor`：批量跑评估样例

当你有 100 条评估问题时，不想一条一条串行跑。线程池适合 I/O 密集任务，比如多次 LLM API 调用。

```python
from concurrent.futures import ThreadPoolExecutor


def evaluate_question(question: str) -> str:
    return f"已评估：{question}"


questions = [
    "孩子不写作业怎么办？",
    "孩子总是发脾气怎么办？",
    "孩子害怕上学怎么办？",
]

with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(executor.map(evaluate_question, questions))

print(results)
```

注意：

- 线程池适合网络等待，不适合大量 CPU 计算。
- 调真实 LLM 时要考虑限流、重试、费用和日志。
- 多线程里不要随意修改共享变量。

## 16. 生成器 `yield`：一条一条处理数据

评估集很大时，不一定要一次性全部读进内存。

```python
from typing import Iterator


def load_questions() -> Iterator[str]:
    yield "孩子不写作业怎么办？"
    yield "孩子总是发脾气怎么办？"
    yield "孩子害怕上学怎么办？"


for question in load_questions():
    print(question)
```

注意：

- `yield` 会让函数变成生成器。
- 生成器适合流式处理数据。
- LLM streaming 不是同一个概念，但心智模型类似：不要等全部完成才处理。

## 17. 装饰器：给函数包一层通用能力

装饰器常用于记录耗时、重试、权限检查、缓存。

```python
import time
from collections.abc import Callable
from typing import TypeVar


F = TypeVar("F", bound=Callable)


def log_time(func: F) -> F:
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        cost = time.time() - start
        print(f"{func.__name__} cost: {cost:.3f}s")
        return result

    return wrapper  # type: ignore[return-value]


@log_time
def fake_llm_call(prompt: str) -> str:
    time.sleep(0.1)
    return f"回答：{prompt}"


print(fake_llm_call("孩子拖延怎么办？"))
```

注意：

- 初学时不建议过早自己写复杂装饰器。
- 看到 `@something` 时，要意识到函数被额外包了一层逻辑。
- Agent 框架里大量工具、回调、重试都可能用装饰器表达。

## 18. `async / await`：高并发 I/O 的另一种方式

```python
import asyncio


async def fake_llm_call(question: str) -> str:
    await asyncio.sleep(0.1)
    return f"回答：{question}"


async def main() -> None:
    result = await fake_llm_call("孩子拖延怎么办？")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
```

注意：

- `async` 不等于多线程。
- 它适合大量 I/O 等待，比如网络请求。
- 初学 Agent 时可以先掌握普通同步代码，再学 `async`。

## 19. `copy`：避免可变对象互相影响

Agent state 里经常有 list、dict。可变对象如果直接复用，可能互相污染。

```python
from copy import deepcopy


base_state = {
    "messages": ["你好"],
    "metadata": {"risk": "low"},
}

new_state = deepcopy(base_state)
new_state["messages"].append("新的问题")

print(base_state)
print(new_state)
```

注意：

- `dict.copy()` 是浅拷贝，嵌套对象仍可能共享。
- `deepcopy()` 会复制嵌套结构，但成本更高。
- Agent memory、conversation state、tool result 都要注意这个问题。

## 20. `assert`：学习阶段的小检查

```python
def normalize_question(question: str) -> str:
    return question.strip()


assert normalize_question("  hello  ") == "hello"
```

注意：

- `assert` 适合学习和内部不变量检查。
- 不要用 `assert` 替代正式用户输入校验。
- 后续应该把关键检查升级成测试文件。

## LLM Agent 开发中最常用的组合

最小 Agent 脚本里，常见组合是：

```text
argparse
  -> dataclass / TypedDict
  -> build_prompt()
  -> LlmClient Protocol
  -> FakeLlmClient 或真实 LLM client
  -> json.dumps()
  -> logging
  -> if __name__ == "__main__"
```

对应到代码：

```python
import argparse
import json
import logging
from dataclasses import dataclass
from typing import Protocol


logging.basicConfig(level=logging.INFO)
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
    return f"孩子年龄：{request.child_age}。家长问题：{request.question}"


def run_agent(request: ParentingRequest, llm_client: LlmClient) -> dict:
    logger.info("开始运行 Parenting Copilot 最小 Agent")
    prompt = build_prompt(request)
    answer = llm_client.generate(prompt)
    return {
        "answer": answer,
        "risk_level": "low",
        "source": "fake_llm",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--question", required=True)
    parser.add_argument("--age", type=int, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    request = ParentingRequest(question=args.question, child_age=args.age)
    result = run_agent(request, FakeLlmClient())
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
```

这段代码后续可以独立放到 `labs/python-fundamentals/08_mini_parenting_advisor.py`，作为可运行版本。


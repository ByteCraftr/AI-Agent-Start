---
type: concept
topic: Python 中级
project: Parenting Copilot
status: draft
tags:
  - python
  - oop
  - modules
---

# Python 中级：模块、类、关系、继承、接口、调用

## 1. 模块和包

一个 `.py` 文件就是一个模块。多个模块放在目录里，可以组成包。

```text
parenting_agent/
  __init__.py
  advisor.py
  safety.py
  models.py
```

建议职责：

- `models.py`：数据结构。
- `safety.py`：风险判断。
- `advisor.py`：建议生成流程。
- `api_client.py`：外部 API 调用。

Android 类比：模块拆分对应 package 分层，但 Python 项目早期可以先保持简单。

## 2. 类是什么

类把数据和行为组织在一起。

```python
class ParentingQuestion:
    def __init__(self, text: str, child_age: int) -> None:
        self.text = text
        self.child_age = child_age
```

- `class`：定义类。
- `__init__`：对象创建时调用的初始化方法。
- `self`：当前对象本身，类似 Kotlin/Java 的 `this`。

创建对象：

```python
question = ParentingQuestion("孩子不写作业怎么办？", 8)
print(question.text)
```

## 3. dataclass：更适合数据对象

Python 常用 `dataclass` 表达数据结构。

```python
from dataclasses import dataclass


@dataclass
class ParentingQuestion:
    text: str
    child_age: int
```

这比手写 `__init__` 更简洁，适合 DTO、配置、内部结构化结果。

注意：`@dataclass` 是装饰器。它会帮类自动生成初始化、打印等基础方法。

## 4. 类与类的关系

常见关系有三种：

- 依赖：A 的某个方法临时使用 B。
- 组合：A 长期持有 B，A 的能力由 B 协作完成。
- 继承：A 是 B 的一种特殊类型。

优先级建议：

1. 能用函数解决，就先用函数。
2. 需要保存状态或组合依赖，再用类。
3. 需要表达稳定的“是一种”关系，再用继承。

## 5. 组合关系

组合是 Agent 工程里最常用的关系。

```python
class SafetyChecker:
    def is_high_risk(self, question: str) -> bool:
        return "不想活" in question


class ParentingAdvisor:
    def __init__(self, safety_checker: SafetyChecker) -> None:
        self.safety_checker = safety_checker

    def answer(self, question: str) -> str:
        if self.safety_checker.is_high_risk(question):
            return "这个情况需要立即寻求专业帮助。"
        return "先共情孩子，再一起拆小任务。"
```

调用关系：

```text
ParentingAdvisor.answer()
  -> SafetyChecker.is_high_risk()
```

Android 类比：`ParentingAdvisor` 像 use case，`SafetyChecker` 像被注入的 collaborator。

## 6. 继承关系

继承表达“子类是父类的一种”。

```python
class Message:
    def __init__(self, content: str) -> None:
        self.content = content


class UserMessage(Message):
    pass


class AssistantMessage(Message):
    pass
```

适合：

- 多种对象共享同一基础结构。
- 框架要求实现某个基类。
- 确实存在稳定的父子类型关系。

不适合：

- 只是为了复用几行代码。
- 业务变化很快。
- 类层级还没有稳定下来。

注意：Python 支持多继承，但初学阶段尽量少用。组合通常更清楚。

## 7. 接口与 Protocol

Python 没有像 Java/Kotlin 一样强制使用 `interface` 关键字。常见做法是用 `Protocol` 表达接口契约。

```python
from typing import Protocol


class LlmClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...
```

任何类只要实现了 `generate(self, prompt: str) -> str`，就可以被当成 `LlmClient` 使用。

```python
class FakeLlmClient:
    def generate(self, prompt: str) -> str:
        return "这是一个测试回答"
```

这很适合测试：

```python
class Advisor:
    def __init__(self, llm_client: LlmClient) -> None:
        self.llm_client = llm_client

    def answer(self, question: str) -> str:
        return self.llm_client.generate(question)
```

## 8. 静态方法、类方法、实例方法

实例方法最常见：

```python
class Counter:
    def __init__(self) -> None:
        self.value = 0

    def increase(self) -> None:
        self.value += 1
```

静态方法不依赖对象状态：

```python
class TextUtils:
    @staticmethod
    def normalize(text: str) -> str:
        return text.strip()
```

建议：初学阶段优先写普通函数或实例方法。不要为了“看起来像工具类”而滥用 `@staticmethod`。

## 9. 异常处理

```python
def parse_age(raw_age: str) -> int:
    try:
        return int(raw_age)
    except ValueError:
        raise ValueError("年龄必须是数字")
```

异常适合表达无法正常继续的情况。对于用户输入错误，要给出可理解的错误信息。

## 10. 中级练习

1. 定义 `ParentingQuestion` dataclass。
2. 定义 `SafetyChecker`。
3. 定义 `LlmClient` Protocol。
4. 定义 `FakeLlmClient`。
5. 定义 `ParentingAdvisor`，组合 `SafetyChecker` 和 `LlmClient`。
6. 写一个最小调用流程，输入问题，输出建议。


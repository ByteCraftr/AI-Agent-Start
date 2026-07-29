---
type: moc
topic: Python 学习
project: Parenting Copilot
status: active
tags:
  - python
  - learning
  - ai-agent
---

# Python 学习专题

这个目录专门补齐 Python 基础、中级和高级使用方式。它不是独立于 AI Agent 的语法手册，而是为了让后续实现 [[../000 AI Agent 学习首页|AI Agent 学习]]、[[../../product/agent-architecture|Parenting Copilot Agent 架构]] 时，能读懂代码、写出可维护的小模块，并逐步理解工程化 Python。

## 学习顺序

1. [[01-python-basic|基础：语法、类型、函数、调用、命名、判断]]
2. [[02-python-intermediate|中级：模块、类、关系、继承、接口、调用]]
3. [[03-python-advanced|高级：标准库、并发、线程、工程习惯]]
4. [[04-python-for-agent-engineering|面向 Agent 工程的 Python 使用建议]]
5. [[05-python-special-usages-for-llm-agent|特殊用法：LLM Agent 开发中要特别注意的写法]]
6. [[06-python-agent-naming-and-architecture|Agent 开发中的命名、架构和特殊写法]]

## 可运行代码

- [[../../labs/python-fundamentals/README|Python Fundamentals 可运行学习脚本]]

## 你要形成的能力

- 看到一段 Python 代码，能分辨变量、类型、函数、类、模块和调用关系。
- 能写出简单函数，把输入转换成明确输出。
- 能用类表达业务概念，但不过度面向对象。
- 能理解继承、组合、接口各自解决什么问题。
- 能知道常用标准库应该在哪里用，不急着引入第三方框架。
- 能理解线程适合什么场景，以及为什么 AI Agent 项目里更常见的是 I/O 并发。

## 和 Android 架构经验的对应关系

- Python 的模块文件类似 Android 项目里的一个职责清晰的 Kotlin 文件。
- Python 的函数类似纯业务函数或 use case 方法。
- Python 的类可以类比 ViewModel、Repository、Service、DTO，但 Python 更鼓励简单直接。
- Python 的 `Protocol` 可以类比接口契约。
- Python 的标准库类似 Android/Kotlin/JDK 自带能力，能先解决大量基础问题。

## 建议节奏

- 第一次：先读基础篇，重点理解类型、函数和 `if-else`。
- 第二次：读中级篇，重点理解类和调用关系。
- 第三次：读高级篇，重点理解常用标准库和线程边界。
- 写 Agent 代码前：读工程建议篇，避免把实验脚本写成不可维护的一大坨。

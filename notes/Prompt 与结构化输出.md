---
type: concept
topic: Prompt 与结构化输出
project: Parenting Copilot
status: draft
tags:
  - ai-agent
  - prompt-engineering
  - structured-output
  - validation
---

# Prompt 与结构化输出

## 它解决什么问题

Prompt 分层把 LLM 的输入设计成可维护的系统接口，而不是把所有要求堆进一整段提示词。

对 [[Parenting Copilot]] 来说，prompt 不只是“让模型说得更好”，而是控制 Agent 如何理解任务、遵守安全边界、使用上下文，并输出可被代码校验的 `ParentingAdvice`。

## 三层 Prompt

### System Prompt

`system prompt` 定义稳定的全局行为：

- Agent 的身份和角色。
- 亲子教育场景下的安全边界。
- 不做诊断、不替代专业人士的原则。
- 回答风格和总约束。

它类似项目里的 `AGENTS.md`、系统级架构约束或全局运行协议。

### Task Prompt

`task prompt` 定义本次请求：

- 家长提出的问题。
- 当前可用上下文。
- 本轮要完成的任务。
- 需要特别注意的场景信息。

它类似 application service 或 use case 收到的一次请求参数。用户输入变化时，主要变化的是这一层。

### Format Prompt

`format prompt` 定义输出契约：

- 必须输出 JSON。
- 必须符合 `ParentingAdvice` 字段。
- 枚举字段只能使用允许值。
- 不允许输出额外字段。

它类似 API response schema、DTO 或接口契约。代码后续会用本地校验器再次验证模型输出。

## 为什么不能混在一起

如果把角色、安全边界、任务说明和 JSON 格式都混在一段 prompt 里，后续修改会变得脆弱。

例如，只想调整输出字段时，可能不小心削弱安全约束；只想更换用户问题时，可能把格式要求带偏；只想优化语气时，也可能影响结构化输出稳定性。

拆分之后，每一层的变化边界更清楚：

```text
system prompt: 稳定行为边界
task prompt: 本次任务和上下文
format prompt: 输出合同
```

## 与结构化输出的关系

结构化输出定义了“代码期望收到什么”。Prompt 分层定义了“怎样把这个期望稳定地告诉模型”。

可靠链路是：

```text
ParentingAdvice schema
  -> format prompt 告诉模型输出合同
  -> LLM 生成 JSON
  -> 本地代码 parse + validate
  -> 通过后进入 UI、安全策略、评估或 Agent Loop
```

所以 prompt 约束不是最终可靠性来源。最终可靠性来自：prompt 约束、schema 声明、本地校验、失败处理一起工作。

## 不同 LLM 的结构化输出差异

JSON 这种格式思想是通用的。大多数 LLM 都可以通过 prompt 要求输出 JSON，因为 JSON 本质上仍然是文本。

但 API 层的结构化输出能力不是统一标准。不同模型和厂商需要看各自文档，常见差异包括：

- 是否支持 JSON mode。
- 是否支持 JSON Schema。
- 是否支持 strict schema。
- 是否支持 `enum`、`required`、`additionalProperties` 等约束。
- schema 应该写在哪个 API 参数里。
- 模型输出不符合 schema 时，API 是报错、自动修复，还是直接返回坏结果。
- streaming、tool calling 和 structured output 能否同时使用。

工程上应该把业务结构掌握在自己代码里：

```text
业务结构：ParentingAdvice
  -> 通用 schema / 本地校验器
  -> 针对不同 LLM API 做 adapter
  -> 调用后统一回到本地 validate
```

关键原则：

> JSON 格式是通用语言，但结构化输出 API 不是统一标准；可靠 Agent 应该把业务 schema 掌握在自己代码里，再针对不同 LLM 做适配。

即使某个模型支持 strict JSON Schema，本地校验也不能省。后续换模型、换供应商、开启 streaming 或接入 tool calling 时，API 行为都可能变化。

## 费曼复述

本次复述：

> Prompt 分层是为了方便分层管理和优化。`system prompt` 像系统 core，`task prompt` 像业务实现层，`format prompt` 像 API 接口。如果不拆分，就不好管理和维护。

修正后的架构表达：

> Prompt 分层的本质，是把 LLM 的输入设计成可维护的接口：system 管行为边界，task 管本次任务，format 管输出合同。这样 Parenting Copilot 才能在不同问题下保持稳定、安全、可校验。

## 验收结果

已实现：

```text
labs/w02-structured-output/prompt_templates.py
```

已验证：

```text
python3 -m py_compile labs/w02-structured-output/prompt_templates.py
python3 labs/w02-structured-output/prompt_templates.py
```

结果：

- Python 语法检查通过。
- 脚本能生成两个家长问题的 prompt messages。
- 修改用户输入时，`system prompt` 保持稳定。
- 修改用户输入时，`task prompt` 发生变化。
- 修改用户输入时，`format prompt` 保持稳定。

## 相关链接

- [[000 AI Agent 学习首页]]
- [[LLM 应用基础]]
- [[结构化输出]]

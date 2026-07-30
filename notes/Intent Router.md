---
type: concept
topic: Intent Router
project: Parenting Copilot
status: draft
tags:
  - ai-agent
  - intent-router
  - agent-loop
  - workflow
---

# Intent Router

## 它解决什么问题

Intent Router 让 Agent 在生成建议前，先判断用户问题属于哪类意图，再选择对应处理流程。

如果没有 Router，所有问题都会被塞进同一个回答流程。对 Parenting Copilot 来说，这会带来明显风险：学习问题、情绪问题、学校关系和高风险问题可能被当成同一种普通咨询处理。

## 三层理解

概念层：Intent Router 解决的是“先判断问题类型，再决定怎么处理”的分流问题。

工程层：Router 输出稳定的 `RouteResult`，包含 `intent`、`confidence`、`reason` 和 `safety_priority`。后续 Agent Loop 根据它选择 Handler。

产品层：Parenting Copilot 可以根据不同意图采用不同策略，例如学习问题强调任务拆解，情绪问题强调陪伴和情绪命名，高风险问题优先安全边界和专业支持。

## Router、Handler、Agent Loop

三者边界：

```text
Router 决定“去哪儿”
Handler 决定“怎么处理”
Agent Loop 决定“按什么顺序运行”
```

更完整的流程：

```text
用户输入
  -> Intent Router 判断问题类型
  -> Agent Loop 选择对应 Handler
  -> Handler 执行具体处理
  -> 结构化输出校验
  -> 返回结果或 fallback
```

Router 不应该生成完整建议，也不应该保存记忆或调用工具。它只负责做分流决策。

## 今天的工程边界

当前实验先使用规则分类器，不调用真实 LLM。这样做是为了先把 Agent 的模块边界跑通：

- 输入：用户的一段亲子教育问题。
- 输出：一个稳定的 `RouteResult`。
- 验收：10 个样例问题分类基本合理。

以后可以把规则分类器替换成 LLM classifier、embedding classifier 或混合分类器，但尽量保持 `RouteResult` 接口稳定。

## 关键发现

第一次验收时，`孩子考试前很焦虑` 被分到了 `learning`。这暴露了一个真实工程问题：路由规则不只是关键词匹配，还涉及优先级。

修正后，情绪信号优先于普通学习信号。高风险信号始终排在最前面。

## 费曼复述

用户复述：

```text
意图路由，先判断该问题是什么意图，先通过不同的意图，配置不同的执行流程，解决不同的问题情况。是有针对性的。这样效果会更好。Handler 执行的链路，根据不同的意图，执行不同的链路。Agent Loop 主进程，统一入口
```

校正：

```text
Handler 更准确地说不是“链路本身”，而是某条链路里的具体处理器。
Agent Loop 才是统一入口和主编排流程。
```

## 验收结果

运行：

```text
python3 -m py_compile labs/w03-agent-core/intent_router.py
python3 labs/w03-agent-core/intent_router.py
```

结果：

- Python 语法检查通过。
- 10 个样例全部通过。
- 高风险样例触发 `safety_priority=True`。

## 相关链接

- [[000 AI Agent 学习首页]]
- [[结构化输出]]
- [[Prompt 与结构化输出]]

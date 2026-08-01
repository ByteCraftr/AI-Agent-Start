# LLM 原理 for Agent Engineering

## 定位

这篇笔记不是研究型 LLM 课程，而是 Agent 工程课程的底层解释入口。

目标是回答一个问题：

```text
LLM 的模型行为边界，如何决定 Agent 的架构边界？
```

对于 Parenting Copilot，LLM 原理学习要服务于可靠、安全、可验证的产品能力，而不是停留在模型概念本身。

## 核心判断

LLM 可以生成高质量语言，但它不是规则引擎、事实数据库或可靠执行器。

因此 Agent 不能只写 prompt 后直接相信输出，而要通过代码建立边界：

- prompt 定义任务和约束。
- schema 定义输出契约。
- validator 检查结果能否进入业务流程。
- router 决定走哪条流程。
- context checker 判断信息是否足够。
- tool 执行确定性动作。
- memory/RAG 管理上下文来源。
- evaluator 判断版本是否真的变好。
- safety policy 处理越界和高风险场景。

## 专题学习小节

### 1. LLM 是预测器，不是规则引擎

要理解：

- LLM 根据上下文生成下一个 token。
- 它可以表现得像理解了问题，但不保证事实正确、格式稳定或永远遵守指令。

对应 Agent 设计：

- 不把模型输出当作最终事实。
- 对关键字段做结构化校验。
- 对高风险回答加安全策略和 fallback。

### 2. Token 与 Context Window

要理解：

- 模型看到的是 token 序列，不是人类意义上的完整记忆。
- 上下文窗口有限，历史可能被截断、压缩或污染。

对应 Agent 设计：

- Memory 不能等于把所有聊天历史塞回 prompt。
- RAG 需要选择相关片段，而不是无限追加资料。
- Parenting Copilot 的孩子画像、事件记忆和建议历史要有来源、类型和更新时间。

### 3. Prompt as Interface

要理解：

- Prompt 不是普通文案，而是模型调用接口。
- system、task、context、format、safety prompt 应该有清晰职责。

对应 Agent 设计：

- Prompt 要版本化。
- Prompt 输出要配合 schema。
- 修改 prompt 后需要 eval，而不是凭感觉判断变好。

### 4. 结构化输出为什么会失败

要理解：

- 模型可能漏字段、乱格式、编造枚举值、混入解释文本。
- JSON 解析成功不等于业务验证成功。

对应 Agent 设计：

- 使用 schema / Pydantic 做业务约束。
- 区分 parse error、validation error、safety error。
- 必要时 retry、repair 或 fallback。

### 5. Tool Calling 的本质

要理解：

- 模型适合判断“是否需要调用工具”和生成候选参数。
- 代码必须负责权限、参数校验、执行、幂等和错误处理。

对应 Agent 设计：

- 工具 schema 要窄而清晰。
- 工具结果要进入 trace。
- Parenting Copilot 中读取孩子档案、生成观察计划、检索资料等动作要有边界。

### 6. 为什么 Agent 必须有 Evaluation

要理解：

- 单个样例的成功不能证明 Agent 可靠。
- Prompt、模型、上下文和工具改动都可能造成回归。

对应 Agent 设计：

- 建立覆盖普通、复杂、高风险场景的 eval set。
- 用 rubric 评估具体性、安全性、可执行性和专业边界。
- 对 Parenting Copilot，安全性和不越界比“回答很像专家”更重要。

## 与学习地图的关系

这个专题放在：

```text
Phase 1: LLM Application Foundation
  -> 横向专题: LLM 原理 for Agent Engineering
  -> Phase 2: Prompt & Structured Output
```

它会支撑后续主题：

- Prompt 与结构化输出：为什么需要接口契约和校验。
- Agent Core：为什么需要 router、state、clarifying questions。
- Tool Use：为什么代码要执行和验证工具调用。
- Memory：为什么记忆需要选择、确认和更新策略。
- RAG：为什么引用来源不等于回答一定可靠。
- Evaluation：为什么不能靠感觉判断 Agent 质量。
- Safety：为什么高风险场景需要流程边界，而不是只靠提示词。

## Parenting Copilot 的应用原则

- 信息不足时先追问。
- 事实、假设、建议和风险信号要分开表达。
- 高风险问题先安全分级，再决定是否回答。
- 对孩子和家长画像的记忆必须有来源和确认机制。
- 任何 prompt 或模型调整，都要通过代表性样例验证。

## 费曼复述问题

- 为什么说 LLM 不是规则引擎？
- 为什么 prompt 不能替代 schema validation？
- 为什么 Memory 不能只是保存全部聊天记录？
- 为什么 Tool Calling 中代码仍然是最终执行边界？
- 为什么 Parenting Copilot 比普通聊天机器人更需要 evaluation 和 safety？

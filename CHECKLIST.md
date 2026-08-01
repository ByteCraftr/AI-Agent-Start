# AI Agent 三个月学习清单

这份清单是 3 个月的可执行任务池，不按天编号。每天从当前周领取一个任务，按 `AGENTS.md` 的流程完成：

```text
define-goal 明确目标
  -> 学概念
  -> 做最小实验
  -> 验收结果
  -> 写 Obsidian 笔记
  -> 更新周复盘
```

完成任务时，把 `[ ]` 改成 `[x]`。如果任务较大，可以拆成多次完成，但要在周复盘里记录卡点。

## 三个月目标

3 个月后，你应该完成：

- 能解释 AI Agent 的核心机制：LLM、prompt、structured output、agent loop、tool use、memory、RAG、evaluation、safety。
- 能手写一个可运行的 Parenting Copilot Agent 原型。
- 能把 Agent 封装成基础后端服务。
- 能设计亲子教育 Agent 的记忆、安全、评估和产品化方案。
- 能形成 Obsidian 知识体系、项目 README、架构文档和作品集雏形。

## Month 1: Agent 基础闭环

目标：先跑通一个最小但完整的 Agent，从 LLM 调用到结构化输出、路由、追问和最小 Agent Loop。

### Week 1: Learning System + LLM Foundation

- [x] W1-T1: 建立学习系统与 Obsidian Vault
  - 目标：确认这个项目如何作为长期学习系统运行。
  - 你要理解：清单驱动、目标定义、Obsidian 双链、周复盘。
  - 你要实现：打开当前项目为 Obsidian Vault，并从 `notes/000 AI Agent 学习首页.md` 进入学习。
  - 验收标准：能说明 `CHECKLIST.md`、`ROADMAP.md`、`AGENTS.md`、`notes/`、`labs/`、`product/` 各自作用。
  - Obsidian 笔记：写一篇每日学习笔记。
  - 复盘问题：为什么学习 Agent 不能只靠看教程？

- [x] W1-T2: 实现第一个 LLM API 调用
  - 目标：理解一次 LLM 调用的完整链路。
  - 你要理解：model、messages、temperature、max tokens、API key、错误处理。
  - 你要实现：`labs/w01-llm-foundation/parenting_advisor.py`。
  - 验收标准：输入一个亲子教育问题，能得到模型回答。
  - Obsidian 笔记：新增或更新 `LLM 应用基础`。
  - 复盘问题：一次 LLM 调用和普通 HTTP API 调用有什么相同和不同？

- [x] W1-T3: 比较模型参数对输出的影响
  - 目标：理解输出稳定性如何受参数影响。
  - 你要理解：temperature、top_p、max tokens、streaming。
  - 你要实现：对同一问题运行多组参数并记录输出差异。
  - 验收标准：能解释为什么教育类建议更需要稳定输出。
  - Obsidian 笔记：记录参数对比表。
  - 复盘问题：什么时候应该让模型更发散，什么时候应该更稳定？

### Week 1 专题: LLM 原理 for Agent Engineering

- [ ] W1-S1: 从 LLM 原理理解 Agent 设计边界
  - 目标：理解 LLM 的工程行为边界，并把它映射到 Agent 架构设计。
  - 你要理解：next-token prediction、token/context window、prompt as interface、结构化输出漂移、tool calling 分工、evaluation 必要性。
  - 你要实现：完成 `notes/LLM 原理 for Agent Engineering.md` 的费曼复述，并补充 1 个 Parenting Copilot 场景映射。
  - 验收标准：能说明为什么可靠 Agent 不能只靠 prompt，以及至少 3 个“LLM 原理 -> Agent 设计边界”的例子。
  - Obsidian 笔记：更新 `LLM 原理 for Agent Engineering`。
  - 复盘问题：我以前把哪些 LLM 能力误认为了确定性能力？

### Week 2: Prompt & Structured Output

- [x] W2-T1: 设计 ParentingAdvice 结构化输出
  - 目标：把 Agent 的回答从自然语言变成可验证结构。
  - 你要理解：JSON schema、Pydantic、类型约束、输出契约。
  - 你要实现：`ParentingAdvice`、`RiskLevel`、`AdviceCategory`。
  - 验收标准：模型输出可以被代码校验。
  - Obsidian 笔记：新增 `结构化输出`。
  - 复盘问题：结构化输出如何降低 Agent 的不可控性？

- [x] W2-T2: 拆分 Prompt 职责
  - 目标：把 prompt 设计成可维护的系统接口。
  - 你要理解：角色、任务、上下文、约束、输出格式、示例。
  - 你要实现：system prompt、task prompt、format prompt 的分层模板。
  - 验收标准：修改用户输入时，输出结构仍稳定。
  - Obsidian 笔记：新增 `Prompt 与结构化输出`。
  - 复盘问题：prompt 和传统代码里的接口契约有什么相似和不同？

- [x] W2-T3: 实现输出校验与失败重试
  - 目标：让 Agent 面对坏输出时能恢复。
  - 你要理解：validation、retry、repair prompt、fallback。
  - 你要实现：非法 JSON 检测、重试或修复流程。
  - 验收标准：故意制造坏输出时，程序能给出可理解的错误或自动修复。
  - Obsidian 笔记：记录失败样例和修复策略。
  - 复盘问题：为什么可靠 Agent 不能只假设模型永远按格式输出？

### Week 3: Agent Core

- [x] W3-T1: 实现 Intent Router
  - 目标：让 Agent 先判断问题类型，再决定处理方式。
  - 你要理解：intent classification、routing、workflow。
  - 你要实现：学习问题、情绪问题、亲子沟通、行为习惯、学校关系、高风险问题分类。
  - 验收标准：10 个样例问题分类基本合理。
  - Obsidian 笔记：新增 `Intent Router`。
  - 复盘问题：为什么复杂 Agent 需要路由，而不是直接回答？

- [x] W3-T2: 实现信息充分性判断与追问
  - 目标：让 Agent 在信息不足时先追问。
  - 你要理解：clarifying questions、slot filling、多轮状态。
  - 你要实现：判断缺少年龄、持续时间、场景、家长目标时自动追问。
  - 验收标准：信息不足时输出追问；信息充分时输出建议。
  - Obsidian 笔记：新增 `澄清问题`。
  - 复盘问题：可靠 Agent 如何处理“不知道”？

- [ ] W3-T3: 手写最小 Agent Loop
  - 目标：实现 observe、reason、act、persist 的基础循环。
  - 你要理解：agent loop、state、action、persistence。
  - 你要实现：`ParentingAgent.run(input)`。
  - 验收标准：一次输入能经过分类、判断、生成、记录四步。
  - Obsidian 笔记：新增 `Agent Loop`。
  - 复盘问题：Agent Loop 和普通函数调用有什么区别？

### Week 4: Tools + Month 1 Demo

- [ ] W4-T1: 实现第一个 Tool Calling
  - 目标：让 Agent 能调用外部能力。
  - 你要理解：tool schema、参数生成、工具结果回填。
  - 你要实现：`get_child_profile` 工具。
  - 验收标准：Agent 能根据问题决定是否读取孩子档案。
  - Obsidian 笔记：新增 `Tool Calling`。
  - 复盘问题：工具调用为什么是 Agent 从聊天走向行动的关键？

- [ ] W4-T2: 实现一周观察计划工具
  - 目标：把部分确定性逻辑交给代码。
  - 你要理解：工具边界、确定性逻辑、LLM 与代码协作。
  - 你要实现：`create_weekly_plan` 工具。
  - 验收标准：输出计划包含目标、行动、观察点、反馈方式。
  - Obsidian 笔记：记录“代码负责什么，模型负责什么”。
  - 复盘问题：哪些逻辑不应该交给模型自由发挥？

- [ ] W4-T3: 完成 Month 1 最小 Demo
  - 目标：把 LLM、结构化输出、路由、追问、工具调用串起来。
  - 你要理解：端到端链路、最小可用闭环。
  - 你要实现：命令行版 Parenting Copilot v0.1。
  - 验收标准：能处理一个完整亲子教育问题，并输出结构化建议。
  - Obsidian 笔记：写 Month 1 总结。
  - 复盘问题：这个 Demo 离“可靠 Agent”还差什么？

## Month 2: 可靠 Agent 核心

目标：把 Agent 从“能回答”升级为“更可靠”：加入记忆、知识库、评估和安全边界。

### Week 5: Memory System

- [ ] W5-T1: 设计孩子与家长画像
  - 目标：定义长期陪伴型 Agent 的基础记忆结构。
  - 你要理解：profile memory、preference memory、privacy。
  - 你要实现：Child Profile、Parent Profile、Family Context 模型。
  - 验收标准：Agent 回答时能引用基础画像。
  - Obsidian 笔记：新增 `Memory 长期记忆系统`。
  - 复盘问题：长期记忆如何提升个性化，又会带来哪些风险？

- [ ] W5-T2: 实现对话后的记忆提取
  - 目标：从对话中提取值得保存的信息。
  - 你要理解：memory extraction、事实与推测分离、confidence。
  - 你要实现：提取新事实、观察、偏好、后续跟进点。
  - 验收标准：记忆内容标注来源、类型和置信度。
  - Obsidian 笔记：记录记忆提取样例。
  - 复盘问题：为什么不能把所有对话都塞进长期记忆？

- [ ] W5-T3: 设计记忆更新确认机制
  - 目标：避免错误记忆直接污染用户画像。
  - 你要理解：human confirmation、memory update policy。
  - 你要实现：待确认记忆、确认后写入、拒绝后丢弃的流程。
  - 验收标准：重要记忆写入前有明确确认点。
  - Obsidian 笔记：写一条记忆策略决策记录。
  - 复盘问题：AI 产品中的“记住”为什么也是一种风险？

### Week 6: RAG & Knowledge System

- [ ] W6-T1: 建立最小教育知识库
  - 目标：让 Agent 基于资料回答，而不是只依赖模型常识。
  - 你要理解：document parsing、chunking、embedding、vector search。
  - 你要实现：导入 3-5 篇教育资料或自己的笔记。
  - 验收标准：能检索到与问题相关的资料片段。
  - Obsidian 笔记：新增 `RAG 与知识库`。
  - 复盘问题：RAG 解决了什么问题，又不能解决什么问题？

- [ ] W6-T2: 实现带引用的建议输出
  - 目标：让回答包含依据和来源。
  - 你要理解：citation、context packing、grounded answer。
  - 你要实现：回答中输出“建议、依据、来源、不确定性”。
  - 验收标准：每条关键建议至少能关联一个来源或明确说明不确定。
  - Obsidian 笔记：记录一次带引用回答样例。
  - 复盘问题：引用来源是否等于回答一定可靠？

- [ ] W6-T3: 比较检索策略
  - 目标：理解检索质量如何影响最终回答。
  - 你要理解：query rewrite、hybrid search、rerank。
  - 你要实现：对同一问题比较至少两种检索策略。
  - 验收标准：能解释哪种结果更适合当前问题。
  - Obsidian 笔记：记录检索对比表。
  - 复盘问题：RAG 系统最容易失败在哪里？

### Week 7: Evaluation

- [ ] W7-T1: 建立 50 条亲子教育评估样例
  - 目标：用测试集评估 Agent，而不是靠感觉。
  - 你要理解：eval dataset、rubric、expected behavior。
  - 你要实现：覆盖普通、复杂、高风险场景的 50 条样例。
  - 验收标准：每条样例都有问题类型、期望行为、评分维度。
  - Obsidian 笔记：新增 `Evaluation 与安全`。
  - 复盘问题：AI 产品为什么必须有评估集？

- [ ] W7-T2: 设计评分规则
  - 目标：让回答质量可比较。
  - 你要理解：rubric、LLM-as-judge、人工评估边界。
  - 你要实现：具体性、安全性、尊重孩子、可执行性、专业边界评分。
  - 验收标准：能对 10 条回答给出一致评分。
  - Obsidian 笔记：记录评分规则。
  - 复盘问题：什么样的回答看似有帮助但其实危险？

- [ ] W7-T3: 做一次 Prompt 版本对比
  - 目标：用评估结果驱动 prompt 迭代。
  - 你要理解：regression test、prompt versioning。
  - 你要实现：对比两个 prompt 版本在测试集上的表现。
  - 验收标准：能说明哪个版本更好以及为什么。
  - Obsidian 笔记：写 Prompt 版本对比记录。
  - 复盘问题：为什么不能只凭一两个样例判断 prompt 好坏？

### Week 8: Safety & Trust

- [ ] W8-T1: 设计安全分级策略
  - 目标：让 Agent 在敏感场景下有明确边界。
  - 你要理解：risk classification、guardrail、professional boundary。
  - 你要实现：普通、复杂、高风险、紧急四级响应策略。
  - 验收标准：高风险问题不会给出越界建议。
  - Obsidian 笔记：新增 `Safety Policy`。
  - 复盘问题：教育类 Agent 最应该避免哪几类伤害？

- [ ] W8-T2: 实现 Risk Classifier
  - 目标：在生成建议前识别风险等级。
  - 你要理解：risk signal、fallback、human-in-the-loop。
  - 你要实现：风险识别模块和安全响应模板。
  - 验收标准：霸凌、心理健康、家庭冲突等样例能触发对应策略。
  - Obsidian 笔记：记录高风险样例。
  - 复盘问题：什么时候 Agent 应该少说，而不是多说？

- [ ] W8-T3: 完成 Month 2 可靠性 Demo
  - 目标：把记忆、RAG、评估和安全串进 Agent。
  - 你要理解：可靠 Agent 的最小组成。
  - 你要实现：Parenting Copilot v0.2。
  - 验收标准：能基于画像和知识库回答，并经过风险判断。
  - Obsidian 笔记：写 Month 2 总结。
  - 复盘问题：当前系统的最大不可靠来源是什么？

## Month 3: 产品化、移动端和作品集

目标：把学习项目推向可展示、可试用、可讲述的产品原型。

### Week 9: Product Engineering

- [ ] W9-T1: 封装 FastAPI Agent Service
  - 目标：把命令行 Agent 变成可调用后端服务。
  - 你要理解：API contract、request/response model、error handling。
  - 你要实现：`POST /advice` 或类似接口。
  - 验收标准：可以通过 HTTP 调用 Agent。
  - Obsidian 笔记：新增 `Agent Backend`。
  - 复盘问题：Agent Backend 和普通业务后端有什么不同？

- [ ] W9-T2: 设计数据库与日志
  - 目标：保存对话、记忆、评估和工具调用。
  - 你要理解：PostgreSQL、conversation log、tool log、cost tracking。
  - 你要实现：核心数据库 schema 或文档版 schema。
  - 验收标准：能说明每类数据为什么要保存。
  - Obsidian 笔记：写数据库设计决策。
  - 复盘问题：哪些数据不应该保存？

- [ ] W9-T3: 加入可观测性和成本意识
  - 目标：理解 Agent 服务如何运维。
  - 你要理解：logging、tracing、latency、token cost、rate limit。
  - 你要实现：请求日志、工具日志、token 成本记录。
  - 验收标准：一次请求能追踪主要步骤和成本。
  - Obsidian 笔记：记录一次请求 trace。
  - 复盘问题：为什么 Agent 产品需要比普通应用更重视可观测性？

### Week 10: Frameworks + Android Integration

- [ ] W10-T1: 对比手写 Agent 与框架 Agent
  - 目标：理解什么时候需要 LangGraph / AutoGen / CrewAI 等框架。
  - 你要理解：workflow graph、checkpoint、multi-agent、framework tradeoff。
  - 你要实现：选择一个框架重写最小流程，或写框架对比文档。
  - 验收标准：能说明是否应该在 Parenting Copilot v0.1 使用框架。
  - Obsidian 笔记：写框架选型决策。
  - 复盘问题：框架解决了什么，又隐藏了什么？

- [ ] W10-T2: 设计 Android 与 Agent Backend 的接口
  - 目标：把你的 Android 架构经验接入 Agent 产品。
  - 你要理解：API contract、streaming response、offline cache、state sync。
  - 你要实现：Android API contract 文档。
  - 验收标准：能说明 Android 端和后端各自职责。
  - Obsidian 笔记：新增 `Android Integration`。
  - 复盘问题：哪些 Agent 状态应该在服务端，哪些可以在客户端？

- [ ] W10-T3: 设计移动端核心页面
  - 目标：形成 Parenting Copilot 的移动端产品雏形。
  - 你要理解：conversation UI、growth profile、feedback loop、reminder。
  - 你要实现：信息架构或低保真页面说明。
  - 验收标准：至少包含提问、建议、成长档案、反馈四个关键场景。
  - Obsidian 笔记：写移动端产品设计记录。
  - 复盘问题：长期陪伴型 Agent 的 UI 和普通聊天框有什么不同？

### Week 11: Parenting Copilot MVP

- [ ] W11-T1: 定义 v0.1 MVP 范围
  - 目标：明确第一个可展示版本做什么、不做什么。
  - 你要理解：MVP、scope control、user journey。
  - 你要实现：更新 `product/parenting-copilot-prd.md`。
  - 验收标准：v0.1 功能范围、非目标、验收标准清楚。
  - Obsidian 笔记：写产品范围决策。
  - 复盘问题：哪些功能看起来重要，但现在应该先不做？

- [ ] W11-T2: 完成端到端 Demo 脚本
  - 目标：让项目可以被别人看懂和试用。
  - 你要理解：demo story、happy path、edge case。
  - 你要实现：一个完整演示脚本和样例输入输出。
  - 验收标准：5 分钟内能讲清楚产品价值和技术链路。
  - Obsidian 笔记：记录 demo 讲述方式。
  - 复盘问题：好的 demo 应该展示能力，还是展示价值？

- [ ] W11-T3: 收集 3-5 个真实场景反馈
  - 目标：让产品假设接受现实检验。
  - 你要理解：user feedback、problem interview、iteration。
  - 你要实现：记录 3-5 个真实家长问题或访谈结果。
  - 验收标准：能把反馈转化为 eval 样例或产品需求。
  - Obsidian 笔记：写用户反馈记录。
  - 复盘问题：真实用户问题和我们想象的有什么不同？

### Week 12: Portfolio + Startup Validation

- [ ] W12-T1: 完成项目 README 作品集版
  - 目标：把学习项目变成能展示的作品。
  - 你要理解：project storytelling、architecture summary、tradeoff。
  - 你要实现：更新 `README.md`，包含项目目标、架构、能力、运行方式、演示。
  - 验收标准：陌生工程师能通过 README 理解项目价值。
  - Obsidian 笔记：写作品集整理笔记。
  - 复盘问题：这个项目最能证明你的哪种能力？

- [ ] W12-T2: 准备 Agent 系统设计讲稿
  - 目标：能在面试或交流中讲清楚 Agent 架构。
  - 你要理解：system design、tradeoff、reliability、safety。
  - 你要实现：5-10 分钟讲稿或架构文章大纲。
  - 验收标准：能讲清楚为什么这样设计，而不只是说用了哪些工具。
  - Obsidian 笔记：新增 `Android 架构师如何理解 AI Agent 架构`。
  - 复盘问题：Android 架构经验如何迁移到 Agent 工程？

- [ ] W12-T3: 做创业验证计划
  - 目标：判断 Parenting Copilot 是否有真实产品机会。
  - 你要理解：problem interview、user segment、value proposition、risk。
  - 你要实现：5-10 位家长访谈计划和问题清单。
  - 验收标准：能区分学习项目、作品集项目和创业产品的不同目标。
  - Obsidian 笔记：写创业验证决策记录。
  - 复盘问题：家长会为什么能力付费，而不只是觉得有趣？

- [ ] W12-T4: 三个月总复盘
  - 目标：总结能力增长和下一阶段方向。
  - 你要理解：复盘、取舍、能力地图更新。
  - 你要实现：三个月总结文档。
  - 验收标准：明确下一阶段是求职、产品化、创业验证还是技术深入。
  - Obsidian 笔记：写季度复盘。
  - 复盘问题：这三个月最值得继续投入的方向是什么？

## 领取任务规则

每次学习开始时，说：

```text
今天领取 CHECKLIST 里的下一个任务，带我完成。
```

Codex 应该：

1. 找到当前最靠前的未完成任务。
2. 用 `define-goal` 思路改写今日目标。
3. 询问学习模式：概念优先、代码优先、架构优先、复盘优先。
4. 完成最小实验或文档产物。
5. 做验收。
6. 更新 Obsidian 笔记和周复盘。

## 调整规则

- 如果某周任务太多，可以延长，不需要硬赶进度。
- 如果某个主题已经掌握，可以跳过或改为复盘任务。
- 如果 Parenting Copilot 出现更真实的产品方向，优先调整任务以服务项目。
- 每个月结束时，可以根据复盘重排下一月任务。

# Week 01 Review

## 本周目标

- 完成 LLM 应用最小闭环。
- 理解结构化输出。
- 建立 Parenting Copilot v0.1 的最小模型。

## 完成的任务

- [x] Day 00: 建立学习仓库与工作流
- [x] W1-T2: 实现第一个 LLM API 调用
- [x] W1-T3: 比较模型参数对输出的影响
- [x] W2-T1: 设计 ParentingAdvice 结构化输出
- [x] W2-T2: 拆分 Prompt 职责
- [x] W2-T3: 实现输出校验与失败重试
- [x] W3-T1: 实现 Intent Router

## 本周关键理解

- AI Agent 学习不能只靠看教程，需要形成“任务、目标、产物、验收、复盘”的闭环。
- 当前仓库可以作为 Obsidian Vault 使用，入口是 `notes/000 AI Agent 学习首页.md`。
- `CHECKLIST.md` 负责每天领取任务，`ROADMAP.md` 负责能力地图，`AGENTS.md` 负责协作规则，`notes/` 负责长期知识沉淀，`labs/` 负责代码实验，`product/` 负责 Parenting Copilot 产品和架构资产。
- LLM API 调用和普通 HTTP API 调用类似，都需要认证、请求体、响应解析和错误处理；不同点是 LLM 输出是概率生成结果，需要额外关注参数、prompt、安全边界和后续校验。
- 模型参数影响输出稳定性、完整性和交互体验：`max_output_tokens` 太小会破坏可用性，`temperature/top_p` 属于模型支持能力，`streaming` 主要改善等待体验而不是内容可靠性。
- 结构化输出让 Agent 的回答从自然语言文本变成可验证合同。`ParentingAdvice`、`RiskLevel`、`AdviceCategory` 让后续 UI、安全策略、评估和 Agent Loop 可以依赖明确字段，而不是猜模型文本含义。
- `Enum` 可以限制模型输出的类别和风险等级；`TypeVar("EnumT", bound=Enum)` 用来表达一个泛型枚举校验函数，传入 `RiskLevel` 就返回 `RiskLevel`，传入 `AdviceCategory` 就返回 `AdviceCategory`。
- LLM 不会自动知道 Python 里的 `ParentingAdvice`，需要把结构转换成 JSON Schema，并通过 prompt 或 API structured output 参数传给模型；本地仍然需要再次校验。
- Streaming 主要改善等待体验。可以边接收边显示草稿，但正式业务状态必须等完整输出拼接、JSON parse 和 `ParentingAdvice` 校验通过后再产生。
- Prompt 分层让 LLM 输入成为可维护接口：`system prompt` 管稳定身份和安全边界，`task prompt` 管本次问题，`format prompt` 管输出合同。
- 可靠 Agent 不能假设模型永远按格式输出。模型原始输出要先 parse，再 validate；包装问题可以有限修复，业务字段错误不能用默认值掩盖。
- 修复失败后的 fallback 不是假装成功，而是停止保存记忆、调用工具、进入正式建议卡片等危险流程，并给家长保守、可理解的下一步。
- Intent Router 让 Agent 在生成建议前先判断问题类型，再选择不同处理流程。Router 决定“去哪儿”，Handler 决定“怎么处理”，Agent Loop 决定“按什么顺序运行”。
- 路由规则有优先级问题：高风险信号必须优先，情绪信号也应优先于普通学习信号，否则“考试焦虑”这类问题会被普通学习流程截走。

## 本周代码产物

- Day 00 无代码产物，产物是学习系统说明与每日学习笔记。
- W1-T2 初版代码产物：`labs/w01-llm-foundation/parenting_advisor.py`，用于演示最小 LLM API 调用链路。
- W1-T3 参数实验产物：`labs/w01-llm-foundation/parameter_experiment.py` 和 `labs/w01-llm-foundation/parameter_experiment_results.md`，用于对比同一问题在不同参数下的请求形态和输出结果。
- W2-T1 结构化输出产物：`labs/w02-structured-output/parenting_advice_schema.py`，用于定义并校验 `ParentingAdvice` 输出契约。
- W2-T2 Prompt 分层产物：`labs/w02-structured-output/prompt_templates.py`，用于演示 system/task/format prompt 的职责拆分。
- W2-T3 输出恢复产物：`labs/w02-structured-output/output_repair.py`，用于演示 parse、validate、有限修复和 fallback。
- W3-T1 Intent Router 产物：`labs/w03-agent-core/intent_router.py`，用于演示用户输入到处理流程的最小分流。
- W2-T1 概念笔记：`notes/结构化输出.md`。
- W3-T1 概念笔记：`notes/Intent Router.md`。

## 本周卡点

- `gpt-5-mini` 不支持 `temperature` 和 `top_p` 参数，脚本已改为默认不发送采样参数；专门比较采样策略时需要选择支持这些参数的模型。
- 过小的 `max_output_tokens` 可能导致没有可提取文本，后续脚本可以记录完整响应状态辅助诊断。
- API key 不能写入代码，应始终通过环境变量读取。
- 后续需要避免只写 demo、不做验收和复盘。
- 当前环境没有安装 Pydantic，因此 W2-T1 先使用标准库 `Enum`、`dataclass` 和手写校验完成最小实验；后续可以切换到 Pydantic 自动生成 JSON Schema 和校验错误。
- LLM repair 后仍然必须再次 parse 和 validate，不能因为“已经修复过”就直接进入业务成功路径。
- Handler 容易被误解成“执行链路本身”。更准确的边界是：Handler 是某条链路里的具体处理器，Agent Loop 才是统一入口和主编排流程。

## 下周调整

- 每次任务结束时都补齐每日笔记、验收结果和复盘问题，让学习结果能持续沉淀。

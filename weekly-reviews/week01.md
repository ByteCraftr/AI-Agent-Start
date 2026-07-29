# Week 01 Review

## 本周目标

- 完成 LLM 应用最小闭环。
- 理解结构化输出。
- 建立 Parenting Copilot v0.1 的最小模型。

## 完成的任务

- [x] Day 00: 建立学习仓库与工作流
- [x] W1-T2: 实现第一个 LLM API 调用
- [x] W1-T3: 比较模型参数对输出的影响
- [ ] W2-T1: 设计 ParentingAdvice 结构化输出
- [ ] W2-T2: 拆分 Prompt 职责
- [ ] W2-T3: 实现输出校验与失败重试

## 本周关键理解

- AI Agent 学习不能只靠看教程，需要形成“任务、目标、产物、验收、复盘”的闭环。
- 当前仓库可以作为 Obsidian Vault 使用，入口是 `notes/000 AI Agent 学习首页.md`。
- `CHECKLIST.md` 负责每天领取任务，`ROADMAP.md` 负责能力地图，`AGENTS.md` 负责协作规则，`notes/` 负责长期知识沉淀，`labs/` 负责代码实验，`product/` 负责 Parenting Copilot 产品和架构资产。
- LLM API 调用和普通 HTTP API 调用类似，都需要认证、请求体、响应解析和错误处理；不同点是 LLM 输出是概率生成结果，需要额外关注参数、prompt、安全边界和后续校验。
- 模型参数影响输出稳定性、完整性和交互体验：`max_output_tokens` 太小会破坏可用性，`temperature/top_p` 属于模型支持能力，`streaming` 主要改善等待体验而不是内容可靠性。

## 本周代码产物

- Day 00 无代码产物，产物是学习系统说明与每日学习笔记。
- W1-T2 初版代码产物：`labs/w01-llm-foundation/parenting_advisor.py`，用于演示最小 LLM API 调用链路。
- W1-T3 参数实验产物：`labs/w01-llm-foundation/parameter_experiment.py` 和 `labs/w01-llm-foundation/parameter_experiment_results.md`，用于对比同一问题在不同参数下的请求形态和输出结果。

## 本周卡点

- `gpt-5-mini` 不支持 `temperature` 和 `top_p` 参数，脚本已改为默认不发送采样参数；专门比较采样策略时需要选择支持这些参数的模型。
- 过小的 `max_output_tokens` 可能导致没有可提取文本，后续脚本可以记录完整响应状态辅助诊断。
- API key 不能写入代码，应始终通过环境变量读取。
- 后续需要避免只写 demo、不做验收和复盘。

## 下周调整

- 每次任务结束时都补齐每日笔记、验收结果和复盘问题，让学习结果能持续沉淀。

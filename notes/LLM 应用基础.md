---
type: concept
topic: LLM 应用基础
project: Parenting Copilot
status: draft
tags:
  - ai-agent
  - llm
  - api
---

# LLM 应用基础

## 它解决什么问题

LLM API 让应用可以把自然语言理解、生成、归纳、改写等能力接入到产品流程里。对 [[Parenting Copilot]] 来说，第一次 API 调用是整个 Agent 的起点：先让系统能接收一个亲子教育问题，并返回一段有边界的建议。

## 一次调用的核心组成

- `model`：选择使用哪个模型能力。
- `messages/input`：传给模型的上下文，包括用户问题和必要的角色约束。
- `temperature`：控制输出随机性；教育建议类任务通常先用较低值，追求稳定。
- `top_p`：控制候选 token 的概率范围；范围越窄，输出通常越保守。
- `max_output_tokens`：控制回答长度和成本。
- `streaming`：控制返回方式，让用户更早看到输出，但不改变回答质量本身。
- `API key`：调用身份凭证，必须从环境变量读取，不写死到代码里。
- 错误处理：处理缺少 key、网络失败、鉴权失败、限流、返回格式异常等情况。

## 参数对输出的影响

[[Parenting Copilot]] 默认应该偏稳定：足够的 `max_output_tokens`、明确的安全边界、不要为了“有创意”而牺牲可预测性。

W1-T3 的实验记录在 `labs/w01-llm-foundation/parameter_experiment_results.md`：

- `max_output_tokens` 太小会破坏可用性，可能导致回答不完整或没有可提取文本。
- `temperature` 和 `top_p` 不是所有模型都支持；参数能力属于模型契约。
- `streaming` 适合改善等待体验，但可靠性仍要靠 prompt、结构化输出、校验、重试和评估。

## 和普通 HTTP API 的相同点

它们都需要请求地址、认证、请求体、响应体、超时和错误处理。工程上都应该封装调用边界，避免业务代码散落网络细节。

## 和普通 HTTP API 的不同点

普通业务 API 通常返回稳定结构，LLM API 返回的是概率生成结果。即使输入相同，输出也可能不同。因此 Agent 工程需要额外关注 prompt 约束、参数控制、结构化输出、校验、重试和评估。

## Parenting Copilot 的产品含义

亲子教育建议不能只追求“像人一样会说”，还要追求稳定、尊重孩子、可执行、有安全边界。第一次 LLM 调用先放入最小安全提示词：不诊断、不替代专业人员、遇到高风险场景建议寻求帮助。

## 相关链接

- [[000 AI Agent 学习首页]]
- [[Agent Loop]]

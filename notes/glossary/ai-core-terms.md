# AI 核心术语表

这个文件用于保存 AI Agent 学习中的主干术语。格式采用学习卡片，而不是大表格：先看英文和全称，再用中文解释建立直觉。

## 总览索引

| 分类     | English            | Full name                         | 中文        |
| ------ | ------------------ | --------------------------------- | --------- |
| 基础概念   | AI                 | Artificial Intelligence           | 人工智能      |
| 基础概念   | Model              | Model                             | 模型        |
| 基础概念   | LLM                | Large Language Model              | 大语言模型     |
| 基础概念   | Token              | Token                             | 词元        |
| 基础概念   | Context Window     | Context Window                    | 上下文窗口     |
| Prompt | Prompt             | Prompt                            | 提示词 / 提示  |
| Prompt | System Prompt      | System Prompt                     | 系统提示词     |
| Prompt | User Prompt        | User Prompt                       | 用户提示词     |
| Prompt | Few-shot Prompting | Few-shot Prompting                | 少样本提示     |
| 模型参数   | Temperature        | Temperature                       | 温度        |
| 模型参数   | Max Tokens         | Maximum Tokens                    | 最大输出词元数   |
| 模型参数   | Top-p              | Nucleus Sampling / Top-p Sampling | 核采样       |
| 输出控制   | Structured Output  | Structured Output                 | 结构化输出     |
| 输出控制   | JSON Mode          | JavaScript Object Notation Mode   | JSON 模式   |
| 输出控制   | Schema             | Schema                            | 模式 / 结构定义 |
| Agent  | Agent              | Agent                             | 智能体       |
| Agent  | Agent Loop         | Agent Loop                        | 智能体循环     |
| Agent  | Tool Calling       | Tool Calling                      | 工具调用      |
| Agent  | Function Calling   | Function Calling                  | 函数调用      |
| 知识与记忆  | Memory             | Memory                            | 记忆        |
| 知识与记忆  | RAG                | Retrieval-Augmented Generation    | 检索增强生成    |
| 知识与记忆  | Embedding          | Embedding                         | 向量表示      |
| 知识与记忆  | Vector Database    | Vector Database                   | 向量数据库     |
| 评估与安全  | Evaluation         | Evaluation                        | 评估        |
| 评估与安全  | Guardrail          | Guardrail                         | 护栏        |
| 评估与安全  | Safety             | Safety                            | 安全        |
| 评估与安全  | Hallucination      | Hallucination                     | 幻觉        |
| 工程化    | Inference          | Inference                         | 推理 / 生成   |
| 工程化    | Fine-tuning        | Fine-tuning                       | 微调        |
| 工程化    | API                | Application Programming Interface | 应用程序接口    |

## 基础概念

### AI

- Full name: Artificial Intelligence
- 中文：人工智能
- 解释：让机器完成需要理解、判断、生成或决策的任务。你可以先把它理解成“把一部分人的认知工作交给程序处理”。
- 学习提示：学 AI Agent 时，不要只看 AI 会回答什么，更要看它如何被接入一个可控的工程流程。

### Model

- Full name: Model
- 中文：模型
- 解释：模型是从数据中学到规律的程序。输入一个问题或数据后，它根据学到的规律给出预测、分类或生成结果。
- 学习提示：模型不是完整产品，它更像一个能力模块；真正的 Agent 还需要上下文、工具、记忆、评估和安全边界。

### LLM

- Full name: Large Language Model
- 中文：大语言模型
- 解释：Large 表示大规模，Language 表示处理语言，Model 表示模型。它能理解和生成自然语言，是很多 AI Agent 的核心能力来源。
- 学习提示：理解 LLM 时，不要只记“大语言模型”，要记住它擅长语言推理和生成，但不天然保证事实正确或行为安全。

### Token

- Full name: Token
- 中文：词元
- 解释：Token 是模型处理文本的基本单位，可能是一个字、一个词，也可能是词的一部分。模型不是直接按人类看到的句子理解，而是先把文本切成 token。
- 学习提示：Token 会影响成本、速度和上下文长度。做 Agent 时，长对话、长文档和 RAG 都会遇到 token 管理问题。

### Context Window

- Full name: Context Window
- 中文：上下文窗口
- 解释：模型一次能看到的输入、历史消息、工具结果和系统规则的总长度。超出窗口的内容，模型就无法直接使用。
- 学习提示：上下文窗口不是记忆。真正的记忆需要设计保存、检索和压缩机制。

## Prompt

### Prompt

- Full name: Prompt
- 中文：提示词 / 提示
- 解释：Prompt 是给模型的输入，用来说明任务、规则、背景和输出要求。它不是“咒语”，更像一次对模型能力的接口调用。
- 学习提示：Prompt 设计的重点是减少歧义，让模型知道目标、边界和输出格式。

### System Prompt

- Full name: System Prompt
- 中文：系统提示词
- 解释：System Prompt 是开发者设置的高优先级规则，用来约束模型的角色、行为边界和输出方式。
- 学习提示：在 Agent 中，System Prompt 类似架构层约束；它不应该承载所有业务逻辑，复杂规则要进入代码、工具或评估。

### User Prompt

- Full name: User Prompt
- 中文：用户提示词
- 解释：User Prompt 是用户当前提出的问题、任务或请求。它表达用户意图，但经常不完整、有歧义或带有隐藏背景。
- 学习提示：Agent 的第一步常常不是回答，而是判断用户意图是否足够清楚、上下文是否足够。

### Few-shot Prompting

- Full name: Few-shot Prompting
- 中文：少样本提示
- 解释：在 Prompt 里提供几个示例，让模型模仿示例的格式、风格或推理方式。Few-shot 的意思是“给少量样本”。
- 学习提示：当你希望输出稳定时，示例往往比抽象描述更有效。

## 模型参数

### Temperature

- Full name: Temperature
- 中文：温度
- 解释：Temperature 控制输出的随机性。温度低时更稳定、保守；温度高时更发散、更有变化。
- 学习提示：做评估、结构化输出和安全场景时，通常更偏向稳定；做创意发散时才提高随机性。

### Max Tokens

- Full name: Maximum Tokens
- 中文：最大输出词元数
- 解释：限制模型最多生成多少 token。它不是控制答案质量的参数，而是控制输出长度和成本的边界。
- 学习提示：如果输出被截断，要检查是不是 max tokens 太低，而不是直接认为模型“不会回答”。

### Top-p

- Full name: Nucleus Sampling / Top-p Sampling
- 中文：核采样
- 解释：Top-p 控制模型从多大概率范围内选择下一个 token。它和 Temperature 都会影响随机性，但控制方式不同。
- 学习提示：初学时不要同时乱调 Temperature 和 Top-p；先理解一个参数，再做对比实验。

## 输出控制

### Structured Output

- Full name: Structured Output
- 中文：结构化输出
- 解释：让模型按固定结构输出，例如 JSON。这样程序可以稳定读取字段，而不是从一段自然语言里猜答案。
- 学习提示：结构化输出是 Agent 工程化的基础，因为后续工具调用、评估和业务流程都需要可解析的数据。

### JSON Mode

- Full name: JavaScript Object Notation Mode
- 中文：JSON 模式
- 解释：JSON 是一种常见的数据格式。JSON Mode 要求模型输出合法 JSON，减少程序解析失败的概率。
- 学习提示：JSON 合法不代表业务正确。还需要 schema、字段校验和测试样例。

### Schema

- Full name: Schema
- 中文：模式 / 结构定义
- 解释：Schema 定义数据应该有哪些字段、字段类型是什么、哪些字段必填。它像一份输出契约。
- 学习提示：在 Agent 中，Schema 能把“模型随便说”变成“模型按接口交付结果”。

## Agent

### Agent

- Full name: Agent
- 中文：智能体
- 解释：Agent 是围绕目标进行观察、思考、调用工具和输出结果的系统。它不只是一个聊天模型，而是模型加上流程、工具和边界。
- 学习提示：判断一个系统是不是 Agent，不要只看它有没有聊天界面，要看它是否能根据状态选择下一步行动。

### Agent Loop

- Full name: Agent Loop
- 中文：智能体循环
- 解释：Agent Loop 是 Agent 反复执行“观察、决策、行动、反馈”的流程。Loop 让 Agent 可以不止回答一次，而是逐步推进任务。
- 学习提示：Agent Loop 的风险在于失控、重复和错误累积，所以必须设计停止条件和评估点。

### Tool Calling

- Full name: Tool Calling
- 中文：工具调用
- 解释：模型自己不能直接查数据库、跑代码或读文件，但它可以请求外部工具来完成这些动作。Tool Calling 就是让模型把一部分任务交给工具。
- 学习提示：工具调用把 LLM 从“只会说”变成“可以行动”，但也带来了权限、安全和错误处理问题。

### Function Calling

- Full name: Function Calling
- 中文：函数调用
- 解释：模型按约定参数调用某个函数，通常是工具调用的一种形式。它强调函数名、参数和返回值都要可控。
- 学习提示：Function Calling 的学习重点是接口设计：函数应该暴露什么能力，不应该暴露什么能力。

## 知识与记忆

### Memory

- Full name: Memory
- 中文：记忆
- 解释：Memory 是 Agent 保存和使用过往信息的能力。它可以保存用户偏好、历史任务、长期事实或中间状态。
- 学习提示：记忆不是越多越好。好的记忆系统要知道保存什么、什么时候检索、什么时候忘记。

### RAG

- Full name: Retrieval-Augmented Generation
- 中文：检索增强生成
- 解释：Retrieval 是检索，Augmented 是增强，Generation 是生成。模型先从文档、数据库或知识库里找资料，再基于资料回答问题。可以理解成“先翻资料，再回答”。
- 学习提示：RAG 的重点不是让模型记住更多，而是让模型在回答前拿到可信资料。

### Embedding

- Full name: Embedding
- 中文：向量表示
- 解释：Embedding 把文本转成数字向量，让程序可以计算两段文本在语义上是否接近。它让“意思相近”变成可以计算的距离。
- 学习提示：RAG 能检索相似内容，背后通常依赖 embedding 和向量搜索。

### Vector Database

- Full name: Vector Database
- 中文：向量数据库
- 解释：Vector Database 专门存储和检索向量。它可以快速找到和用户问题语义相近的文档片段。
- 学习提示：向量数据库不是知识库本身，它只是帮助从知识库中找相关内容的一种基础设施。

## 评估与安全

### Evaluation

- Full name: Evaluation
- 中文：评估
- 解释：Evaluation 用样例、指标或人工检查判断模型输出是否符合目标。它回答的问题是：这个 Agent 到底有没有可靠地完成任务？
- 学习提示：没有评估，Agent 很容易停留在 demo 阶段；有评估，才知道改动是变好还是变坏。

### Guardrail

- Full name: Guardrail
- 中文：护栏
- 解释：Guardrail 是限制模型行为、防止危险或不合规输出的规则和机制。它可以在输入前、输出后或工具调用前生效。
- 学习提示：在 Parenting Copilot 中，护栏尤其重要，因为用户问题可能涉及儿童、安全、心理和家庭关系。

### Safety

- Full name: Safety
- 中文：安全
- 解释：Safety 指 AI 系统不造成伤害、误导、越权或不当建议的能力。它不是一句“注意安全”，而是一组设计和验证机制。
- 学习提示：安全边界应该进入系统设计，而不是等出问题后再靠 Prompt 补救。

### Hallucination

- Full name: Hallucination
- 中文：幻觉
- 解释：Hallucination 指模型生成看似合理但实际不准确的内容。它可能编造事实、引用不存在的来源，或给出过度确定的判断。
- 学习提示：减少幻觉不能只靠提醒模型“不要编”，还需要检索资料、结构化输出、校验和评估。

## 工程化

### Inference

- Full name: Inference
- 中文：推理 / 生成
- 解释：Inference 是模型根据输入生成输出的过程。训练是让模型学能力，推理是使用这个能力。
- 学习提示：你调用 API 获得回答时，大多数时候是在做 inference，而不是训练模型。

### Fine-tuning

- Full name: Fine-tuning
- 中文：微调
- 解释：Fine-tuning 是用特定数据继续训练模型，让它更适合某类任务、风格或格式。
- 学习提示：初学 Agent 时不要急着微调。很多问题应该先用 Prompt、RAG、工具、评估和流程设计解决。

### API

- Full name: Application Programming Interface
- 中文：应用程序接口
- 解释：API 是程序之间互相调用能力的接口。调用模型服务时，你通常是通过 API 把输入发给模型，再拿回输出。
- 学习提示：从工程视角看，LLM API 是一个外部依赖，需要处理认证、失败、超时、成本和返回格式。

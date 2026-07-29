# Parenting Copilot Agent 架构

## v0.1 架构

```text
User Input
  -> Input Normalizer
  -> Intent Router
  -> Context Builder
  -> Risk Classifier
  -> Advice Generator
  -> Output Validator
  -> Memory Extractor
  -> Response
```

## 模块职责

### Input Normalizer

把家长输入整理成稳定结构，例如：

- 孩子年龄。
- 问题描述。
- 持续时间。
- 场景。
- 家长期望。

### Intent Router

判断问题类型：

- 学习问题。
- 情绪问题。
- 亲子沟通。
- 行为习惯。
- 学校关系。
- 高风险问题。

### Context Builder

组合 Agent 需要的上下文：

- 当前问题。
- 孩子画像。
- 家长画像。
- 最近事件。
- 检索到的教育资料。

### Risk Classifier

判断风险等级：

- 普通。
- 复杂。
- 高风险。
- 紧急。

### Advice Generator

生成结构化建议：

- 问题判断。
- 可能原因。
- 具体行动。
- 沟通话术。
- 观察计划。
- 风险提醒。

### Output Validator

检查输出：

- 是否符合 schema。
- 是否包含越界建议。
- 是否表达不确定性。
- 是否给出可执行步骤。

### Memory Extractor

从对话中提取可保存信息：

- 新事实。
- 观察。
- 偏好。
- 后续跟进点。

## Android 架构类比

可以把 Agent 系统粗略类比成：

- Intent Router 类似导航或业务分发层。
- Context Builder 类似 use case 的输入装配。
- Tool Calling 类似 repository 调用外部数据源。
- Memory 类似本地数据库和用户画像。
- Output Validator 类似响应模型校验和业务规则校验。
- Evaluation 类似自动化测试和质量门禁。

---
type: concept
topic: Agent 命名与代码架构
project: Parenting Copilot
status: draft
tags:
  - python
  - ai-agent
  - architecture
  - naming
---

# Agent 开发中的命名、架构和特殊写法

这篇专门记录 LLM Agent 开发中要特别注意的命名、文件组织和代码写法。目标不是把代码写复杂，而是让每个概念有稳定边界，后续扩展 [[../../product/parenting-copilot-prd|Parenting Copilot]] 时不容易混乱。

## 1. Agent 不是一个聊天函数

普通聊天函数通常是：

```text
user_input -> call_llm() -> answer
```

Agent 更像一条可观察、可控制、可评估的执行链路：

```text
Request
  -> Context
  -> State
  -> SafetyCheck
  -> IntentRoute
  -> Prompt
  -> LlmCall
  -> ToolCall
  -> Validation
  -> Response
  -> Trace
```

注意：Agent 开发里，命名的第一目标是把这些边界说清楚。

## 2. 高频命名词典

| 名称 | 代表什么 | 不要混淆 |
| --- | --- | --- |
| `request` | 外部输入请求 | 不是 prompt |
| `user_input` | 用户原始输入文本 | 不是完整上下文 |
| `message` | 对话里的一条消息 | 不是一次完整运行 |
| `context` | 本轮给模型看的背景集合 | 不是长期记忆 |
| `memory` | 跨轮次保存的信息 | 不是当前状态 |
| `state` | Agent 当前运行状态 | 不是数据库数据 |
| `prompt` | 发给 LLM 的指令文本 | 不是用户原话 |
| `system_prompt` | 系统级行为约束 | 不是业务数据 |
| `tool` | Agent 可调用能力 | 不是普通函数都叫 tool |
| `tool_call` | 一次工具调用请求 | 不是工具返回值 |
| `tool_result` | 工具调用结果 | 不是最终回答 |
| `raw_response` | LLM 原始返回 | 不是已解析结果 |
| `parsed_response` | 解析后的结构 | 不是一定通过校验 |
| `validation_result` | 校验结果 | 不是最终业务输出 |
| `trace` | 执行过程记录 | 不是用户可见回答 |
| `run` | 一次完整执行 | 不是单个 step |
| `step` | 执行过程中的一步 | 不是完整 Agent |
| `policy` | 决策规则 | 不是 prompt |
| `guardrail` | 安全护栏 | 不是普通 if 判断 |

## 3. 最应该区分的 5 组词

### 3.1 `prompt` vs `message`

```python
user_message = "孩子不写作业怎么办？"
system_prompt = "你是一个亲子教育助手，必须保持安全边界。"
prompt = f"{system_prompt}\n家长问题：{user_message}"
```

注意：

- `message` 是对话消息。
- `prompt` 是最终组织给模型看的输入。
- 多轮对话里，prompt 可能由很多 message、memory、tool_result 拼出来。

### 3.2 `context` vs `memory`

```python
context = {
    "current_question": "孩子不写作业怎么办？",
    "recent_messages": ["昨天也问过拖延问题"],
}

memory = {
    "child_age": 8,
    "family_rule": "晚上 8 点后不写作业",
}
```

注意：

- `context` 是本轮临时要给模型看的材料。
- `memory` 是跨轮次保存的信息。
- 不要把所有东西都叫 `context`，否则后面很难判断哪些该持久化。

### 3.3 `state` vs `result`

```python
state = {
    "step_count": 2,
    "risk_level": "low",
    "tool_calls": [],
}

result = {
    "answer": "先共情，再拆小任务。",
}
```

注意：

- `state` 描述过程进行到哪里。
- `result` 是某一步或最终的输出。
- Agent loop 里，`state` 会不断变化，`result` 通常是某个阶段产生的值。

### 3.4 `raw_response` vs `parsed_response`

```python
raw_response = '{"answer": "先共情", "risk_level": "low"}'
parsed_response = {
    "answer": "先共情",
    "risk_level": "low",
}
```

注意：

- `raw_response` 是模型或 API 的原始文本。
- `parsed_response` 是已经转成 Python 对象的结果。
- `parsed` 不代表可信，还需要校验。

### 3.5 `tool_call` vs `tool_result`

```python
tool_call = {
    "name": "search_parenting_knowledge",
    "arguments": {"query": "孩子拖延写作业"},
}

tool_result = {
    "name": "search_parenting_knowledge",
    "content": "拖延常和任务太大、情绪压力有关。",
}
```

注意：

- `tool_call` 是请求。
- `tool_result` 是返回。
- 真实 Agent 里要记录两者，方便追踪错误。

## 4. 坏命名与好命名对比

### 4.1 函数名

不建议：

```python
def process(data):
    ...
```

建议：

```python
def classify_parenting_intent(user_question: str) -> str:
    ...
```

原因：Agent 里步骤多，`process` 这种词很快失去信息量。

### 4.2 变量名

不建议：

```python
result = call_model(input)
```

建议：

```python
raw_llm_response = call_llm(prompt)
parsed_advice = parse_advice_response(raw_llm_response)
```

原因：要区分原始响应、解析结果、校验结果、最终输出。

### 4.3 类名

不建议：

```python
class Manager:
    ...
```

建议：

```python
class ParentingAdvisor:
    ...


class SafetyChecker:
    ...


class IntentRouter:
    ...
```

原因：`Manager`、`Helper`、`Util` 太泛，通常说明职责还没想清楚。

## 5. 推荐的 Agent 文件职责

```text
parenting_agent/
  models.py          # 数据结构：Request、Response、State、ToolCall、ToolResult
  prompts.py         # prompt 模板和 prompt 构造函数
  router.py          # 意图识别和任务分流
  safety.py          # 风险判断、安全策略、升级建议
  llm_client.py      # LLM API 调用边界
  tools.py           # 工具定义和工具调用适配
  memory.py          # 记忆读写，短期和长期记忆边界
  evaluator.py       # 测试集、评分、回归评估
  trace.py           # 执行过程记录
  advisor.py         # 主流程编排
  cli.py             # 命令行入口
```

注意：

- `llm_client.py` 不应该知道 Parenting Copilot 的业务规则。
- `safety.py` 不应该直接调用 LLM API。
- `prompts.py` 不应该执行网络请求。
- `advisor.py` 可以编排流程，但不要把所有细节都塞进去。
- `models.py` 应该尽量少依赖其他业务模块。

## 6. 最小 Agent 调用链

```text
cli.main()
  -> parse_args()
  -> ParentingRequest
  -> ParentingAdvisor.answer()
  -> SafetyChecker.classify()
  -> IntentRouter.route()
  -> build_parenting_prompt()
  -> LlmClient.generate()
  -> parse_advice_response()
  -> AdviceResponse
  -> TraceRecorder.record()
```

这个链路里，真正调用 LLM 只是其中一步。Agent 工程的核心价值在于前后的边界、状态、工具、安全和评估。

## 7. Agent 中常见数据结构命名

```python
from dataclasses import dataclass, field
from typing import Literal


RiskLevel = Literal["low", "medium", "high"]
Intent = Literal["learning", "emotion", "behavior", "high_risk", "unknown"]


@dataclass
class ParentingRequest:
    user_question: str
    child_age: int | None = None


@dataclass
class AgentState:
    request: ParentingRequest
    intent: Intent = "unknown"
    risk_level: RiskLevel = "low"
    step_count: int = 0
    tool_results: list[str] = field(default_factory=list)


@dataclass
class AdviceResponse:
    answer: str
    risk_level: RiskLevel
    should_escalate: bool
```

注意：

- `field(default_factory=list)` 用来避免多个对象共享同一个默认 list。
- `int | None` 表示可能是整数，也可能没有值。
- `Literal` 让状态值范围更清楚。

## 8. 特殊写法 1：默认参数不要写可变对象

不建议：

```python
def add_tool_result(result: str, tool_results: list[str] = []) -> list[str]:
    tool_results.append(result)
    return tool_results
```

建议：

```python
def add_tool_result(result: str, tool_results: list[str] | None = None) -> list[str]:
    if tool_results is None:
        tool_results = []
    tool_results.append(result)
    return tool_results
```

注意：Python 的默认参数只在函数定义时创建一次。Agent state 里如果犯这个错，多轮运行可能互相污染。

## 9. 特殊写法 2：用 `Protocol` 隔离外部依赖

```python
from typing import Protocol


class LlmClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class MemoryStore(Protocol):
    def load_context(self, user_id: str) -> dict:
        ...

    def save_interaction(self, user_id: str, response: str) -> None:
        ...
```

注意：

- `Protocol` 让业务代码依赖接口，不依赖具体实现。
- 测试时可以传入 `FakeLlmClient`、`InMemoryStore`。
- 这和 Android 里的 Repository interface 思路接近。

## 10. 特殊写法 3：用 `Enum` 或 `Literal` 管住状态

不建议：

```python
risk = "hight"
```

建议：

```python
from enum import Enum


class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
```

注意：Agent 的状态值经常进入日志、评估、数据库和前端。越早管住，越少出错。

## 11. 特殊写法 4：解析和校验分开

不建议：

```python
def parse_response(raw_text: str) -> dict:
    return json.loads(raw_text)
```

建议：

```python
import json


def parse_json(raw_text: str) -> dict:
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError as error:
        raise ValueError("LLM 返回内容不是合法 JSON") from error


def validate_advice_response(data: dict) -> None:
    required_fields = ["answer", "risk_level", "should_escalate"]
    for field_name in required_fields:
        if field_name not in data:
            raise ValueError(f"缺少必要字段：{field_name}")
```

注意：

- `parse` 只负责格式转换。
- `validate` 负责检查字段和业务约束。
- 不要因为 `json.loads()` 成功，就认为模型输出可信。

## 12. 特殊写法 5：用 trace 记录过程

```python
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class AgentTrace:
    run_id: str
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    steps: list[str] = field(default_factory=list)

    def add_step(self, step_name: str) -> None:
        self.steps.append(step_name)
```

注意：

- Agent 出错时，trace 能告诉你卡在哪一步。
- trace 不等于日志。trace 更偏一次业务运行的结构化记录。
- 不要在 trace 里保存 API key、儿童隐私、完整敏感对话。

## 13. 特殊写法 6：Fake 实现优先

```python
class FakeLlmClient:
    def generate(self, prompt: str) -> str:
        return """
        {
          "answer": "先共情孩子，再把作业拆成 10 分钟的小任务。",
          "risk_level": "low",
          "should_escalate": false
        }
        """
```

注意：

- 学习和测试时先用 Fake，避免每次都花钱、受网络影响。
- Fake 返回值要尽量接近真实 LLM 的结构。
- 等流程稳定后，再接真实 API。

## 14. Parenting Copilot 最小骨架示例

这段代码不直接调用真实 LLM，而是展示命名和架构边界。

```python
import json
from dataclasses import dataclass, field
from typing import Literal, Protocol


RiskLevel = Literal["low", "medium", "high"]
Intent = Literal["learning", "emotion", "behavior", "high_risk", "unknown"]


@dataclass
class ParentingRequest:
    user_question: str
    child_age: int | None = None


@dataclass
class AgentState:
    request: ParentingRequest
    intent: Intent = "unknown"
    risk_level: RiskLevel = "low"
    step_count: int = 0
    trace_steps: list[str] = field(default_factory=list)

    def add_step(self, step_name: str) -> None:
        self.step_count += 1
        self.trace_steps.append(step_name)


@dataclass
class AdviceResponse:
    answer: str
    risk_level: RiskLevel
    should_escalate: bool


class LlmClient(Protocol):
    def generate(self, prompt: str) -> str:
        ...


class FakeLlmClient:
    def generate(self, prompt: str) -> str:
        return json.dumps(
            {
                "answer": "先接住孩子的情绪，再把任务拆成一个 10 分钟的小步骤。",
                "risk_level": "low",
                "should_escalate": False,
            },
            ensure_ascii=False,
        )


class SafetyChecker:
    def classify(self, user_question: str) -> RiskLevel:
        high_risk_keywords = ["不想活", "自伤", "伤害自己"]
        if any(keyword in user_question for keyword in high_risk_keywords):
            return "high"
        return "low"


class IntentRouter:
    def route(self, user_question: str) -> Intent:
        if "作业" in user_question or "学习" in user_question:
            return "learning"
        if "发脾气" in user_question or "哭" in user_question:
            return "emotion"
        return "unknown"


class ParentingAdvisor:
    def __init__(
        self,
        llm_client: LlmClient,
        safety_checker: SafetyChecker,
        intent_router: IntentRouter,
    ) -> None:
        self.llm_client = llm_client
        self.safety_checker = safety_checker
        self.intent_router = intent_router

    def answer(self, request: ParentingRequest) -> AdviceResponse:
        state = AgentState(request=request)

        state.add_step("safety_check")
        state.risk_level = self.safety_checker.classify(request.user_question)
        if state.risk_level == "high":
            return AdviceResponse(
                answer="这个情况可能涉及安全风险，请优先联系当地紧急服务或专业人士。",
                risk_level="high",
                should_escalate=True,
            )

        state.add_step("intent_route")
        state.intent = self.intent_router.route(request.user_question)

        state.add_step("build_prompt")
        prompt = self._build_prompt(state)

        state.add_step("llm_call")
        raw_response = self.llm_client.generate(prompt)

        state.add_step("parse_response")
        parsed_response = json.loads(raw_response)

        return AdviceResponse(
            answer=parsed_response["answer"],
            risk_level=parsed_response["risk_level"],
            should_escalate=parsed_response["should_escalate"],
        )

    def _build_prompt(self, state: AgentState) -> str:
        return (
            "你是一个亲子教育助手。"
            "请给出低风险、家长可监督执行的建议。\n"
            f"孩子年龄：{state.request.child_age}\n"
            f"问题类型：{state.intent}\n"
            f"家长问题：{state.request.user_question}"
        )
```

## 15. 写 Agent 代码前的命名检查清单

- 这个变量是原始输入、上下文、状态、记忆，还是结果？
- 这个函数名能不能看出它只做一件事？
- 这个类名能不能看出它的业务职责？
- LLM 原始响应和解析后响应有没有分开命名？
- tool 调用请求和 tool 返回结果有没有分开命名？
- 安全判断有没有独立出来，而不是散落在 prompt 里？
- 是否用了 `FakeLlmClient` 来支持不联网测试？
- 是否避免了 `data`、`result`、`manager`、`helper` 这种过泛命名？
- 是否避免了可变默认参数？
- 是否有 trace 或日志帮助排查 Agent 每一步？


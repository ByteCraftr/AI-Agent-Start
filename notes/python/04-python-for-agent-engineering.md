---
type: concept
topic: Python Agent 工程建议
project: Parenting Copilot
status: draft
tags:
  - python
  - ai-agent
  - engineering
---

# 面向 Agent 工程的 Python 使用建议

## 1. 先把代码写成可读的调用链

Agent 代码最怕所有逻辑都堆在一个函数里。推荐先形成这样的最小链路：

```text
main()
  -> read_user_input()
  -> build_prompt()
  -> call_llm()
  -> parse_response()
  -> print_result()
```

每个函数只做一件事。这样后面加入结构化输出、工具调用、记忆、评估时，才有地方放。

## 2. 函数优先，类其次

早期实验优先写函数：

```python
def build_prompt(question: str) -> str:
    return f"请回答这个亲子教育问题：{question}"
```

当你遇到这些情况，再考虑类：

- 需要保存配置，例如模型名、超时时间、API 地址。
- 需要组合多个依赖，例如 LLM client、safety checker、memory store。
- 需要替换实现，例如真实 LLM 和测试 fake LLM。

## 3. 数据结构要明确

简单阶段可以用 `dict`：

```python
result = {
    "answer": "先共情，再拆小任务。",
    "risk_level": "low",
}
```

复杂一点后用 `dataclass`：

```python
from dataclasses import dataclass


@dataclass
class AdviceResult:
    answer: str
    risk_level: str
```

注意：当输出要给外部系统或前端稳定使用时，需要更严格的 schema 校验。后续可以学习 Pydantic 或 JSON Schema。

## 4. 边界代码单独放

把不稳定的外部世界隔离起来：

- 读取环境变量：单独函数。
- 调 LLM API：单独函数或 client 类。
- 解析模型返回：单独函数。
- 文件读写：单独函数。
- 安全判断：单独模块。

这样业务逻辑不会被网络、文件、认证、异常处理污染。

## 5. 错误处理不要吞掉信息

不建议：

```python
try:
    call_llm()
except Exception:
    pass
```

建议：

```python
try:
    call_llm()
except TimeoutError as error:
    raise RuntimeError("LLM 调用超时，请稍后重试") from error
```

错误要保留原因，方便调试。

## 6. Parenting Copilot 的代码边界

亲子教育 Agent 的核心边界应该尽早进入代码：

- 不诊断儿童心理或医学问题。
- 不替代老师、医生、心理咨询师。
- 对高风险表达给出升级建议。
- 建议必须家长监督执行。
- 回答要具体、低风险、可观察。

这类边界不只写在 prompt，也要写在函数、测试和评估样例里。

## 7. 推荐的最小目录结构

```text
labs/w01-llm-foundation/
  parenting_advisor.py
  parameter_experiment.py

未来可演进为：

parenting_copilot/
  __init__.py
  models.py
  safety.py
  prompts.py
  llm_client.py
  advisor.py
tests/
  test_safety.py
  test_advisor.py
```

## 8. 初学阶段的代码质量检查

每次写完 Python，至少做三件事：

```bash
python3 -m py_compile your_file.py
python3 your_file.py --help
python3 your_file.py --dry-run
```

如果没有 `--help` 或 `--dry-run`，至少保证能运行一个最小示例。

## 9. 后续学习路线

1. 基础语法：变量、类型、判断、循环、函数。
2. 数据结构：list、dict、dataclass、JSON。
3. 模块拆分：把一个脚本拆成几个职责清楚的文件。
4. 接口抽象：用 `Protocol` 支持 fake client 和测试。
5. 错误处理：网络错误、解析错误、输出不完整。
6. 自动化测试：先测纯函数，再测流程。
7. 并发评估：用线程池批量跑测试集。


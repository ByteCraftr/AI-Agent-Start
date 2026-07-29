---
type: concept
topic: Python 基础
project: Parenting Copilot
status: draft
tags:
  - python
  - basics
---

# Python 基础：语法、类型、函数、调用、命名、判断

## 1. Python 程序的基本单位

Python 代码通常从小到大分为：

- 值：`"hello"`、`123`、`True`
- 变量：给值起名字，例如 `user_name = "Ford"`
- 表达式：能算出一个结果，例如 `age >= 6`
- 语句：执行一个动作，例如 `print("hello")`
- 函数：把一段逻辑封装起来，方便重复调用
- 模块：一个 `.py` 文件
- 包：多个模块组成的目录

Android 类比：一个 Python 模块可以像一个 Kotlin 文件，函数像一个 use case 方法，变量像局部状态。

## 2. 常见内置类型

```python
name = "Ford"              # str：字符串
age = 10                   # int：整数
score = 9.5                # float：小数
is_parent = True           # bool：布尔值
tags = ["homework", "mood"] # list：有顺序、可修改
profile = {"age": 10}      # dict：key-value 字典
roles = ("parent", "child") # tuple：有顺序、通常不修改
unique_tags = {"mood"}     # set：去重集合
empty_value = None         # None：没有值
```

常见判断：

- `str`：文本输入、模型回答、日志内容。
- `int` / `float`：年龄、分数、费用、耗时。
- `bool`：是否通过校验、是否高风险。
- `list`：多条消息、多条建议、多轮对话。
- `dict`：结构化数据、JSON 请求体、API 响应。
- `None`：没有传入、没有结果、可选字段为空。

## 3. 变量命名规则

Python 常用 `snake_case`：

```python
user_question = "孩子不愿意写作业怎么办？"
max_output_tokens = 800
is_high_risk = False
```

常见命名约定：

- 变量和函数：`snake_case`
- 类名：`PascalCase`，例如 `ParentingAdvisor`
- 常量：`UPPER_SNAKE_CASE`，例如 `DEFAULT_MODEL`
- 私有意图：前缀 `_`，例如 `_parse_response`

注意：Python 不靠大括号分组，而靠缩进分组。缩进错了，逻辑就变了。

## 4. if-else 判断

`if-else` 用来根据条件选择不同路径。

```python
age = 5

if age < 3:
    stage = "toddler"
elif age < 7:
    stage = "preschool"
else:
    stage = "school_age"

print(stage)
```

在 [[../../product/parenting-copilot-prd|Parenting Copilot]] 里，判断常用于安全边界：

```python
question = "孩子说自己不想活了，我该怎么办？"

if "不想活" in question:
    response_type = "high_risk"
else:
    response_type = "normal_advice"
```

注意：真实产品不能只靠关键词判断风险，这里只是学习 `if-else` 的最小例子。

## 5. 函数是什么

函数把输入、处理和输出封装起来。

```python
def build_parenting_prompt(question: str, child_age: int) -> str:
    return f"孩子年龄：{child_age}。家长问题：{question}"
```

拆开看：

- `def`：定义函数。
- `build_parenting_prompt`：函数名。
- `question: str`：参数名和类型提示。
- `child_age: int`：第二个参数。
- `-> str`：返回值类型提示。
- `return`：返回结果。

调用函数：

```python
prompt = build_parenting_prompt("孩子不写作业怎么办？", 8)
print(prompt)
```

## 6. 参数和返回值

```python
def classify_age_stage(age: int) -> str:
    if age < 3:
        return "toddler"
    if age < 7:
        return "preschool"
    return "school_age"
```

这里用了多个 `return`，好处是每个分支清楚结束。

注意：类型提示不是运行时强制检查。`age: int` 是给人、编辑器和类型检查工具看的工程契约。

## 7. 函数调用关系

```python
def normalize_question(question: str) -> str:
    return question.strip()


def build_payload(question: str) -> dict:
    clean_question = normalize_question(question)
    return {"input": clean_question}
```

调用链是：

```text
build_payload()
  -> normalize_question()
```

这和 Android 里 `ViewModel -> UseCase -> Repository` 的调用链类似。区别是 Python 小脚本开始时可以更轻，不必一开始就分太多层。

## 8. import 导入

```python
import json
from pathlib import Path
```

- `import json`：导入整个模块，使用 `json.dumps(...)`。
- `from pathlib import Path`：只导入模块中的某个对象，直接使用 `Path(...)`。

注意：先优先使用标准库，等标准库不够再引入第三方库。

## 9. 基础练习

1. 写一个 `classify_age_stage(age: int) -> str`。
2. 写一个 `build_prompt(question: str, age: int) -> str`。
3. 写一个 `is_high_risk(question: str) -> bool`。
4. 把三个函数串起来，输出一个字典。

示例目标：

```python
{
    "stage": "school_age",
    "risk": False,
    "prompt": "孩子年龄：8。家长问题：孩子不写作业怎么办？"
}
```


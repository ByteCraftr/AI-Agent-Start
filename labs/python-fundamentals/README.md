# Python Fundamentals 可运行学习脚本

这个目录把 `notes/python/` 里的学习资料落成可以直接运行的 Python 脚本。每个脚本都尽量只使用 Python 标准库，方便你先理解语言和 Agent 工程边界，再学习框架。

## 推荐运行顺序

```bash
python3 labs/python-fundamentals/01_basic_types_functions_if.py
python3 labs/python-fundamentals/02_collections_loops_files.py
python3 labs/python-fundamentals/03_functions_errors_cli.py --question "孩子不写作业怎么办？" --age 8
python3 labs/python-fundamentals/04_classes_composition_inheritance.py
python3 labs/python-fundamentals/05_protocol_fake_client.py
python3 labs/python-fundamentals/06_standard_library_json_path_logging.py
python3 labs/python-fundamentals/07_threads_thread_pool.py
python3 labs/python-fundamentals/08_mini_parenting_advisor.py --question "孩子拖延写作业怎么办？" --age 8
python3 labs/python-fundamentals/09_agent_special_usages_demo.py --question "孩子害怕上学怎么办？" --age 7
python3 labs/python-fundamentals/10_agent_naming_architecture_demo.py --question "孩子写作业总是拖延怎么办？" --age 8
```

## 文件说明

- `01_basic_types_functions_if.py`：基础类型、函数、调用、命名、if-else。
- `02_collections_loops_files.py`：list、dict、set、循环、文件读写。
- `03_functions_errors_cli.py`：函数拆分、异常处理、命令行参数。
- `04_classes_composition_inheritance.py`：类、组合、继承。
- `05_protocol_fake_client.py`：Protocol、Fake LLM、可测试设计。
- `06_standard_library_json_path_logging.py`：json、pathlib、logging。
- `07_threads_thread_pool.py`：线程池与批量评估样例。
- `08_mini_parenting_advisor.py`：最小 Parenting Copilot Agent。
- `09_agent_special_usages_demo.py`：LLM Agent 常见 Python 特殊写法。
- `10_agent_naming_architecture_demo.py`：Agent 命名、状态、trace、架构边界。

## 验证命令

```bash
python3 -m py_compile labs/python-fundamentals/*.py
```


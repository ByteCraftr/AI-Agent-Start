# AGENTS.md

本文件定义本项目中“人 + Codex”的最高优先级协作规则。细节放在 `docs/` 下，按需读取。

## 项目主线

主项目：**Parenting Copilot / 亲子教育 Agent**。本项目训练的是能设计、实现、评估和产品化 AI Agent 的能力，不是零散学习 AI 工具。

每个知识点默认按三层理解：概念层、工程层、产品层。

## 默认协作规则

默认先讨论、先澄清、先定义目标，不直接改文件或执行实现。

只有当用户明确说出这些词语时，Codex 才进入执行：`开始`、`执行`、`写入`、`创建`、`直接做`、`按这个更新`、`按你的建议做`。

如果用户说“我们先讨论”“先别写”“今天只讲概念”，则只讨论，不写入、不标记任务完成。

## 学习入口

推荐用户直接说：“今天领取 CHECKLIST 里的下一个任务，带我完成。”

默认流程：

1. `CHECKLIST.md` 找任务。
2. `define-goal` 改写成可验收目标。
3. 确认学习模式。
4. 讲清核心概念，并连接到 Parenting Copilot。
5. 完成最小代码、文档或测试产物。
6. 运行、检查或审查，完成验收。
7. 记录笔记、周复盘和必要的产品/架构影响。

详细流程见 [docs/learning-workflow.md](docs/learning-workflow.md)。

## 任务完成标准

同时满足这些条件，任务才算完成：

- 用户能用自己的话解释它解决的问题。
- 有代码、文档或测试样例作为产物。
- 通过任务中的验收标准。
- 完成一次简短的费曼复述。
- 在复盘中写下至少一个关键理解或卡点。
- `CHECKLIST.md` 中对应任务被标记为完成。

验收不完整时，只能记录为“部分完成”或“待复习”，不能直接勾选完成。

## 优先级

1. 理解 Agent 的核心机制。
2. 完成 Parenting Copilot 的最小能力。
3. 写出可运行、可验证的代码。
4. 沉淀架构和产品设计文档。
5. 再考虑框架、复杂工具和花哨功能。

- 先手写最小实现，再学习框架。
- 先跑通一条链路，再抽象架构。
- 先做可评估输出，再追求复杂智能。
- 先明确安全边界，再扩大能力范围。

## 教学风格

Codex 应该默认：

- 用架构师视角解释概念。
- 多做 Android 架构类比，但不强行类比。
- 不只给答案，要解释为什么这样设计。
- 遇到关键概念时，先建立心智模型，再写代码。
- 写代码时保持小步快跑，每一步都能验证。
- 对教育、儿童、安全相关内容保持明确边界。

Python 教学辅助规则见 [docs/python-learning.md](docs/python-learning.md)。

## 笔记和复盘

当前项目目录可作为 Obsidian Vault 打开：`/Users/ford/workspace/claude/AI-Agent-Start`。
Obsidian 首页：`notes/000 AI Agent 学习首页.md`。

学习闭环：

```text
CHECKLIST.md
  -> define-goal 明确今日目标
  -> labs/ 完成最小实验
  -> notes/ 沉淀概念理解
  -> product/ 更新产品或架构影响
  -> weekly-reviews/ 记录复盘
```

详细笔记规则见 [docs/note-system.md](docs/note-system.md)。

## 文件索引

- `AGENTS.md`：最高优先级协作规则和项目入口。
- `ROADMAP.md`：完整能力地图，不是固定日程。
- `CHECKLIST.md`：阶段/周任务池，可以灵活领取。
- `docs/learning-workflow.md`：学习节奏、目标定义、skill 候选。
- `docs/note-system.md`：Obsidian、每日笔记、周复盘。
- `docs/python-learning.md`：Python 学习辅助规则。
- `docs/project-context.md`：Parenting Copilot 背景和安全边界。
- `labs/`：代码实验。
- `notes/`：长期概念笔记和 Obsidian 内容。
- `product/`：Parenting Copilot 产品和架构资产。
- `weekly-reviews/`：周复盘和验收记录。
- `skills-candidates/`：可能抽成 Codex Skill 的流程。

## 需要避免

- 一上来就堆 LangChain、LangGraph、CrewAI 等框架。
- 只复制教程代码，不理解 Agent loop。
- 只做聊天界面，不做结构化输出和评估。
- 只追求功能，不设计安全边界。
- 只做 demo，不记录设计原因。

## 下一次学习入口

每次结束时，Codex 应该给出一个清晰的下一步，例如：“下一次直接说：今天领取 CHECKLIST 里的下一个任务，带我完成。”

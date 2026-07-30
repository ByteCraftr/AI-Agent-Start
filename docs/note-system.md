# 笔记和复盘系统

本文件承接 `AGENTS.md` 中的 Obsidian、笔记、周复盘规则。

## Obsidian Vault

当前项目目录本身可以作为一个独立 Obsidian Vault 打开：

```text
/Users/ford/workspace/claude/AI-Agent-Start
```

Obsidian 首页：

```text
notes/000 AI Agent 学习首页.md
```

## 目录分工

- `notes/`：长期概念笔记和 Obsidian 首页。
- `notes/templates/`：每日学习、概念、决策模板。
- `weekly-reviews/`：每周复盘。
- `product/`：Parenting Copilot 的产品和架构资产。
- `labs/`：代码实验，不强行写成笔记。

## 学习闭环

```text
CHECKLIST.md
  -> define-goal 明确今日目标
  -> labs/ 完成最小实验
  -> notes/ 沉淀概念理解
  -> product/ 更新产品或架构影响
  -> weekly-reviews/ 记录复盘
```

## 每次结束时默认更新

- `CHECKLIST.md`：标记任务完成或记录部分完成。
- `weekly-reviews/weekXX.md`：记录关键理解、代码产物、卡点。
- `notes/`：必要时补充概念笔记。
- `product/`：如果涉及产品或架构设计，更新对应文档。

## 每日学习笔记

每次学习结束时，优先沉淀：

- 今日学习笔记：使用 `notes/templates/daily-learning-note-template.md`。
- 新概念：使用 `notes/templates/concept-note-template.md`。
- 架构或产品取舍：使用 `notes/templates/decision-note-template.md`。

每日学习笔记至少包含：

- 今日目标。
- 核心概念。
- 三层理解：概念层、工程层、产品层。
- 今日产物。
- 验收结果。
- 费曼复述。
- 卡点。
- 下次复习问题。

笔记尽量使用 Obsidian 双链，例如：

```text
[[Agent Loop]]
[[Tool Calling]]
[[Memory 长期记忆系统]]
[[Parenting Copilot]]
```

# AI Agent Start

这个仓库用于系统学习 AI Agent 开发，并以 **Parenting Copilot / 亲子教育 Agent** 为主线，把概念学习、工程实验、产品设计和复盘沉淀到同一个项目里。

## 你要达成的能力

- 理解 LLM 应用的基本链路：prompt、上下文、结构化输出、工具调用。
- 能设计 Agent 的核心架构：intent、routing、agent loop、memory、RAG、evaluation。
- 能用 Python/FastAPI 做出可运行的 Agent 原型。
- 能围绕亲子教育场景设计可靠、安全、可长期成长的 AI 产品。
- 能把学习过程沉淀为作品集、面试材料和创业产品雏形。

## 仓库结构

```text
AI-Agent-Start/
├── CHECKLIST.md              # 每天领取任务的主清单
├── ROADMAP.md                # 阶段地图
├── notes/                    # 概念笔记
├── labs/                     # 每天的代码实验
├── product/                  # Parenting Copilot 产品与架构设计
├── weekly-reviews/           # 每周复盘
└── skills-candidates/        # 将来可抽成 Codex skill 的流程候选
```

## 每天怎么用

每天开始时，对 Codex 说：

```text
今天领取 CHECKLIST 里的下一个任务，带我完成。
```

每天结束时，让 Codex 帮你完成：

```text
请帮我更新今天的学习记录、验收结果和复盘问题。
```

## 当前主项目

**Parenting Copilot v0.1**

一个面向家长的亲子教育 Agent。它能基于孩子年龄、问题描述和家庭上下文，给出结构化、可靠、有边界的建议，并逐步形成孩子和家长的长期成长档案。

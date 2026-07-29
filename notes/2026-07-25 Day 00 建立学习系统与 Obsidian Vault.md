---
type: daily-learning
date: 2026-07-25
day: Day 00
topic: 建立学习系统与 Obsidian Vault
project: Parenting Copilot
status: done
tags:
  - ai-agent
  - daily-learning
  - learning-system
---

# 2026-07-25 建立学习系统与 Obsidian Vault

## 今日目标

理解这个仓库如何作为长期 AI Agent 学习系统运行，并能从 [[000 AI Agent 学习首页]] 进入任务、路线、实验、复盘和产品沉淀。

## 我先前的理解

学习 AI Agent 容易变成零散看教程、复制 demo、追框架。今天要先确认学习系统的结构，让后续每个任务都有目标、产物、验收和复盘。

## 核心概念

AI Agent 学习需要一个闭环系统，而不只是资料集合。这个系统用 [[../CHECKLIST|CHECKLIST]] 管理任务，用 [[../ROADMAP|ROADMAP]] 管理能力地图，用 [[../AGENTS|AGENTS]] 管理人和 Codex 的协作方式，用 `notes/` 沉淀长期知识，用 `labs/` 承载代码实验，用 `product/` 连接 [[Parenting Copilot]] 的产品与架构，用 `weekly-reviews/` 防止学习结果丢失。

## 三层理解

概念层：学习系统解决的是持续性和可验证性问题。每天不是随便学一点，而是从清单领取任务，定义完成标准，产出可检查的结果。

工程层：这个仓库把学习拆成稳定目录结构。`CHECKLIST.md` 像任务队列，`ROADMAP.md` 像技术路线图，`notes/` 像知识库，`labs/` 像实验工程，`product/` 像 PRD 和架构文档，`weekly-reviews/` 像迭代复盘。

产品层：所有学习最终都要回到 [[Parenting Copilot]]。每个 Agent 概念都要回答三个问题：它解决什么问题，代码上怎么实现，它如何让亲子教育 Agent 更可靠、更安全或更有产品价值。

## 今日产物

- 代码：无，今天是学习系统初始化任务。
- 文档：本每日学习笔记。
- 测试：检查 `CHECKLIST.md`、`ROADMAP.md`、`AGENTS.md`、`notes/`、`labs/`、`product/`、`weekly-reviews/` 的职责是否清楚。

## 验收结果

已达到 W1-T1 的核心验收标准：能说明关键文件和目录的职责，并明确 Obsidian 首页是 `notes/000 AI Agent 学习首页.md`。当前项目已经包含 `notes/.obsidian/` 配置，可以作为 Obsidian Vault 使用。

## 费曼复述

如果向一个熟悉 Android 架构但不了解 Agent 的工程师解释：这个仓库不是一个单纯 sample project，而是一套学习工程。`ROADMAP.md` 是技术能力地图，`CHECKLIST.md` 是 backlog，`AGENTS.md` 是协作规范，`labs/` 是可运行实验，`product/` 是产品和架构设计，`notes/` 是长期 wiki，`weekly-reviews/` 是迭代复盘。这样做的目的，是让每次学习都能沉淀成 Parenting Copilot 的真实能力，而不是只停留在看教程。

## 卡点

今天没有代码卡点。需要注意的是，后续不能只完成 demo，还要持续补上验收、笔记和复盘，否则学习系统会退化成普通代码仓库。

## 下次复习问题

- 为什么学习 Agent 不能只靠看教程？
- 一个 Agent 学习任务怎样才算真的完成？
- `labs/` 里的实验如何反哺 `product/` 里的 Parenting Copilot 设计？

## 相关链接

- [[000 AI Agent 学习首页]]
- [[../CHECKLIST|CHECKLIST]]
- [[../ROADMAP|ROADMAP]]
- [[../AGENTS|AGENTS]]
- [[../weekly-reviews/week01|Week 01 Review]]

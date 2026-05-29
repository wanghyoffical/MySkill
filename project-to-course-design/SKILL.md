---
name: project-to-course-design
description: 当用户想把开源项目、代码库、技术教程或技术系统初始化成模块化学习课程包时使用，尤其适用于新人入门、简历项目、面试准备、源码学习、二次开发或从使用者成长为系统构建者。
---

# 项目课程初始化

## 目的

这个 skill 只负责“初始化课程包”：读取项目、拆模块、生成学习状态文件、AI 上下文、部分学习内容、权威资料入口和可运行示例代码。

它不负责后续学习会话中的每日带学、复习判断、互动提问和 demo 陪练。后续会话使用 `project-learning-session-coach`。

## 核心原则

课程包不是源码目录导读，也不是一次性学习路线。它是后续 AI 学习教练能持续工作的状态系统。

初始化时只生成必要材料：
- 项目模块地图。
- 每个模块的核心概念、权威资料和项目源码依据。
- 每个模块的完整可运行小轮子示例。
- 学习状态、复习队列、掌握度记录。
- 后续 AI 会话协议。
- 候选输出资产模板。

不要把概念写成空洞口号；也不要把所有教学都静态写死在文件里。真正学习时，AI 要根据状态引导用户读文件、看权威资料、回答问题、运行 demo、讲回和复习。

## 何时使用

使用本 skill：
- 用户要为某个项目生成学习课程包。
- 用户要初始化源码学习、简历项目学习或面试准备材料。
- 用户要把开源项目拆成模块化训练路线。

不要使用本 skill：
- 用户已经在课程包里开始学习某一天任务。
- 用户问“今天学什么”“我不懂这个概念”“带我实现 demo”。
- 用户需要根据 `state/*` 判断该复习还是继续学习。

这些情况使用 `project-learning-session-coach`。

## 初始化流程

### 1. 确认目标

先确认或从上下文推断：
- 学习目标：会用、会读源码、会复现、会改造、能面试讲清。
- 学习者基础：语言、框架、领域经验。
- 产物目标：Demo、个人改造点、架构讲解、简历 bullet、面试问答。
- 输出目录：课程包写到哪里。

如果用户只要方案，不落盘。只有用户明确要求生成文件、覆盖课程、写入目录时才修改文件。

### 2. 读取项目事实

优先读取：
- README、架构文档、go.mod/package manifest。
- 入口命令、examples、tests。
- 关键目录、类型定义、接口、核心函数。

事实边界：
- README 定义项目定位，但不等于字段或协议。
- 字段、JSON key、结构体、协议层级必须来自类型定义、schema、配置样例或协议文档。
- 源码路径必须用 `test -e`、`rg --files` 或等价方式确认存在。
- 当前 checkout 是准绳；旧评审和旧教程只能作为参考。

### 3. 拆项目模块地图

先生成 `module-map.md`，不要套 `stage-00/stage-01` 固定阶段。

模块来自项目能力边界和用户目标，例如：
- agent-core
- tool-use
- session-persistence
- provider-model
- memory-palace
- subagent-orchestration
- protocols-mcp-acp-jsonrpc
- cli-tui
- lsp-editor-integration

每个模块必须满足：
- 能在源码中找到依据。
- 能解释为什么值得学。
- 能产出一个练习或小轮子。
- 能说明和其他模块的关系。

### 4. 每个模块生成 8 个文件

每个 `modules/<module>/` 必须包含：
- `README.md`：模块目标和学习顺序。
- `concepts.md`：核心概念讲解。
- `code-reading.md`：源码阅读路径。
- `relationships.md`：模块依赖和协作关系。
- `build-wheel.md`：AI 提供的完整可运行小轮子示例。
- `lab.md`：学习者动手任务。
- `teach-back.md`：讲回问题。
- `checks.md`：验收标准。

模块内部遵循：

```text
用轮子 -> 拆轮子 -> 学概念 -> 读代码 -> 理解抽象 -> 看模块关联 -> 造小轮子 -> 改轮子 -> 讲回
```

### 5. 概念讲解标准

`concepts.md` 中每个核心概念至少包含：
- 权威资料：官方文档、协议规范、标准文档、经典资料，并用自己的话解释。
- 为什么存在：没有它系统会坏在哪里。
- 项目如何实现：绑定源码路径、类型、函数、测试或配置。
- 通俗理解：给新人能理解的类比或最小例子。
- 模块关系：依赖谁、服务谁、影响谁。
- 常见误解：字段、协议、抽象边界、安全边界的混淆点。

不要只写“链接 + 源码路径 + 一句解释”。

### 6. 造小轮子标准

`build-wheel.md` 必须给完整可运行示例代码：
- 文件结构。
- 核心代码。
- 运行命令。
- 期望输出。
- 最小测试或检查命令。
- 和原项目实现的差异。
- 下一步改造任务。

不能写“略”“自行实现”“参考源码补全”。示例太大时，缩小目标，但仍要完整可运行。

### 7. 必备课程包结构

输出根目录必须包含：

```text
START_HERE.md
AGENTS.md
SELF_CHECK.md
README.md
module-map.md
syllabus.md
tasks.md
glossary.md
modules/
ai/
  context.md
  coach-protocol.md
  concept-explanation-protocol.md
  ask-template.md
state/
  metadata.json
  progress.md
  review_schedule.json
  mastery.md
outputs/
```

`START_HERE.md` 必须告诉学习者：
- 第一天做什么。
- 第一条命令是什么。
- 先学哪个模块，为什么。
- 让 AI 先读哪些文件。
- 完成后更新哪些状态文件。

`AGENTS.md` 必须告诉后续 AI：
- 先读 `START_HERE.md`、`module-map.md`、`state/*`、`ai/*`。
- 学习前检查到期复习。
- 用户不知道怎么开始时只给当天一个小任务。
- 概念讲解按 `ai/concept-explanation-protocol.md`。
- 后续会话使用 `project-learning-session-coach` 的方式引导。

### 8. 状态文件要求

`review_schedule.json` 必须是可执行复习队列，不只是节奏说明。至少包含：
- `intervals_days`
- `due_selection_rule`
- `mastery_update_gate`
- `reviews`
- `append_example`
- `review_pass_example`

`mastery.md` 必须定义掌握等级和每个模块当前证据。

`progress.md` 必须给出学习日志模板。

### 9. 输出资产

`outputs/**` 只能是候选模板。每条简历、面试、架构结论都要留证据槽：
- 证据编号
- 命令/测试
- 关键输出
- 源码路径
- 讲回记录

没有证据不得写成已完成成果。

## 自检

交付前必须验证：
- JSON 文件可解析。
- 顶层结构完整。
- 每个模块 8 个文件齐全。
- 不存在旧的固定 `stage-*` 目录，除非用户明确要求。
- 源码路径真实存在。
- `AGENTS.md` 有复习机制和后续会话规则。
- `build-wheel.md` 没有“略/自行实现/补全”。
- `SELF_CHECK.md` 记录源码版本、核验命令、事实边界、二次评审重点。

## 常见错误

- 把课程初始化 skill 写成后续带学 skill。
- 用固定 stage 模板替代项目模块地图。
- 没有 `START_HERE.md`，用户不知道怎么开始。
- `AGENTS.md` 没有复习机制。
- `concepts.md` 只有链接和一句话。
- `build-wheel.md` 没有完整可运行代码。
- outputs 写成学习者已经完成的成果。

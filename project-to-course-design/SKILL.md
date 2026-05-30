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
- 每个模块的函数级源码阅读任务单。
- 学习状态、复习队列、掌握度记录。
- 后续 AI 会话协议。
- 结构化任务注册表。
- 跨模块综合改造任务。
- 候选输出资产模板。
- 可选的 VitePress 教程站点展示层。

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
- 是否生成 VitePress 教程站点：默认不生成；如果用户提到“图文并茂”“前端页面”“VitePress”“教程站点”“可发布文档”，必须确认或直接记录为需要生成。

如果用户只要方案，不落盘。只有用户明确要求生成文件、覆盖课程、写入目录时才修改文件。

如果需要 VitePress，不要在本 skill 内展开站点细节。先完成核心课程包，再调用 `project-course-vitepress-site` 子 skill，把课程包根目录、模块顺序、目标读者和展示风格传过去。

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
- README 的实际学习顺序必须先体验或运行，再拆输出，再学概念；不能嘴上写“用轮子”但步骤从读概念开始。

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

对变化快的资料，例如模型列表、ADK、MCP、ACP、OpenAI/Anthropic/Gemini 工具调用，写入“需要会话时核对官方资料”的提醒；无法联网时必须声明基于课程包生成时资料。

如果模块名包含某个实现级能力，必须读取对应源码后再写项目实现。例如课程写 MCP 实现，就必须读取本项目的 MCP 接入源码；否则只能写成概念对照，不能写成实现事实。

### 6. 造小轮子标准

`build-wheel.md` 必须给完整可运行示例代码：
- 文件结构。
- 运行前预测题。
- 核心代码。
- 运行命令。
- 期望输出。
- 最小测试或检查命令。
- 和原项目实现的差异。
- 下一步改造任务，且包含要改什么、预期输出变化、验证命令。
- 完成后应写入哪些 evidence。

不能写“略”“自行实现”“参考源码补全”。示例太大时，缩小目标，但仍要完整可运行。

### 7. 源码阅读任务单

`code-reading.md` 不能只是文件列表。每个模块至少包含：
- 3 个必须定位的类型或函数。
- 2 条调用链追踪任务。
- 1 个字段、协议或事实边界核验任务。
- 1 个容易误读的点。
- 1 个读完后能改的小需求。

### 8. relationships 与 lab 不能套模板

`relationships.md` 必须是模块专属关系图，不允许所有模块复用同一组泛化关系。每条关系至少包含：
- 上游输入。
- 本模块输出。
- 下游如何使用。
- 源码依据。
- 不能证明什么。

删除自指关系，例如 `agent-core` 不要写“与 agent-core 的关系”。只写 3 到 5 条真实相邻关系。

`lab.md` 必须是模块专属动手任务，不允许只给“运行 go test、填表、写风险”这类通用模板。每个 lab 至少包含：
- 具体输入。
- 具体预期输出。
- 要运行的命令。
- 要对照的源码路径。
- 一个最小改造任务。
- 完成后的 evidence 写入位置。

lab 的目标是服务“改轮子”和“讲回”，不是让学习者凭空填空。

### 9. 必备课程包结构

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
capstone.md
scripts/
  verify-wheels.sh
modules/
ai/
  context.md
  coach-protocol.md
  concept-explanation-protocol.md
  ask-template.md
state/
  metadata.json
  current.json
  task_registry.json
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
- 每次会话必须先读 `state/current.json`、`state/task_registry.json`、`state/review_schedule.json`。
- 有到期复习时先复习；没有到期复习时用 `state/current.json.next_task_id` 到 registry 展开任务。

`AGENTS.md` 必须告诉后续 AI：
- 先读 `START_HERE.md`、`module-map.md`、`state/current.json`、`state/task_registry.json`、`state/*`、`ai/*`。
- 学习前检查到期复习。
- 用户不知道怎么开始时只给当天一个小任务。
- 概念讲解按 `ai/concept-explanation-protocol.md`。
- 后续会话使用 `project-learning-session-coach` 的方式引导。

### 10. 状态文件要求

`current.json` 必须是结构化学习状态选择器，至少包含：
- `current_module`
- `current_task_id`
- `next_task_id`
- `next_task`
- `task_registry`
- `blocked_on`
- `selection_rule`
- 当前任务完成后如何更新 progress、mastery、review_schedule 和下一任务。

`next_task_id` 是本次会话任务指针，必须能在 `state/task_registry.json.tasks` 里解析到完整任务。`next_task` 只是 registry 当前任务的同步快照；如果保留它，必须和 registry 中对应任务完全一致。不要让 `current.json` 和 `task_registry.json` 形成两个不一致的事实源。

`task_registry.json` 必须能把每个 `next_task_id` 机械展开成完整任务对象，至少包含：
- `module_graph`
- `tasks`
- 每个 task 的 `objective`、`files_to_read`、`commands`、`evidence_required`、`on_completion`
- 每个 task 的 `prerequisites`

registry 当前任务的 `on_completion.next_task_id` 不能只是自然语言提示，必须能在 `task_registry.json.tasks` 找到。

`review_schedule.json` 必须是可执行复习队列，不只是节奏说明。至少包含：
- `intervals_days`
- `due_selection_rule`
- `activation_policy`
- `mastery_update_gate`
- `reviews`
- `append_example`
- `review_pass_example`

`review_schedule.json` 中所有 evidence 示例也必须使用 `state/progress.md#<task_id>`，不能用日期型锚点，例如 `state/progress.md#2026-05-30-review-jsonrpc`。示例会被后续 AI 模仿，必须和硬规则一致。

`mastery.md` 必须定义掌握等级和每个模块当前证据。

`progress.md` 必须给出学习日志模板。
`progress.md` 必须定义证据锚点规则，例如 `state/progress.md#<task_id>`；`mastery.md` 和 `review_schedule.json` 只能引用这种锚点，不能写“已完成”“见上文”。

`capstone.md` 必须给出一个跨模块真实改造任务，要求先写事实边界、再改代码、跑测试、补 evidence。它不能假设学习者已经完成成果。

`scripts/verify-wheels.sh` 必须能从每个 `build-wheel.md` 提取 Go 代码并运行，作为可复现自检入口。

### 11. 输出资产

`outputs/**` 只能是候选模板。每条简历、面试、架构结论都要留证据槽：
- 证据编号
- 命令/测试
- 关键输出
- 源码路径
- 讲回记录

没有证据不得写成已完成成果。

capstone 输出必须支持简历项目闭环，但只能给候选模板：
- README 候选结构。
- 关键 diff 证据槽。
- 测试命令和关键输出证据槽。
- 失败用例和边界说明。
- 面试讲回问题。
- 简历 bullet 候选句式。

只有 evidence 填满后，候选句式才能变成可用表述。

### 12. 可选 VitePress 展示层

当用户要求图文并茂、前端页面、教程站点、VitePress、可发布文档或 docs site 时，额外调用 `project-course-vitepress-site` 子 skill。

主 skill 只负责传递这些输入：
- 课程包根目录。
- `module-map.md` 和 `state/task_registry.json` 的模块顺序。
- 学习者画像和教程风格。
- 是否需要本地预览。

VitePress 站点默认写到课程包根目录的 `site/`。它只是阅读入口，不能替代 `modules/`、`state/`、`ai/` 和 `AGENTS.md`。如果站点内容和课程事实源冲突，以课程事实源为准并修正站点。

生成站点后必须按子 skill 验证 `npm run docs:build`；如果依赖安装或构建失败，不能声称站点可运行。

## 自检

交付前必须验证：
- JSON 文件可解析。
- 顶层结构完整。
- 每个模块 8 个文件齐全。
- 不存在旧的固定 `stage-*` 目录，除非用户明确要求。
- 源码路径真实存在。
- `AGENTS.md` 有复习机制和后续会话规则。
- `build-wheel.md` 没有“略/自行实现/补全”。
- `build-wheel.md` 有期望输出、检查命令、差异清单和最小改造任务。
- `code-reading.md` 有函数级任务单，不只是文件列表。
- `state/current.json` 可解析并能指向下一小步。
- `state/current.json.next_task_id` 存在，并能在 `task_registry.json.tasks` 中解析。
- 如果 `state/current.json.next_task` 存在，必须和 registry 当前任务对象一致。
- `state/task_registry.json` 可解析，并且所有 `next_task_id` 都能解析。
- `scripts/verify-wheels.sh` 能运行全部或指定模块小轮子。
- `relationships.md` 没有自指关系和跨模块通用模板。
- `lab.md` 都有模块专属输入、预期输出、最小改造和 evidence 位置。
- 如果用户选择 VitePress，必须存在 `site/package.json`、`site/docs/.vitepress/config.ts`、`site/docs/index.md`，并按 `project-course-vitepress-site` 完成构建验证。
- `SELF_CHECK.md` 记录源码版本、核验命令、事实边界、二次评审重点。

## 常见错误

- 把课程初始化 skill 写成后续带学 skill。
- 用固定 stage 模板替代项目模块地图。
- 没有 `START_HERE.md`，用户不知道怎么开始。
- `AGENTS.md` 没有复习机制。
- `concepts.md` 只有链接和一句话。
- `build-wheel.md` 没有完整可运行代码。
- outputs 写成学习者已经完成的成果。
- 把 VitePress 站点做成第二套事实源，导致 `site/docs` 和 `modules/state` 漂移。
- 用户没有要求站点时默认生成前端项目，增加维护成本。

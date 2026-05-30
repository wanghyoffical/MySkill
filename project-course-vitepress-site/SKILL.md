---
name: project-course-vitepress-site
description: Use when 已经生成模块化项目课程包，用户要求图文并茂、VitePress、前端页面、教程站点、可发布文档或 docs site 展示层。
---

# VitePress 课程站点

## 定位

本 skill 只负责把已有课程包生成 VitePress 展示层。它不是新的事实源，不替代 `modules/`、`state/`、`ai/`、`AGENTS.md`。

核心规则：`modules/state/ai` 是学习系统事实源，`site/docs` 是面向人的阅读入口。

## 输入

调用前必须已有课程包根目录，并读取：
- `README.md`
- `START_HERE.md`
- `module-map.md`
- `tasks.md`
- `capstone.md`
- `modules/*/{README.md,concepts.md,relationships.md,build-wheel.md,lab.md,teach-back.md,checks.md}`
- `state/task_registry.json`

如果课程包还没生成，先回到 `project-to-course-design`。

## 输出结构

默认写到课程包根目录的 `site/`：

```text
site/
  package.json
  docs/
    index.md
    start.md
    module-map.md
    capstone.md
    modules/
      <module>.md
    .vitepress/
      config.ts
```

不要把 `state/` 移进站点。站点页面只链接或摘要状态，不复制成第二套状态协议。

## 页面要求

`docs/index.md`：
- 项目定位。
- 学习者画像。
- 学习路线图。
- Mermaid 总架构图。
- 第一天入口链接。

`docs/start.md`：
- 对应 `START_HERE.md`。
- 明确先读 `state/current.json`、`state/task_registry.json`、`state/review_schedule.json`。
- 给出第一条命令和完成证据。

每个 `docs/modules/<module>.md`：
- 为什么学这个模块。
- 先运行什么。
- 核心概念，必须引用 `modules/<module>/concepts.md` 的事实边界。
- Mermaid 流程图、时序图或模块关系图，至少一种。
- 小轮子代码入口和运行命令。
- lab 任务、常见误解、讲回问题。
- 指向原始 `modules/<module>/*` 文件。

`docs/capstone.md`：
- 跨模块改造目标。
- README 候选结构。
- 关键 diff、测试、输出、失败用例、讲回记录的证据槽。
- 简历候选表述必须保持“候选”，不能伪造成已完成成果。

## 写作风格

- 中文。
- 像工程师手把手教学，讲“为什么这么设计”“这一步解决什么问题”“代码如何跑起来”。
- 少用论文腔和泛泛介绍。
- 图表服务理解，不做装饰。
- Mermaid 节点文字要短，避免整段话塞进节点。
- 不确定的事实回到源码路径或官方资料，不在站点里扩写成结论。

## 技术约束

- VitePress 使用 Markdown/Vue 生态；不要默认把教程站点做成 React。
- 如果用户要求最终教学版项目用 React/Node/TypeScript，把它放在 capstone 或 demos 中，不要混淆为 VitePress 站点实现。
- `package.json` 至少包含：
  - `docs:dev`
  - `docs:build`
  - `docs:preview`
- `.vitepress/config.ts` 必须配置 title、description、nav、sidebar。
- 侧边栏顺序必须来自 `state/task_registry.json` 或 `module-map.md`，不要按文件名随意排序。

## 验证

生成后必须运行：

```bash
cd <course-root>/site
npm install
npm run docs:build
```

如果依赖安装因网络失败，报告失败原因和未完成验证，不要声称站点可构建。

如果用户要立即预览，再启动：

```bash
npm run docs:dev -- --host 127.0.0.1
```

并返回本地 URL。

## 禁止事项

- 不要让 `site/docs` 成为第二套课程事实源。
- 不要把未完成 capstone 写成已完成项目。
- 不要只生成漂亮首页，缺少模块页面和运行命令。
- 不要只贴 Mermaid 图，不解释图里每个关键边。
- 不要把官方文档长篇复制进站点。

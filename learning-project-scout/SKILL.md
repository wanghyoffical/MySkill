---
name: learning-project-scout
description: Use when 用户想寻找、比较或筛选适合学习、读懂、仿写、复刻、vibe coding 模仿的开源项目，尤其关注新手是否能读懂主线、是否有真实工程架构、是否适合实习生用 AI/Web Coding 做小复刻、是否被社区认可、GitHub stars/近期热度是否健康，以及避免玩具 demo 或过大代码库。
---

# 开源学习项目侦察

## 目标

帮助用户找到“适合学习的实战型开源项目”：新手能读懂，但架构又不脱离真实工程。

不要默认推荐最火项目、最简单 demo，或很长的学习路线。输出应该是小而有判断力的项目短名单。

默认目标是“先读懂主线，再判断是否适合用 AI/Web Coding 做小复刻来加深理解”。读懂是首要要求，复刻是验证和加深理解的方式，不是替代读源码。

## 适用场景

当用户提出类似需求时使用：

- “找一个适合新手学习的 Go coding agent 项目。”
- “推荐几个能学习数据库内部实现的开源项目。”
- “我想找一个真实但读得动的项目，学习 X 是怎么实现的。”
- “找类似 Y 的项目，但希望更容易读懂。”

如果用户要的是课程、教程、论文、书籍、普通文档或付费产品，不使用本 skill，除非用户明确要求一起纳入。

## 核心原则

推荐/发现信源负责寻找候选项目；代码仓库本体负责验证项目是否真的适合学习。

GitHub 通常是最重要的项目验证源，但不应该是唯一的项目发现源。

如果需要比较 GitHub 项目的人气、维护状态或近期 star 趋势，优先使用本 skill 附带的 `scripts/github_repo_activity.py`，再结合 README、目录结构和源码入口做学习适配判断。

不要要求用户把 GitHub token 发到聊天里。需要更高 API 额度时，优先让用户在本机完成认证：`gh auth login`，或设置环境变量 `GITHUB_TOKEN`/`GH_TOKEN`。

## 工作流程

### 1. 澄清学习目标

如果用户需求不清楚，先问一个简短问题。优先澄清：

- 想学习的主题、架构或实现模式
- 偏好的语言或技术栈
- 当前水平
- 能接受的代码规模
- 更看重新手可读性、真实架构，还是两者都要

如果用户没有说明，默认同时追求“新手读得懂”和“接近真实工程架构”。

必须先判断用户属于哪种学习重点：

- 主线读懂：默认重点。用户需要读懂核心调用链和工程架构。
- 复刻加深：用户想在读懂后，自己仿写、vibe coding、用 AI 辅助复刻、做 mini clone。
- 背书/展示：用户明确提到秋招、简历、面试、项目故事、社区背书。

不要因为用户说“实习生能读得动”就自动切到背书/展示。实习生场景首先仍然是读懂主线；只有用户明确说要面试表达或简历项目时，才把展示性作为主排序因素。

### 2. 生成目标项目画像

搜索前先写出简短画像：

```text
学习目标：
学习重点：
硬性约束：
真实架构信号：
新手可读信号：
复刻适配信号：
排除条件：
```

按具体领域定义“真实架构信号”。例如：

- Coding agent：agent loop、tool calling、文件读写、shell 执行、session/history、模型 provider 抽象、CLI/TUI、权限或 sandbox 边界。
- 数据库：parser/planner、storage engine、index、transaction、WAL 或 recovery、带查询示例的测试。
- 前端框架：组件模型、状态/响应式系统、renderer、路由或构建集成、示例应用。

不要只停留在“类似 Claude Code”“像数据库”“production-ready”这种模糊标签，要把它们拆成可检查的架构信号。

还要定义“复刻适配信号”，但它必须建立在读懂主线之后：

- 核心链路集中，能在 3-7 天内读完主线。
- 有清楚的最小闭环，例如输入 → agent loop → tool call → 文件/命令执行 → session 记录。
- 项目可以被拆成 mini clone：先做 provider、tool registry、read/write/bash、session，再扩展 TUI/LSP/MCP。
- 代码规模和抽象层数适中；成熟产品级项目即使架构完整，也可能只适合作为进阶参考或架构对照。

### 3. 先查推荐/发现信源

除非用户明确禁止联网，否则要查当前信息。优先使用包含人工筛选、社区讨论或大众认可信号的来源。

推荐的发现信源：

- HelloGitHub：中文友好，经常介绍有趣、入门级开源项目。<https://github.com/521xueweihan/HelloGitHub>
- Awesome Lists：按主题整理的人工 curated 项目入口。<https://github.com/sindresorhus/awesome>
- GitHub Explore、Topics、Trending、Collections。<https://github.com/explore>
- Hacker News，尤其是 Show HN 和相关讨论。<https://github.com/HackerNews/API>
- 垂直榜单，例如 JavaScript/前端领域可参考 Best of JS。<https://bestofjs.org/>
- 与领域强相关的 newsletter、curated list、社区项目展示。

也可以使用 GitHub search，但它只是一个渠道，不能把它当作完整答案。

候选召回要保持梯度，不要只召回高人气项目。候选集至少尝试覆盖：

- 小而完整：stars 可以低，但必须有清楚架构、可运行主线，并适合读懂后做小复刻。
- 中等实战：有真实工程结构，仍能读完主要模块。
- 成熟参考：高 stars 或产品级项目，只作为对照，不默认首推。

低 stars 不能单独淘汰项目。对学习来说，低 stars + 高目标匹配 + 主线清晰，往往比高 stars + 巨大代码库更适合作为第一个项目。

### 4. 回到仓库本体验证

打开候选项目仓库后，再判断是否值得推荐。检查：

- README 是否清楚说明项目目标和运行方式
- 目录结构是否能看出阅读入口
- 代码规模是否适合学习者建立整体地图
- license
- 最近 commit、release、issue/PR 活跃情况
- stars、forks，以及能否查到近期 stars 增长
- 是否有 examples、tests、demo 或 runnable quick start
- 代码里是否真的包含目标画像中的架构信号

人气是证据，不是结论。一个项目即使很有名，如果范围过大、入口混乱或学习适配度弱，也应该降级为“进阶参考”或直接排除。

如果候选项目来自 GitHub，先执行认证门槛，再用脚本抓基础元数据。

认证门槛是硬步骤：

```bash
python scripts/github_repo_activity.py --auth-status
```

- 如果结果显示已经认证，或能读取到认证后的更高 rate limit，继续查询。
- 如果未认证、匿名额度不足，或 `rate_limit.remaining` 太低，先暂停项目查询，询问用户是否授权执行 GitHub CLI 登录。
- 不要跳过询问直接用匿名 API 得出“近期 star/fork unknown”的结论。

推荐询问句：

```text
当前 GitHub API 未认证或匿名额度不足。是否授权我在本机执行 GitHub CLI 登录？
如果你回复“是/可以/执行/帮我登录”，我将运行：
gh auth login --web
```

用户明确同意后，执行：

```bash
gh auth login --web
```

如果用户给出了自定义登录命令，只有命令以 `gh auth login` 开头时才可以执行。登录完成后必须再次执行：

```bash
python scripts/github_repo_activity.py --auth-status
```

确认认证可用后，再继续 GitHub 项目查询。如果 `gh` 未安装，提示用户安装 GitHub CLI，或改用 `GITHUB_TOKEN`/`GH_TOKEN` 环境变量。

基础元数据查询示例：

```bash
python scripts/github_repo_activity.py \
  --repo OWNER/REPO \
  --window 30 \
  --window 90 \
  --max-star-pages 2 \
  --max-fork-pages 2 \
  --format markdown
```

可重复传入 `--repo` 比较多个项目。脚本会抓取 stars、forks、license、language、size、archived、pushed_at、updated_at、open issues，并扫描近期 stars 与近期 forks。

脚本的 token 来源：

- `--token TOKEN`：显式传入，优先级最高；不推荐把 token 写进聊天或长期 shell history。
- `GITHUB_TOKEN` / `GH_TOKEN`：推荐方式之一。
- `gh auth token`：默认 `--token-source auto` 会在没有环境变量时读取 GitHub CLI 登录态。
- `--token-source none`：强制匿名请求，适合确认匿名限额行为。

安全边界：

- 不要让用户把 token 发到聊天里。
- 不要使用 `gh auth login --with-token`，除非用户明确要求并理解 token 会经过 stdin。
- 不要把 token 写入仓库、日志、文档或最终回复。
- 如果登录过程要求浏览器或一次性 code，只转述 GitHub CLI 显示的操作提示，不要索要用户密码或 token。
- 只有在用户拒绝登录、认证失败、GitHub CLI 不可用且用户没有提供环境变量时，才继续使用匿名查询，并把 recent stars/forks 标记为 `unknown` 或低可信度。

### 4.1 近期 star/fork 可信度规则

近期 star 与 fork 增长必须按可信度表达：

- `exact`：脚本从最新 stargazer 页往前扫，已经跨过目标窗口 cutoff，例如近 30/90 天，因此计数完整。
- `sampled`：项目近期很热，达到 `--max-star-pages` 仍未跨过 cutoff；输出的是下限，例如 `>=500`，不能当完整计数。
- `unknown`：API 无法返回时间戳、请求失败，或未执行 recent star/fork 扫描。

不要写“近期 star 增长未验证，所以把 stars/forks/pushed_at 当作近期趋势”。应改成：

```text
近期 star 增长：unknown。原因：用户拒绝认证 / 认证失败 / GitHub CLI 不可用 / API 不支持时间戳。本次只把 total stars、forks、pushed_at 作为大众认可和维护状态的弱信号，不计入近期趋势加分。
```

脚本采用早停优化：

- stars：GitHub stargazers 分页通常越靠后的页越新，因此脚本从 `last_page` 倒着扫；一旦某页最早的 `starred_at` 早于最大窗口 cutoff，就停止。
- forks：GitHub forks API 使用 `sort=newest`，因此脚本从第 1 页开始扫；一旦某页最早的 fork `created_at` 早于最大窗口 cutoff，就停止。

### 5. 先按学习适配度评分

下面的权重是判断框架，不要假装精确计算：

| 维度 | 权重 | 判断重点 |
|---|---:|---|
| 目标匹配度 | 20% | 是否直接匹配用户主题、语言和约束 |
| 实战架构价值 | 20% | 是否有真实实现结构，而不是玩具 demo |
| 新手可读性 | 25% | 模块清晰、规模适中、入口可理解，能先读懂主线 |
| 复刻适配度 | 15% | 读懂之后是否适合实习生用 AI/Web Coding 做小复刻 |
| 人工推荐/学习信源背书 | 10% | 是否被 HelloGitHub、awesome list、HN、GitHub Explore 或垂直榜单提到 |
| 人气与近期趋势 | 5% | stars、近期 stars、forks、社区关注度 |
| 维护状态与许可证 | 5% | 对学习目的来说没有明显废弃，license 可接受 |

如果某个候选项目人气很高但可读性很差，不要把它放在首推位置。

背书/展示来自项目的架构优点和工程取舍，而不是 stars 本身。如果用户明确选择背书/展示，可以临时提高“人工推荐/学习信源背书”和“人气与近期趋势”的权重，但必须说明这是重点切换。不要用“更适合秋招讲”覆盖“更适合先读懂主线”。

### 6. 分类，而不是堆列表

最多推荐 3 个项目。候选项目要分类：

- 最适合第一个读
- 合适备选
- 进阶参考
- 排除项目，并简述原因

如果在当前约束下找不到好项目，可以直接说没有找到，并建议放宽一个约束。

每个推荐项目都必须单独回答一句：“是否适合实习生在读懂后，用 AI/Web Coding 做小复刻？”如果不适合，说明它更适合只读架构、做进阶参考，还是做面试对照。

## 输出格式

使用这个结构：

```markdown
## 目标项目画像
- 学习目标：
- 学习重点：
- 硬性约束：
- 真实架构信号：
- 新手可读信号：
- 复刻适配信号：

## 项目短名单
### 1. 项目名
- 链接：
- 为什么适合：
- 为什么可能不适合：
- 证据信源：
- 阅读入口：
- 建议 3 天阅读路径：
- 复刻适配判断：
- 可复刻切入点：

## 排除或延后
- 项目：原因

## 推荐结论
建议先读 X，因为它最适合先读懂主线……
Y 适合作为后续进阶参考……
```

始终附上使用过的来源链接。如果无法验证近期热度数据，要明确说明。

## 搜索查询模式

不要只用一个宽泛 query。组合多组查询：

```text
<主题> beginner open source project GitHub
<主题> architecture source code GitHub <语言>
site:github.com/521xueweihan/HelloGitHub <主题> <语言>
site:github.com/sindresorhus/awesome <主题>
site:news.ycombinator.com <项目或主题> Show HN
<主题> GitHub trending <语言>
```

GitHub 仓库搜索可以组合这些约束：

```text
<主题> language:<语言> archived:false
<主题> stars:>100 pushed:>YYYY-MM-DD archived:false
<主题> size:<上限> language:<语言>
```

根据目标画像改写关键词，不要只搜索用户原话。

## 常见错误

- 推荐很多项目，而不是给出可辩护的短名单。
- 把 GitHub stars 当成学习价值证明。
- 推荐缺乏真实架构的玩具 demo。
- 推荐成熟产品级项目，却不提醒它更适合进阶参考。
- 把复刻当成替代读源码；复刻只能发生在读懂主线之后。
- 把高 stars/秋招故事性当成首推理由，而没有说明实际架构优点。
- 因为低 stars 或社区背书弱，漏掉结构清晰、适合读懂和小复刻的项目。
- 忽略 license，或忽略项目是否真的能读、能跑。
- 没检查 README、目录结构和源码入口，就说项目适合学习。
- 输出很长的泛泛学习路线，而不是具体文件入口和短阅读计划。
- 没有区分 recent stars 的 `exact`、`sampled`、`unknown` 可信度。
- GitHub 匿名额度不足时，没有先询问用户是否授权执行 `gh auth login --web`，就直接把近期趋势写成 `unknown`。

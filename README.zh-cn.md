# cli-anyweb

通过结构化 CLI，让任何网站对 Agent 更加友好。

`cli-anyweb` 是一个基于 Vercel Labs `agent-browser` 的浏览器 harness 与插件化工作流，通过结构化命令面把普通网站转化为可复用的、对 Agent 原生友好的操作接口。

[English](./README.md) | 简体中文

一条命令：通过浏览器控制、站点 reference、可回放路径与 eval 评估，把为人类设计的 Web 软件变成 Agent 可复用的工具。

## 项目简介

`cli-anyweb` 整合了三个层面：

- 基于 `agent-browser` 构建的通用 runtime 层
- 面向未知网站的接入方法论与可复用 flow 的发现流程
- 插件化结构，使每个站点可以通过 `cli-anything-plugin` 定义自己的 setup、reference 与 eval 资产

## 快速链接

- [快速开始](#快速开始)
- [为什么这件事重要](#为什么这件事重要)
- [为什么不直接用 `agent-browser`](#为什么不直接用-agent-browser)
- [仓库结构](#仓库结构)
- [路线图](#路线图)
- [cli-anyweb-plugin/HARNESS.md](./cli-anyweb-plugin/HARNESS.md)
- [ROADMAP.md](./ROADMAP.md)
- [cli-anyweb-plugin](./cli-anyweb-plugin)

## 痛点

现代前沿模型已经具备很强的 GUI 操作能力，`agent-browser` 这类工具也让浏览器控制变得更容易接入。

但原始能力并不等同于稳定的 Agent 工具。

在实际任务中，很多模型依然会在网页里反复"随机游走"：

- 每次运行都要重新寻找相同的操作路径
- 重复花费 token 和时间重新定位已经找过的按钮、菜单和流程
- 即使能完成任务，也不一定是最高效或最可复用的方式

对于最强的 SOTA 模型，这有时还能接受；但对于更小、更便宜或更专用的模型，这种损耗会更明显。

真正缺少的，不只是浏览器控制能力，而是一层可复用的、对 Agent 原生友好的交互层，让 Web 不再是无结构环境，而是逐渐变成可靠的工具面。

## 愿景

`cli-anyweb` 致力于帮助构建 Agent 原生的 Web 生态：

- 无门槛接入：任何网站都可以通过结构化 CLI 立刻被 Agent 操控
- 无缝集成：不需要专门 API、不需要视觉通道驱动 GUI、不需要重构代码，也不需要复杂适配层
- 面向未来：为人类设计的网站可以变成 Agent 可复用的工具面

## 为什么这件事重要

如果 Web 要成为 Agent 的真实执行环境，成功就不能依赖于每次都重新发现同样的 UI 路径。

重要的转变是：

- 从一次性浏览器控制
- 到可复用的 Web 工作流
- 再到经过评估、持续改进的站点知识

这就是这个仓库试图构建的那一层。

## 为什么不直接用 `agent-browser`

`agent-browser` 是这里的基础，它已经提供了很强的浏览器控制能力。

但仅靠浏览器控制，并不能解决更高层的 Agent 问题：

- 能控制，不等于有可复用的工作流结构
- 一次成功交互，不等于有稳定的路径发现能力
- 一次成功运行，不等于形成了可积累、持续改进的 Web 操作层

`cli-anyweb` 补上了缺失的那一层：

- 更适合 Agent 重复调用的结构化 CLI 命令面
- 比纯视觉驱动更轻量、更稳定的 snapshot 检查原语
- 每站点 reference，让已解决的导航路径可以复用，而不必重新发现
- replay 与 eval 支撑，让系统能持续改进，而不是每次从头开始
- 插件结构，使每个站点可以定义自己的 setup 与浏览器要求

简言之：`agent-browser` 提供浏览器能力，而 `cli-anyweb` 试图把这种能力变成可复用的 Agent Web CLI。

## 核心思路

核心闭环很简单：

1. 通过结构化浏览器 harness 打开并检查网站
2. 发现可行的交互路径
3. 把这条路径沉淀成可复用的 Agent 知识
4. 持续回放、评估并迭代优化

这样，Web 交互就不再是每次重复探索，而是会逐渐变成一个可积累的系统。

## 工作流

```text
Open -> Inspect -> Act -> Capture -> Reuse -> Evaluate
```

更具体一点：

- `open`：打开目标页面
- `snapshot` / `ls` / `cat` / `grep` / `find`：检查当前交互面
- `click` / `type`：执行交互路径
- references：把成功路径沉淀下来
- evals：当站点变化时，回放并评估这些路径
- plugin setup：为站点定义自定义 UA 或浏览器 flags 等特定要求

## 安装

```bash
pip install -e .
npm install -g agent-browser
agent-browser install
```

## 快速开始

```bash
cli-anyweb open https://example.com
cli-anyweb snapshot
cli-anyweb find Example
cli-anyweb get url
```

CLI 使用扁平命令面，例如 `open`、`snapshot`、`ls`、`click` 和 `find`。

## 你能得到什么

- 扁平的、对 Agent 友好的浏览器命令
- 基于 snapshot 的检查与路径发现
- 存储站点 reference 与可复用 flow 知识的地方
- 面向 replay、evaluation 与持续改进的路径
- 用于站点特定 setup 与封装的插件布局

## 仓库结构

- [setup.py](./setup.py)
- [cli_anyweb/README.md](./cli_anyweb/README.md)
- [cli_anyweb/skills/SKILL.md](./cli_anyweb/skills/SKILL.md)
- [cli_anyweb/skills/references](./cli_anyweb/skills/references)
- [cli_anyweb/skills/evals](./cli_anyweb/skills/evals)
- [cli_anyweb/tests/TEST.md](./cli_anyweb/tests/TEST.md)
- [cli-anyweb-plugin](./cli-anyweb-plugin)
- [references](./references)
- [cli-anyweb-plugin/HARNESS.md](./cli-anyweb-plugin/HARNESS.md)

## 路线图

- 清理 `CLI_ANYTHING_ANYWEB_*` 等历史命名以及偏 filesystem 风格的遗留表述
- 增加 `example.com` 之外的真实站点 references
- 构建模型驱动路径发现的 replay/eval 闭环
- 扩展 backend 相关测试，如可执行文件解析、snapshot 解析、path-to-ref 转换
- 使 site-specific plugin setup 成为一等公民，适用于真实网站

完整执行计划见 [ROADMAP.md](./ROADMAP.md)。

## 配置

- 推荐包名：`cli-anyweb`
- 推荐 CLI 命令：`cli-anyweb`
- 推荐额外浏览器 flag 环境变量：`CLI_ANYWEB_AGENT_BROWSER_FLAGS`
- 当前内部 Python 包路径：`cli_anyweb`

## 为什么这个仓库要独立出来

这个仓库最初是从更大的 `CLI-Anything` 生态中拆分出来的一个专注的浏览器 harness。

现在正在围绕更具体的目标重塑：

- 提供通用 runtime 层
- 提供类似 `cli-anything-plugin` 的插件结构
- 让贡献者可以把任意网站变成可复用的站点特定 CLI

## 致谢与归属

这个项目继承并参考了以下工作：

- [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything)
- `cli-anything-plugin/HARNESS.md` 中描述的 harness 方法论
- 原始仓库内的现有浏览器 harness 工作
- 浏览器 harness 打包布局、REPL 约定与 backend 集成方式，后来被此处适配到 `agent-browser`

`cli-anyweb` 是基于 `CLI-Anything` 仓库结构与 harness 方式整理出来的衍生项目。

该仓库应在文档、发布说明、镜像与对外介绍中继续保留对上游项目的清晰归属说明。

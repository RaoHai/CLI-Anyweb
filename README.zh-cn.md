# gui-agent-harness

把为人类设计的网站，变成可复用的 Agent 原生工具。

`gui-agent-harness` 是一个独立仓库，目标是基于 Vercel Labs 的 `agent-browser`，通过结构化 CLI，把普通 Web 站点转化为 Agent 可直接调用、可持续复用的操作接口。

它主要聚焦三个层面：

- 基于 `agent-browser` 的可运行浏览器 harness
- 面向 GUI 导航与决策的 skill 体系
- 用于发现、沉淀、评估最佳路径的站点 reference 与 eval 工作流

## 痛点

今天的大模型已经具备很强的 GUI 操作能力，`agent-browser` 这类工具也让浏览器控制变得更容易接入。

但“能操作”并不等于“适合长期稳定地作为 Agent 基础设施来使用”。

在真实任务里，很多模型依然会在网页里反复“随机游走”：

- 每次运行都要重新寻找相同的操作路径
- 重复花费 token 和时间去定位已经找过的按钮、菜单和流程
- 即使任务能完成，也不一定是最高效、最稳定、最可复用的方式

对于最强的 SOTA 模型，这种低效有时还能接受；但对于更小、更便宜、或更专用的模型，这种损耗会更明显。

真正缺少的，不只是浏览器控制能力，而是一层可积累、可复用、对 Agent 友好的交互基础设施，让 Web 不再是每次都要重新探索的环境，而是逐渐变成稳定可靠的工具面。

## 愿景

`gui-agent-harness` 希望帮助构建 Agent 原生的 Web 生态：

- 无门槛接入：任何 Web 都可以通过结构化 CLI，立刻被 Agent 操控
- 无缝集成：不需要专门 API、不需要视觉通道驱动 GUI、不需要重构代码，也不需要复杂适配层
- 面向未来：只需要一条命令，就能把为人类设计的 Web 变成 Agent 的原生工具

## 为什么不直接使用 `agent-browser`？

`agent-browser` 是这个项目的基础，而且它本身已经提供了很强的浏览器控制能力。

但仅有“控制浏览器”并不能解决更高一层的 Agent 问题：

- 能控制，不等于有可复用的工作流结构
- 能完成一次交互，不等于有稳定的路径发现能力
- 一次成功运行，不等于形成了会持续积累、持续改进的 Web 操作层

`gui-agent-harness` 想补上的，就是这一层：

- 更适合 Agent 重复调用的结构化 CLI 命令面
- 比纯视觉驱动更轻量、更稳定的 snapshot 检查原语
- 可沉淀站点经验的 references，避免每次都从头发现路径
- 可回放、可评估、可持续优化的 eval/replay 支撑

可以简单理解为：`agent-browser` 提供浏览器能力，而 `gui-agent-harness` 试图把这种能力变成可复用的 Agent 基础设施。

## 核心思路

它的核心闭环很简单：

1. 通过结构化浏览器 harness 打开并检查网站
2. 找到一条可行的交互路径
3. 把这条路径沉淀成可复用的 Agent 知识
4. 持续回放、评估并迭代优化

这样，Web 交互就不再是一次次重复探索，而会逐渐变成一个可积累的系统。

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

## 安装

```bash
pip install -e .
npm install -g agent-browser
agent-browser install
```

## 快速开始

```bash
gui-agent-harness open https://example.com
gui-agent-harness snapshot
gui-agent-harness find Example
gui-agent-harness get url
```

当前 CLI 已采用扁平命令面，例如 `open`、`snapshot`、`ls`、`click`、`find`，而不是旧式的分组命令壳。

## 仓库结构

- [setup.py](/Y:/gui-agent-harness/setup.py)
- [agent_harness/README.md](/Y:/gui-agent-harness/agent_harness/README.md)
- [agent_harness/skills/SKILL.md](/Y:/gui-agent-harness/agent_harness/skills/SKILL.md)
- [agent_harness/skills/references](/Y:/gui-agent-harness/agent_harness/skills/references)
- [agent_harness/skills/evals](/Y:/gui-agent-harness/agent_harness/skills/evals)
- [agent_harness/tests/TEST.md](/Y:/gui-agent-harness/agent_harness/tests/TEST.md)
- [HARNESS.md](/Y:/gui-agent-harness/HARNESS.md)

## 当前状态

当前仓库已经提供：

- 一个可运行的、基于 `agent-browser` 的 harness
- 一套以 `open`、`snapshot`、`ls`、`click`、`type`、`get`、`find` 为核心的扁平 CLI
- 可扩展的 skill 与 site reference 体系
- 用于自动路径发现与评估的文档脚手架

当前实现细节：

- 工作目录：`Y:\gui-agent-harness`
- 主 CLI 模块：`agent_harness/gui_agent_harness_cli.py`
- 内部包路径：`agent_harness`
- 浏览器 profile 默认位于项目根目录下的 `.agent-browser-profile`

## 路线图

- 决定是否将内部包目录从 `agent_harness` 重命名为 `gui_agent_harness`
- 继续清理 `CLI_ANYTHING_ANYWEB_*` 等历史命名，以及偏 filesystem 风格的遗留表述
- 增加 `example.com` 之外的真实站点 references
- 建立模型驱动路径发现的 replay/eval 闭环
- 扩展 backend 相关测试，例如可执行文件解析、snapshot 解析、path-to-ref 转换等

## 配置

- 推荐包名：`gui-agent-harness`
- 推荐 CLI 命令：`gui-agent-harness`
- 推荐环境变量前缀：`CLI_ANYTHING_ANYWEB_*`
- 旧的 `CLI_ANYTHING_BROWSER_*` 变量仍保留兼容支持

## 为什么这个仓库要独立出来？

这个仓库将浏览器 harness 从更大的 `CLI-Anything` 单仓库中拆分出来，使它可以作为一个更聚焦的 GUI Agent 项目独立演进。

当前 Python 包位于仓库根目录下的 `agent_harness/`，而不再是原来更深的 `cli_anything/anyweb/` 路径。

## 致谢与归属

这个项目继承并参考了以下工作：

- [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything)
- `cli-anything-plugin/HARNESS.md` 中的 harness 方法论
- 原始浏览器 harness 的实现思路
- 后续被迁移并适配到 `agent-browser` 的打包结构、REPL 约定和 backend 集成方式

`gui-agent-harness` 是基于 `CLI-Anything` 的仓库结构与 harness 方法整理出来的衍生项目。

在文档、发布说明、镜像或对外介绍中，应继续保留对上游项目的清晰归属说明。

<a id="what-it-does"></a>

## 它能做什么

`wizard` 生成交互式 bash 脚本，逐步引导人类完成手动流程：接入第三方服务、执行一次性迁移、将项目从状态 A 转到状态 B。它打开每个 URL，说明该点击和复制什么，捕获返回的值，并写入 `.env` 文件和 GitHub Actions secrets。

[agent](https://www.aihero.dev/ai-coding-dictionary/agent) 编写脚本，绝不运行。由你在自己的机器上运行。因此，向导不是一份供你照做的说明清单；它是驱动流程、保存状态的程序，你只需点击、粘贴、按 Enter。

<a id="when-to-reach-for-it"></a>

## 何时使用

可以输入 `/wizard`，agent 也可以自行使用。当它遇到必须由你完成的步骤（无法替你生成的密钥、无法点击的控制台）时，会构建向导，而不是把说明写进会不断滚动的聊天中。

当下一个阻塞你的事情是去控制台操作时使用：

| 情况 | 向导做什么 |
| --- | --- |
| 新开发者需要先配置六个服务，应用才能启动 | 依次打开控制台，捕获密钥，写入 `.env` 和 CI |
| 一次性迁移需要按特定顺序切换开关 | 将不可逆步骤排好顺序，并设确认关卡 |
| 项目需要一次性从状态 A 转到状态 B | 引导转换，并报告未能完成的内容 |
| 你正准备把这些步骤写进 README | 改为编写可执行版本，使其不易悄然过时 |

不要用它*决定*要构建什么；那应当使用 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 和 [to-spec](https://aihero.dev/skills-to-spec)。

<a id="prerequisites"></a>

## 前置条件

生成向导没有前置条件。生成的向导运行于 bash；阶段需要设置 GitHub secret 或 variable 时，会使用 `gh`。如果 `gh` 缺失或未认证，该阶段会给出警告，结束摘要告诉你哪些需要手动设置，而不是让整次运行失败。

<a id="stages"></a>

## 阶段

一个 **stage** 是一屏内的一项聚焦任务。脚本在阶段之间清空终端，因此超过一屏的阶段会丢掉滚出屏幕的部分。按依赖顺序编写阶段，并设置用于驱动进度显示的 `TOTAL_STAGES`。

编写任何代码之前，先界定范围。[技能](https://www.aihero.dev/ai-coding-dictionary/skill)会先读取仓库，而不是毫无准备地提问：`.env*`、`docker-compose*`、框架配置，以及 `.github/workflows/` 中每个 `secrets.*` / `vars.*` 引用；这些都是向导必须产出的值。之后展示有序阶段列表供你确认，再将各阶段映射为人类遵循的精确路径（"Dashboard → Developers → API keys → Reveal test key → copy"）。不知道当前 UI 时，会问你或查文档，不会编造点击步骤。

界定范围时，为每个捕获值确定去向：

| 目标位置 | 何时使用 |
| --- | --- |
| 仅 `.env` | 本地开发需要，CI 不需要 |
| GitHub secret | CI 读取，且属于敏感值 |
| GitHub variable | CI 读取，且属于公开值 |
| 同时写入 `.env` 和 secret | 本地开发与 CI 都需要 |
| 不写入任何位置 | 阶段只是一个动作：切换开关、升级套餐 |

<a id="the-template-already-solves-the-ux"></a>

## 模板已经解决了使用体验

[模板](https://github.com/mattpocock/skills/blob/main/skills/engineering/wizard/template.sh)提供完整体验：带剩余时间的进度、确认关卡、包括 WSL 的跨平台 URL 打开、秘密值隐藏输入、幂等 `.env` 插入／更新、`gh secret` / `gh variable` 写入，以及汇总所有跳过事项的结束摘要。`STAGES` 标记上方是固定库，每个向导完全相同，绝不手动编辑。一致性正是目的。你的工作只是界定流程并编写各阶段。

编写向导的 agent 绝不端到端运行它，因为它会打开浏览器并等待人类输入。验证采用静态方式：`bash -n`、可用时的 `shellcheck`，以及追踪每个值是否到达范围界定时指定的位置，每个 `set_secret` 名称是否匹配 CI 中真实的 `secrets.*` 引用。请据此调整预期：第一次运行由你完成，那次运行才是测试。

<a id="ephemeral-by-default"></a>

## 默认临时使用

| 你的情况 | 如何处理脚本 |
| --- | --- |
| 一次性迁移、个人设置、不会重复的状态转换 | 保存到临时用途目录或 `scripts/` 路径，运行后删除 |
| 仓库下一位使用者也需要的设置路径 | 提交并从 README 链接，让对方运行脚本，而不是再次问 agent |

<a id="common-questions"></a>

## 常见问题

**API 密钥会进入模型上下文吗？**

不会。agent 编写脚本，不运行它。你自己运行，脚本通过隐藏终端输入捕获密钥，直接写入 `.env` 或 `gh secret`。向导是 CLI，模型没有连接到它。有一个前提：这只适用于向导在运行时捕获的值。如果在界定流程时把密钥粘贴进聊天，它就会像其他粘贴内容一样进入[上下文](https://www.aihero.dev/ai-coding-dictionary/context)。

**能返回去改正输错的值吗？**

运行中不能。没有后退按钮：阶段向前推进，第 3 阶段答错就需要 Ctrl-C 后重新运行。重新运行被设计得很便宜：已经写入 `.env` 的值会作为默认值再次提供，因此正确阶段按 Enter 通过，只重输错误的值。发布当周就有人提过，之后仍未解决：“很喜欢！不过，能返回去修改已经输入的内容吗？”

**它知道哪些已经设置好了吗？**

部分知道，但没有发布时人们想象得那么多。它在提问前读取仓库（`.env` 文件、`docker-compose`、框架配置、CI 中的 `secrets.*` 引用），因此会针对确实缺失的值界定范围，而不像 README 那样从零开始。它不会检查第三方服务。如果 `.env` 里有密钥，向导会再次提供，按 Enter 即保留；如果已经创建 Stripe 账户却没保存密钥，向导仍会把你送到控制台获取。

**它在工作流哪里，追问和规格说明之后吗？**

没有特定位置。它是独立工具，不是流程步骤。常见猜测是 `/grill-with-docs → /to-spec → /wizard`，这个顺序没问题，但触发条件是出现手动流程，可能发生在任何时候：开始之前、构建中途，或交付很久以后。它也能作为发现工具：在你承诺工作之前，界定范围会暴露隐藏前提，例如此前没想到的三把 API 密钥。

**在 Claude Code 之外也能工作吗？**

交付物无条件可以：它是普通 bash 脚本，不关心由哪种 [agent 运行环境](https://www.aihero.dev/ai-coding-dictionary/harness)生成。技能本身可由模型调用，因此会在各处列出：在 Claude Code 输入 `/wizard`，在 Codex 输入 `$wizard`，或直接描述遇到的设置障碍。可由模型调用也让它避开 [#693](https://github.com/mattpocock/skills/issues/693)：该问题中，Claude 桌面和网页界面会从[模型](https://www.aihero.dev/ai-coding-dictionary/model)列表中移除*用户调用*技能，并报告未安装。

**它以前不是只能由用户调用吗？**

是的。现在可以由模型调用，因此遇到必须由你完成的步骤时，agent 会主动使用。以前能做的事情没有失效：模型调用只是*增加* agent 的调用能力，绝不会取消你的能力，所以 `/wizard` 的行为完全与以前相同。改变的是它消除的一种失败模式：agent 在构建中途碰到凭据障碍，把六条编号步骤扔进聊天，让你自己照做。

**它以前在 `in-progress/`，现在在哪里？**

从 v1.2 起位于 `engineering/`。它从 beta 分类毕业，现在随插件交付，因此会与其他正式收录技能一起到达，无需单独安装。毕业时行为没有改变。

<a id="its-working-if"></a>

## 如何判断它有效

- 脚本存在之前，先展示有序阶段列表及每阶段产出的值，并请你确认。
- 每个 URL 都在询问对应页面的值之前打开。不会让你粘贴尚未引导你去获取的内容。
- 秘密值盲输。敏感内容不会回显到终端历史。
- 每个阶段一屏容纳。仍需要的内容不会滚出屏幕。
- Ctrl-C 后重新运行，会提供已保存值作为默认值，让你从上次进度继续。
- 最后一屏列出写入了什么，并单独列出哪些未完成、需要手动处理。

<a id="where-it-fits"></a>

## 它在流程中的位置

`wizard` 是随时可用的独立工具，位于自动化停止、必须由人点击的界线上。最接近的相邻技能是 [setup-matt-pocock-skills](https://aihero.dev/skills-setup-matt-pocock-skills)，因为两者都为了让仓库进入可工作状态：后者配置这套技能，`wizard` 则为其他内容生成设置路径。它也与 [implement](https://aihero.dev/skills-implement) 配合：构建落地的功能需要凭据或手动切换时，向导负责完成人类那一半工作。不确定此刻哪个技能适合时，[ask-matt](https://aihero.dev/skills-ask-matt) 会为你指路。

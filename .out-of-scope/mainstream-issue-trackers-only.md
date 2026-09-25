<a id="issue-tracker-integrations-are-limited-to-mainstream-tools"></a>

# Issue 跟踪器集成仅限主流工具

`setup-matt-pocock-skills` 仅对**主流** issue 跟踪器提供一等支持。添加小众、新兴或单一厂商实验性跟踪器支持的请求，不在范围内。

<a id="why-this-is-out-of-scope"></a>

## 为什么超出范围

每个 issue 跟踪器后端都会把 CLI 形态硬编码进技能（命令、标志、输出解析）。每个新增后端都成为永久维护面，因为工具 CLI 演变时必须继续可用，还要持续与 `/to-spec`、`/to-tickets`、`/triage` 等配合测试。只有相当一部分用户实际拥有的跟踪器，才值得付出该成本。

“主流”需要判断，不是数字门槛：

- GitHub、GitLab 和 Backlog.md 属于我们认为的主流工具：广为人知、广泛使用，早已走出实验阶段。
- 一个全新、面向 agent、只有几百 GitHub stars 的工具不算，无论设计多有趣。

Stars、年龄、下载量都是有用信号，但都不是规则。规则是：普通工程师是否认识这个工具，并且有可能为团队选择它？

非主流跟踪器已有变通入口：

- `local markdown`：用于轻量仓库内跟踪。
- `other/custom`：供想自行接入的用户使用。

两者都不要求核心技能了解具体工具。

<a id="prior-requests"></a>

## 既往请求

- #99：“添加 dex 作为 issue 跟踪器后端”（请求时 dex 约发布 3 个月，约有 300 stars）

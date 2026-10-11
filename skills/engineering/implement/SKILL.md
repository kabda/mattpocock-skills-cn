---
name: implement
description: "根据规格说明或一组工单实现一项工作。"
disable-model-invocation: true
---

实现用户在规格说明或工单中描述的工作。

用户传入工单引用时，从 issue 跟踪器获取，开始前说明标题。引用有歧义时，询问用户。

尽可能通过 Skill 工具调用 "tdd"，在预先约定的 seam 上工作。

定期运行类型检查，定期运行单个测试文件，并在结束时运行一次完整测试套件。

完成后，通过 Skill 工具调用 "code-review" 审查工作。

将工作提交到当前分支。

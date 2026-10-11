<a id="what-it-does"></a>

## 它能做什么

当一条消息没能让你理解时，输入 `wait-what`。[agent](https://www.aihero.dev/ai-coding-dictionary/agent) 随后会重新讲述刚才的内容。它补上你缺少的背景，用浅显英语表达，并使用项目 `GLOSSARY.md` 中的词汇。

这个技能只有三行。这是有意的设计，不是未完成的草稿。对抗啰嗦的技能会因自身膨胀而失败：一个四百行的简洁表达技能依然会让[模型](https://www.aihero.dev/ai-coding-dictionary/model)啰嗦，因为模型读到的是体量，而不是恳求。本技能只带着一个精确的引导词，没有其他负担。

<a id="when-to-reach-for-it"></a>

## 何时使用

输入 `/wait-what` 调用它。agent 不会自行使用，也不应当自行使用。只有你知道自己从哪里开始跟不上。

一旦发现自己开始略读，就使用它。agent 可能偏离到自创术语里、堆叠了五个缩写，或者解释一项你从未见过前提的决策。它修复当前已经发生的对话。如果想从源头防止术语混乱，使用 [grill-with-docs](https://aihero.dev/skills-grill-with-docs)，预先建立共享语言。

<a id="the-name-is-the-mechanism"></a>

## 名称就是机制

引导词是 **wait**（等一下）。"Be concise"（简洁一点）是关于 agent 输出的指令，模型会通过裁掉词语来遵守，让你更加跟不上。**Wait** 关注的是*你的*状态。它说明理解在这里中断了。听到“简短些”的 agent 会写成电报体；听到“等等，我跟不上了”的 agent 会退一步解释。

这个区别就是整个技能。所有流行的治啰嗦方法，都以*输出*命名：`/tldr`、`/no-fluff`、`/talk-normal`。模型会矫枉过正，写出原始人式的简陋表达，虽然更短，却并不更清楚。把*听者*的状态说出来，就同时提出了两个要求：更少的词，**以及**你缺少的背景。

技能说的是重新讲述 **that**（那件事），而不是“上一条消息”。让你跟不上的内容通常不止一个段落，因此由 agent 决定回溯多远。

<a id="it-plugs-into-the-language-you-already-have"></a>

## 复用你已有的语言

正文复用了全局 `CLAUDE.md` 和项目 `GLOSSARY.md` 中已有的引导词。ASD-STE100 Simplified Technical English 决定表达风格，通用语言提供名词。技能、`CLAUDE.md` 与 `GLOSSARY.md` 使用相同的 [token](https://www.aihero.dev/ai-coding-dictionary/token)，因此调用它并不是新增指令，而是提醒 agent 遵守已同意的指令。

如果没有 `GLOSSARY.md`（也没有 `GLOSSARY-MAP.md` 指向当前上下文的对应文件），技能仍然有效。你只会失去领域词汇这一部分。

<a id="its-working-if"></a>

## 如何判断它有效

- 重新讲述的内容**更短、更清楚**，而不是更短、更生硬。
- 它补上你缺少的前提，而不是只删字。
- 项目名词取代自创词语。`GLOSSARY.md` 中的术语重新出现。
- 你可以连续使用两次，而不会退化成过度简略的表达。

<a id="where-it-fits"></a>

## 它在流程中的位置

你可以在任何对话的任何时刻、任何其他技能内部使用 `wait-what`。它在事后修复一条消息。真正的根治方式是事先约定共享语言，这正是 [grill-with-docs](https://aihero.dev/skills-grill-with-docs) 的作用：在[追问](https://www.aihero.dev/ai-coding-dictionary/grilling)会话中同步运行 [domain-modeling](https://aihero.dev/skills-domain-modeling)，将双方使用的词语写入 `GLOSSARY.md`。如果不确定此刻哪个技能适合，[ask-matt](https://aihero.dev/skills-ask-matt) 会为你指路。

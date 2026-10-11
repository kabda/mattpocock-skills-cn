---
"mattpocock-skills": patch
---

`code-review` 现在会搜索仓库中的标准文件，并始终把 `CODING_STANDARDS.md` / `CONTRIBUTING.md` 交给 Standards 子 agent（#1065）；在前台运行两个子 agent，使用它们返回的报告（#1073）；通过已提供的跟踪器文档解析 issue 跟踪器，不再使用硬编码路径（#937）。

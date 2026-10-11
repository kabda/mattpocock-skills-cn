---
"mattpocock-skills": patch
---

`handoff` 现在明确操作系统临时目录的位置（`$TMPDIR`，否则 `/tmp`；Windows 使用 `%TEMP%`），让 agent 不再猜测（#272）。

---
"mattpocock-skills": patch
---

`wizard` 模板修复：`_existing` 解码双引号包裹的 `.env` 值，避免按 Enter 保留当前值时把引号也存进去（#1220）；阶段在 `run_wizard` 内运行，避免运行中编辑脚本使它中止（#1142）；`tput clear` 失败时 `_clear` 回退到 ANSI（#1081）；`write_env` 同时设置 shell 变量（#1041）；移除未使用的 `RED`（#1003）。

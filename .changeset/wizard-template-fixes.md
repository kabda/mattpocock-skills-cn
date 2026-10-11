---
"mattpocock-skills": patch
---

`wizard` 模板修复：`ask` 使用 Readline，使方向键可以移动光标（#741）；`write_env` 用单引号包裹值，使空格、`#`、`$` 和引号经 `source` 及 dotenv 读取后仍保留（#770）；没有浏览器打开器时，`open_url` 输出自行打开链接的提示（#774）；`write_env` 通过符号链接写入 `.env`，保留既有文件的 mode（#811）；`ask` 和 `ask_secret` 遇到 EOF 时失败，不再循环（#852）。

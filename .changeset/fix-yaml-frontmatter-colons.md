---
"mattpocock-skills": patch
---

为 `to-spec`、`code-review`、`setup-matt-pocock-skills`、`writing-fragments`、`writing-shape` 和 `wait-what` 的 frontmatter `description` 加引号。#905 清理 em dash 后留下未加引号的冒号加空格，导致各块 YAML 无效，`skills.sh` 发现阶段跳过这六项，无法通过 `npx skills` 列出或安装。

---
"mattpocock-skills": patch
---

retro：在记录编码标准发现前，先区分机械性问题与判断取舍。机械性违规（固定语法模式、禁止的 API、导入形态、文件位置规则）现在改用确定性检查（linter 规则、pre-commit hook 或 CI job），把 `CODING_STANDARDS.md` 留给真正的判断取舍。自动检查部分现在也把完全没有护栏的仓库（没有 pre-commit hook，没有 CI lint/typecheck/test job）本身视为发现。

# 跨平台安装提示词（Codex / WorkBuddy / Trae / 其他 AI）

把下面整段复制给目标 AI 即可。仓库是 Private，目标机器需要已登录有权限的 GitHub 账号；或者能访问 NAS 上的 `Y:\Skills\codex-skills-library`。

---

```text
请把我的技能库安装到你自己的技能/规则系统里，并按统一标准配置。全程不要问我，做完再汇报。

【来源】
- 优先：git clone https://github.com/ElevenZhou/codex-skills-library.git （已存在就 git pull）
- 备选：本机/NAS 路径 Y:\Skills\codex-skills-library 或 \\192.168.31.121\projects\Skills\codex-skills-library
- 以仓库 main 分支为唯一标准，不要自己改写技能内容。

【要安装的技能（skills/ 目录下）】
核心 5 个，必须装：
1. auto-loop —— 别名：老大、大哥、老大哥、大当家、头儿（总调度）
2. project-inception-analysis-cockpit —— 别名：小二、老二、二哥、二当家（立项调研）
3. project-employee-agents —— 别名：小三、老三、三哥、三神、三当家（项目团队推进）
4. xiaowu-contract-review —— 别名：小五（合同审阅）
5. local-image-generator —— 唯一的出图技能（默认 gpt-image-2.5-flare，high 画质）
其余技能：auto-loop/references/skill-registry.md 技能表里列出、且你的平台能用的，也一并安装。

【安装方式（按你的平台能力选一种）】
A. 你支持 Agent Skills（目录里放 SKILL.md）：
   把 skills/<技能名>/ 整个目录复制到你的技能目录，保持 SKILL.md、references/、scripts/ 的结构不变。
   - Codex：$CODEX_HOME/skills/<技能名>/（默认 ~/.codex/skills），保留 agents/openai.yaml
   - Claude Code：~/.claude/skills/<技能名>/，不需要 agents/
   - 其他平台：放到你官方文档规定的技能目录。
B. 你不支持 Skills、只支持规则/记忆/自定义指令（如 Trae 的 Rules、WorkBuddy 的知识库或自定义指令）：
   1. 把仓库放在本地固定路径，不要拆散文件。
   2. 新建一条全局规则，内容如下（把 <仓库路径> 换成实际路径）：
      ---
      我有一个技能库，位于 <仓库路径>/skills/。
      当我说出以下别名或任务时，先完整读取对应的 SKILL.md，再严格按它执行；SKILL.md 里提到的 references/ 文件按需读取：
      - 老大/大哥/老大哥/大当家/头儿，或“全自动/自动驾驶舱/循环优化” → skills/auto-loop/SKILL.md
      - 小二/老二/二哥/二当家，或“项目立项/可行性分析” → skills/project-inception-analysis-cockpit/SKILL.md
      - 小三/老三/三哥/三神/三当家，或“启动项目团队/继续推进项目” → skills/project-employee-agents/SKILL.md
      - 小五，或“审合同/看合同” → skills/xiaowu-contract-review/SKILL.md
      - 作图/生成图片/画图 → skills/local-image-generator/SKILL.md
      - 其他任务：先查 skills/auto-loop/references/skill-registry.md，有对口技能就读对应 SKILL.md。
      技能自己的确认门禁（如小五未经许可不改合同、广告启停需授权）优先于“全自动不打扰”。
      ---
C. 如果你的平台同时支持 A 和 B，用 A，并额外加上 B 的规则作为兜底。

【统一标准（必须遵守）】
1. 技能名、别名、版本号以仓库为准；每个 SKILL.md 标题下有 `Skill version`，安装后逐个核对。
2. 不修改技能内容；平台不兼容的地方（例如命令写法）只在你的规则里补充说明，不改源文件。
3. 不复制、不打印、不提交任何 API key。图片工具的 key 只存在于工具自己的 .env.local，不要读出或转存。
4. 安装前如果目标位置已有同名技能，先改名备份（加 -backup-日期 后缀），再安装。
5. 安装后从仓库同步更新：以后我说“同步技能库”，就 git pull 后按同样方式重新安装。

【验收（做完逐项回报）】
1. 列出已安装的技能、安装位置、每个技能的 Skill version，并与仓库对比是否一致。
2. 用一句话自测别名路由，不要真正执行任务，只回答会调用哪个技能、会先读哪个文件：
   - “老大，帮我做个产品介绍 PPT”
   - “小二，看看这个项目值不值得做”
   - “三哥，继续推进项目”
   - “小五看下这份合同”
   - “画一张网站首图”
3. 说明你用的是安装方式 A、B 还是 C，以及平台不支持、做不到的部分（例如无法运行脚本、读不到 NAS），不要假装成功。
```

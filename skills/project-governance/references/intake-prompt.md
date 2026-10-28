# Empty-project intake prompt

Use this prompt when initializing an empty directory without enough project information:

```text
这是一个空项目目录，目前没有足够信息安全初始化。请先提供以下必须资料：

1. 项目名称：给人看的正式名称
2. 项目代号：短、稳定、适合目录和 Git 使用的代号
3. 项目目标：希望解决什么问题，或交付什么结果（一句话）
4. 目标用户：谁使用，或哪个内部系统/团队使用
5. 初始范围：第一阶段明确要做什么
6. 明确排除项：第一阶段不做什么
7. 首个验收标准：怎样判断第一阶段完成
8. 当前阶段：discovery / build / integration / validation / release / maintenance
9. 参考对象：没有就写“无”；有就列出名称、链接或本地路径

建议资料可以稍后补充：
- Git 方式：new 或 cloned-existing
- 远程仓库地址
- 截止日期或评审日期
- 目标平台和运行时版本
- 技术偏好与限制
- 依赖和外部服务
- 设计或竞品参考
- 环境矩阵、部署目标、测试策略
- 成本边界、已知风险和开放问题

收到必须资料后，我再创建项目目录、README、AGENTS、AI_PROJECT_HANDOFF、项目文档和治理配置。
```

Do not ask for owner/team or authorization status. References are treated as authorized by default. Do not require Git remote information before initialization.

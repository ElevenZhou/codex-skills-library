---
name: project-employee-agents
description: (Aliases 小三 / 老三 / 三哥 / 三神 / 三当家) Build and operate a reusable virtual project company with executive, product, market, design, delivery, growth, customer, finance, procurement, and partnership roles across the full project lifecycle. Automatically apply when the user says 小三, 老三, 三哥, 三神, 三当家, 启动项目团队、项目员工开工、项目全周期管理、组建岗位团队, or describes a project goal that needs multiple business roles; do not require the user to name a specific role.
metadata:
  short-description: 项目员工 Agent 团队与全周期管理
---

# Project Employee Agents（小三 / 老三）

Skill version: `2026.10.05`

别名：**小三**、老三、三哥、三神、三当家。三兄弟分工：老大 = `auto-loop` 总调度；老二 = `project-inception-analysis-cockpit` 立项调研；老三（本技能）= 项目团队，负责立项后的计划、执行、上线和运营。

把 Agent 当作岗位员工管理：每个角色有职责边界、经验判断、工作行为、技能包、输入、输出、验收标准和交接规则。角色文件是行为契约，不是人物设定。

## Operating rule

先判断项目阶段、目标和约束，再只激活所需岗位。每次工作必须产生可检查的管理成果；成果要写明事实、假设、决策、负责人、截止时间、风险、下一步和验收证据。

不要让多个角色同时对同一成果做无边界修改。由项目经理维护任务与决策台账，由 COO 维护流程和资源约束，由 CEO 在重大取舍上拍板。

## Team map

- CEO：方向、重大取舍、资源优先级、最终责任。
- COO：经营节奏、流程、跨部门协同、风险关闭。
- 项目经理：范围、计划、依赖、会议、台账、交付验收。
- 产品经理：用户问题、价值假设、需求优先级、产品指标。
- 策划经理：方案、叙事、活动机制、内容和执行路径。
- 市场经理：市场洞察、细分、渠道和需求验证。
- 品牌经理：定位、品牌资产、信息一致性和声誉。
- 设计经理：体验、视觉、设计系统、可用性和交付质量。
- 技术经理：架构、技术路线、质量、成本、可维护性。
- 测试经理：验收标准、测试策略、缺陷风险和发布门禁。
- 客户经理：客户需求、关系、反馈、续约和问题升级。
- 合作经理：伙伴选择、合作方案、商务边界和联合交付。
- 投放经理：预算、素材、实验、归因、优化和止损。
- 采购经理：供应商、采购规格、比价、交付和合同风险。
- 财务经理：预算、现金流、成本、收益、回款和经营分析。

## Lifecycle routing

Read `references/usage.md` when deciding how a user invokes the team without naming individual roles. Read `references/architecture.md` when turning this operating system into a runnable agent product. Read `references/lifecycle.md` before assigning work by phase. Read `references/role-cards.md` when activating a role. Read `references/deliverables.md` when creating or reviewing outputs. Read `references/operating-templates.md` when the project needs a brief, weekly review, decision record, risk register, launch review, or retrospective.

The default phase order is: pre-initiation, early, middle, late-middle, late delivery, initial launch, early promotion, mid promotion, iterative loop, late operations, and closeout. A project may move backward when evidence invalidates an assumption.

For a deep go/no-go analysis in the pre-initiation phase (market, competitors, open-source options, ten-role scoring, inception report), hand off to 老二 (`project-inception-analysis-cockpit`) and import its decision, risks, and rollout plan into the project brief. This skill owns everything after the go decision.

## Minimum execution loop

1. Project manager creates the brief, phase, objective, decision owner, and acceptance checks.
2. CEO/COO confirm strategic fit, resource ceiling, risk tolerance, and operating cadence.
3. Relevant specialists produce independent inputs with sources and confidence levels.
4. Project manager reconciles conflicts into options, decision points, dependencies, and owners.
5. Decision owner records the decision and why rejected options were rejected.
6. Builders execute against the approved scope; test and finance review the relevant gates.
7. Customer, market, and delivery signals are captured as evidence, not anecdotes.
8. COO closes blocked dependencies; CEO intervenes only on strategic or resource exceptions.
9. Project manager publishes a status snapshot and next-cycle plan.
10. At each loop, preserve reusable lessons in the project memory and update the role or phase card only when the lesson generalizes.

## Quality gates

- Every role has a single accountable owner for each deliverable.
- Every recommendation separates fact, assumption, option, and decision.
- Every phase has a measurable exit condition.
- Every launch or spend decision has a rollback or stop-loss rule.
- Customer, financial, security, legal, and production risks are visible before commitment.
- Outputs are stored in durable project files and linked from the project index.
- A reviewer checks whether the output changes the next action; decorative analysis does not pass.

## Safety and authority

Agents may analyze, draft, compare, and prepare reversible changes. Production changes, external commitments, budget spend, contract acceptance, customer promises, or irreversible deletion require explicit human authorization at the point of action. Never put credentials or private customer data in role cards or project memory.


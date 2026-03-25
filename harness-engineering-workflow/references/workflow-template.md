# Harness Engineering Workflow Template

基于 OpenAI 2026-02-11 文章《工程技术：在智能体优先的世界中利用 Codex》抽象而成。

适用场景：
- 需要启动多个 agent 完成研究、设计、实现、评审或修复任务
- 希望把人类工作重心从“亲自执行”切换到“设计环境、明确意图、构建反馈回路”
- 希望降低上下文漂移、重复劳动、审核瓶颈和 AI 残渣扩散

不适用场景：
- 没有稳定代码仓库或记录系统
- 无法提供基础工具、验证环境或最小质量门
- 任务本身高度模糊，且短时间内无法收敛目标

## 1. First Principles

1. 人类掌舵，智能体执行。
2. 不先催模型，先修环境。
3. 代码仓库是记录系统，不在仓库里的知识默认不存在。
4. `AGENTS.md` 是目录，不是百科全书。
5. 上下文采用渐进披露，禁止一次性灌满。
6. 约束必须机械执行，不能只靠文档倡议。
7. UI、日志、指标、追踪必须对 agent 可读。
8. 高吞吐下等待成本高于纠错成本，流程应小步快跑。
9. 必须持续做熵治理和垃圾回收，把人的品味编码成系统规则。
10. 优先消灭非编码瓶颈，尤其是验证、测试、部署、排障和 Review。
11. 上下文设计要尽量保持稳定前缀，优先追加，不轻易重写。
12. 外部反馈是对冲幻觉的核心机制，不能只靠模型内推理。
13. 当单 agent 上下文逼近上限时，用 subagent 分治，不强行塞进一个窗口。
14. 人类默认从逐行检查者转向结果验收者。

## 2. Operating Model

### Human Responsibilities

- 定义目标、非目标、约束和成功标准
- 设计运行环境、状态流转和质量门
- 只在争议、优先级、验收标准和发布时介入

### Agent Responsibilities

- 检索、拆解、实现、验证、评审、重构
- 按固定契约输出可检查结果
- 使用标准工具直接读取代码、日志、测试和运行态信号

### Default Rule

如果任务失败，先问：
- 缺了什么工具
- 缺了什么结构
- 缺了什么约束
- 缺了什么记录
- 缺了什么反馈回路

不要先问 agent 为什么“不够努力”。

## 3. Required Environment

开始前必须至少具备以下骨架：

```text
repo/
  AGENTS.md
  ARCHITECTURE.md
  docs/
    design-docs/
    product-specs/
    references/
  exec-plans/
    active/
    completed/
  generated/
  scripts/
  tools/
```

环境要求：
- `AGENTS.md` 只保留入口、导航、角色规则和关键禁区
- `docs/` 承载真实知识，不把关键约束藏在聊天记录中
- `exec-plans/` 记录计划、决策日志、进度和回退点
- `generated/` 存放 schema、索引、派生文档等可再生资产
- `scripts/` 和 `tools/` 让 agent 可直接执行常见操作
- 工具优先提供结构化输出，而不是长篇自然语言
- 错误信息必须足够清晰，便于 agent 反思和纠偏
- 高频工具优先低延迟，避免 agent 在反馈链路上空转
- 尽量保持 system instructions 和核心前缀稳定，减少上下文缓存失效

建议优先接入的 AI 友好工具：
- LSP 或静态分析器
- 单元测试、集成测试和验收测试入口
- 浏览器自动化或 UI 验证工具
- 日志、指标、trace 查询入口
- 部署、回滚和灰度状态读取接口

## 4. Standard Roles

| Role | Objective | Inputs | Outputs | Must Not Do |
|---|---|---|---|---|
| `Orchestrator` | 拆任务、分派、收敛 | 目标、约束、源材料 | `Task Brief`, `Task Graph`, `Integration Ledger`, `Decision Log` | 深入替代其他 agent 完成专业子任务 |
| `Source Analyst` | 抽取事实、证据、术语 | 原始材料 | `Claims List`, `Evidence Map`, `Glossary` | 直接设计方案 |
| `Principle Mapper` | 从材料抽象工程原则 | claims, evidence | `Principle Set`, `Mapping Table` | 写实现细节 |
| `Workflow Designer` | 设计步骤、依赖和回退 | 原则、任务目标 | `Workflow Draft` | 越权裁决 |
| `Implementer` | 完成代码或文档产出 | task brief, context pack | patch, draft, tests | 改写上游目标 |
| `Critic` | 找缺口、冲突和风险 | 草案、过程记录 | `Risk Register`, `Revision Requests` | 充当主叙事 writer |
| `Quality Gate` | 判定是否过门 | 各阶段产物 | `Pass`, `Conditional Pass`, `Fail` | 直接修改内容 |
| `Template Editor` | 把结果编排成可复用资产 | 已过门内容 | `Reusable Template`, `Runbook` | 改变核心结论 |
| `Human Decision Maker` | 做方向性裁决 | 待裁决项、残余风险 | `Decision Log` | 回到亲自执行所有细节 |

Artifact schemas and ownership are canonical in `artifact-registry.md`.

## 5. Phase-by-Phase Workflow

### Step S0. Task Brief

Objective:
压缩成单一任务陈述，避免多个目标混跑。

Inputs:
- 用户请求
- 源材料
- 时间、范围、交付约束

Method:
- 定义 `Goal`
- 定义 `Non-goals`
- 定义 `Constraints`
- 定义 `Success Criteria`
- 定义 `Human Decision Points`

Outputs:
- `Task Brief`

Acceptance:
- 目标单一
- 完成标准可判断
- 非目标明确

Fallback:
- 目标含糊时，不启动后续 agent

### Step S1. Environment Design

Objective:
先设计运行环境，再启动 agent。

Inputs:
- `Task Brief`

Method:
- 定义目录结构
- 定义文件命名
- 定义统一输出格式
- 定义状态、版本和日志字段
- 定义只读与可写边界
- 定义 `Role Owner Table`

Outputs:
- `Execution Environment Spec`
- `Role Owner Table`

Acceptance:
- 所有 agent 使用同一套骨架
- 产物可合并、可追踪、可审计
- 每个角色已有明确 owner

Fallback:
- 输出无法合并时，先修环境而不是继续执行

### Step S2. Context Packaging

Objective:
按角色最小化发放上下文。

Inputs:
- `Execution Environment Spec`
- 原始材料

Method:
- 切分为 `Core Context`
- 切分为 `Optional Context`
- 明确 `Forbidden Scope`
- 标注事实、推断和未知项
- 固定稳定前缀，只在尾部追加任务态上下文
- 将高频复用说明沉淀为稳定系统规则，而不是每轮重写
- 把长历史压缩成状态摘要，避免全文回灌

Outputs:
- 每个角色的 `Context Pack`

Acceptance:
- 每个 agent 只拿到完成当前任务所需内容
- 关键来源可追溯
- 核心前缀尽可能稳定
- 新增上下文以追加为主，而不是反复改写

Fallback:
- 越权和幻觉上升时，缩小上下文并增加约束

### Step S3. Task Graph

Objective:
把任务拆成可并行、可验收的子任务。

Inputs:
- `Task Brief`
- `Context Pack`

Method:
- 定义并行块
- 定义串行依赖
- 定义 owner
- 定义每个任务的命名输出和 `Writable Area`
- 定义终止条件
- 定义人工裁决点
- 标记上下文重载风险点
- 对高复杂度任务预先定义 subagent 拆分策略

Outputs:
- `Task Graph`

Acceptance:
- 每个节点只有一个 owner
- 依赖清晰，没有责任空洞
- 不把超长链路任务硬塞给单个 agent

Fallback:
- 若两个 agent 在做同一件事，重构任务树

### Step S4. Parallel Execution

Objective:
让 agent 在边界内并行工作。

Inputs:
- `Task Graph`
- role-specific `Context Pack`
- 固定输出契约

Method:
- 并行运行分析、设计、实现、风险扫描
- 统一格式输出
- 中间结果只写入各自区域
- 通过工具调用获取外部事实反馈，而不是只做文本推理
- 当主 agent 上下文压力过高时，拆给子 agent 独立执行

Outputs:
- 子任务产物集合

Acceptance:
- 输出字段统一
- 结论能回溯来源
- 未越权定稿
- 关键步骤有外部验证信号支撑

Fallback:
- 失败仅回退到责任节点

### Step S5. Risk Scan

Objective:
在过门前稳定产出风险结论，而不是把风险检查隐含进整合过程。

Inputs:
- 子任务产物集合

Method:
- 由 `Critic` 扫描来源可靠性、角色边界、可验证性、上下文膨胀和工具友好度
- 逐条记录风险、证据、owner 和 required action

Outputs:
- `Risk Register`

Schema:
- `Risk`
- `Severity`
- `Evidence`
- `Owner`
- `Required Action`
- `Status`

Acceptance:
- 关键风险有明确 owner
- 每条高风险都带 evidence 和 required action

Fallback:
- 若高风险无法归属 owner，回退到 `Task Graph`

### Step S6. Integration

Objective:
从并行发散收敛到统一草案。

Inputs:
- 各 agent 输出
- `Risk Register`

Method:
- 去重
- 消歧
- 标记冲突
- 合并为统一草案
- 保留带完整证据字段的整合账本
- 将冲突裁决、人工决策和 gate 返工要求追加到同一份 `Decision Log`

Outputs:
- `Unified Draft`
- `Open Questions`
- `Integration Ledger`
- `Decision Log`

Ledger Schema:
- `Agent`
- `Claim`
- `Artifact Name`
- `Owner`
- `Evidence Source`
- `Decision`
- `Next Step Or Fallback`

Acceptance:
- 没有重复叙述
- 冲突被显式标记
- 原则到执行步骤映射闭环完整
- 冲突裁决有记录，不是直接“写平”

Fallback:
- 冲突较大时，交 `Critic` 或人裁决

### Step S7. Quality Gate

Objective:
用固定 rubric 决定是否推进。

Inputs:
- `Unified Draft`
- `Risk Register`
- `Integration Ledger`

Method:
- 严格按 `checklists.md` 的 canonical gate 规则执行
- 记录 gate evidence、blocking/non-blocking 结论和返工步骤
- 若 `Fail`，必须填写稳定的 `Return Step`，其值只能是 `S0` 到 `S7`
- `S8` 是 publish-only 步骤，不能作为返工目标
- 若 `Fail`，必须指定 `Rework Owner`
- 若 `Conditional Pass`，必须指定 `Return Step`、`Rework Owner`、`Re-gate Owner`、`Re-gate Condition`、`Re-gate Evidence` 和 `Due Before`
- 若 `checklists.md` 临时不可读，先从版本库恢复；若必须继续推进，只能使用本节列出的最小 gate 规则做临时判定，并在发布前与 canonical checklist 对齐
- 若 `artifact-registry.md` 临时不可读，先从版本库恢复；未恢复前不得凭记忆重写 `Gate Decision` 字段名；若没有上一份有效 gate artifact 可复用，则不得继续过 gate
- gate 完成后，`Orchestrator` 必须先把 gate outcome 追加到 `Decision Log`，再进入返工或发布

Outputs:
- `Gate Decision`

Gate Result Schema:
- canonical field names live in `artifact-registry.md`

Acceptance:
- 给出 `Pass`, `Conditional Pass`, `Fail`
- 每个失败项都指向具体返工步骤
- 每个 `Conditional Pass` 都有明确 re-gate owner、条件和时点
- blocking gate 失败时不得放行

Fallback:
- 失败时只回到具体步骤，不整链重来
- 没有 `Integration Ledger` 时不得进入 `S7`
- 返工时必须从 `Return Step` 重跑到 `S7`，并刷新该步骤及其后续步骤产出的 artifact

### Step S8. Publish and Learn

Objective:
发布资产并沉淀下一轮改进。

Inputs:
- 已过门的最终稿

Method:
- 冻结版本
- 记录决策
- 总结返工模式
- 抽取通用规则

Outputs:
- `Published Version`
- `Decision Log`
- `Next Iteration Notes`

Decision Log Owner:
- 默认由 `Orchestrator` 产出
- 若存在 `Human Decision Maker`，其最终裁决必须追加到同一份 `Decision Log`

Decision Log Schema:
- `Decision`
- `Decision Owner`
- `Reason`
- `Affected Artifact`
- `Recorded At`
- `Next Step`

Acceptance:
- 可复用
- 可追溯
- 下次可以直接开跑
- 结果验收标准清晰，不依赖逐行人工复核

Fallback:
- 若仍依赖口头解释，回到模板化步骤补齐骨架

## 6. Mechanical Constraints

所有 agent 必须遵守：

- 只回答自己角色的问题
- 所有结论标记为 `Fact`, `Inference`, `Open Question`
- 不允许 silently rewrite 上游前提
- 不允许消费未声明上下文
- 不允许修改共享终稿区，除非被明确授权
- 不允许跳过验收标准直接宣称完成

建议统一输出字段：

```text
Objective
Inputs
Method
Outputs
Acceptance
Risks
Escalation
Dependencies
Fact / Inference / Open Question
```

## 7. Quality Gates

Canonical gate definitions live in `checklists.md`.
This template assumes:
- blocking gates must pass before publish
- `Risk Register` and `Integration Ledger` are required inputs to gate review
- gate decisions must include evidence and explicit return steps
- `Reusability` and `Entropy Control` 默认是 non-blocking，除非任务显式要求它们成为 release-critical

## 8. Observability and Entropy

### Observability

每一步记录：
- 输入版本
- 执行 agent
- 时间戳
- 核心结论
- 失败原因
- 回退去向

建议让 agent 直接可读：
- UI 状态
- DOM 快照
- 屏幕截图
- 日志
- 指标
- trace
- 测试结果
- LSP 诊断结果
- 部署和灰度状态
- 结构化错误码与错误定位

### Entropy Control

- 术语表集中维护
- `AGENTS.md` 保持简短
- 背景知识逐步注入，不整包广播
- 周期性运行重构和清理任务
- 把黄金原则写成规则、lint 或结构测试
- 上下文以追加为主，避免频繁重写稳定前缀
- 长历史定期摘要，避免 ReAct 循环把上下文拖爆
- 当出现 3 个以上未决问题、2 次以上同步骤返工或需要回读 4 份以上上游产物时，强制摘要或拆 subagent

## 9. AI-Friendly Tooling Heuristics

为 agent 设计工具时，优先满足三条：

1. 快
- 反馈越慢，agent 的自回归等待成本越高

2. 结构化
- 返回明确字段、状态和位置，而不是模糊叙述

3. 错误清晰
- 好的报错往往比“成功信息”更有价值
- 错误必须帮助 agent 快速定位、反思和修正

适合模板化为工具接口的能力：
- 代码诊断
- 测试执行
- 页面交互与截图
- 部署状态读取
- 日志和 trace 查询
- 验收检查

## 10. Minimal Example

场景：
阅读一篇工程文章，产出一套可复用的多 agent workflow 模板。

最小运行方式：

1. `S0` `Orchestrator` 写 `Task Brief` 并打开 `Decision Log`
2. `S1` `Orchestrator` 产出 `Execution Environment Spec` 和 `Role Owner Table`
3. `S2` `Orchestrator` 产出 `Context Pack`
4. `S2` `Source Analyst` 抽取文章 claims 和 evidence
5. `S2` `Principle Mapper` 压缩成工程原则
6. `S3` `Workflow Designer` 生成步骤化模板
7. `S4` `Implementer` 执行并产出 `Execution Output Record`
8. `S5` `Critic` 产出 `Risk Register`
9. `S6` `Orchestrator` 产出 `Integration Ledger` 并更新 `Decision Log`
10. `S7` `Quality Gate` 判定是否过门
11. `S7` `Orchestrator` 追加 gate outcome 到 `Decision Log`
12. `S8` `Template Editor` 编排为最终模板
13. `S8` 人类只裁决争议和版本冻结，并追加 `Decision Log`

## 11. Anti-Patterns

- 一个巨大的 `AGENTS.md`
- 把知识留在聊天软件里
- 用“多给点提示”代替系统建设
- 多个 agent 同时修改同一终稿
- 没有质量门就直接合并
- 只做 happy path，不做异常路径
- 手工清理 AI 残渣但不把规则系统化
- 每轮都重写 system prompt 或稳定前缀
- 把验证、测试、部署和排障继续留给人工兜底
- 没有结构化错误反馈，导致 agent 无法快速纠偏
- 明明上下文已溢出，仍坚持单 agent 硬扛
- 人类仍逐行 review，而不是转向结果验收

## 12. Starter Checklist

- [ ] 目标、非目标、成功标准已定义
- [ ] `AGENTS.md` 仅作入口，不作百科
- [ ] 关键知识已进入 repo
- [ ] 角色边界明确
- [ ] 输出契约明确
- [ ] 验收标准明确
- [ ] 回退路径明确
- [ ] 观测信号可供 agent 直接读取
- [ ] 存在持续熵治理机制
- [ ] 人类只保留关键裁决职责
- [ ] 高频工具满足快、结构化、错误清晰三条
- [ ] 核心前缀稳定，上下文以追加为主
- [ ] 单 agent 超载时已预设 subagent 分治策略
- [ ] 人类验收关注结果与指标，而非逐行复核

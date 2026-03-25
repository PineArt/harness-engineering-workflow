# Workflow Template Lite

这是可直接填写的 run sheet。
`Lite` 用于中等复杂度任务：一个主工作流、有限并行、固定 gate。
完整原则、扩展角色和背景说明见 [workflow-template.md](workflow-template.md)。
角色 prompt 见 [agent-prompts.md](agent-prompts.md)。
canonical gate 以 [checklists.md](checklists.md) 为准。
artifact 最小 schema 以 [artifact-registry.md](artifact-registry.md) 为准。

首次执行默认顺序：
- 先只填写本文件
- 到 `Step S7` 时再打开 [checklists.md](checklists.md) 和 [artifact-registry.md](artifact-registry.md)
- 只有需要发给具体角色 prompt 时才打开 [agent-prompts.md](agent-prompts.md)

## Step S0. Task Brief

```text
Goal:

Non-goals:

Constraints:

Success Criteria:

Human Decision Points:
```

## Step S1. Role Set And Owners

`Lite` 默认至少指定这 4 个职责：

- `Orchestrator`
- `Implementer`
- `Critic`
- `Quality Gate`

按任务需要追加：
- `Source Analyst`
- `Workflow Designer`
- `Human Decision Maker`
- `Principle Mapper`
- `Template Editor`

角色表必须显式写 owner：

```text
Role | Owner | Notes
Orchestrator |  |
Implementer |  |
Critic |  |
Quality Gate |  |
```

说明：
- 同一个人或同一个 agent 可以承担多个职责
- `Critic` 和 `Quality Gate` 不能在本轮中被省略
- 若需要 5 个以上独立 owner，直接升级到 `Full`

## Step S2. Context Pack

```text
Core Context:

Optional Context:

Forbidden Scope:

Stable Prefix:

Required Tools:
```

## Step S3. Task Graph

```text
Task:
Owner:
Depends On:
Outputs:
Writable Area:
Fallback:
```

至少写清：
- 并行块
- 串行块
- 唯一 owner
- 命名后的 `Outputs` 和唯一 `Writable Area`
- 人工裁决点

## Step S4. Execute

每个执行角色必须产出：

```text
Objective
Inputs
Method
Outputs
Acceptance
Risks
Escalation
Fact / Inference / Open Question
```

执行要求：
- 优先通过测试、LSP、日志、浏览器、部署状态等外部反馈取事实
- 中间结果只写入各自区域
- `Outputs` 必须对应 `Task Graph` 中命名的 artifact，且只写到该任务的 `Writable Area`
- 失败只回退到责任步骤

## Step S5. Risk Scan

在过门前，`Critic` 必须产出：

```text
Risk Register:
- Risk:
  Severity:
  Evidence:
  Owner:
  Required Action:
  Status:
```

`Status` 只允许：
- `Open`
- `Mitigating`
- `Closed`

完整字段定义见 [artifact-registry.md](artifact-registry.md)。

## Step S6. Integration Ledger And Decision Log

`Orchestrator` 在整合时必须同时维护 `Integration Ledger` 和 `Decision Log`。
不要只输出一份“写平了的”统一草案。
`S7` 结束后，`Orchestrator` 也必须把 gate outcome 追加进同一份 `Decision Log`，再进入返工或发布。

`Integration Ledger`：

```text
Agent:
Claim:
Artifact Name:
Owner:
Evidence Source:
Decision:
Next Step Or Fallback:
```

`Decision Log`：

```text
Decision:
Decision Owner:
Reason:
Affected Artifact:
Recorded At:
Next Step:
```

最少要记录：
- 人工裁决
- 冲突消解
- gate 要求的返工或条件放行

完整字段定义见 [artifact-registry.md](artifact-registry.md)。

## Step S7. Gate

`Quality Gate` 优先按 [checklists.md](checklists.md) 判定：
- `Pass`
- `Conditional Pass`
- `Fail`

阻断项：
- `Source Fidelity`
- `Boundary Integrity`
- `Execution Completeness`
- `External Feedback`

Gate 输出必须使用 [artifact-registry.md](artifact-registry.md) 里的 `Gate Decision` schema。

规则：
- `Return Step` 只能填 `S0` 到 `S7`
- `S8` 是发布步骤，不能作为返工目标
- `Fail` 必须填写 `Return Step` 和 `Rework Owner`
- `Conditional Pass` 必须填写 `Return Step`、`Rework Owner`、`Re-gate Owner`、`Re-gate Condition`、`Re-gate Evidence` 和 `Due Before`
- `Pass` 应将 `Return Step`、`Rework Owner` 和全部 re-gate 字段填写为 `N/A`
- 返工时必须从 `Return Step` 重跑到 `S7`，并刷新该步骤及其后续步骤产出的 artifact

若 `checklists.md` 临时不可读：
- 先从版本库恢复该文件
- 未恢复前不得凭记忆自创 gate 结论
- 只有在必须继续推进时，才可按本节列出的最小规则做临时判定，并在发布前与 canonical checklist 对齐

若 [artifact-registry.md](artifact-registry.md) 临时不可读：
- 先从版本库恢复该文件
- 未恢复前不得凭记忆重写 `Gate Decision` 字段名
- 未恢复且没有上一份有效 `Gate Decision` 可复用时，不得继续过 gate

## Step S8. Publish

发布前至少具备：

- [ ] `Task Brief`
- [ ] 角色 owner 表
- [ ] `Context Pack`
- [ ] `Task Graph`
- [ ] `Risk Register`
- [ ] `Integration Ledger`
- [ ] `Gate Decision`
- [ ] `Decision Log`

`Decision Log` 默认由 `Orchestrator` 维护。
如果存在 `Human Decision Maker`，其最终裁决必须追加到同一份 `Decision Log`。
`Quality Gate` 不直接拥有 `Decision Log`，但其 `Gate Decision` 必须在 `S7` 结束后由 `Orchestrator` 追加到同一份日志。

## Context Control Rules

出现任一情况就必须摘要或拆 subagent：
- 超过 3 个未决问题
- 同一步骤失败超过 2 次
- 继续执行需要回读超过 4 份上游产物
- 当前 agent 已开始靠长历史回忆，而不是稳定摘要

## Escalate To Full If

出现任一情况就升级到 [workflow-template.md](workflow-template.md)：
- 需要 5 个以上独立职责
- 需要 2 个以上并行工作流同时收敛
- 需要 `Template Editor` 或 `Principle Mapper` 参与最终交付
- 需要正式的环境设计或 repo 结构调整
- 风险项持续跨越 2 轮以上仍未关闭
- gate 输出开始依赖大量人工解释而不是固定 schema

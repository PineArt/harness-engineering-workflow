# Feature Template Ultra Lite

适用场景：
- 单个小 feature
- 单个 bugfix
- 小范围文档或配置修改
- 不需要多 agent 并行
- 不需要完整风险扫描和整合账本

不要用于：
- 跨模块重构
- 需要多个角色并行
- 验证链路复杂
- 需求边界不清
- 预计会有多轮返工

## 1. Fill This In

```text
Goal:

Scope:

Constraints:

Owner:

Validation:

Done When:
```

## 2. Minimal Flow

1. 写清 `Goal` 和 `Done When`
2. 指定唯一 `Owner`
3. 执行修改
4. 用一个最直接的外部反馈完成验证
5. 满足 `Done When` 就结束

## 3. Default Rules

- 不默认拆多 agent
- 不默认写 `Risk Register`
- 不默认写 `Integration Ledger`
- 不默认开完整质量门
- 优先用最短验证链路闭环
- 人类只看结果，不逐行兜底
- 默认 `Owner` 对应 `Implementer`
- 只有当目标、范围或验收标准说不清时，才额外加 `Orchestrator`
- 如果你需要 role prompt，先使用 `Implementer`；只有边界不清时再补 `Orchestrator`

## 4. Validation Options

优先选一个最便宜、最直接的：
- 单元测试
- 页面手动/自动验证
- LSP / lint / typecheck
- 日志或接口返回检查
- 构建成功

## 5. If Validation Fails

按下面顺序处理：

1. 若范围不变、owner 不变、且仍可用同一条验证链路闭环，继续由当前 `Owner` 修正并重试一次。
2. 若第二次仍失败，或开始需要第二个 owner、第二种验证来源、或更明确的风险记录，立即升级到 `workflow-template-lite.md`。
3. 升级到 `Lite` 时，至少把以下字段原样带过去，作为 `Task Brief` 和 `Context Pack` 的种子：

```text
Goal:
Scope:
Constraints:
Owner:
Validation:
Done When:
Failure Learned:
```

## 6. Escalate To Lite If

出现任一情况就升级到 `workflow-template-lite.md`：
- 需要第二个 owner
- 需要多个验证来源
- 出现两次以上返工
- 范围开始扩张
- 需要人工裁决需求边界
- 需要保留明确风险记录
- 只能依赖弱验证，例如仅 build 成功或非常粗的人工目测

## 7. Example

```text
Goal:
修复 gallery 页面日期筛选默认值错误

Scope:
只改前端筛选初始化逻辑，不改后端 API

Constraints:
不改现有接口契约；不影响其他筛选项

Owner:
Implementer

Validation:
本地打开页面，确认默认日期正确；运行相关前端测试

Done When:
页面默认日期正确，测试通过，无控制台报错
```

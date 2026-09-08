# wallet-cli proposal approve

批准提案，或取消你的批准。

## 用法

```
wallet-cli proposal approve <id> [--cancel]
                            [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                            [--permission-id <n>] [options]
```

## 说明

为提案投出你的批准；`--cancel` 则撤回你已经投出的批准。TRON 治理只有这两种状态——没有"反对"票，弃权就是什么都不做。

只有已注册的见证人才能批准；其他账户会以 `not_a_witness` 失败。链上除此之外不做任何检查，所以未当选候选人的批准同样会被接受并上链——但统计时只有**前 27 名活跃超级代表**的批准才计入阈值，因此这样的批准并不会让提案离通过更近一步。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `<id>` | **必填。** 提案 id |
| `--cancel` | 撤回你此前投出的批准，而不是新增一个 |
| `--dry-run` | 只构建和估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥；配合 `--expiration` 使用 |
| `--build-only` | 构建并估算，输出**未签名**的 hex；与 `--dry-run` / `--sign-only` 互斥；配合 `--expiration` 使用 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin（fd 0）读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

```bash
echo "$PW" | wallet-cli proposal approve 47 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Proposal approved
  Proposal   #47
  Voter      TSRmq8kP...9dEf (main)
  Approvals  13 / 18
  TxID       b1e...
  Block      57,880,240
  Fee        0 TRX  (267 bandwidth)
  Status     success
```

`--cancel` 会把你自己的批准从提案上撤下来：

```bash
echo "$PW" | wallet-cli proposal approve 47 --cancel --network tron:3448148188 --wait --password-stdin
```

```console
✅ Approval canceled
  Proposal   #47
  Voter      TSRmq8kP...9dEf (main)
  Approvals  12 / 18
  TxID       b2f...
  Block      57,880,255
  Fee        0 TRX  (267 bandwidth)
  Status     success
```

```bash
echo "$PW" | wallet-cli proposal approve 47 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"proposal.approve","data":{"kind":"proposal-approve","stage":"confirmed","txId":"b1e...","confirmed":true,"blockNumber":57880240,"failed":false,"proposalId":47,"voterAddress":"TSRmq8kP...","addApproval":true,"approvals":13,"approvalThreshold":18,"feeSun":0,"energyUsed":0,"netUsed":267,"energyFeeSun":0,"netFeeSun":0,"resource":{"netUsage":267,"netFeeSun":0,"energyUsage":0,"energyFeeSun":0}},"meta":{"durationMs":6410,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "proposal-approve"`、`stage: "submitted"`、`txId`、`proposalId`、`voterAddress`、`addApproval`（加 `--cancel` 时为 `false`）、`approvals`，以及 `approvalThreshold` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、它们面向治理命令的兼容视图 `resource`（`netUsage`、`netFeeSun`、`energyUsage`、`energyFeeSun`）、`failed` |

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`not_a_witness`、`proposal_not_found`——没有该提案、`already_approved`——你已经批准过了、`not_approved`——用了 `--cancel` 但没有可撤回的批准、`proposal_expired`、`watch_only_no_signer`、`auth_failed`） · `2` 用法错误（`invalid_value`——id 不是数字）。

## 另请参见

[`proposal show`](show.md) · [`proposal list`](list.md) · [`proposal delete`](delete.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)

# wallet-cli proposal delete

删除你创建的提案。

## 用法

```
wallet-cli proposal delete <id>
                           [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                           [--permission-id <n>] [options]
```

## 说明

撤回提案本身。只有创建者能这么做，而且只能在提案仍处于投票窗口内时进行；此后提案已完成统计，成为终态。

该操作不同于 [`proposal approve --cancel`](approve.md)：前者删除提案，后者只撤销一项批准。两者的回执分别显示 `Proposal deleted` 和 `Approval canceled`。

链上将删除后的状态记为 `canceled`；操作成功后，[`proposal show`](show.md) 会显示 `State canceled`。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `<id>` | **必填。** 提案 id |
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
echo "$PW" | wallet-cli proposal delete 48 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Proposal deleted
  Proposal  #48
  Proposer  TSRmq8kP...9dEf (main)
  TxID      c7d...
  Block     57,880,355
  Fee       0 TRX  (265 bandwidth)
  Status    success
```

```bash
echo "$PW" | wallet-cli proposal delete 48 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"proposal.delete","data":{"kind":"proposal-delete","stage":"confirmed","txId":"c7d...","confirmed":true,"blockNumber":57880355,"failed":false,"proposalId":48,"proposerAddress":"TSRmq8kP...","feeSun":0,"energyUsed":0,"netUsed":265,"energyFeeSun":0,"netFeeSun":0,"resource":{"netUsage":265,"netFeeSun":0,"energyUsage":0,"energyFeeSun":0}},"meta":{"durationMs":6390,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "proposal-delete"`、`stage: "submitted"`、`txId`、`proposalId`、`proposerAddress` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、它们面向治理命令的兼容视图 `resource`（`netUsage`、`netFeeSun`、`energyUsage`、`energyFeeSun`）、`failed` |

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`proposal_not_found`——没有该提案、`not_proposal_owner`——你不是它的创建者、`proposal_expired`、`already_canceled`、`watch_only_no_signer`、`auth_failed`） · `2` 用法错误（`invalid_value`——id 不是数字）。

## 另请参见

[`proposal create`](create.md) · [`proposal approve`](approve.md) · [`proposal show`](show.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)

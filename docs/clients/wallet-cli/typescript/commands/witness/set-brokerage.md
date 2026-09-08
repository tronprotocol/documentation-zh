# wallet-cli witness set-brokerage

设置 SR 保留的出块奖励份额。

## 用法

```
wallet-cli witness set-brokerage <percent>
                                 [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                                 [--permission-id <n>] [options]
```

## 说明

`<percent>` 表示**佣金比例**（brokerage），即 SR 为自己保留的出块奖励百分比；剩余的 `100 − percent` 按票数比例分配给投票者。默认值为 20，广播前会在本地校验该值是否为 0–100 之间的整数。

该值对应 [`vote list`](../vote/list.md) 中的 `brokeragePct`；该页面的 `Reward ratio` 列显示其补数，即投票者获得的份额。设为 `100` 时，投票者不会从该 SR 的出块奖励中获得分配。

任何已注册的见证人都可以设置它，无论是否当选。执行操作的账户必须是候选人，否则命令会以 `not_a_witness` 失败。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

Ledger 的 TRON 应用无法对见证人类合约签名。Ledger 账户可以做试运行或构建，但签名模式会在与设备交互之前就以 `ledger_unsupported` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `<percent>` | **必填。** SR 保留的份额，0–100 的整数 |
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

自己保留 20 %，把 80 % 分给投票人：

```bash
echo "$PW" | wallet-cli witness set-brokerage 20 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Brokerage set
  Witness    TSRmq8kP...9dEf (main)
  Brokerage  20%
  TxID       f8c...
  Block      57,881,402
  Fee        0 TRX  (269 bandwidth)
  Status     success
```

```bash
echo "$PW" | wallet-cli witness set-brokerage 20 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"witness.set-brokerage","data":{"kind":"witness-set-brokerage","stage":"confirmed","txId":"f8c...","confirmed":true,"blockNumber":57881402,"failed":false,"witnessAddress":"TSRmq8kP...","brokerage":20,"feeSun":0,"energyUsed":0,"netUsed":269,"energyFeeSun":0,"netFeeSun":0,"resource":{"netUsage":269,"netFeeSun":0,"energyUsage":0,"energyFeeSun":0}},"meta":{"durationMs":6470,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "witness-set-brokerage"`、`stage: "submitted"`、`txId`、`witnessAddress`、`brokerage` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、它们面向治理命令的兼容视图 `resource`（`netUsage`、`netFeeSun`、`energyUsage`、`energyFeeSun`）、`failed` |

`brokerage` 是当前生效的值，类型为 number。

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`not_a_witness`、`watch_only_no_signer`、`ledger_unsupported`、`auth_failed`） · `2` 用法错误（`missing_option`——未给出 percent；`invalid_value`——percent 不是整数，或超出 0–100 范围）。

## 另请参见

[`witness create`](create.md) · [`vote list`](../vote/list.md) · [`reward balance`](../reward/balance.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)

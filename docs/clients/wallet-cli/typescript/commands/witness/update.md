# wallet-cli witness update

修改候选人信息页 URL。

## 用法

```
wallet-cli witness update --url <url>
                          [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                          [--permission-id <n>] [options]
```

## 说明

替换现有 SR 候选人的信息页 URL。URL 是链上为候选人保存的唯一可编辑字段，可以根据需要多次修改，每次操作只消耗带宽。

执行操作的账户必须已经是候选人，否则命令会以 `not_a_witness` 失败。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

Ledger 的 TRON 应用无法对见证人类合约签名。Ledger 账户可以做试运行或构建，但签名模式会在与设备交互之前就以 `ledger_unsupported` 失败。

## 选项

| 选项 | 说明 |
|---|---|
| `--url <url>` | **必填。** 新的候选人信息页 |
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
echo "$PW" | wallet-cli witness update --url https://sr.acme.io/v2 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Witness updated
  Witness  TSRmq8kP...9dEf (main)
  Url      https://sr.acme.io/v2
  TxID     e5b...
  Block    57,881,190
  Fee      0 TRX  (270 bandwidth)
  Status   success
```

```bash
echo "$PW" | wallet-cli witness update --url https://sr.acme.io/v2 --network tron:3448148188 --wait --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"witness.update","data":{"kind":"witness-update","stage":"confirmed","txId":"e5b...","confirmed":true,"blockNumber":57881190,"failed":false,"witnessAddress":"TSRmq8kP...","url":"https://sr.acme.io/v2","feeSun":0,"energyUsed":0,"netUsed":270,"energyFeeSun":0,"netFeeSun":0,"resource":{"netUsage":270,"netFeeSun":0,"energyUsage":0,"energyFeeSun":0}},"meta":{"durationMs":6440,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "witness-update"`、`stage: "submitted"`、`txId`、`witnessAddress`、`url` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、返回时的扁平结算字段（`feeSun`、`energyUsed`、`netUsed`、`energyFeeSun`、`netFeeSun`）、它们面向治理命令的兼容视图 `resource`（`netUsage`、`netFeeSun`、`energyUsage`、`energyFeeSun`）、`failed` |

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`not_a_witness`、`watch_only_no_signer`、`ledger_unsupported`、`auth_failed`） · `2` 用法错误（`missing_option`——未提供 `--url`）。

## 另请参见

[`witness create`](create.md) · [`witness set-brokerage`](set-brokerage.md) · [`vote list`](../vote/list.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)

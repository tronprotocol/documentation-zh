# wallet-cli stake freeze

质押 TRX 换取能量/带宽。

## 用法

```
wallet-cli stake freeze --amount-sun <n> [--resource energy|bandwidth]
                        [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]] [--permission-id <n>] [options]
```

## 说明

从当前账户的余额中质押 TRX（Stake 2.0），换取所选资源的持续额度——`energy`（智能合约执行）或 `bandwidth`（交易字节数，默认值）。质押同时会带来投票权：1 TRX 质押 = 1 TP，可通过 [`vote cast`](../vote/cast.md) 使用。

金额单位为 SUN（1 TRX = 1,000,000 SUN）。质押的 TRX 仍然属于你；要拿回来，先执行 [`stake unfreeze`](unfreeze.md)，等待期结束后再执行 [`stake withdraw`](withdraw.md)。

**该命令默认在交易提交后返回**；使用 `--wait` 可阻塞至交易确认。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `--amount-sun <string>` | **必填。** 质押金额，单位 SUN |
| `--resource <energy\|bandwidth>` | 要换取的资源类型（默认 `bandwidth`） |
| `--dry-run` | 只估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥；配合 `--expiration` 使用 |
| `--build-only` | 构建并估算，输出**未签名**的 hex；与 `--dry-run` / `--sign-only` 互斥；配合 `--expiration` 使用 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin 读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

默认——质押 1,000 TRX 换取能量，返回**已提交**的回执：

```bash
echo "$PW" | wallet-cli stake freeze --amount-sun 1000000000 --resource energy --network tron:3448148188 --password-stdin
```

```console
⏳ Staked 1,000 TRX for energy
  TxID    c3d...
  Status  pending — not yet on-chain
! Track it: wallet-cli tx info --network tron:3448148188 --txid c3d...
```

```bash
echo "$PW" | wallet-cli stake freeze --amount-sun 1000000000 --resource energy --network tron:3448148188 --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"stake.freeze","data":{"kind":"stake-freeze","stage":"submitted","txId":"c3d...","amountSun":"1000000000","resource":"energy"},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

加 `--wait` 可阻塞直到已确认：

```bash
echo "$PW" | wallet-cli stake freeze --amount-sun 1000000000 --resource energy --network tron:3448148188 --wait --password-stdin
```

```console
✅ Staked 1,000 TRX for energy
  TxID    c3d...
  Block   #68,762,990
  Status  success
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "stake-freeze"`, `stage: "submitted"`, `txId`, `amountSun`（string）, `resource` |
| `--wait`（已确认） | 同上，另加 `confirmed`、`blockNumber`、`feeSun`、`failed` |

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`） · `2` 用法错误。

## 另请参见

[`stake info`](info.md) · [`stake unfreeze`](unfreeze.md) · [`stake delegate`](delegate.md) · [质押指南](../../guide/stake-and-resources.md)

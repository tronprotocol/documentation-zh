# wallet-cli stake unfreeze

解质押 TRX。

## 用法

```
wallet-cli stake unfreeze --amount-sun <n> [--resource energy|bandwidth]
                          [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]] [--permission-id <n>] [options]
```

## 说明

开始解质押：该金额离开质押池，进入**赎回等待期**，等待期结束后才能用 [`stake withdraw`](withdraw.md) 提取。对应的资源额度和投票权（TP）会立即下降——由这部分 TRX 支撑的投票随之失效。

Stake 2.0 规定每个账户同一时间最多有 **32 笔待解锁的解质押**；用 [`stake info`](info.md) 查看剩余名额。待解锁的解质押可以用 [`stake cancel-unfreeze`](cancel-unfreeze.md) 回滚。

**该命令默认在交易提交后返回**；使用 `--wait` 可阻塞至交易确认。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `--amount-sun <string>` | **必填。** 解质押金额，单位 SUN |
| `--resource <energy\|bandwidth>` | 要释放的资源类型（默认 `bandwidth`） |
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

默认——返回**已提交**的回执：

```bash
echo "$PW" | wallet-cli stake unfreeze --amount-sun 1000000000 --resource energy --network tron:3448148188 --password-stdin
```

```console
⏳ Unstaked 1,000 TRX
  TxID    d4e...
  Status  pending — not yet on-chain
! Track it: wallet-cli tx info --network tron:3448148188 --txid d4e...
```

```bash
echo "$PW" | wallet-cli stake unfreeze --amount-sun 1000000000 --resource energy --network tron:3448148188 --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"stake.unfreeze","data":{"kind":"stake-unfreeze","stage":"submitted","txId":"d4e...","amountSun":"1000000000","resource":"energy"},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

加 `--wait` 可阻塞直到已确认：

```bash
echo "$PW" | wallet-cli stake unfreeze --amount-sun 1000000000 --resource energy --network tron:3448148188 --wait --password-stdin
```

```console
✅ Unstaked 1,000 TRX
  TxID          d4e...
  Block         #68,763,004
  Withdrawable  after the unlock period — then run `stake withdraw`
  Status        success
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "stake-unfreeze"`, `stage: "submitted"`, `txId`, `amountSun`（string）, `resource` |
| `--wait`（已确认） | 同上，另加 `confirmed`、`blockNumber`、`feeSun`、`failed` |

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`） · `2` 用法错误。

## 另请参见

[`stake withdraw`](withdraw.md) · [`stake cancel-unfreeze`](cancel-unfreeze.md) · [`stake info`](info.md)

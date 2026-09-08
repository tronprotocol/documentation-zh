# wallet-cli stake delegate

将资源代理给其他地址。

## 用法

```
wallet-cli stake delegate --receiver <address> --amount-sun <n>
                          [--resource energy|bandwidth] [--lock [--lock-period <blocks>]]
                          [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]] [--permission-id <n>] [options]
```

## 说明

把你质押的 TRX 所支撑的资源出借给另一个地址——接收方拿到能量/带宽，而 TRX 本身始终留在你的质押里。金额以支撑该资源的质押 TRX 表示，单位 SUN。接收方必须是与所有者不同的地址。

`--lock` 让这笔代理在一段时间内不可收回（`--lock-period` 以区块数计，每区块约 3 秒）——相当于给接收方的一份保证。不加该选项时，你可以随时执行 [`stake undelegate`](undelegate.md)。

用 [`stake delegated`](delegated.md)（`Max delegatable` 一栏）查看你还能代理多少。

**该命令默认在交易提交后返回**；使用 `--wait` 可阻塞至交易确认。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `--amount-sun <string>` | **必填。** 支撑所代理资源的质押 TRX 金额，单位 SUN |
| `--receiver <string>` | **必填。** 接收资源的地址（必须与所有者不同） |
| `--resource <energy\|bandwidth>` | 要代理的资源类型（默认 `bandwidth`） |
| `--lock` | 锁定这笔代理，禁止提前取消代理 |
| `--lock-period <number>` | 锁定时长，以区块数计（每区块约 3 秒）；需要配合 `--lock` |
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
echo "$PW" | wallet-cli stake delegate --receiver TYzp9RbQmtAjCtyGeHb9W7GRwjDKtjUvvx --amount-sun 1000000000 --resource energy --network tron:3448148188 --password-stdin
```

```console
⏳ Delegated 1,000 TRX of energy
  To      TYzp9RbQmtAjCtyGeHb9W7GRwjDKtjUvvx
  TxID    b7c...
  Status  pending — not yet on-chain
! Track it: wallet-cli tx info --network tron:3448148188 --txid b7c...
```

```bash
echo "$PW" | wallet-cli stake delegate --receiver TYzp9RbQmtAjCtyGeHb9W7GRwjDKtjUvvx --amount-sun 1000000000 --resource energy --network tron:3448148188 --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"stake.delegate","data":{"kind":"stake-delegate","stage":"submitted","txId":"b7c...","amountSun":"1000000000","resource":"energy","receiver":"TYzp9RbQmtAjCtyGeHb9W7GRwjDKtjUvvx"},"meta":{"durationMs":15,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "stake-delegate"`, `stage: "submitted"`, `txId`, `amountSun`（string）, `resource`, `receiver` |
| `--wait`（已确认） | 同上，另加 `confirmed`、`blockNumber`、`feeSun`、`failed` |

## 退出码

`0` 已提交（早退模式下为已构建/已签名） · `1` 执行失败（`watch_only_no_signer`、`auth_failed`、`rpc_error`、`timeout`） · `2` 用法错误（`invalid_value`——接收方与所有者相同，或未加 `--lock` 就用了 `--lock-period`）。

## 另请参见

[`stake undelegate`](undelegate.md) · [`stake delegated`](delegated.md) · [能量与带宽](../../concepts/energy-bandwidth.md)

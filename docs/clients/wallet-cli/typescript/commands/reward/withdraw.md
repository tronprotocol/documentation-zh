# wallet-cli reward withdraw

把累积的奖励提取到余额。

## 用法

```
wallet-cli reward withdraw [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                           [--permission-id <n>] [options]
```

## 说明

把你累积的投票奖励（如果你是 SR，还包括出块奖励）转入账户的可用余额。链上规定**每 24 小时最多只能提取一次**——请先用 [`reward balance`](balance.md) 查看；提前尝试会以 `withdraw_too_frequent` 失败，没有奖励可领时则为 `no_reward`。

回执中的 `Amount`：在 `submitted` 阶段，它是广播时读取到的可领取金额；`--wait` 得到的已确认回执显示的则是链上的实际金额（两者只差几秒钟的累积量——可以忽略）。

**该命令默认在交易提交后返回**；使用 `--wait` 可阻塞至交易确认。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `--dry-run` | 只构建和估算，不签名/不广播；与 `--sign-only` / `--build-only` 互斥 |
| `--sign-only` | 只签名不广播，输出已签名的 hex；与 `--dry-run` / `--build-only` 互斥；配合 `--expiration` 使用 |
| `--build-only` | 构建并估算，输出**未签名**的 hex；与 `--dry-run` / `--sign-only` 互斥；配合 `--expiration` 使用 |
| `--expiration <ms>` | 交易过期时间（毫秒），最大 `86400000`（24 小时）；仅可与 `--sign-only` 或 `--build-only` 同用；省略时使用节点默认值（约 60 秒） |
| `--permission-id <n>` | 用于签名的权限组（0=owner，1=witness，2-9=active）；默认 `0` |
| `--wait` / `--wait-timeout <ms>` | 广播后轮询直到已确认/失败（上限默认取配置 `waitTimeoutMs`，内置 60000） |
| `--password-stdin` | 从 stdin 读取 master password |

此外还有[全局选项](../index.md#global-options-every-command)。

## 示例

示例中的 `$PW` 是你的 master password（来自环境变量、密码管理器等），通过 `--password-stdin` 从 stdin 传入。

默认——广播并返回**已提交**的回执：

```bash
echo "$PW" | wallet-cli reward withdraw --network tron:3448148188 --password-stdin
```

```console
⏳ Withdrew voting/block rewards
  Amount  123.456789 TRX
  TxID    a1b...
  Status  pending — next withdrawal available in ~24h
! Track it: wallet-cli tx info --network tron:3448148188 --txid a1b...
```

```bash
echo "$PW" | wallet-cli reward withdraw --network tron:3448148188 --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"reward.withdraw","data":{"kind":"reward-withdraw","stage":"submitted","txId":"a1b...","rewardSun":"123456789"},"meta":{"durationMs":17,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

加上 `--wait` 可阻塞直到已确认（回执中会带上真实的区块号 / 手续费）：

```bash
echo "$PW" | wallet-cli reward withdraw --network tron:3448148188 --wait --password-stdin
```

```console
✅ Withdrew voting/block rewards
  Amount  123.456789 TRX
  TxID    c7d...
  Block   #84,121,010
  Fee     0.268 TRX
  Status  success — next withdrawal available in ~24h
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "reward-withdraw"`、`stage: "submitted"`、`txId`、`rewardSun`（string） |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`、`blockNumber`、`feeSun`、`failed` |

## 退出码

`0` 已提交 · `1` 执行失败（`watch_only_no_signer`、`auth_failed`、`withdraw_too_frequent`——距上次提取不足 24 小时、`no_reward`——没有可领取的奖励） · `2` 用法错误。

## 另请参见

[`reward balance`](balance.md) · [`vote cast`](../vote/cast.md) · [`stake withdraw`](../stake/withdraw.md)（提取已解质押的 TRX 是另一条命令）

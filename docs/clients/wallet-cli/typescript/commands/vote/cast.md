# wallet-cli vote cast

投出或替换你的完整票数分配。

## 用法

```
wallet-cli vote cast --for <SR=votes> ... [--dry-run | (--sign-only | --build-only) [--expiration <ms>] | --wait [--wait-timeout <ms>]]
                     [--permission-id <n>] [options]
```

## 说明

命令提交的是**完整**票数分配，这是 TRON 的链上规则，而非 CLI 自行设计的行为。提供的全部 `--for` 条目会替换此前的投票分配，未列出的 SR 票数将归零。要修改投票，只需再次执行 `vote cast`；没有单独的撤票命令。

链上有两项强制规则：

- **总票数 ≥ 1**——不能提交总票数为零的分配。要彻底停止投票，请解除用于产生投票权的 TRX 质押（[`stake unfreeze`](../stake/unfreeze.md)）；TP 减少后，相关投票会失效。
- **每笔交易最多 30 个条目**（java-tron 的 `MAX_VOTE_NUMBER`）。由于一次投票即是完整分配，一个账户最多同时给 30 个 SR 投票——而当选的始终只有 27 个，所以正常投票不会触及这个上限。

投票在下一个维护周期（约 6 小时）才生效。每一票占用 1 TP（是占用而非消耗——重新投票或解除质押都会把它释放出来）；可用 TP = 已质押的 TRX 减去已投出的票数（见 [`vote status`](status.md)）。

**该命令默认在交易提交后返回**（`stage: "submitted"`），不会等待确认。使用 `--wait` 可阻塞至交易确认或失败。命令需要一个账户；仅在需要签名的模式下，才必须通过 `--password-stdin` 提供 master password。`--dry-run` 和 `--build-only` 不会解锁钱包，因此无需密码。仅观察账户无法签名，会返回 `watch_only_no_signer`。

## 选项

| 选项 | 说明 |
|---|---|
| `--for <SR=votes>` | **必填，可重复。** SR 地址 = 票数（正整数）；这一整组条目就是你的完整分配（1–30 个条目） |
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

默认——广播并返回**已提交**的回执，不等待：

```bash
echo "$PW" | wallet-cli vote cast --for TZ4...=600 --for TT5...=400 --network tron:3448148188 --password-stdin
```

```console
⏳ Voted 1,000 TP across 2 witnesses
  Votes   TZ4...=600, TT5...=400
  TxID    e5f...
  Status  pending — tallied at next maintenance cycle (~6h)
! Track it: wallet-cli tx info --network tron:3448148188 --txid e5f...
```

```bash
echo "$PW" | wallet-cli vote cast --for TZ4...=600 --for TT5...=400 --network tron:3448148188 --password-stdin -o json
```

```json
{"schema":"wallet-cli.result.v1","success":true,"command":"vote.cast","data":{"kind":"vote-cast","stage":"submitted","txId":"e5f...","votes":[{"witness":"TZ4...","count":600},{"witness":"TT5...","count":400}],"totalVotes":1000},"meta":{"durationMs":18,"warnings":[]},"chain":{"family":"tron","network":"tron:3448148188","chainId":"3448148188"}}
```

加 `--wait` 可阻塞直到投票在链上被确认（会补上真实的区块号 / 手续费）：

```bash
echo "$PW" | wallet-cli vote cast --for TZ4...=600 --for TT5...=400 --network tron:3448148188 --wait --password-stdin
```

```console
✅ Voted 1,000 TP across 2 witnesses
  Votes   TZ4...=600, TT5...=400
  TxID    f8a...
  Block   #84,121,055
  Fee     0 TRX
  Status  success — tallied at next maintenance cycle (~6h)
```

## 输出

`data` 随阶段而变：

| 阶段 | 字段 |
|---|---|
| 默认（提交） | `kind: "vote-cast"`、`stage: "submitted"`、`txId`、`votes[]`（`witness`、`count`）、`totalVotes` |
| `--wait`（已确认） | 同上，另加 `stage: "confirmed"`、`confirmed`（boolean）、`blockNumber`、`feeSun`、`failed` |

## 退出码

`0` 已提交（提前退出的模式下则是已构建/已签名） · `1` 执行失败（`watch_only_no_signer`、`auth_failed`） · `2` 用法错误（`insufficient_voting_power`——总票数超出该账户的**总** TP（已投出的票是被重新分配，而不是叠加，因此这里比对的是总量，而不是剩余可用量）；`invalid_value`——SR 地址不合法、票数非正整数，或条目超过 30 个）。

## 另请参见

[`vote status`](status.md) · [`vote list`](list.md) · [`reward withdraw`](../reward/withdraw.md) · [`stake freeze`](../stake/freeze.md) · [脚本安全](../../machine-interface.md#script-safety-never-mistake-submitted-for-confirmed)
